import os

def allowed_file(filename):
    allowed_extensions = {'png', 'jpg', 'jpeg', 'mp4', 'mp3', 'wav'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

def get_file_path(folder, filename):
    return os.path.join(folder, filename)
