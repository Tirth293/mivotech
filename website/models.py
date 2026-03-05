from django.db import models
from django.contrib.auth.models import User
import os

# =========================
# Feedback Model
# =========================
class Feedback(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.created_at.strftime('%Y-%m-%d')}"


# =========================
# Admin Profile Model
# =========================
class AdminProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='adminprofile')
    profile_image = models.ImageField(
        upload_to='admin_profiles/',
        default='admin_profiles/default.png',
        blank=True,
        null=True
    )

    def __str__(self):
        return f"{self.user.username}'s Profile"
    
    def delete(self, *args, **kwargs):
        # Delete image file when profile is deleted (if not default)
        if self.profile_image and self.profile_image.name != 'admin_profiles/default.png':
            if os.path.isfile(self.profile_image.path):
                os.remove(self.profile_image.path)
        super().delete(*args, **kwargs)