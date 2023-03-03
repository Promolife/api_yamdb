import csv
import sqlite3

from django.conf import settings
from django.core.management.base import BaseCommand


def CSVImport(filename):
    path = settings.DATABASES['default']['NAME']
    con = sqlite3.connect(path)
    cur = con.cursor()
    filepath = settings.BASE_DIR / 'static/data/' / filename
    print(filepath)
    try:
        with open(filepath, 'r', encoding="utf-8") as file:
            read_result = csv.DictReader(file, delimiter=",")
            db_result = [
                (row['id'], row['name'], row['slug'])
                for row in read_result
            ]
    except Exception as error:
        print(f'File {filename} open error. {error}')
        return 0
    try:
        cur.executemany(
            (
                """
                INSERT INTO reviews_genre (id, name, slug)
                VALUES (?, ?, ?);
            """
            ),
            db_result
        )
    except Exception as error:
        print(f'File {filename} open error. {error}')
        return 0
    con.commit()
    con.close()
    print(f'Import {filename} DONE')


class Command(BaseCommand):
    help = 'Import records to Title from csv'

    def handle(self, *args, **options):
        if options['file']:
            CSVImport(options['file'])
        else:
            return 'It\'s work'

    def add_arguments(self, parser):
        parser.add_argument(
            '-f',
            '--file',
            action='store',
            default=False,
            help='Файл для импорта'
        )
