import re
import requests
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand
from tasks.models import Task, TaskNumber, TaskYear, TaskType, TaskDifficulty


class Command(BaseCommand):
    help = 'Парсит задания №1 с сайта kpolyakov.spb.ru'

    def handle(self, *args, **kwargs):
        url = ('https://kpolyakov.spb.ru/school/ege/gen.php'
               '?action=viewAllEgeNo&egeId=1&cat12=on&cat13=on')
        base_images = 'https://kpolyakov.spb.ru/cms/images/'

        self.stdout.write("Загрузка страницы...")
        headers = {
            'User-Agent': ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                           'AppleWebKit/537.36 (KHTML, like Gecko) '
                           'Chrome/124.0.0.0 Safari/537.36'),
            'Accept-Language': 'ru-RU,ru;q=0.9,en;q=0.8',
            'Referer': 'https://kpolyakov.spb.ru/school/ege.htm',
        }
        resp = requests.get(url, headers=headers, timeout=30)
        if resp.status_code != 200:
            self.stderr.write(self.style.ERROR(f'Ошибка загрузки: {resp.status_code}'))
            return

        soup = BeautifulSoup(resp.text, 'html.parser')

        task_num, _ = TaskNumber.objects.get_or_create(
            number=1, defaults={'topic': 'Анализ информационных моделей'}
        )
        task_type, _ = TaskType.objects.get_or_create(name='ЕГЭ')
        difficulty, _ = TaskDifficulty.objects.get_or_create(
            name='Средний', defaults={'color': '#f59e0b'}
        )

        count = 0

        for row in soup.find_all('tr'):
            topic_cell = row.find('td', class_='topicview')
            if not topic_cell:
                continue

            js_code = str(topic_cell)

            num_match = re.search(r'\(№&nbsp;(\d+)\)', js_code)
            if not num_match:
                continue
            task_id = int(num_match.group(1))

            text_match = re.search(
                r"document\.write\(\s*changeImageFilePath\('(.*?)'\)\s*\);",
                js_code, re.DOTALL
            )
            if not text_match:
                continue
            raw_text = text_match.group(1)

            year = None
            year_match = re.search(
                r'\((Демо|ЕГЭ|Апробация|Открытый вариант|ЕГКР|Досрочный ЕГЭ)-(\d{4})\)',
                raw_text
            )
            if year_match:
                year, _ = TaskYear.objects.get_or_create(year=int(year_match.group(2)))
                raw_text = raw_text.replace(year_match.group(0), '').strip()

            image_url = ''
            img_match = re.search(r'<img\s+src="([^"]+\.(?:gif|png|jpg|jpeg))"', raw_text)
            if img_match:
                src = img_match.group(1)
                filename = src.rsplit('/', 1)[-1]
                image_url = base_images + filename
                raw_text = raw_text.replace(img_match.group(0), '').strip()

            clean_text = BeautifulSoup(raw_text, 'html.parser').get_text(' ', strip=True)

            answer = ''
            answer_row = row.find_next_sibling('tr')
            if answer_row and answer_row.find('td', class_='answer'):
                ans_div = answer_row.find('div', class_='hidedata')
                if ans_div:
                    ans_js = str(ans_div)
                    ans_match = re.search(r"changeImageFilePath\('(.*?)'\)", ans_js)
                    if ans_match:
                        answer = ans_match.group(1).strip()

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
                self.stdout.write(self.style.SUCCESS(f'Сохранена задача №{task_id}'))

        self.stdout.write(self.style.SUCCESS(f'Готово! Добавлено: {count}'))
