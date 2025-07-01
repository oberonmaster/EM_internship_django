from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Video(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    is_published = models.BooleanField(default=False)
    total_likes = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class VideoFile(models.Model):
    class Quality(models.TextChoices):
        HD = "HD", "720p"
        FHD = "FHD", "1080p"
        UHD = "UHD", "4K"

    video = models.ForeignKey(Video, related_name='files', on_delete=models.CASCADE)
    file = models.FileField(upload_to='videos/')
    quality = models.CharField(max_length=3, choices=Quality.choices)

    def __str__(self):
        return f"{self.video.name} - {self.quality}"


class Like(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('video', 'user')  # 1 пользователь = 1 лайк на видео

    def __str__(self):
        return f"{self.user.username} ❤️ {self.video.name}"
