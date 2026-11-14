import requests
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from tasks.models import Task


class Command(BaseCommand):
    help = 'Скачивает картинки по image_url в ImageField'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force', action='store_true',
            help='Перекачать даже если image уже есть'
        )

    def handle(self, *args, **options):
        # Берем только те задачи, у которых есть ссылка на картинку
        qs = Task.objects.exclude(image_url='')
        
        # Если не указан --force, качаем только те, где картинки еще нет
        if not options['force']:
            qs = qs.filter(image='')

        total = qs.count()
        self.stdout.write(f'К скачиванию: {total}')

        ok = fail = 0
        for i, task in enumerate(qs.iterator(), 1):
            try:
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                    'Referer': 'https://kpolyakov.spb.ru/'
                }
                resp = requests.get(task.image_url, headers=headers, timeout=20)
                resp.raise_for_status()

                # Имя файла из URL (например, 9296.gif)
                filename = task.image_url.rsplit('/', 1)[-1]

                # Если файл уже есть — удаляем старый, чтобы не плодить копии
                if task.image:
                    task.image.delete(save=False)

                # Сохраняем файл в поле ImageField
                task.image.save(filename, ContentFile(resp.content), save=True)
                ok += 1
                self.stdout.write(
                    self.style.SUCCESS(f'[{i}/{total}] OK {task.external_id} → {filename}')
                )
            except Exception as e:
                fail += 1
                self.stderr.write(f'[{i}/{total}] FAIL {task.external_id}: {e}')

        self.stdout.write(self.style.SUCCESS(f'Готово: OK={ok}, FAIL={fail}'))