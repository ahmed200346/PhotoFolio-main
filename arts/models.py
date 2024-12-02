from django.db import models
from django.core.validators import FileExtensionValidator
from users.models import User

class Art(models.Model):
    id = models.AutoField(primary_key=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='arts') 
    title = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    category = models.CharField(max_length=50, blank=True, null=True) 
    tags = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    price = models.FloatField(default=0)
    is_public = models.BooleanField(default=False)  
    likes = models.ManyToManyField(
        User, related_name='likes'
    )
    file = models.FileField(
        upload_to='arts/img/',
        validators=[
            FileExtensionValidator(
                allowed_extensions=['png', 'jpg', 'jpeg', 'gif', 'jfif', 'mp4', 'avi', 'mov', 'webm'],
                message="Le fichier doit être une vidéo (.avi, .mp4, .mov, .webm) "
                        "ou une image (.jpg, .png, .gif, .jfif)"
            )
        ]
    )

    def is_image(self):
        image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.jfif', 'webp']
        return any(self.file.name.lower().endswith(ext) for ext in image_extensions)

    def is_video(self):
        video_extensions = ['.mp4', '.avi', '.mov', '.webm']
        return any(self.file.name.lower().endswith(ext) for ext in video_extensions)

    def __str__(self):
        return f"{self.title} ({'Public' if self.is_public else 'Private'})"


class Like(models.Model):
    art = models.ForeignKey(
        Art, on_delete=models.CASCADE, related_name='arts_likes'  # Spécifiez un related_name unique ici
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)