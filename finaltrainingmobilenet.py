

import os
import numpy as np
import cv2
import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import precision_score, recall_score, f1_score, confusion_matrix
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense, Dropout, GlobalAveragePooling2D, Input
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import CSVLogger, EarlyStopping

#loading data
def load_data(base_path):
    images, labels, bboxes = [], [], []
    # iterate through image and label folders
    for label in os.listdir(base_path):
        label_path = os.path.join(base_path, label)
        if os.path.isdir(label_path):
            for img_file in os.listdir(os.path.join(label_path, 'images')):
                if img_file.lower().endswith('.jpg'):
                    img_path = os.path.join(label_path, 'images', img_file)
                    img = cv2.imread(img_path)
                    original_height, original_width = img.shape[:2]
                    img = cv2.resize(img, (224, 224))
                    images.append(img)

                    xml_path = os.path.join(label_path, 'annotation', img_file.rsplit('.', 1)[0] + '.xml')
                    if os.path.exists(xml_path):
                        # extracting xml file info
                        tree = ET.parse(xml_path)
                        root = tree.getroot()
                        for obj in root.findall('object'):
                            bndbox = obj.find('bndbox')
                            xmin, ymin = int(bndbox.find('xmin').text), int(bndbox.find('ymin').text)
                            xmax, ymax = int(bndbox.find('xmax').text), int(bndbox.find('ymax').text)
                            #resizing & normalization of bb
                            new_xmin, new_ymin = xmin / original_width * 224, ymin / original_height * 224
                            new_xmax, new_ymax = xmax / original_width * 224, ymax / original_height * 224
                            bboxes.append([new_xmin / 224, new_ymin / 224, new_xmax / 224, new_ymax / 224])
                            labels.append(label)
                    else:
                        print(f"Warning: XML file not found for {img_file}")

    return np.array(images), np.array(labels), np.array(bboxes)


base_path = 'D:/FINAL SIGNS/augmented_dataset_final'
X, y, bboxes = load_data(base_path)
#dataset prepration
X_train, X_val, y_train, y_val, bboxes_train, bboxes_val = train_test_split(X, y, bboxes, test_size=0.2, random_state=42)
print("Training Data Shape:")
print(f"Images: {X_train.shape}")
print(f"Labels: {y_train.shape}")
print(f"Bounding Boxes: {bboxes_train.shape}")

print("\nValidation Data Shape:")
print(f"Images: {X_val.shape}")
print(f"Labels: {y_val.shape}")
print(f"Bounding Boxes: {bboxes_val.shape}")

X_train = X_train.astype('float32') / 255.0
X_val = X_val.astype('float32') / 255.0

label_encoder = LabelEncoder()
y_train_encoded = label_encoder.fit_transform(y_train)
y_val_encoded = label_encoder.transform(y_val)

y_train_cat = to_categorical(y_train_encoded)
y_val_cat = to_categorical(y_val_encoded)
#model architecture
input_tensor = Input(shape=(224, 224, 3))
base_model = MobileNetV2(weights='imagenet', include_top=False, input_tensor=input_tensor)
base_model.trainable = False

x = GlobalAveragePooling2D()(base_model.output)

class_output = Dense(128, activation='relu')(x) #NON LINEARITY REMOVE
class_output = Dropout(0.5)(class_output)#AVOID OVERFITTING
class_output = Dense(len(np.unique(y)), activation='softmax', name='class_output')(class_output)#CLASSIFICATION

bbox_output = Dense(128, activation='relu')(x)
bbox_output = Dropout(0.5)(bbox_output)
bbox_output = Dense(4, activation='sigmoid', name='bbox_output')(bbox_output)#PRIDICT BOUNDINGBOX

model = Model(inputs=input_tensor, outputs=[class_output, bbox_output])

model.compile(optimizer=Adam(learning_rate=0.0001),
              loss={'class_output': 'categorical_crossentropy', 'bbox_output': 'mean_squared_error'},
              metrics={'class_output': 'accuracy'})

output_dir = "D:/FINAL SIGNS/epoch100"
os.makedirs(output_dir, exist_ok=True)

csv_logger = CSVLogger(os.path.join(output_dir, 'training_log.csv'), append=True)
early_stopping = EarlyStopping(monitor='val_loss', patience=5, mode=min, restore_best_weights=True)

# Train the model with early stopping
history = model.fit(
    X_train, {'class_output': y_train_cat, 'bbox_output': bboxes_train},
    validation_data=(X_val, {'class_output': y_val_cat, 'bbox_output': bboxes_val}),
    epochs=100,
    batch_size=32,
    callbacks=[csv_logger, early_stopping]
)

model_save_path = os.path.join(output_dir, 'signwise_model100epoch.h5')
model.save(model_save_path)

def save_evaluation_results():
    evaluation_results = model.evaluate(X_val, {'class_output': y_val_cat, 'bbox_output': bboxes_val})
    print("Evaluation Results:", evaluation_results)

    final_training_loss = history.history['loss'][-1]
    final_training_accuracy = history.history['class_output_accuracy'][-1]

    final_validation_loss = evaluation_results[0]
    final_validation_accuracy = evaluation_results[3] if len(evaluation_results) > 3 else None

    with open(os.path.join(output_dir, 'evaluation_results.txt'), 'w') as f:
        f.write(f"Evaluation Results:\n")
        f.write(f"Total Loss: {evaluation_results[0]:.4f}\n")
        f.write(f"Final Training Loss: {final_training_loss:.4f}\n")
        f.write(f"Final Training Accuracy: {final_training_accuracy:.4f}\n")
        f.write(f"Final Validation Loss: {final_validation_loss:.4f}\n")
        if final_validation_accuracy is not None:
            f.write(f"Validation Accuracy: {final_validation_accuracy:.4f}\n")
        else:
            f.write(f"Validation Accuracy: Not available\n")

y_pred = model.predict(X_val)
y_pred_classes = np.argmax(y_pred[0], axis=1)

precision = precision_score(y_val_encoded, y_pred_classes, average='weighted')
recall = recall_score(y_val_encoded, y_pred_classes, average='weighted')
f1 = f1_score(y_val_encoded, y_pred_classes, average='weighted')
conf_matrix = confusion_matrix(y_val_encoded, y_pred_classes)

plt.figure(figsize=(6, 4))
metrics_text = f"Precision: {precision:.2f}\nRecall: {recall:.2f}\nF1 Score: {f1:.2f}"
plt.text(0.1, 0.5, metrics_text, fontsize=12)
plt.axis('off')
plt.title("Evaluation Metrics")
plt.savefig(os.path.join(output_dir, 'signwise_evaluation_metrics_epoch100.png'))
plt.close()

plt.figure(figsize=(8, 6))
sns.heatmap(conf_matrix, annot=True, fmt="d", cmap="Blues", xticklabels=label_encoder.classes_,
            yticklabels=label_encoder.classes_)
plt.title("Confusion Matrix")
plt.xlabel("Predicted Labels")
plt.ylabel("True Labels")
plt.savefig(os.path.join(output_dir, 'signwise_confusion_matrix_epoch100.png'))
plt.close()

print(f"Evaluation metrics saved in {output_dir}")
print(f"Confusion Matrix plot saved in {output_dir}")

with open(os.path.join(output_dir, 'training_validation_results.txt'), 'w') as f:
    f.write("Training and Validation Results:\n")
    for epoch in range(len(history.history['loss'])):
        f.write(f"Epoch {epoch + 1}:\n")
        f.write(f" - Training Loss: {history.history['loss'][epoch]:.4f}\n")
        f.write(f" - Validation Loss: {history.history['val_loss'][epoch]:.4f}\n")
        f.write(f" - Training Classification Accuracy: {history.history['class_output_accuracy'][epoch]:.4f}\n")
        f.write(f" - Validation Classification Accuracy: {history.history['val_class_output_accuracy'][epoch]:.4f}\n\n")
    print(f"Training and Validation Results saved in {output_dir}")