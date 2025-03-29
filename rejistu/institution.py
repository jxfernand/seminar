# rejistu/intitution.py
from django.db import models
from django.core.exceptions import ValidationError
import uuid
from django.core.validators import RegexValidator





class Institution(models.Model):
    name = models.CharField(max_length=100, unique=True)
    quota = models.PositiveIntegerField(default=10)  # Total quota for the institution
    access_pass_counter = models.PositiveIntegerField(default=0)  # Track allocated access passes

    def __str__(self):
        return self.name

    def is_quota_full(self):
        return self.access_pass_counter >= self.quota

    # def save(self, *args, **kwargs):
    #     # Check if the institution is being created or updated
    #     if self.pk is None:  # New institution being created
    #         super().save(*args, **kwargs)  # Save the institution first to get an ID
    #         # Generate Access Passes based on the quota
    #         for _ in range(self.quota):
    #             AccessPass.objects.create(institution=self)
    #     else:  # Existing institution being updated
    #         super().save(*args, **kwargs)

    def save(self, *args, **kwargs):
        # Check if the institution is being created or updated
        if self.pk is None:  # New institution being created
            super().save(*args, **kwargs)  # Save the institution first to get an ID
            # Generate Access Passes based on the quota
            for _ in range(self.quota):
                AccessPass.objects.create(institution=self)
        else:  # Existing institution being updated
            # Get the current quota from the database
            current_quota = Institution.objects.get(pk=self.pk).quota

            if self.quota > current_quota:  # Quota increased
                # Generate additional Access Passes
                for _ in range(self.quota - current_quota):
                    AccessPass.objects.create(institution=self)
            elif self.quota < current_quota:  # Quota decreased
                # Delete excess Access Passes (unused ones first)
                excess = current_quota - self.quota
                unused_passes = self.access_passes.filter(is_used=False)[:excess]
                unused_passes.delete()

            super().save(*args, **kwargs)


    def delete(self, *args, **kwargs):
        # Delete all associated Access Passes when the institution is deleted
        self.access_passes.all().delete()
        super().delete(*args, **kwargs)



class AccessPass(models.Model):
    code = models.CharField(max_length=10, unique=True, blank=True)  # Auto-generated access pass code
    institution = models.ForeignKey('Institution', on_delete=models.CASCADE, related_name='access_passes')
    is_used = models.BooleanField(default=False)  # Track if the access pass has been used

    def save(self, *args, **kwargs):
        # Generate a unique access pass code if it doesn't exist
        if not self.code:
            self.code = str(uuid.uuid4())[:8].upper()  # Generate a random 8-character code
        super().save(*args, **kwargs)





    def __str__(self):
        return f"{self.code} ({self.institution.name})"




