from flask import Flask, request, jsonify
import numpy as np
import cv2
import base64
import logging
import mediapipe as mp
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)

try:
    model = load_model('C:/Users/HP/PycharmProjects/PSL_AugDataSet/epoch100/signwise_model100epoch.h5')
    logging.info("Model loaded successfully.")
except Exception as e:
    logging.error(f"Error loading model: {e}")

label_mapping = {
    'aen': 'ع', 'alif': 'ا', 'bari yeh': 'ے', 'bay': 'ب', 'cheh': 'چ',
    'choti yeh': 'ی', 'daal': 'د', 'dhaal': 'ڈ', 'dwaad': 'ض', 'fay': 'ف',
    'gaen': 'غ', 'gaf': 'گ', 'haa': 'ھ', 'hamza': 'ء', 'hey': 'ح',
    'khey': 'خ', 'lam': 'ل', 'meem': 'م', 'noon': 'ن', 'pay': 'پ',
    'qaaf': 'ق', 'qaf': 'ک', 'saa': 'ژ', 'say': 'ث', 'seen': 'س',
    'sheen': 'ش', 'swaad': 'ص', 'tay': 'ت', 'they': 'ٹ', 'toy': 'ط',
    'wow': 'و', 'zal': 'ذ', 'zoy': 'ظ'
}

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=True, max_num_hands=1, min_detection_confidence=0.6)

def detect_hand(img):
    """Detects if there's any hand in the image using MediaPipe."""
    try:
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = hands.process(img_rgb)
        return results.multi_hand_landmarks is not None
    except Exception as e:
        logging.error(f"Error in hand detection: {e}")
        return False

@app.route("/get_prediction", methods=["POST"])
def predict():
    data = request.get_json()
    if 'image' not in data:
        return jsonify({'error': 'No image data provided'})

    image_data = base64.b64decode(data["image"])
    img = cv2.imdecode(np.frombuffer(image_data, np.uint8), cv2.IMREAD_COLOR)
    if img is None:
        return jsonify({'error': 'Invalid image format'})

    hands_detected = detect_hand(img)
    if not hands_detected:
        return jsonify({'predicted_label': ''})

    img_resized = cv2.resize(img, (224, 224))
    img_array = img_to_array(img_resized) / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    classification_output, bounding_box_output = model.predict(img_array)

    # Get the class label in English and convert to Urdu
    class_index = np.argmax(classification_output[0])
    class_label_english = list(label_mapping.keys())[class_index]
    class_label_urdu = label_mapping[class_label_english]

    # Get bounding box coordinates and scale them to the original image size
    bounding_box = bounding_box_output[0]
    height, width, _ = img.shape
    x_min = int(bounding_box[0] * width)
    y_min = int(bounding_box[1] * height)
    x_max = int(bounding_box[2] * width)
    y_max = int(bounding_box[3] * height)

    # Return both Urdu label and bounding box coordinates as response
    return jsonify({
        'predicted_label': class_label_urdu,

    })

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)