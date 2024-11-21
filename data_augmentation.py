import cv2
import os
import numpy as np
import xml.etree.ElementTree as ET

# Define paths
image_folder = "C:/Users/izzaf/PycharmProjects/ModelTraining/Signwise Dataset/new noon/images"
annotation_folder = "C:/Users/izzaf/PycharmProjects/ModelTraining/Signwise Dataset/new noon/annotations"
output_image_folder = "C:/Users/izzaf/PycharmProjects/ModelTraining/Signwise Dataset/new noon/augmented/images"
output_annotation_folder = "C:/Users/izzaf/PycharmProjects/ModelTraining/Signwise Dataset/new noon/augmented/annotations"
bounding_box_output_folder = "C:/Users/izzaf/PycharmProjects/ModelTraining/Signwise Dataset/new noon/augmented/bounding_boxes"

# Create output directories if they don’t exist
os.makedirs(output_image_folder, exist_ok=True)
os.makedirs(output_annotation_folder, exist_ok=True)
os.makedirs(bounding_box_output_folder, exist_ok=True)

# Function to update bounding box coordinates for scaled images while retaining the original label
def update_bounding_box_scale(xml_file, scale, center):
    # Parse the XML file
    tree = ET.parse(xml_file)
    root = tree.getroot()

    for obj in root.findall('object'):
        bndbox = obj.find('bndbox')
        xmin = int(bndbox.find('xmin').text)
        xmax = int(bndbox.find('xmax').text)
        ymin = int(bndbox.find('ymin').text)
        ymax = int(bndbox.find('ymax').text)

        # Calculate new bounding box coordinates based on scaling
        points = np.array([[xmin, ymin], [xmax, ymin], [xmax, ymax], [xmin, ymax]], dtype='float32')

        # Scaling matrix
        scale_matrix = cv2.getRotationMatrix2D(center, 0, scale)
        scaled_points = cv2.transform(np.array([points]), scale_matrix)[0]

        # Update XML with new bounding box coordinates
        new_xmin, new_ymin = np.min(scaled_points, axis=0).astype(int)
        new_xmax, new_ymax = np.max(scaled_points, axis=0).astype(int)

        # Ensure bounding box is within image bounds
        new_xmin = max(0, new_xmin)
        new_xmax = min(width - 1, new_xmax)
        new_ymin = max(0, new_ymin)
        new_ymax = min(height - 1, new_ymax)

        bndbox.find('xmin').text = str(new_xmin)
        bndbox.find('xmax').text = str(new_xmax)
        bndbox.find('ymin').text = str(new_ymin)
        bndbox.find('ymax').text = str(new_ymax)

        # Retain the original label
        name_tag = obj.find('name')
        if name_tag is not None:
            original_label = name_tag.text
            name_tag.text = original_label
        else:
            name_tag = ET.SubElement(obj, "name")
            name_tag.text = "لیبل"  # Placeholder label

    return tree


# Process each image and its corresponding XML annotation
for index, image_file in enumerate(os.listdir(image_folder)):
    if image_file.lower().endswith((".jpg", ".jpeg", ".png")):
        # Load the image
        image_path = os.path.join(image_folder, image_file)
        image = cv2.imread(image_path)

        if image is None:
            print(f"Warning: Could not load image {image_file}. Skipping.")
            continue

        height, width, _ = image.shape

        # Load the corresponding XML annotation
        xml_file = os.path.join(annotation_folder, os.path.splitext(image_file)[0] + ".xml")

        if not os.path.exists(xml_file):
            print(f"Warning: Annotation file {xml_file} does not exist. Skipping.")
            continue

        # Calculate the center for scaling
        center = (width / 2, height / 2)

        # Determine scale based on bounding box size
        tree = ET.parse(xml_file)
        root = tree.getroot()
        for obj in root.findall('object'):
            bndbox = obj.find('bndbox')
            xmin = int(bndbox.find('xmin').text)
            xmax = int(bndbox.find('xmax').text)
            ymin = int(bndbox.find('ymin').text)
            ymax = int(bndbox.find('ymax').text)

            box_width = xmax - xmin
            box_height = ymax - ymin

            # Heuristic for zoom: if box is smaller, zoom in; if larger, zoom out
            scale = 1.1 if box_width < 0.5 * width and box_height < 0.5 * height else 0.9

            # Ensure the scaled box stays within bounds
            scaled_image = cv2.warpAffine(image, cv2.getRotationMatrix2D(center, 0, scale), (width, height))
            scaled_tree = update_bounding_box_scale(xml_file, scale, center)

            # Check if bounding boxes fit within the image dimensions after scaling
            for obj in scaled_tree.findall('object'):
                bndbox = obj.find('bndbox')
                xmin = int(bndbox.find('xmin').text)
                xmax = int(bndbox.find('xmax').text)
                ymin = int(bndbox.find('ymin').text)
                ymax = int(bndbox.find('ymax').text)

                # Ensure the scaled bounding box is within image bounds
                if xmin < 0 or xmax >= width or ymin < 0 or ymax >= height:
                    print(f"Warning: Scaling caused bounding box to exceed image bounds for {image_file}. Skipping this scale.")
                    continue

            # Save the augmented image
            output_image_path = os.path.join(output_image_folder, f"{os.path.splitext(image_file)[0]}_scaled.jpg")
            cv2.imwrite(output_image_path, scaled_image)

            # Save the updated XML annotation
            output_xml_path = os.path.join(output_annotation_folder, f"{os.path.splitext(image_file)[0]}_scaled.xml")
            scaled_tree.write(output_xml_path, encoding='utf-8', xml_declaration=True)

            # Draw bounding boxes on the scaled image
            for obj in scaled_tree.findall('object'):
                bndbox = obj.find('bndbox')
                xmin = int(bndbox.find('xmin').text)
                xmax = int(bndbox.find('xmax').text)
                ymin = int(bndbox.find('ymin').text)
                ymax = int(bndbox.find('ymax').text)

                # Draw the bounding box on the image
                cv2.rectangle(scaled_image, (xmin, ymin), (xmax, ymax), (0, 255, 0), 2)

            # Save the image with bounding boxes
            bounding_box_image_path = os.path.join(bounding_box_output_folder,
                                                   f"{os.path.splitext(image_file)[0]}_bounding_box.jpg")
            cv2.imwrite(bounding_box_image_path, scaled_image)

print("Augmentation completed, annotations updated, and original labels retained.")