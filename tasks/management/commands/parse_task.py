import re
import requests
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand
from tasks.models import Task, TaskNumber, TaskYear, TaskType, TaskDifficulty


class Command(BaseCommand):
    help = 'Парсит задания с сайта kpolyakov.spb.ru'

    def add_arguments(self, parser):
        parser.add_argument('--task', type=int, default=1, help='Номер задания (1-27)')

    def handle(self, *args, **kwargs):
        task_num_id = kwargs['task']
        
        # Словарь правильных URL-параметров для каждого задания
        CAT_MAP = {
            1: 'cat12=on&cat13=on',
            2: 'cat8=on',
        }
        cat_params = CAT_MAP.get(task_num_id, 'cat12=on&cat13=on')
        
        url = f'https://kpolyakov.spb.ru/school/ege/gen.php?action=viewAllEgeNo&egeId={task_num_id}&{cat_params}'
        base_images = 'https://kpolyakov.spb.ru/cms/images/'

        self.stdout.write(f"Загрузка страницы для Задания №{task_num_id}...")
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Referer': 'https://kpolyakov.spb.ru/school/ege.htm',
        }
        resp = requests.get(url, headers=headers, timeout=30)
        
        if resp.status_code != 200:
            self.stderr.write(self.style.ERROR(f'Ошибка загрузки: {resp.status_code}'))
            return

        soup = BeautifulSoup(resp.text, 'html.parser')

        task_num, _ = TaskNumber.objects.get_or_create(
            number=task_num_id, 
            defaults={'topic': f'Задание {task_num_id}'}
        )
        task_type, _ = TaskType.objects.get_or_create(name='ЕГЭ')
        difficulty, _ = TaskDifficulty.objects.get_or_create(
            name='Средний', defaults={'color': '#f59e0b'}
        )

        count = 0
        rows_processed = 0

        for row in soup.find_all('tr'):
            topic_cell = row.find('td', class_='topicview')
            if not topic_cell:
                continue

            rows_processed += 1
            js_code = str(topic_cell)

            # 1. Номер задачи
            num_match = re.search(r'\(№&nbsp;(\d+)\)', js_code)
            if not num_match:
                continue
            task_id = int(num_match.group(1))

            # 2. Текст задачи
            text_match = re.search(r"document\.write\(\s*changeImageFilePath\(['\"](.*?)['\"]\)\s*\);", js_code, re.DOTALL)
            if not text_match:
                self.stdout.write(self.style.WARNING(f'Задача №{task_id}: не найден текст в скрипте'))
                continue
            raw_text = text_match.group(1)

            # 3. Год
            year = None
            year_match = re.search(r'\((Демо|ЕГЭ|Апробация|Открытый вариант|ЕГКР|Досрочный ЕГЭ)-(\d{4})\)', raw_text)
            if year_match:
                year, _ = TaskYear.objects.get_or_create(year=int(year_match.group(2)))
                raw_text = raw_text.replace(year_match.group(0), '').strip()

            # 4. Картинка
            image_url = ''
            img_match = re.search(r'<img\s+src=["\']([^"\']+\.(?:gif|png|jpg|jpeg))["\']\s*/?>', raw_text)
            if img_match:
                src = img_match.group(1)
                filename = src.rsplit('/', 1)[-1]
                image_url = base_images + filename
                raw_text = raw_text.replace(img_match.group(0), '').strip()

            # 5. Очистка текста
            clean_text = BeautifulSoup(raw_text, 'html.parser').get_text(' ', strip=True)

            # 6. Ответ (универсальный поиск)
            answer = ''
            answer_row = row.find_next_sibling('tr')
            if answer_row and answer_row.find('td', class_='answer'):
                ans_div = answer_row.find('div', class_='hidedata')
                if ans_div:
                    ans_html = str(ans_div)
                    
                    # Ищем changeImageFilePath с любыми кавычками
                    ans_match = re.search(r"changeImageFilePath\(\s*['\"](.*?)['\"]\s*\)", ans_html, re.DOTALL)
                    
                    if ans_match:
                        answer = ans_match.group(1).strip()
                    else:
                        # Если не нашли в скрипте, берем просто текст из div
                        clean_div = re.sub(r'<script.*?</script>', '', ans_html, flags=re.DOTALL)
                        answer = BeautifulSoup(clean_div, 'html.parser').get_text(strip=True)

            # 7. Сохранение
            if not Task.objects.filter(external_id=task_id).exists():
                Task.objects.create(
                    external_id=task_id,
                    task_number=task_num,
                    year=year,
                    task_type=task_type,
                    difficulty=difficulty,
                    text=clean_text,
                    answer=answer,
                    image_url=image_url,
                )
                count += 1
                self.stdout.write(self.style.SUCCESS(f'Сохранена задача №{task_id} | Ответ: {answer}'))
            else:
                self.stdout.write(f'Пропуск №{task_id} (уже есть)')

        self.stdout.write(f'Всего найдено ячеек с задачами: {rows_processed}')
        self.stdout.write(self.style.SUCCESS(f'Готово! Добавлено: {count}'))