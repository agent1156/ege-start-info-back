# tasks/management/commands/download_images.py (набросок)
import requests
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from tasks.models import Task

class Command(BaseCommand):
    help = 'Скачивает картинки по image_url в ImageField'

    def handle(self, *args, **kwargs):
        qs = Task.objects.exclude(image_url='').filter(image='')
        for task in qs.iterator():
            try:
                resp = requests.get(task.image_url, timeout=15)
                resp.raise_for_status()
                filename = task.image_url.rsplit('/', 1)[-1]
                task.image.save(filename, ContentFile(resp.content), save=True)
                self.stdout.write(self.style.SUCCESS(f'OK {task.external_id}'))
            except Exception as e:
                self.stderr.write(f'FAIL {task.external_id}: {e}')