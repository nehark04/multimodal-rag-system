import os
import logging
from services.audio_service import process_audio
from services.video_service import process_video
from services.image_service import process_image
from services.text_service import process_text

# Setting up logging
logging.basicConfig(level=logging.INFO)

def process_file_based_on_extension(filepath):
    """
    Process files based on their extension.

    Args:
    - filepath: The path of the file to process.

    This function determines the file type based on the extension and delegates processing to the appropriate service.
    """
    # Get the file extension
    file_extension = filepath.rsplit('.', 1)[1].lower()

    # Redirect processing based on file extension
    if file_extension in ['txt', 'pdf']:
        logging.info(f"Processing text file: {filepath}")
        return process_text(filepath)
    elif file_extension in ['mp3', 'wav', 'm4a']:
        logging.info(f"Processing audio file: {filepath}")
        upload_folder = os.path.dirname(filepath)
        return process_audio(upload_folder)
    elif file_extension in ['mp4', 'avi', 'mov']:
        logging.info(f"Processing video file: {filepath}")
        upload_folder = os.path.dirname(filepath)
        return process_video(upload_folder)
    elif file_extension in ['jpg', 'jpeg', 'png']:
        logging.info(f"Processing image file: {filepath}")
        return process_image(filepath)

    logging.error(f"Unsupported file type: {file_extension} for file {filepath}")
    return None
