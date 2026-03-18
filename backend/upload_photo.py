import os
from werkzeug.utils import secure_filename
from PIL import Image
import hashlib
import uuid

class PhotoUploadHandler:
    def __init__(self, upload_folder='static/uploads'):
        self.upload_folder = upload_folder
        self.allowed_extensions = {'png', 'jpg', 'jpeg', 'gif'}
        self.max_file_size = 5 * 1024 * 1024  # 5MB
        self.thumbnail_size = (150, 150)
        
        # Create upload folder if it doesn't exist
        os.makedirs(upload_folder, exist_ok=True)
        os.makedirs(os.path.join(upload_folder, 'thumbnails'), exist_ok=True)
    
    def allowed_file(self, filename):
        """Check if file extension is allowed"""
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in self.allowed_extensions
    
    def generate_unique_filename(self, original_filename):
        """Generate unique filename to avoid conflicts"""
        ext = original_filename.rsplit('.', 1)[1].lower()
        unique_name = hashlib.md5(str(uuid.uuid4()).encode()).hexdigest()
        return f"{unique_name}.{ext}"
    
    def create_thumbnail(self, image_path, thumbnail_path):
        """Create thumbnail from uploaded image"""
        try:
            img = Image.open(image_path)
            img.thumbnail(self.thumbnail_size, Image.Resampling.LANCZOS)
            img.save(thumbnail_path, optimize=True, quality=85)
            return True
        except Exception as e:
            print(f"Error creating thumbnail: {e}")
            return False
    
    def upload_photo(self, file, user_id):
        """Handle photo upload process"""
        if file and self.allowed_file(file.filename):
            # Check file size
            file.seek(0, os.SEEK_END)
            file_size = file.tell()
            file.seek(0)
            
            if file_size > self.max_file_size:
                return {'success': False, 'error': 'File size too large. Max 5MB allowed.'}
            
            # Generate unique filename
            filename = self.generate_unique_filename(file.filename)
            
            # Save original image
            user_folder = os.path.join(self.upload_folder, str(user_id))
            os.makedirs(user_folder, exist_ok=True)
            
            file_path = os.path.join(user_folder, filename)
            file.save(file_path)
            
            # Create thumbnail
            thumbnail_folder = os.path.join(user_folder, 'thumbnails')
            os.makedirs(thumbnail_folder, exist_ok=True)
            thumbnail_path = os.path.join(thumbnail_folder, filename)
            
            if self.create_thumbnail(file_path, thumbnail_path):
                return {
                    'success': True,
                    'original': f'/static/uploads/{user_id}/{filename}',
                    'thumbnail': f'/static/uploads/{user_id}/thumbnails/{filename}',
                    'filename': filename
                }
            else:
                return {'success': False, 'error': 'Failed to create thumbnail'}
        
        return {'success': False, 'error': 'Invalid file type'}
    
    def delete_photo(self, user_id, filename):
        """Delete user photo and thumbnail"""
        try:
            user_folder = os.path.join(self.upload_folder, str(user_id))
            file_path = os.path.join(user_folder, filename)
            thumbnail_path = os.path.join(user_folder, 'thumbnails', filename)
            
            if os.path.exists(file_path):
                os.remove(file_path)
            if os.path.exists(thumbnail_path):
                os.remove(thumbnail_path)
            
            return True
        except Exception as e:
            print(f"Error deleting photo: {e}")
            return False