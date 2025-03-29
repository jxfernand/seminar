from django.db import models
import uuid
from django.core.exceptions import ValidationError
from .institution import Institution, AccessPass  # Import Institution from the new file
from django.db import transaction, connection
import json


class Registrant(models.Model):
    GENDER_CHOICES = [
        ('Feto', 'Feto'),
        ('Mane', 'Mane'),
    ]

    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)  # Replace the CharField with ForeignKey
    picture = models.ImageField(upload_to='registrant_pictures/')
    # face_encoding = models.TextField(blank=True, null=True)  # Store encoding as JSON
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    position = models.CharField(max_length=100)
    access_pass = models.OneToOneField(AccessPass, on_delete=models.CASCADE, blank=True, null=True, unique=True)  # One-to-one relationship
    mobile_phone = models.CharField(max_length=15)
    email = models.EmailField()
    signature = models.ImageField(upload_to='signatures/', blank=True, null=True)  # Change to ImageField
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True, null=True)  # Add this field
    created_at = models.DateTimeField(auto_now_add=True)


    def save_face_encoding(self, encoding):
        self.face_encoding = json.dumps(encoding.tolist())  # Convert to JSON
        self.save()
    
    def get_face_encoding(self):
        if self.face_encoding:
            return np.array(json.loads(self.face_encoding))  # Convert back to NumPy array
        return None


    def save(self, *args, **kwargs):
        # Assign an available access pass to the registrant
        if not self.access_pass:
            # Check if the institution's quota is full
            if self.institution.is_quota_full():
                raise ValidationError(f"The institution {self.institution.name} has reached its quota of {self.institution.quota} access passes.")

            # Find an available access pass for the institution
            access_pass = AccessPass.objects.filter(institution=self.institution, is_used=True).first()

            if not access_pass:
                raise ValidationError(f"No available access passes for the institution {self.institution.name}.")


            self.access_pass = access_pass.code  # Link access_pass to AccessPass.code
            access_pass.is_used = True
            access_pass.save()

            

            # Increment the institution's access pass counter
            self.institution.access_pass_counter += 1
            self.institution.save()


        # --- QR Code generated ---
        # Generate QR code if it doesn't exist
        if not self.qr_code:
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(self.access_pass)  # Use the access pass as QR code data
            qr.make(fit=True)

            img = qr.make_image(fill='black', back_color='white')

            # Save the QR code to the qr_code field
            buffer = BytesIO()
            img.save(buffer, format="PNG")
            file_name = f'qr_code_{self.access_pass}.png'
            self.qr_code.save(file_name, ContentFile(buffer.getvalue()), save=False)


    # def __str__(self):
    #     return f"{self.first_name} {self.last_name}"

    # Generate a QR code linking to the welcome page
        if not self.qr_code:
            welcome_url = f"http://0.0.0.0:8000/rejistu/welcome/{self.access_pass}/"  # Replace with your domain
            qr = qrcode.QRCode(version=1, box_size=10, border=5)
            qr.add_data(welcome_url)
            qr.make(fit=True)
            img = qr.make_image(fill='black', back_color='white')

            # Save the QR code to the qr_code field
            buffer = BytesIO()
            img.save(buffer, format="PNG")
            qr_code_file = ContentFile(buffer.getvalue())
            self.qr_code.save(f'{self.access_pass}.png', qr_code_file)


    def save(self, *args, **kwargs):
        if self.institution.access_pass_counter >= self.institution.quota:
            raise ValidationError(f"The institution {self.institution.name} has reached its quota of {self.institution.quota} access passes.")


        # # Generate a unique access pass if it doesn't exist
        # if not self.access_pass:
        #     self.access_pass = f"{self.institution.name[:3].upper()}-{self.institution.access_pass_counter + 1:03d}"

        # Increment the institution's access pass counter
        self.institution.access_pass_counter += 1
        self.institution.save()


        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def save_face_encoding(self, encoding):
        # Save the encoding as a JSON string
        self.face_encoding = json.dumps(encoding.tolist())  # Convert numpy array to list and then to JSON
        self.save()




