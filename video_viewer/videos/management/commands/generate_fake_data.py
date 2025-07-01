from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from videos.models import Video, VideoFile
from faker import Faker
import random
from tqdm import tqdm

User = get_user_model()
fake = Faker()


class Command(BaseCommand):
    help = "Генерирует 10к пользователей и 100к видео"

    def handle(self, *args, **kwargs):
        self.stdout.write("Создаём пользователей...")
        users = []
        for _ in tqdm(range(10000)):
            users.append(User(
                username=fake.unique.user_name(),
                email=fake.email(),
            ))
        User.objects.bulk_create(users, batch_size=1000)

        all_users = list(User.objects.all())
        videos = []

        self.stdout.write("Создаём видео...")
        for _ in tqdm(range(100000)):
            videos.append(Video(
                owner=random.choice(all_users),
                name=fake.sentence(nb_words=3),
                is_published=random.choice([True, False]),
                total_likes=0,
            ))
        Video.objects.bulk_create(videos, batch_size=1000)

        all_videos = list(Video.objects.all())
        video_files = []
        qualities = ['HD', 'FHD', 'UHD']

        self.stdout.write("Создаём видеофайлы...")
        for video in tqdm(all_videos):
            selected_qualities = random.sample(qualities, k=random.randint(1, 3))
            for quality in selected_qualities:
                video_files.append(VideoFile(
                    video=video,
                    quality=quality,
                    file=f'videos/{video.id}_{quality}.mp4'  # просто строка, файл не нужен
                ))

        VideoFile.objects.bulk_create(video_files, batch_size=1000)

        self.stdout.write(self.style.SUCCESS("🎉 Данные успешно сгенерированы!"))
