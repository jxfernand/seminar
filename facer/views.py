# seminar_project/facer/views.py
import cv2
import face_recognition
import json
from django.http import JsonResponse
from django.shortcuts import render
# from registrant.models import Registrant

def capture_and_compare(request):
    # Open webcam for face capture
    video_capture = cv2.VideoCapture(0)

    while True:
        ret, frame = video_capture.read()
        if not ret:
            continue

        # Convert image to RGB (required by face_recognition)
        rgb_frame = frame[:, :, ::-1]

        # Detect face locations and encodings in the webcam image
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        for face_encoding in face_encodings:
            # Compare with stored face encodings of registrants
            for registrant in Registrant.objects.all():
                stored_encoding = json.loads(registrant.face_encoding)  # Load stored encoding from JSON
                match = face_recognition.compare_faces([stored_encoding], face_encoding)

                if True in match:
                    # Face matched, return success message
                    return JsonResponse({"message": f"Welcome, {registrant.name}!"})

        # If no face matched
        return JsonResponse({"message": "Face not recognized. Please register."})

    # Release the video capture when done
    video_capture.release()
