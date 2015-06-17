# Django Movie Ratings

## Description

Create an interface in Django to the [MovieLens dataset][movielens].

## File Structure

The Rater class was created as its own app, with most of the files there.
The top-level is movingratings, which is on a different level from the
original repository.

A live version on heroku can be found at:

https://nameless-mountain-9760.herokuapp.com/index.html

## Learning Objectives

After completing this assignment, you should be able to:

### Night 1

* Create a new Django application
* Translate real-world data to Django models
* Explain what a database is
* Explain what a model is
* Use the Django admin
* Structure the Django admin to reflect your data

### Night 2

* Create regular expressions to map URLs to views
* Explain what a view is
* Explain what a template is
* Design simple views
* Use basic HTML
* Extrapolate from basic HTML how to create templates

### Night 3

* Distinguish when to use GET vs POST
* Create forms
* Understand registration and login
* Make use of Django's built in authentication forms and helper
* Extend user objects via OneToOneFields

## Night 4

* Expand upon current knowledge to build new Django applications and features
* Determine which model field types to use to represent data
* Understand the difference between 1:1, 1:n, and n:n relationships
* Distinguish when to use each relationship type in modeling data
* Translate English descriptions of data queries into Django ORM queries
* Use PostgreSQL to store Django data
* Use django-extensions to make development easier

## Night 5

* Build structured documents using HTML
* Make use of Bootstrap and hand-written CSS to style your application
* Organize templates for reuse

## Night 6

* Show the attributes of the request object in Views
* Create custom HTTP responses
* Use exceptions to handle common web responses
* Explain the difference between function-based views and class-based views
* Select generic views from Django to speed development

## Details

### Deliverables

* A Git repo called django-movies containing at least:
  * a `requirements.txt` file
  * a `README.md` file
  * a Django project called `movieratings`

## Night 1

### Normal Mode

Choose a dataset from the [MovieLens dataset options][movielens] and read its
README.

Create a new Django application in the `movieratings` project to hold your
models.

Create Django models for users (call the model `Rater` so as not to
confuse it with Django users), movies, and ratings. Make sure that your models
can contain the data from your dataset.

Create Django admin pages for your models.

[movielens]: http://grouplens.org/datasets/movielens/

### Hard Mode

Start adding methods to your models that you will need later. For `movie`,
you'll want the average rating for each movie, and the ability to get the
top movies by rating.

For `rater`, you'll want the average rating that rater gave to a movie, and
the ability to get the top movies that rater has not seen. You will also want
to be able to find the Euclidean distance between that rater and another using
their movie ratings. (See [our command-line version of this](https://github.com/tiyd-python-2015-05/movie-recommendations)
to see more.)

In order to do this, you'll want to [read up on the model layer of Django](https://docs.djangoproject.com/en/1.8/#the-model-layer).

Try to test these new methods. Read [Testing in Django](https://docs.djangoproject.com/en/1.8/topics/testing/)
and then either look at [django-nose](https://pypi.python.org/pypi/django-nose) or [pytest-django](https://pytest-django.readthedocs.org/en/latest/).

## Night 2

### Normal Mode

Take [the script I wrote to turn MovieLens 1M data into fixtures](https://github.com/tiyd-python-2015-05/django-movies/blob/night-1/convert_ml_1m_data.py)
and modify it to turn your CSV data into fixtures, then load those fixtures
with `python manage.py loaddata <fixture_file>`.

In your Django application, create views and templates for:

* The top 20 movies rated. This list of movies should have their average rating,
  and each movie listed should have a link to its individual page.

* Each individual movie. This page should have the movie, its average rating,
  and each person who rated it. The list of people should have the rating
  with each person and should have a link to that person's page.

* Each individual user. This page should have their demographic data, and a
  list of all movies they've rated, with the rating they gave it. Each movie
  listed should have the rating they gave it beside it and should have a link
  to that movie's page.

### Hard Mode

Try to get your recommendation algorithms from the command-line version of this
working. If you can get it working, show on each user page a list of users
most like them, and also a list of movies they might like based off those
users.

## Night 3

### Normal Mode

Link your Rater model to the built-in User model via a OneToOneField. Create
a username, email, and password for all raters.

Add registration, login, and logout to your application.

Add the ability for a user to rate a movie they have not previously rated from
the movie page.

### Hard Mode

Add the ability for a user to edit a rating they've made.

When logged in, customize pages for the user. For example, on the page that
shows the top 20 movies rated, show the user which ones they've rated.

Add a personal page for each user that only they can see. It should have all
their ratings, allow them to edit or delete those ratings, and also show
them the top 20 movies they have not rated.

## Night 4

Tonight focuses on using the Django ORM better. You have a list of changes
to make:

* Ensure users can rate movies.
* Validate that new ratings are between 1 and 5.
* Make sure new ratings are timestamped correctly.
* Allow for a short review with the rating.
* Add a personal page for each user that only they can see. It should have all
their ratings and allow them to edit or delete those ratings.
* Add a public page for each user that has all their ratings and their
user info.
* Movies should have genres, and each genre should have a page where you can
see the top rated movies for that genre.
* Have a page both for showing movies with the most ratings and movies with the highest ratings.
* Convert your application to use PostgreSQL.

### Hard Mode

Start to exercise your own creativity here. Add features based off what you're
interested in.

## Night 5: Catch up

We have a few more features we are going to add to this application. Tonight
is a good time to stop and make sure you have all the previous normal modes
done.

Focus on polish tonight. Add in Bootstrap and customize the CSS. Organize
your URLs.

## Night 6

Take your page that shows the top 20 (or however many) movies by average rating. Turn this into a paginated list using the generic class-based view (GCBV) `ListView`.

Convert the rest of your views to use GCBV's.

### Hard Mode

Add charts to your application using Matplotlib. An ideal chart -- which would require new models and caching data -- would be the average rating of a movie over time.
