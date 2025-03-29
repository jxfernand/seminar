# rejistu/views.py
import os
import logging
import uuid
import face_recognition
import numpy as np
from django.http import JsonResponse
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail
from django.conf import settings
from .models import Registrant, Institution
from .forms import RegistrantForm
import qrcode
from io import BytesIO
from django.core.files.base import ContentFile
import base64
from .institution import Institution  # Import Institution from the new file
from django.views.decorators.csrf import csrf_exempt
from .utils import recognize_face
from django.core.files.storage import default_storage
from django.db import IntegrityError, transaction
from django.core.exceptions import ValidationError
from .models import AccessPass
from django.http import HttpResponseNotFound
import gc
import cv2
from PIL import Image, ImageEnhance



@csrf_exempt
def recognize_face_view(request):
    if request.method == 'POST' and request.FILES.get('image'):
        # Generate a unique filename
        unique_filename = f"temp_images/{uuid.uuid4().hex}.jpg"
        image_file = request.FILES['image']
        
        file_name = default_storage.save(unique_filename, ContentFile(image_file.read()))
        file_path = default_storage.path(file_name)

        try:
            # Perform face recognition
            registrant_id = recognize_face(file_path)

            if registrant_id:
                return JsonResponse({'status': 'success', 'registrant_id': registrant_id})
            else:
                return JsonResponse({'status': 'error', 'message': 'No matching face found or no face detected.'})
        except Exception as e:
            logging.error(f"Error in recognize_face_view: {e}")
            return JsonResponse({'status': 'error', 'message': 'Internal server error.'})
        finally:
            # Ensure the temporary image file is deleted
            if os.path.exists(file_path):
                os.remove(file_path)

    return JsonResponse({'status': 'error', 'message': 'Invalid request.'})


def enhance_image(image_path):
    """Enhance the uploaded image for better face detection."""
    image = Image.open(image_path)

    # Convert to grayscale (optional, may help with detection)
    grayscale_image = image.convert("L")

    # Enhance contrast to make the face stand out more
    enhancer = ImageEnhance.Contrast(grayscale_image)
    enhanced_image = enhancer.enhance(2)  # Increase contrast by a factor of 2

    # Save the enhanced image to a temporary location
    enhanced_image_path = "enhanced_" + image_path
    enhanced_image.save(enhanced_image_path)
    
    return enhanced_image_path


def recognize_face(file_path):
    try:
        # Enhance the uploaded image for better face detection
        enhanced_image_path = enhance_image(file_path)
        unknown_image = face_recognition.load_image_file(file_path)
        unknown_face_encodings = face_recognition.face_encodings(unknown_image)

        if not unknown_face_encodings:
            print("No face detected in the uploaded image.")
            return None  # No face detected in the uploaded image
        print(f"Detected {len(unknown_face_encodings)} face(s) in the uploaded image.")


        
        # Load known face encodings from the database (registrants' pictures)
        known_face_encodings = []
        known_face_ids = []
        for registrant in Registrant.objects.all():
            try:
                # Load the registrant's image and extract face encodings
                image = face_recognition.load_image_file(registrant.picture.path)
                face_encodings = face_recognition.face_encodings(image)
                
                if face_encodings:
                    known_face_encodings.append(face_encodings[0])
                    known_face_ids.append(registrant.id)
                else:
                    print(f"No face encoding found for registrant {registrant.id}.")
            except Exception as e:
                print(f"Error loading image for registrant {registrant.id}: {e}")

        if not known_face_encodings:
            print("No known face encodings loaded.")
            return None

        # Compare the uploaded face encodings with known faces
        for unknown_encoding in unknown_face_encodings:
            matches = face_recognition.compare_faces(known_face_encodings, unknown_encoding)
            face_distances = face_recognition.face_distance(known_face_encodings, unknown_encoding)
            best_match_index = np.argmin(face_distances)

            # Set a threshold for more strict matching
            threshold = 0.6  # Adjust as needed for better matching sensitivity
            if matches[best_match_index] and face_distances[best_match_index] <= threshold:
                print(f"Matching registrant found with ID: {known_face_ids[best_match_index]}")
                return known_face_ids[best_match_index]  # Return the matched Registrant ID
        
        print("No matching face found.")
        return None  # No match found
    
    except Exception as e:
        logging.error(f"Error in recognize_face: {e}")
        return None


        # del unknown_image  # Free image memory
        gc.collect()  # Force garbage collection

    #     # Load known faces
    #     known_face_encodings = []
    #     known_face_ids = []

    #     for registrant in Registrant.objects.all():
    #         try:
    #             image = face_recognition.load_image_file(registrant.picture.path)
    #             face_encodings = face_recognition.face_encodings(image)
    #             if face_encodings:
    #                 known_face_encodings.append(face_encodings[0])
    #                 known_face_ids.append(registrant.id)

    #             del image  # Free image memory after processing
    #             gc.collect()
    #         except Exception as e:
    #             print(f"Skipping registrant {registrant.id} due to error: {e}")

    #     if not known_face_encodings:
    #         return None

    #     # Compare faces
    #     for unknown_encoding in unknown_face_encodings:
    #         matches = face_recognition.compare_faces(known_face_encodings, unknown_encoding)
    #         face_distances = face_recognition.face_distance(known_face_encodings, unknown_encoding)

    #         if face_distances.size > 0:
    #             best_match_index = np.argmin(face_distances)
    #             if matches[best_match_index]:
    #                 return known_face_ids[best_match_index]

    #     return None
    # except Exception as e:
    #     print(f"Error in recognize_face: {e}")
    #     return None
    # finally:
    #     gc.collect()  # Final memory cleanup

# Create a view for the webcam interface
def webcam_interface(request):
    return render(request, 'rejistu/webcam.html')


def get_institution_quota(request, institution_id):
    try:
        institution = Institution.objects.get(id=institution_id)
        data = {
            'name': institution.name,
            'quota': institution.quota,
            'access_pass_counter': institution.access_pass_counter,
        }
        return JsonResponse(data)
    except Institution.DoesNotExist:
        return JsonResponse({'error': 'Institution not found.'}, status=404)



def registrant_detail(request, access_pass_id):
    # Query by access_pass_id field
    registrant = get_object_or_404(Registrant, access_pass_id=access_pass_id)
    return render(request, 'rejistu/registrant_detail.html', {'registrant': registrant})



def seminar_page(request):
    return render(request, 'seminar_page.html')

def welcome(request, registrant_id):
    registrant = Registrant.objects.get(id=registrant_id)
    return render(request, 'rejistu/welcome.html', {'registrant': registrant})

    if request.method == "POST":
        # Extract data from POST request
        name = request.POST['name']
        picture = request.FILES['picture']

        # Save the registrant picture
        registrant = Registrant.objects.create(name=name, picture=picture)

        # Load image and extract face encoding
        image_path = os.path.join('media', str(registrant.picture))
        image = face_recognition.load_image_file(image_path)
        encodings = face_recognition.face_encodings(image)

        if encodings:
            # Save the first detected face encoding
            registrant.save_face_encoding(encodings[0])

        return JsonResponse({"message": "Registrant created and face encoding saved."})

    return render(request, 'registrant/create.html')


def register(request):
    registrant = None  # Initialize registrant to avoid UnboundLocalError

    if request.method == "POST":
        try:
            with transaction.atomic():  # Ensure atomic transaction
                form = RegistrantForm(request.POST, request.FILES)
                if form.is_valid():
                    registrant = form.save(commit=False)

                    # Ensure the registrant is saved before using it in the filter
                    registrant.save()  # Save the registrant if it hasn't been saved yet
                    # Find an unused access pass for this institution and registrant
                    access_pass = AccessPass.objects.select_for_update().filter(
                        institution=registrant.institution, 
                        is_used=False,
                        registrant=registrant  # Ensuring the access pass is for this specific registrant
                    ).first()



                    if not access_pass:
                        raise ValidationError(
                            f"Access pass code {access_pass_code} is either already used or invalid."
                        )

                    # Assign the access pass to the registrant
                    registrant.access_pass = access_pass
                    registrant.save()  # This will trigger the UNIQUE constraint check

                    # Mark the access pass as used
                    access_pass.is_used = True
                    access_pass.save()



                    # Process signature data
                    signature_data = request.POST.get('signature_data')
                    if signature_data:
                        format, imgstr = signature_data.split(';base64,')  # Split the base64 string
                        ext = format.split('/')[-1]  # Get file extension
                        data = ContentFile(base64.b64decode(imgstr), name=f'signature_{registrant.access_pass}.{ext}')
                        registrant.signature = data

                    registrant_url = request.build_absolute_uri(f'/rejistu/registrant/{registrant.access_pass_id}/')

                    # Generate QR Code with the registrant's detail URL
                    qr = qrcode.QRCode(version=1, box_size=10, border=5)
                    qr.add_data(registrant_url)
                    qr.make(fit=True)
                    img = qr.make_image(fill='black', back_color='white')

                    # Save QR Code to the qr_code field
                    buffer = BytesIO()
                    img.save(buffer, format="PNG")
                    qr_code_file = ContentFile(buffer.getvalue())
                    registrant.qr_code.save(f'{registrant.access_pass}.png', qr_code_file)

                    # Send email with QR Code
                    send_mail(
                        'Your Registration QR Code',
                        f'Thank you for registering! Your access pass is: {registrant.access_pass}',
                        settings.EMAIL_HOST_USER,
                        [registrant.email],
                        fail_silently=False,
                        html_message=f'<p>Thank you for registering! Your access pass is: <strong>{registrant.access_pass}</strong></p>'
                                    f'<p>Scan the QR code below to view your registration details:</p>'
                                    f'<img src="{settings.MEDIA_URL}{registrant.qr_code.url}" alt="QR Code">',
                    )

                    return redirect('welcome', registrant_id=registrant.id)

        except IntegrityError:
            return HttpResponseNotFound("This access pass is already assigned.")

        except ValidationError as e:
            return HttpResponseNotFound(str(e))  # Show validation errors

    else:
        form = RegistrantForm()

    return render(request, 'rejistu/register.html', {'form': form})


