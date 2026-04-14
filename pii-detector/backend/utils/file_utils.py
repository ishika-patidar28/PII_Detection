def save_file(file, upload_folder):
    """Save the uploaded file to the specified folder."""
    if file:
        file_path = os.path.join(upload_folder, file.filename)
        file.save(file_path)
        return file_path
    return None

def read_file(file_path):
    """Read the contents of a file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def delete_file(file_path):
    """Delete a file from the filesystem."""
    if os.path.exists(file_path):
        os.remove(file_path)
        return True
    return False

def allowed_file(filename):
    """Check if the file has an allowed extension."""
    ALLOWED_EXTENSIONS = {'pdf', 'txt', 'png', 'jpg', 'jpeg', 'gif', 'bmp'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS