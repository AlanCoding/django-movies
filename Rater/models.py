from django.db import models
from django.db.models import Avg
from django.contrib.auth.models import User
import datetime


class ProgBar:
    text = ""
    val = 0
    def __init__(self, text, val):
        self.text = text
        self.val = val


class Genre(models.Model):
    text = models.CharField(default="", max_length=300)
    Nratings_save = models.IntegerField(null=True)
    Nmovies_save = models.IntegerField(null=True)

    def __str__(self):
        return self.text

    def total_movies(self):
        return len(self.movie_set.all())

    def total_ratings(self):
        net = 0
        for movie in self.movie_set.all():
            net += movie.total_ratings()
        return net

    def prior_genre(self):
        i = self.id - 1
        if i < 1:
            i = 1
        return i

    def next_genre(self):
        i = self.id + 1
        if i > len(Genre.objects.all()) + 1:
            i = len(Genre.objects.all()) + 1
        return i

    def prior_name(self):
        i = self.prior_genre()
        other_genre = Genre.objects.get(pk=i)
        return other_genre.text

    def next_name(self):
        i = self.next_genre()
        other_genre = Genre.objects.get(pk=i)
        return other_genre.text


class Rater(models.Model):
    age = models.IntegerField(default=0)
    gender_options = (('M', 'Male'), ('F', 'Female'))
    gender = models.CharField(max_length=1, choices=gender_options, default='M')
    occupation_options = (
    	( 0, "other"),
    	( 1, "academic/educator"),
    	( 2, "artist"),
    	( 3, "clerical/admin"),
    	( 4, "college/grad student"),
    	( 5, "customer service"),
    	( 6, "doctor/health care"),
    	( 7, "executive/managerial"),
    	( 8, "farmer"),
    	( 9, "homemaker"),
    	(10, "K-12 student"),
    	(11, "lawyer"),
    	(12, "programmer"),
    	(13, "retired"),
    	(14, "sales/marketing"),
    	(15, "scientist"),
    	(16, "self-employed"),
    	(17, "technician/engineer"),
    	(18, "tradesman/craftsman"),
    	(19, "unemployed"),
    	(20,  "writer") )
    occupation = models.IntegerField(choices=occupation_options)
    zip_code = models.CharField(max_length=10)#, default="00000)

    user = models.OneToOneField(User, null=True) # added for user accounts

    def greeting(self):
        if self.gender == "M":
            return "his"
        else:
            return "her"

    def rating_count(self):
        return self.rating_set.count()

    def prior_user(self):
        i = self.id - 1
        if i < 1:
            i = 1
        return i

    def next_user(self):
        i = self.id + 1
        if i > len(Rater.objects.all()):
            i = len(Rater.objects.all())
        return i

    def avg_rating(self):
        r_set = self.rating_set.all()
        if len(r_set) == 0:
            return 0
        else:
            dict = r_set.aggregate(Avg('rating'))
            return round(dict["rating__avg"], 2)

    def has_rated(self, movie):
        for r in self.rating_set.all():
            if r.movie == movie:
                return True
        return False

    def star_hist(self):
        hist = [0 for i in range(5)]
        for r in self.rating_set.all():
            hist[r.rating-1] += 1
        star_max = 50
        if max(hist) > star_max:
            h_max = max(hist)
            for i in range(5):
                hist[i] = int(star_max*hist[i]/h_max)
        s = ["" for i in range(5)]
        for i in range(5):
            s[i] = str(i+1)+" star: "+"#"*hist[i]
        return s


    def star_numbs(self):
        hist = [0 for i in range(5)]
        for r in self.rating_set.all():
            hist[r.rating-1] += 1
        star_max = 100
        if max(hist) > star_max:
            h_max = max(hist)
            for i in range(5):
                hist[i] = int(star_max*hist[i]/h_max)
        ret_prog = [None for i in range(5)]
        for i in range(5):
            in_text = " " + "*"*(i+1)
            ret_prog[i] = ProgBar(text=in_text, val=hist[i])
        return ret_prog


    def __str__(self):
        return "user #"+str(self.pk).ljust(5)+" with "+\
                str(self.rating_set.count())+" reviews"


class Movie(models.Model):
    title = models.CharField(max_length=200, default="unknown")
    release_date = models.IntegerField(default=1990)
    genre = models.ManyToManyField(Genre)
    avg_save = models.FloatField(null=True)
    total_save = models.IntegerField(null=True)

    def update_store(self, star, old_star=None):
        star_ct = self.avg_save*self.total_save + int(star)
        if old_star is None:
            for g in self.genre.all():
                g.Nratings_save += 1
                g.save()
            self.total_save += 1
        else:
            star_ct -= int(old_star)
        self.avg_save = star_ct / self.total_save
        self.save()

    def update_delete(self, star):
        star_ct = self.avg_save*self.total_save - int(star)
        self.total_save -= 1
        self.avg_save = star_ct / self.total_save
        self.save()

    def avg_rating(self):
        r_set = self.rating_set.all()
        if len(r_set) == 0:
            return 0
        else:
            dict = r_set.aggregate(Avg('rating'))
            return round(dict["rating__avg"], 2)

    def total_ratings(self):
        return self.rating_set.count()

    def prior_movie(self):
        i = self.id - 1
        if i < 1:
            i = 1
        return i

    def next_movie(self):
        i = self.id + 1
        if i > len(Movie.objects.all()) + 1:
            i = len(Movie.objects.all()) + 1
        return i

    def prior_name(self):
        i = self.prior_movie()
        other_movie = Movie.objects.get(pk=i)
        return other_movie.title

    def next_name(self):
        i = self.next_movie()
        other_movie = Movie.objects.get(pk=i)
        return other_movie.title

    def star_hist(self):
        hist = [0 for i in range(5)]
        for r in self.rating_set.all():
            hist[r.rating-1] += 1
        star_max = 50
        if max(hist) > star_max:
            h_max = max(hist)
            for i in range(5):
                hist[i] = int(star_max*hist[i]/h_max)
        s = ["" for i in range(5)]
        for i in range(5):
            s[i] = str(i+1)+" star: "+"#"*hist[i]
        return s


    def star_numbs(self):
        hist = [0 for i in range(5)]
        for r in self.rating_set.all():
            hist[r.rating-1] += 1
        star_max = 100
        if max(hist) > star_max:
            h_max = max(hist)
            for i in range(5):
                hist[i] = int(star_max*hist[i]/h_max)
        ret_prog = [None for i in range(5)]
        for i in range(5):
            in_text = " " + "*"*(i+1)
            ret_prog[i] = ProgBar(text=in_text, val=hist[i])
        return ret_prog

    def list_of_raters(self):
        s = ""
        for r in self.rating_set.all():
            s+= " #"+str(r.rater.pk)
        return s

    def __str__(self):
        return self.title

class Rating(models.Model):
    rater = models.ForeignKey(Rater, default=1)
    movie = models.ForeignKey(Movie, default=1)
#    posted = models.DateTimeField("rating date", default=datetime.datetime.now)
#    posted = models.DateTimeField(default=datetime.datetime(2000, 7, 14, 12, 30))
#    posted = models.DateTimeField(default=None, null=True, blank=True)
    posted = models.IntegerField(default=0)
    review = models.TextField(null=True)
    # datetime.datetime.fromtimestamp

    star_options = ((1,"*"), (2,"*"*2), (3,"*"*3), (4,"*"*4), (5,"*"*5))
    rating = models.IntegerField(default=1, choices=star_options)
#    posted_at = models.DateTimeField()

    def __str__(self):
        return self.movie.title+" rated "+str(self.rating)\
               +" by #"+str(self.rater.pk)

    def print_date(self):
        return datetime.datetime.fromtimestamp(int(self.posted)).isoformat(" ")
        #return self.posted


def fill_users():
    for r in Rater.objects.all():
        uid = "R"+str(r.id)
        r.user = User.objects.create(username=uid, email="a@example.org", password="pass")
        r.user.set_password("pass")
        r.user.save()
        r.save()

def update_custom_cache():
    print('filling movie values...')
    for m in Movie.objects.all():
        m.avg_save = m.avg_rating()
        m.total_save = m.total_ratings()
        m.save()
    print('filling genre values...')
    for g in Genre.objects.all():
        g.Nmovies_save = g.total_movies()
        g.Nratings_save = g.total_ratings()
        g.save()
    print('finished')
