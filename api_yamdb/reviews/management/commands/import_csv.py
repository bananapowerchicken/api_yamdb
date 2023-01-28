import csv
import sqlite3

from django.core.management.base import BaseCommand
from reviews.models import Category, Comment, Genre, Review, Title, User


class Command(BaseCommand):
    help = 'Импорт данных из csv-файла'
# -------------------------------------------------------------------

    def handle(self, *args, **options):
        with open('./static/data/users.csv',
                  'r', encoding='utf-8') as users:
            for row in csv.DictReader(users):
                User(
                    id=row['id'],
                    username=row['username'],
                    email=row['email'],
                    role=row['role'],
                    bio=row['bio'],
                    first_name=row['first_name'],
                    last_name=row['last_name']
                ).save()
# -------------------------------------------------------------------
        with open('./static/data/category.csv',
                  'r', encoding='utf-8') as category:
            for row in csv.DictReader(category):
                Category(
                    id=row['id'],
                    name=row['name'],
                    slug=row['slug']
                ).save()
# -------------------------------------------------------------------
        with open('./static/data/genre.csv',
                  'r', encoding='utf-8') as genre:
            for row in csv.DictReader(genre):
                Genre(
                    id=row['id'],
                    name=row['name'],
                    slug=row['slug']
                ).save()
# -------------------------------------------------------------------
        with open('./static/data/titles.csv',
                  'r', encoding='utf-8') as titles:
            for row in csv.DictReader(titles):
                Title(
                    id=row['id'],
                    name=row['name'],
                    year=row['year'],
                    category_id=row['category']
                ).save()
# -------------------------------------------------------------------
        con = sqlite3.connect('db.sqlite3')
        cur = con.cursor()
        with open('./static/data/genre_title.csv',
                  'r', encoding='utf-8') as genre_title:
            reader = csv.DictReader(genre_title)
            to_db = [(
                row['id'], row['title_id'], row['genre_id']
            ) for row in reader]

        cur.executemany('''
        INSERT INTO reviews_title_genre (id,title_id,genre_id) VALUES (?,?,?);
        ''', to_db)
        con.commit()
        con.close()
# -------------------------------------------------------------------
        with open('./static/data/review.csv',
                  'r', encoding='utf-8') as reviews:
            for row in csv.DictReader(reviews):
                Review(
                    id=row['id'],
                    title_id=row['title_id'],
                    text=row['text'],
                    author_id=row['author'],
                    score=row['score'],
                    pub_date=row['pub_date']
                ).save()
# -------------------------------------------------------------------
        with open('./static/data/comments.csv',
                  'r', encoding='utf-8') as comments:
            for row in csv.DictReader(comments):
                Comment(
                    id=row['id'],
                    review_id=row['review_id'],
                    text=row['text'],
                    author_id=row['author'],
                    pub_date=row['pub_date']
                ).save()
# -------------------------------------------------------------------
