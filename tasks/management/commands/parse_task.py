import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from tasks.models import Task, TaskNumber, TaskYear, TaskType, TaskDifficulty


class Command(BaseCommand):
    help = 'Парсит задания с сайта kpolyakov.spb.ru'

    def add_arguments(self, parser):
        parser.add_argument('--task', type=int, default=1, help='Номер задания (1-27)')

    def handle(self, *args, **kwargs):
        task_num_id = kwargs['task']
        
        CAT_MAP = {
            1: 'cat12=on&cat13=on',
            2: 'cat8=on',
            3: 'cat169=on',
            4: 'cat21=on&cat22=on&cat23=on&cat25=on&cat166=on',
            5: 'cat27=on&cat28=on&cat144=on',
            6: 'cat175=on&cat179=on&cat180=on',
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
        for row in soup.find_all('tr'):
            topic_cell = row.find('td', class_='topicview')
            if not topic_cell:
                continue

            js_code = str(topic_cell)

            # 1. Номер задачи
            num_match = re.search(r'\(№&nbsp;(\d+)\)', js_code)
            if not num_match:
                continue
            task_id = int(num_match.group(1))

            # 2. Текст задачи
            text_match = re.search(r"document\.write\(\s*changeImageFilePath\(['\"](.*?)['\"]\)\s*\);", js_code, re.DOTALL)
            if not text_match:
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

            # 5. ФАЙЛ
            attachment_url = ''
            file_match = re.search(r'<a\s+href=["\']([^"\']+\.(?:xlsx|xls|ods|csv|doc|docx|txt|zip|rar))["\']', raw_text)
            
            if file_match:
                relative_src = file_match.group(1)
                
                if 'ege-dbase' in relative_src:
                    attachment_url = f'https://kpolyakov.spb.ru/cms/files/{relative_src}'
                elif 'cms/files' in relative_src:
                    attachment_url = relative_src.replace('../../', 'https://kpolyakov.spb.ru/')
                else:
                    attachment_url = f'https://kpolyakov.spb.ru/school/ege/{relative_src}'
                    
                raw_text = raw_text.replace(file_match.group(0), '').strip()

                        # 6. ОЧИСТКА ТЕКСТА (СОХРАНЕНИЕ СТРУКТУРЫ)
            
            # 1. Заменяем теги <br> и <br/> на переносы строк
            raw_text = re.sub(r'<br\s*/?>', '\n', raw_text, flags=re.IGNORECASE)
            
            # 2. Оборачиваем блоки <pre> в переносы (до и после), чтобы отделить код от текста
            raw_text = re.sub(r'<pre[^>]*>', '\n', raw_text, flags=re.IGNORECASE)
            raw_text = re.sub(r'</pre>', '\n', raw_text, flags=re.IGNORECASE)
            
            # 3. Создаем BeautifulSoup для извлечения чистого текста
            soup_text = BeautifulSoup(raw_text, 'html.parser')
            
            # 4. Извлекаем текст. separator='' не добавляет лишние пробелы
            clean_text = soup_text.get_text(separator='')
            
            # 5. Убираем лишние пустые строки (если их больше двух подряд)
            clean_text = re.sub(r'\n{3,}', '\n\n', clean_text)
            
            # 6. Убираем лишние пробелы внутри строк, но оставляем переносы
            clean_text = '\n'.join([line.strip() for line in clean_text.split('\n')])
            
            # 7. Финальная зачистка пустых строк в начале и конце
            clean_text = clean_text.strip()

            # 7. Ответ
            answer = ''
            answer_row = row.find_next_sibling('tr')
            if answer_row and answer_row.find('td', class_='answer'):
                ans_div = answer_row.find('div', class_='hidedata')
                if ans_div:
                    ans_html = str(ans_div)
                    ans_match = re.search(r"changeImageFilePath\(\s*['\"](.*?)['\"]\s*\)", ans_html, re.DOTALL)
                    if ans_match:
                        answer = ans_match.group(1).strip()

            # 8. СОХРАНЕНИЕ
            if not Task.objects.filter(external_id=task_id).exists():
                task = Task.objects.create(
                    external_id=task_id,
                    task_number=task_num,
                    year=year,
                    task_type=task_type,
                    difficulty=difficulty,
                    text=clean_text,
                    answer=answer,
                    image_url=image_url,
                )

                # Скачиваем файл, если он есть
                if attachment_url:
                    try:
                        file_resp = requests.get(attachment_url, headers=headers, timeout=20)
                        file_resp.raise_for_status()
                        filename = attachment_url.rsplit('/', 1)[-1]
                        task.attachment.save(filename, ContentFile(file_resp.content), save=True)
                        self.stdout.write(self.style.SUCCESS(f'  -> Файл {filename} скачан'))
                    except requests.exceptions.HTTPError as e:
                        if e.response.status_code == 404:
                            self.stdout.write(self.style.WARNING(f'  -> Файл не найден на сервере (404), пропускаем'))
                        else:
                            self.stderr.write(f'  -> Ошибка скачивания файла: {e}')
                    except Exception as e:
                        self.stderr.write(f'  -> Ошибка: {e}')

                count += 1
                self.stdout.write(self.style.SUCCESS(f'Сохранена задача №{task_id}'))
            else:
                self.stdout.write(f'Пропуск №{task_id} (уже есть)')

        self.stdout.write(self.style.SUCCESS(f'Готово! Добавлено: {count}'))