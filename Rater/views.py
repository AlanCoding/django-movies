from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse

# Create your views here.
from django.db.models import Count, Avg
from .models import Movie, Rater, Rating
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

# Create your views here.
from Rater.forms import UserForm, ProfileForm, RatingForm

def view_index(request):
    return render(request, "Rater/index.html")

def view_top20_movies(request):
    big_movies = Movie.objects.annotate(num_ratings=Count('rating')).filter(num_ratings__gt=10)
    movies = sorted(big_movies, key=lambda a: a.avg_rating(), reverse=True)[:20]
    return render(request,
                  "Rater/top20.html",
                  {"movies": movies})

def view_user(request, rater_id):
    r = Rater.objects.get(pk=rater_id)
    rs = r.rating_set.all()
    return render(request,
                  "Rater/user.html",
                  {"rater": r, "ratings": rs, "star_hist": r.star_hist() })

def view_movie(request, movie_id):
    movie = Movie.objects.get(pk=movie_id)
    rs = movie.rating_set.all()[:200]
    if request.method == "POST":
        rating_form = RatingForm(request.POST)
        new_rating = request.POST.get('rating')
        user = request.user
        r = Rating(rater=user.rater, movie=movie, rating=new_rating)
        r.save()
        sometext = "You have rated this movie {} stars, ".format(new_rating)
        sometext += "{}.".format(user.username)
        messages.add_message(request, messages.SUCCESS, sometext)
#        return redirect('view_movie')
        return render(request,
                  "Rater/movie.html",
                  {"movie": movie, "ratings": rs, "user_rate": True,
                   "rating_form": rating_form, "star_hist": movie.star_hist() })
    else:
        rating_form = RatingForm()
        user = request.user
        if user is not None:
            user_rate = user.rater.has_rated(movie)
        else:
            user_rate = False
        return render(request,
                      "Rater/movie.html",
                      {"movie": movie, "ratings": rs, "user_rate": user_rate,
                       "rating_form": rating_form, "star_hist": movie.star_hist() })


def view_login(request):
	if request.method == "POST":
		username = request.POST.get('username')
		password = request.POST.get('password')
		user = authenticate(username=username, password=password)
		if user is not None and user.is_active:
			login(request, user)
			sometext = "You have sucessfully logged in, {}!".format(user.username)
			messages.add_message(request, messages.SUCCESS, sometext)
			return redirect('index')
		else:
			return render(request, "Rater/login.html",
						{"failed": True, "username": username} )
	else:
		return render(request, "Rater/login.html")


def view_logout(request):
    user = request.user
    sometext = "You have sucessfully logged out. Bye."
    messages.add_message(request, messages.SUCCESS, sometext)
    logout(request)
    return redirect('index.html')
#    return redirect(reverse('index_view'))


def view_register(request):
    if request.method == "GET":
        user_form = UserForm()
        profile_form = ProfileForm()
    elif request.method == "POST":
        user_form = UserForm(request.POST)
        profile_form = ProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()

            password = user.password
            # The form doesn't know to call this special method on user.
            user.set_password(password)
            user.save()

            # You must call authenticate before login. :(
            user = authenticate(username=user.username,
                                password=password)
            login(request, user)
            messages.add_message(
                request,
                messages.SUCCESS,
                "Congratulations, {}, on creating your new account! You are now logged in.".format(
                    user.username))
            return redirect('index.html')
    return render(request, "Rater/register.html", {'user_form': user_form,
                                                   'profile_form': profile_form})

# from class
# def all_movies(request):
#     top_10_movies = Movie.objects.annotate(
#         rating_count = Count("rating"),
#         avg_rating = Avg("rating__rating"),
#     ).filter(rating_count__gte=10).order_by('-avg_rating')[:10]
#     return render(request, 'movies/index.html', {'movies':top_10_movies})

# def show_user(request, user_id):
#     user = User.objects.get(pk=user_id)
#     statuses = user.status_set.all().order_by('-posted_at')
#     return render(request,
#                   "updates/user.html",
#                   {"user": user,
#                    "statuses": statuses})