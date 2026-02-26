import cv2
import numpy as np
import pickle
from typing import Dict, List
from datetime import datetime

from src.core.config import settings
from src.core.database import SessionLocal
from src.models.face import FaceRecord

class FaceService:
    def __init__(self):
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.recognizer = cv2.face.LBPHFaceRecognizer_create()
        self.known_faces = {}  # user_id -> (face_id, label)
        self.face_data = {}    # label -> {user_id, full_name, email, department}
        self.current_label = 0
        self._load_faces()
    
    def _load_faces(self):
        db = SessionLocal()
        try:
            faces = db.query(FaceRecord).filter(FaceRecord.is_active == True).all()
            face_samples = []
            labels = []
            
            for face in faces:
                if face.face_encoding:
                    nparr = np.frombuffer(face.face_encoding, np.uint8)
                    img = cv2.imdecode(nparr, cv2.IMREAD_GRAYSCALE)
                    if img is not None:
                        face_samples.append(img)
                        labels.append(self.current_label)
                        
                        # حفظ بيانات الوجه
                        self.face_data[self.current_label] = {
                            'user_id': face.user_id,
                            'full_name': face.full_name,
                            'email': face.email,
                            'department': face.department,
                            'created_at': face.created_at.isoformat() if face.created_at else None,
                            'access_count': face.access_count
                        }
                        
                        self.known_faces[face.user_id] = (face.id, self.current_label)
                        self.current_label += 1
            
            if face_samples:
                self.recognizer.train(face_samples, np.array(labels))
                print(f"✅ Loaded {len(face_samples)} faces")
        except Exception as e:
            print(f"❌ Error loading faces: {e}")
        finally:
            db.close()
    
    def _detect_face(self, image_bytes: bytes):
        nparr = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        if img is None:
            return None, None
        
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
        
        if len(faces) == 0:
            return None, None
        
        x, y, w, h = faces[0]
        face_roi = gray[y:y+h, x:x+w]
        return face_roi, img
    
    def enroll(self, user_id: str, image_bytes: bytes, full_name: str, email: str = None, department: str = None):
        face_roi, original_img = self._detect_face(image_bytes)
        if face_roi is None:
            return {"success": False, "error": "No face detected in image"}
        
        if user_id in self.known_faces:
            return {"success": False, "error": f"User ID '{user_id}' already exists"}
        
        face_roi = cv2.resize(face_roi, (200, 200))
        _, buffer = cv2.imencode('.jpg', face_roi)
        encoding_bytes = buffer.tobytes()
        
        db = SessionLocal()
        try:
            face = FaceRecord(
                user_id=user_id,
                full_name=full_name,
                email=email,
                department=department,
                face_encoding=encoding_bytes,
                access_count=0
            )
            db.add(face)
            db.commit()
            
            # إضافة للذاكرة
            label = self.current_label
            self.current_label += 1
            self.face_data[label] = {
                'user_id': user_id,
                'full_name': full_name,
                'email': email,
                'department': department,
                'created_at': datetime.utcnow().isoformat(),
                'access_count': 0
            }
            self.known_faces[user_id] = (face.id, label)
            self._load_faces()  # إعادة تحميل
            
            return {
                "success": True,
                "user_id": user_id,
                "full_name": full_name,
                "message": "Face enrolled successfully"
            }
        except Exception as e:
            db.rollback()
            return {"success": False, "error": str(e)}
        finally:
            db.close()
    
    def verify(self, user_id: str, image_bytes: bytes):
        face_roi, _ = self._detect_face(image_bytes)
        if face_roi is None:
            return {"success": False, "match": False, "error": "No face detected"}
        
        if user_id not in self.known_faces:
            return {"success": False, "match": False, "error": f"User '{user_id}' not found"}
        
        face_roi = cv2.resize(face_roi, (200, 200))
        label, confidence = self.recognizer.predict(face_roi)
        
        similarity = max(0, 1 - (confidence / 100))
        match = (self.face_data.get(label, {}).get('user_id') == user_id) and confidence < 70
        
        # الحصول على بيانات المستخدم
        user_data = self.face_data.get(self.known_faces[user_id][1], {})
        
        # تحديث عدد المرات
        if match:
            db = SessionLocal()
            try:
                face = db.query(FaceRecord).filter(FaceRecord.user_id == user_id).first()
                if face:
                    face.access_count += 1
                    face.last_accessed = datetime.utcnow()
                    db.commit()
                    user_data['access_count'] = face.access_count
            finally:
                db.close()
        
        return {
            "success": True,
            "match": match,
            "confidence": round(similarity, 4),
            "threshold": 0.7,
            "user": {
                "user_id": user_id,
                "full_name": user_data.get('full_name'),
                "email": user_data.get('email'),
                "department": user_data.get('department'),
                "access_count": user_data.get('access_count', 0)
            }
        }
    
    def identify(self, image_bytes: bytes, max_results: int = 5):
        face_roi, _ = self._detect_face(image_bytes)
        if face_roi is None:
            return {"success": False, "matches": [], "error": "No face detected"}
        
        if not self.known_faces:
            return {"success": False, "matches": [], "error": "Database is empty"}
        
        face_roi = cv2.resize(face_roi, (200, 200))
        label, confidence = self.recognizer.predict(face_roi)
        
        results = []
        if confidence < 100:
            user_info = self.face_data.get(label)
            if user_info:
                similarity = max(0, 1 - (confidence / 100))
                
                # تحديث الإحصائيات
                db = SessionLocal()
                try:
                    face = db.query(FaceRecord).filter(FaceRecord.user_id == user_info['user_id']).first()
                    if face:
                        face.access_count += 1
                        face.last_accessed = datetime.utcnow()
                        db.commit()
                        user_info['access_count'] = face.access_count
                finally:
                    db.close()
                
                results.append({
                    "rank": 1,
                    "confidence": round(similarity, 4),
                    "distance": round(float(confidence), 4),
                    "user": {
                        "user_id": user_info['user_id'],
                        "full_name": user_info['full_name'],
                        "email": user_info['email'],
                        "department": user_info['department'],
                        "access_count": user_info.get('access_count', 0),
                        "registered_since": user_info.get('created_at')
                    }
                })
        
        return {
            "success": True,
            "matches": results,
            "total_matches": len(results),
            "database_size": len(self.known_faces)
        }

face_service = FaceService()
