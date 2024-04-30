import csv
from datetime import datetime
from collections import defaultdict

from pep_parse.settings import RESULTS_DIR


class PepParsePipeline:

    def open_spider(self, spider):
        """Создание словаря при запуске паука."""
        self.pep_statuses = defaultdict(int)

    def process_item(self, item, spider):
        """Добавление статусов PEP в словарь и их подсчёт."""
        self.pep_statuses[item.get('status')] += 1
        return item

    def close_spider(self, spider):
        """При закрытии паука задаем формат вывод данных,
        и сохраняем результаты в CSV файл"""
        date_time_now = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        filename = f'{'status_summary'}_{date_time_now}.csv'
        RESULTS_DIR.mkdir(exist_ok=True)
        with open(
            f'{RESULTS_DIR}/{filename}', 'w', newline=''
        ) as csvfile:
            fieldnames = ['status', 'qty']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            total_qty = sum(self.pep_statuses.values())
            writer.writeheader()
            for status, qty in self.pep_statuses.items():
                writer.writerow({'status': status, 'qty': qty})
            writer.writerow({'status': 'Total', 'qty': total_qty})
