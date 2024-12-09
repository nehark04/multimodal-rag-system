import os
import torch
from torchvision import models, transforms
from PIL import Image
import logging

# Setting up logging
logging.basicConfig(level=logging.INFO)

# Initialize the Faster R-CNN model
model = models.detection.fasterrcnn_resnet50_fpn(pretrained=True)
model.eval()

# Transformation for image input
transform = transforms.Compose([transforms.ToTensor()])

# COCO class labels for object detection
COCO_INSTANCE_CATEGORY_NAMES = [
    '__background__', 'person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus', 'train',
    'truck', 'boat', 'traffic light', 'fire hydrant', 'stop sign', 'parking meter', 'bench',
    'bird', 'cat', 'dog', 'horse', 'sheep', 'cow', 'elephant', 'bear', 'zebra', 'giraffe',
    'backpack', 'umbrella', 'handbag', 'tie', 'suitcase', 'frisbee', 'skis', 'snowboard',
    'sports ball', 'kite', 'baseball bat', 'baseball glove', 'skateboard', 'surfboard',
    'tennis racket', 'bottle', 'wine glass', 'cup', 'fork', 'knife', 'spoon', 'bowl', 'banana',
    'apple', 'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza', 'donut', 'cake',
    'chair', 'couch', 'potted plant', 'bed', 'dining table', 'toilet', 'TV', 'laptop', 'mouse',
    'remote', 'keyboard', 'cell phone', 'microwave', 'oven', 'toaster', 'sink', 'refrigerator',
    'book', 'clock', 'vase', 'scissors', 'teddy bear', 'hair drier', 'toothbrush'
]

def process_image(file_path):
    """
    Process a single image file, detect objects using Faster R-CNN, and save the results.

    Args:
    - file_path: Path to the image file.

    Returns:
    - descriptions: A list of descriptions for detected objects if successful, None otherwise.
    """
    if not os.path.exists(file_path):
        logging.error(f"The file {file_path} does not exist.")
        return None

    processed_folder = "../processed_images/"
    # Ensure the processed folder exists
    os.makedirs(processed_folder, exist_ok=True)

    file_name = os.path.basename(file_path)
    processed_file_name = f"{os.path.splitext(file_name)[0]}_objects.txt"
    processed_file_path = os.path.join(processed_folder, processed_file_name)

    try:
        logging.info(f"Processing image file {file_name}...")

        # Open and transform the image
        image = Image.open(file_path).convert("RGB")
        image_tensor = transform(image).unsqueeze(0)

        # Get predictions from the model
        with torch.no_grad():
            outputs = model(image_tensor)

        labels = outputs[0]['labels']
        scores = outputs[0]['scores']

        # Filter and describe objects
        descriptions = []
        for i, label in enumerate(labels):
            if scores[i] > 0.5:  # Confidence threshold
                try:
                    descriptions.append(f"{COCO_INSTANCE_CATEGORY_NAMES[label]} (confidence: {scores[i]:.2f})")
                except IndexError:
                    descriptions.append(f"Unknown object (label index {label}) (confidence: {scores[i]:.2f})")

        # Save descriptions to a file
        with open(processed_file_path, "w", encoding="utf-8") as f:
            for desc in descriptions:
                f.write(desc + "\n")
        logging.info(f"Object detected {descriptions}")
        logging.info(f"Object descriptions saved to {processed_file_path}")
        return descriptions
    except Exception as e:
        logging.error(f"Error processing the image file {file_path}: {e}")
        return None


# import os
# import torch
# from torchvision import models, transforms
# from PIL import Image
# import logging

# # Setting up logging
# logging.basicConfig(level=logging.INFO)

# # Initialize the Faster R-CNN model
# model = models.detection.fasterrcnn_resnet50_fpn(pretrained=True)
# model.eval()

# # Transformation for image input
# transform = transforms.Compose([transforms.ToTensor()])

# # COCO class labels for object detection
# COCO_INSTANCE_CATEGORY_NAMES = [
#     '__background__', 'person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus', 'train',
#     'truck', 'boat', 'traffic light', 'fire hydrant', 'stop sign', 'parking meter', 'bench',
#     'bird', 'cat', 'dog', 'horse', 'sheep', 'cow', 'elephant', 'bear', 'zebra', 'giraffe',
#     'backpack', 'umbrella', 'handbag', 'tie', 'suitcase', 'frisbee', 'skis', 'snowboard',
#     'sports ball', 'kite', 'baseball bat', 'baseball glove', 'skateboard', 'surfboard',
#     'tennis racket', 'bottle', 'wine glass', 'cup', 'fork', 'knife', 'spoon', 'bowl', 'banana',
#     'apple', 'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza', 'donut', 'cake',
#     'chair', 'couch', 'potted plant', 'bed', 'dining table', 'toilet', 'TV', 'laptop', 'mouse',
#     'remote', 'keyboard', 'cell phone', 'microwave', 'oven', 'toaster', 'sink', 'refrigerator',
#     'book', 'clock', 'vase', 'scissors', 'teddy bear', 'hair drier', 'toothbrush'
# ]

# def extract_image_objects(image_path):
#     """
#     Detect objects in an image using Faster R-CNN and generate descriptions.

#     Args:
#     - image_path: Path to the image file.

#     Returns:
#     - A list of descriptions for detected objects in the image.
#     """
#     try:
#         # Open and transform the image
#         image = Image.open(image_path).convert("RGB")
#         image_tensor = transform(image).unsqueeze(0)

#         # Get predictions from the model
#         with torch.no_grad():
#             outputs = model(image_tensor)

#         labels = outputs[0]['labels']
#         scores = outputs[0]['scores']
        
#         # Filter out objects with low confidence
#         descriptions = []
#         for i, label in enumerate(labels):
#             if scores[i] > 0.5:  # Confidence threshold
#                 try:
#                     descriptions.append(f"{COCO_INSTANCE_CATEGORY_NAMES[label]} (confidence: {scores[i]:.2f})")
#                 except IndexError:
#                     descriptions.append(f"Unknown object (label index {label}) (confidence: {scores[i]:.2f})")

#         return descriptions
#     except Exception as e:
#         logging.error(f"Error extracting objects from image {image_path}: {e}")
#         return []

# def process_image(upload_folder):
#     """
#     Process image files uploaded to the server and perform object detection.

#     Args:
#     - upload_folder: The folder where the uploaded image files are stored.
#     """
#     image_files = get_image_files(upload_folder)
    
#     if not image_files:
#         logging.info("No image files found to process.")
#         return

#     for image_file in image_files:
#         try:
#             file_path = os.path.join(upload_folder, image_file)
#             logging.info(f"Processing image file: {file_path}")
            
#             # Perform object detection
#             descriptions = extract_image_objects(file_path)
#             logging.info(f"Detected objects for {image_file}: {descriptions}")
        
#         except Exception as e:
#             logging.error(f"Error processing image {image_file}: {e}")

# def get_image_files(upload_folder):
#     """
#     Get a list of image files in the upload folder.
#     """
#     return [f for f in os.listdir(upload_folder) if f.endswith(('.jpg', '.jpeg', '.png'))]
