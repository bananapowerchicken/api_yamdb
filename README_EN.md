### Group project YaMDb.
### Description
The Yandex Workshop educational project YaMDb collects reviews (Review) of users on works (Title).
The works are divided into categories: “Books”, “Movies”, “Music”.
The list of categories (Category) can be expanded (for example, you can add the category “Fine Arts”).

Dev team:
- :white_check_mark: [Anna Mitelkova (as 1st Python developer and Team Lead): user model, registration, authentication, access rights, email confirmation](https://github.com/bananapowerchicken)
- :white_check_mark: [Georgy Morgunov (as the 2nd Python developer): models, handlers and urls for works, categories, genres](https://github.com/georgii265)
- :white_check_mark: [Alina Almukhametova (as the 3rd Python developer): models, handlers and urls for reviews and comments, import from csv, rating of works](https://github.com/AlmukhametovaAR)

The works themselves are not stored in YaMDb; you cannot watch a movie or listen to music here.

Each category contains works: books, films or music. For example, in the “Books” category there may be the works “Winnie the Pooh and All-All-All” and “The Martian Chronicles”, and in the “Music” category there may be the song “Davecha” by the group “Insects” and Bach’s second suite. The work can be assigned a genre from the list of preset ones (for example, “Fairy Tale”, “Rock” or “Arthouse”). Only the administrator can create new genres.

Users leave text reviews for works (Review) and give the work a rating (score ranging from one to ten). From the set of ratings, the average rating of the work is automatically calculated.

Complete documentation for the API can be found at the /redoc endpoint

### Technology stack:
- Python 3.7
- Django 3.2
- DRF
- JWT

### Launching a project in dev mode
- Clone the repository and go to it on the command line.
- Install and activate the virtual environment taking into account the version of Python 3.7 (select python no lower than 3.7):

```bash
py -m venv venv
```

```bash
source venv/Scripts/activate
```

- Then you need to install all the dependencies from the file requirements.txt

```bash
python -m pip install --upgrade pip
```

```bash
pip install -r requirements.txt
```

- Make migrations:

```bash
python manage.py migrate --run-syncdb
```

If necessary, fill the database with test data using the command:

```bash
python manage.py load_data
```

We create a superuser, then change the role in the admin panel from user to admin:

```bash
python manage.py createsuperuser
```

Start project:

```bash
python manage.py runserver localhost:80
```

### Examples of working with the API for all users

Detailed documentation is available at the endpoint /redoc/

For unauthorized users, working with the API is available in read mode; they will not be able to change or create anything.

```
Access rights: Available without a token.
GET /api/v1/categories/ - Retrieving a list of all categories
GET /api/v1/genres/ - Retrieving a list of all genres
GET /api/v1/titles/ - Retrieving a list of all works
GET /api/v1/titles/{title_id}/reviews/ - Retrieving a list of all reviews
GET /api/v1/titles/{title_id}/reviews/{review_id}/comments/ - Retrieving a list of all comments for a review
Access rights: Administrator
GET /api/v1/users/ - Retrieving a list of all users
```

