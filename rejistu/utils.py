# rejistu/utils.py
import face_recognition
import numpy as np
from .models import Registrant



def recognize_face(image_path):
    # Load known registrant faces and encodings
    known_face_encodings = []
    known_face_ids = []



    for registrant in Registrant.objects.all():
        try:
            image = face_recognition.load_image_file(registrant.picture.path)
            face_encodings = face_recognition.face_encodings(image)
            if face_encodings:  # Ensure a face encoding exists
                known_face_encodings.append(face_encodings[0])
                known_face_ids.append(registrant.id)
        except Exception as e:
            print(f"Error processing image for {registrant.id}: {e}")
    
    if not known_face_encodings:
        print("No known faces found in database.")
        return None  # No known faces to compare with

    # Load the uploaded image
    try:
        unknown_image = face_recognition.load_image_file(image_path)
        unknown_face_encodings = face_recognition.face_encodings(unknown_image)

        if not unknown_face_encodings:
            print("No face detected in the uploaded image.")
            return None  # No face detected
    except Exception as e:
        print(f"Error processing uploaded image: {e}")
        return None

    # Compare each face found in the uploaded image
    for unknown_encoding in unknown_face_encodings:
        matches = face_recognition.compare_faces(known_face_encodings, unknown_encoding)
        face_distances = face_recognition.face_distance(known_face_encodings, unknown_encoding)

        if face_distances.size > 0:
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                return known_face_ids[best_match_index]  # Return the matched Registrant ID

    return None  # No match found
