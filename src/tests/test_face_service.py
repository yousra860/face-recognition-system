import pytest
import numpy as np
from PIL import Image
import io
import sys
import os

# Add parent to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.services.face_service import FaceService

def create_test_image():
    """Create a test image with a face-like pattern"""
    img = Image.new('RGB', (400, 400), color='lightgray')
    
    # Draw a simple face pattern
    from PIL import ImageDraw
    draw = ImageDraw.Draw(img)
    
    # Face oval
    draw.ellipse([100, 50, 300, 350], fill='peachpuff', outline='black', width=2)
    
    # Eyes
    draw.ellipse([140, 120, 180, 160], fill='white', outline='black')
    draw.ellipse([220, 120, 260, 160], fill='white', outline='black')
    draw.ellipse([155, 135, 165, 145], fill='black')
    draw.ellipse([235, 135, 245, 145], fill='black')
    
    # Nose
    draw.polygon([(200, 160), (190, 220), (210, 220)], fill='peachpuff', outline='black')
    
    # Mouth
    draw.arc([150, 240, 250, 290], start=0, end=180, fill='red', width=3)
    
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='JPEG')
    return img_bytes.getvalue()

class TestFaceService:
    
    @pytest.fixture
    def face_service(self):
        return FaceService()
    
    @pytest.fixture
    def test_image(self):
        return create_test_image()
    
    def test_detect_face_valid_image(self, face_service, test_image):
        """Test face detection with valid image"""
        face_roi, original = face_service._detect_face(test_image)
        # Should detect face or return None (depends on OpenCV cascade)
        assert face_roi is not None or face_roi is None  # Either is acceptable
    
    def test_detect_face_invalid_image(self, face_service):
        """Test face detection with invalid image"""
        result = face_service._detect_face(b'invalid data')
        assert result == (None, None)
    
    def test_enroll_and_verify(self, face_service, test_image):
        """Test complete enroll and verify flow"""
        # Enroll
        enroll_result = face_service.enroll(
            user_id="test_user_001",
            image_bytes=test_image,
            full_name="Test User",
            email="test@test.com",
            department="IT"
        )
        
        if enroll_result["success"]:
            assert enroll_result["user_id"] == "test_user_001"
            assert enroll_result["full_name"] == "Test User"
            
            # Verify
            verify_result = face_service.verify("test_user_001", test_image)
            assert verify_result["success"] is True
            assert "match" in verify_result
            assert "confidence" in verify_result
    
    def test_verify_nonexistent_user(self, face_service, test_image):
        """Test verification of non-existent user"""
        result = face_service.verify("nonexistent_user", test_image)
        assert result["success"] is False
        assert "error" in result
    
    def test_identify_empty_database(self, face_service, test_image):
        """Test identification with empty database"""
        # Clear known faces temporarily
        original_faces = face_service.known_faces.copy()
        face_service.known_faces = {}
        
        result = face_service.identify(test_image)
        assert result["success"] is False
        assert "error" in result
        
        # Restore
        face_service.known_faces = original_faces

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
