import os
import torch
import logging
import cv2
from torchvision import transforms
from torchvision.models.detection import fasterrcnn_resnet50_fpn
from pathlib import Path

# Setting up logging
logging.basicConfig(level=logging.INFO)

# Initialize the Faster R-CNN model
model = fasterrcnn_resnet50_fpn(pretrained=True)
model.eval()

COCO_INSTANCE_CATEGORY_NAMES = [
    '__background__', 'person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus',
    'train', 'truck', 'boat', 'traffic light', 'fire hydrant', 'stop sign', 'parking meter',
    'bench', 'bird', 'cat', 'dog', 'horse', 'sheep', 'cow', 'elephant', 'bear', 'zebra',
    'giraffe', 'backpack', 'umbrella', 'handbag', 'tie', 'suitcase', 'frisbee', 'skis',
    'snowboard', 'sports ball', 'kite', 'baseball bat', 'baseball glove', 'skateboard',
    'surfboard', 'tennis racket', 'bottle', 'wine glass', 'cup', 'fork', 'knife', 'spoon',
    'bowl', 'banana', 'apple', 'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza',
    'donut', 'cake', 'chair', 'couch', 'potted plant', 'bed', 'dining table', 'toilet', 'tv',
    'laptop', 'mouse', 'remote', 'keyboard', 'cell phone', 'microwave', 'oven', 'toaster',
    'sink', 'refrigerator', 'book', 'clock', 'vase', 'scissors', 'teddy bear', 'hair drier',
    'toothbrush'
]

def preprocess_frame(frame):
    """Transform the frame into a tensor for model input."""
    transform = transforms.Compose([transforms.ToTensor()])
    return transform(frame)

def perform_object_detection(frame):
    """Detect objects in a frame using Faster R-CNN."""
    frame_tensor = preprocess_frame(frame).unsqueeze(0)

    with torch.no_grad():
        predictions = model(frame_tensor)[0]

    detected_objects = []
    for i, score in enumerate(predictions['scores']):
        if score > 0.5:  # Confidence threshold
            label_index = predictions['labels'][i].item()
            label = COCO_INSTANCE_CATEGORY_NAMES[label_index] if label_index < len(COCO_INSTANCE_CATEGORY_NAMES) else f"Unknown object (label index {label_index})"
            detected_objects.append(f"{label} (confidence: {score:.2f})")

    return detected_objects

def process_video(video_path):
    """
    Process a single video file, perform object detection on frames, and save the results.

    Args:
    - video_path: Path to the video file to process.
    - frame_rate: Number of frames to process per second (default is 1 frame per second).

    Returns:
    - frame_descriptions: A dictionary containing frame numbers and their detected objects.
    """
    frame_rate=1
    
    if not os.path.exists(video_path):
        logging.error(f"The video file {video_path} does not exist.")
        return None

    processed_folder = "../processed_videos/"
    # Ensure the processed folder exists
    os.makedirs(processed_folder, exist_ok=True)

    video_file_name = os.path.basename(video_path)
    processed_file_name = f"{os.path.splitext(video_file_name)[0]}_descriptions.txt"
    processed_file_path = os.path.join(processed_folder, processed_file_name)

    frame_descriptions = {}
    try:
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            logging.error(f"Error: Could not open video {video_path}.")
            return None

        frame_count = 0
        fps = cap.get(cv2.CAP_PROP_FPS)  # Get frames per second
        with open(processed_file_path, 'w') as output_file:
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break

                # Process frame at specified rate
                if frame_count % int(fps // frame_rate) == 0:
                    descriptions = perform_object_detection(frame)
                    if descriptions:
                        frame_description = f"Frame {frame_count}: " + ", ".join(descriptions)
                        output_file.write(frame_description + '\n')
                        frame_descriptions[frame_count] = descriptions
                    else:
                        output_file.write(f"Frame {frame_count}: No objects detected.\n")
                        frame_descriptions[frame_count] = ["No objects detected"]

                frame_count += 1

        cap.release()
        logging.info(f"Object descriptions saved to {processed_file_path}")
        return frame_descriptions
    except Exception as e:
        logging.error(f"Error processing the video file {video_path}: {e}")
        return None


# import os
# import torch
# import logging
# import cv2
# from torchvision import transforms
# from torchvision.models.detection import fasterrcnn_resnet50_fpn
# from pathlib import Path

# # Setting up logging
# logging.basicConfig(level=logging.INFO)

# # Initialize the Faster R-CNN model
# model = fasterrcnn_resnet50_fpn(pretrained=True)
# model.eval()

# COCO_INSTANCE_CATEGORY_NAMES = [
#     '__background__', 'person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus', 
#     'train', 'truck', 'boat', 'traffic light', 'fire hydrant', 'stop sign', 'parking meter', 
#     'bench', 'bird', 'cat', 'dog', 'horse', 'sheep', 'cow', 'elephant', 'bear', 'zebra', 
#     'giraffe', 'backpack', 'umbrella', 'handbag', 'tie', 'suitcase', 'frisbee', 'skis', 
#     'snowboard', 'sports ball', 'kite', 'baseball bat', 'baseball glove', 'skateboard', 
#     'surfboard', 'tennis racket', 'bottle', 'wine glass', 'cup', 'fork', 'knife', 'spoon', 
#     'bowl', 'banana', 'apple', 'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza', 
#     'donut', 'cake', 'chair', 'couch', 'potted plant', 'bed', 'dining table', 'toilet', 'tv', 
#     'laptop', 'mouse', 'remote', 'keyboard', 'cell phone', 'microwave', 'oven', 'toaster', 
#     'sink', 'refrigerator', 'book', 'clock', 'vase', 'scissors', 'teddy bear', 'hair drier', 
#     'toothbrush'
# ]

# def preprocess_frame(frame):
#     """Transform the frame into a tensor for model input."""
#     transform = transforms.Compose([transforms.ToTensor()])
#     return transform(frame)

# def perform_object_detection(frame):
#     """Detect objects in a frame using Faster R-CNN."""
#     frame_tensor = preprocess_frame(frame).unsqueeze(0)

#     with torch.no_grad():
#         predictions = model(frame_tensor)[0]

#     detected_objects = []
#     for i, score in enumerate(predictions['scores']):
#         if score > 0.5:  # Confidence threshold
#             label_index = predictions['labels'][i].item()
#             label = COCO_INSTANCE_CATEGORY_NAMES[label_index] if label_index < len(COCO_INSTANCE_CATEGORY_NAMES) else f"Unknown object (label index {label_index})"
#             detected_objects.append((label, score.item()))

#     return detected_objects

# def process_video_frames(video_path, output_file_path, frame_rate=1):
#     """
#     Process each frame of the video for object detection.
#     """
#     cap = cv2.VideoCapture(video_path)
#     if not cap.isOpened():
#         logging.error(f"Error: Could not open video {video_path}.")
#         return

#     frame_count = 0
#     with open(output_file_path, 'w') as output_file:
#         while cap.isOpened():
#             ret, frame = cap.read()
#             if not ret:
#                 break

#             # Process frame at specified rate
#             if frame_count % int(cap.get(cv2.CAP_PROP_FPS) // frame_rate) == 0:
#                 descriptions = perform_object_detection(frame)
#                 if descriptions:
#                     frame_description = f"Frame {frame_count}: " + ", ".join([f"{obj} (confidence: {confidence:.2f})" for obj, confidence in descriptions])
#                     output_file.write(frame_description + '\n')
#                 else:
#                     output_file.write(f"Frame {frame_count}: No objects detected.\n")

#             frame_count += 1

#     cap.release()

# def extract_video_metadata(video_path):
#     """
#     Extract basic metadata from a video file using OpenCV.
#     """
#     try:
#         # Open video file
#         cap = cv2.VideoCapture(video_path)

#         # Extract metadata
#         duration = cap.get(cv2.CAP_PROP_FRAME_COUNT) / cap.get(cv2.CAP_PROP_FPS)  # in seconds
#         fps = cap.get(cv2.CAP_PROP_FPS)  # frames per second
#         resolution = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))

#         cap.release()

#         video_metadata = {
#             'duration': duration,
#             'fps': fps,
#             'resolution': resolution
#         }
#         return video_metadata
#     except Exception as e:
#         logging.error(f"Error extracting metadata for {video_path}: {e}")
#         return None

# def process_video(upload_folder):
#     """
#     Process video files uploaded to the server and perform object detection on frames.
#     """
#     video_files = get_video_files(upload_folder)
    
#     if not video_files:
#         logging.info("No video files found to process.")
#         return

#     for video_file in video_files:
#         try:
#             file_path = os.path.join(upload_folder, video_file)
#             logging.info(f"Processing video file: {file_path}")
            
#             # Extract basic video metadata (duration, resolution, etc.)
#             video_info = extract_video_metadata(file_path)
#             logging.info(f"Video Metadata for {video_file}: {video_info}")
            
#             # Process frames and perform object detection
#             output_file_path = os.path.splitext(file_path)[0] + "_descriptions.txt"
#             process_video_frames(file_path, output_file_path)
        
#         except Exception as e:
#             logging.error(f"Error processing video {video_file}: {e}")

# def get_video_files(upload_folder):
#     """
#     Get a list of video files in the upload folder.
#     """
#     return [f for f in os.listdir(upload_folder) if f.endswith(('.mp4', '.avi', '.mov'))]
