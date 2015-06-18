from django.shortcuts import render, redirect, render_to_response, get_object_or_404
from django.core.urlresolvers import reverse
from django.template import RequestContext

# Create your views here.
from django.db.models import Count, Avg
from .models import Movie, Rater, Rating, Genre
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views.generic import View, RedirectView, ListView

# for class-based
from django.http import HttpResponse
from django.views.generic import View

# Create your views here.
from Rater.forms import UserForm, RaterForm, RatingForm
import datetime


def handler404(request):
    response = render_to_response('Rater/404.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 404
    return response


def handler500(request):
    response = render_to_response('Rater/500.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 500
    return response


def view_fig(request, movie_id):
    # inspired by: http://wiki.scipy.org/Cookbook/Matplotlib/Django
    from random import randint
    from django.http import HttpResponse

    from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
    from matplotlib.figure import Figure
    from matplotlib.dates import DateFormatter

    movie = Movie.objects.get(pk=movie_id)
    ratings = movie.rating_set.all().order_by('-posted')
    fig=Figure()
    ax=fig.add_subplot(111)
    x=[]
    y=[]
    # datetime.datetime.fromtimestamp(int(self.posted))
    # rating.posted
    now_var = datetime.datetime.now()
    delta = datetime.timedelta(days=1)
    avg_span = 10
    for i in range(len(ratings)-avg_span):
        rating = ratings[i]
        rsum = 0
        for j in range(avg_span):
            rsum += ratings[i+j].rating
        y.append(rsum/avg_span)
        x.append(datetime.datetime.fromtimestamp(rating.posted))
#        x.append(rating.rater.age)
#        y.append(rating.rating)
    ax.plot_date(x, y, '-')
#    ax.scatter(x, y)
    ax.xaxis.set_major_formatter(DateFormatter('%Y-%m'))
    fig.autofmt_xdate()
    fig.suptitle("Ratings over time over "+str(avg_span)+" review intervals")
    ax.set_xlabel("Year and Month", fontsize=12)
    ax.set_ylabel("Average Rating (rolling basis)", fontsize=12)
    canvas=FigureCanvas(fig)
    response= HttpResponse(content_type='image/png')
    canvas.print_png(response)
    return response


def view_index(request):
    return render(request, "Rater/index.html", {"genres": Genre.objects.all()})

def view_top20_movies(request):
    movies = Movie.objects.filter(total_save__gt=10).order_by('-avg_save')[:20]
#    big_movies = Movie.objects.annotate(num_ratings=Count('rating')).filter(num_ratings__gt=10)
#    movies = sorted(big_movies, key=lambda a: a.avg_rating(), reverse=True)[:20]
    return render(request,
                  "Rater/top20.html",
                  {"movies": movies})


class Top20View(ListView):
    template_name = 'Rater/top20.html'
    model = Movie # I think this might be why it wanted to sort by id #
    paginate_by = 20
    context_object_name = 'movies'
    querryset = Movie.objects.filter(total_save__gt=10).order_by('-avg_save')

    def get_queryset(self):
        return self.querryset

#    def get_context_data(self, **kwargs):
#        context = super(Top20View, self).get_context_data(**kwargs)
#        context['movies'] = Movie.objects.filter(total_save__gt=10).order_by('-avg_save')
#        return context

#    context_object_name = 'movies' # do we need these? I don't know.
#    header = 'top_rated_movies'

#    def get(self, request):
#        return response


def view_genre(request, genre_id):
    genre = Genre.objects.get(pk=genre_id)
    genre_movies = genre.movie_set.all()
    big_movies = genre_movies.annotate(num_ratings=Count('rating')).filter(num_ratings__gt=10)
    movies = sorted(big_movies, key=lambda a: a.avg_rating(), reverse=True)[:20]
    return render(request,
                    "Rater/genre.html",
                    {"genre": genre, "movies": movies})


class GenreView(ListView):
    template_name = 'Rater/genre.html'
#    model = Movie
    paginate_by = 20
    context_object_name = 'movies'
    genre_id = None
    genre = None

    def get_queryset(self):
        self.genre = get_object_or_404(Genre, pk=self.args[0])
        self.genre_id = self.genre.id

        genre = Genre.objects.get(pk=self.genre_id)
        genre_movies = genre.movie_set.filter(total_save__gt=10)
#        big_movies = genre_movies.annotate(num_ratings=Count('rating')).filter(num_ratings__gt=10)
        movies = genre_movies.order_by('-avg_save')
#        movies = sorted(big_movies, key=lambda a: a.avg_rating(), reverse=True)
        return movies

    def get_context_data(self, **kwargs):
        print(kwargs)
        context = super(GenreView, self).get_context_data(**kwargs)
        context['genre'] = Genre.objects.get(pk=self.genre_id)
        return context
    #
    # def get(self, request):
    #     self.genre = Genre.objects.get(pk=self.genre_id)
    #     movies = self.get_queryset(genre_id)
    #     return render(request, "Rater/genre.html",
    #             {"genre":self.genre, "movies":movies})


def view_user(request, rater_id):
    r = Rater.objects.get(pk=rater_id)
    rs = r.rating_set.order_by('-posted')
    return render(request,
                  "Rater/user.html",
                  {"rater": r, "ratings": rs })

def view_rating(request, rating_id):
    rating = Rating.objects.get(pk=rating_id)
    if request.method == "POST":
        rating_form = RatingForm(request.POST)
        new_rating = request.POST.get('rating')
        new_review = request.POST.get('review')
        rating.review = str(new_review)
        rating.rating = int(new_rating)
        rating.save()
        sometext = "You have updated your rating"
        messages.add_message(request, messages.SUCCESS, sometext)
        return redirect('user.html'+ str(rating.rater.id))
    else:
        rating_form = RatingForm(initial={"rating":rating.rating,
                                    "review":rating.review})
        return render(request, "Rater/rating.html",
                    {"rating": rating, "rating_form": rating_form})



def view_movie(request, movie_id):
    movie = Movie.objects.get(pk=movie_id)
    rs = movie.rating_set.order_by('-posted')[:200]
    if request.method == "POST":
        rating_form = RatingForm(request.POST)
        new_rating = request.POST.get('rating')
        new_review = request.POST.get('review')
        user = request.user
        r = Rating(rater=user.rater, movie=movie, rating=new_rating, review=new_review)
        dt_now = datetime.datetime.now()
        post_int = (dt_now - datetime.datetime(1970, 1, 1)).total_seconds()
        r.posted = post_int
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
        if user is not None and user.is_authenticated():
            user_rate = user.rater.has_rated(movie)
        else:
            user_rate = False
        return render(request,
                      "Rater/movie.html",
                      {"movie": movie, "ratings": rs, "user_rate": user_rate,
                       "rating_form": rating_form })


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
        rater_form = RaterForm()
    elif request.method == "POST":
        user_form = UserForm(request.POST)
        rater_form = RaterForm(request.POST)
        if user_form.is_valid() and rater_form.is_valid():
            user = user_form.save()
            rater = rater_form.save(commit=False)
            rater.user = user
            rater.save()

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
                                                   'rater_form': rater_form})


def view_dashboard(request):
    user = request.user
    rater = user.rater
    if request.method == "GET":
        pass
    elif request.method == "POST":
        if "user_edit" in request.POST:
            user_form = UserForm(request.POST)
            if user_form.is_valid():
                user.username = requet.POST.get('username')
                user.email = requet.POST.get('email')
                user.save()
                messages.add_message(request, messages.SUCCESS, "You have updated your account")
        elif "rater_edit" in request.POST:
            rater_form = RaterForm(request.POST)
            if rater_form.is_valid():
                rater.age = request.POST.get('age')
                rater.gender = request.POST.get('gender')
                rater.occupation = request.POST.get('occupation')
                rater.zip_code = request.POST.get('zip_code')
                rater.save()
                messages.add_message(request, messages.SUCCESS, "You have updated your profile")
        elif "delete_button" in request.POST:
            idx = int(request.POST.get('rating'))
            rating = Rating.objects.get(pk=idx)
            sometext = "Sucessfully deleted rating of {}".format(rating.movie.title)
            print(idx)
            Rating.objects.get(pk=idx).delete()
            messages.add_message(request, messages.SUCCESS, sometext)

    user_form = UserForm(initial={'username':user.username, 'email':user.email})
    rater_form = RaterForm(initial = {'age':rater.age, 'gender':rater.gender,
                        'occupation':rater.occupation, 'zip_code':rater.zip_code})
    return render(request, "Rater/dashboard.html", {'user_form': user_form,
                                        'rater_form': rater_form})
