import os
import whisper
import logging

# Setting up logging
logging.basicConfig(level=logging.INFO)

# Initialize the Whisper model
model_size = "base"  # You can choose between 'tiny', 'small', 'medium', 'large'
model = whisper.load_model(model_size)

def process_audio(file_path):
    """
    Process a single audio file, transcribe it using Whisper, and save the transcription.

    Args:
    - file_path: Path to the audio file to process.

    Returns:
    - transcription: The transcription text of the audio file if successful, None otherwise.
    """
    if not os.path.exists(file_path):
        logging.error(f"The file {file_path} does not exist.")
        return None

    processed_folder = "../processed_audio/"
    # Ensure the processed folder exists
    os.makedirs(processed_folder, exist_ok=True)

    file_name = os.path.basename(file_path)
    processed_file_name = f"{os.path.splitext(file_name)[0]}_transcription.txt"
    processed_file_path = os.path.join(processed_folder, processed_file_name)

    try:
        logging.info(f"Processing audio file {file_name}...")

        # Transcribe the audio file using Whisper
        result = model.transcribe(file_path)
        transcription = result['text']

        # Save the transcription to the processed folder
        with open(processed_file_path, "w", encoding="utf-8") as f:
            f.write(transcription)

        logging.info(f"Transcription saved to {processed_file_path}")
        return transcription
    except Exception as e:
        logging.error(f"Error processing the audio file {file_path}: {e}")
        return None

# import os
# import whisper
# import logging

# # Setting up logging
# logging.basicConfig(level=logging.INFO)

# # Initialize the Whisper model
# model_size = "base"  # You can choose between 'tiny', 'small', 'medium', 'large'
# model = whisper.load_model(model_size)

# def process_audio(upload_folder):
#     """
#     Process audio files in the given folder and transcribe them using Whisper.

#     Args:
#     - upload_folder: The folder where the uploaded audio files are stored.

#     This function will transcribe audio files and save the transcriptions to a file.
#     """
#     audio_files = get_audio_files(upload_folder)

#     if not audio_files:
#         logging.info("No audio files found to process.")
#         return

#     transcriptions = {}
#     transcriptions_file_path = os.path.join(upload_folder, 'transcriptions.txt')

#     with open(transcriptions_file_path, "w") as f:
#         for audio_file in audio_files:
#             file_path = os.path.join(upload_folder, audio_file)
#             logging.info(f"Processing {audio_file}...")
            
#             try:
#                 # Transcribe the audio file using Whisper
#                 result = model.transcribe(file_path)
#                 transcriptions[audio_file] = result['text']
                
#                 # Write transcription to file
#                 f.write(f"Transcription for {audio_file}:\n{result['text']}\n\n")
#                 logging.info(f"Completed transcription for {audio_file}")
#             except Exception as e:
#                 logging.error(f"Error processing {audio_file}: {e}")

#     logging.info(f"All audio files have been processed. Transcriptions saved to {transcriptions_file_path}")

# def get_audio_files(upload_folder):
#     """
#     Get a list of audio files in the upload folder.
#     """
#     return [f for f in os.listdir(upload_folder) if f.endswith(('.wav', '.mp3', '.m4a'))]
