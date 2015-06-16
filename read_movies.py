import csv
import json
import datetime

source_base = "../data/ml-1m/"
print("Converting users...")
users = []
occupation_list = []
with open(source_base + "users.dat") as infile:
    reader = csv.reader((line.replace("::", ";") for line in infile),
                        delimiter=";")
    for row in reader:
        row_last = row
        users.append({"model": "Rater.Rater",
                      "pk": row[0],
                      "fields": {
                          "gender": row[1],
                          "age": row[2],
                          "occupation": row[3],
                          "zip_code": row[4]
                      }})
        if row[3] not in occupation_list:
            occupation_list.append(row[3])
    print(" example: "+str(users[0]))
    print(" ")

print(occupation_list)

with open("fixtures/users.json", "w") as outfile:
    outfile.write(json.dumps(users))

print("Converting movies...")
movies = []
genre_list = []
with open(source_base + "movies.dat", encoding="windows-1252") as infile:
    reader = csv.reader((line.replace("::", ";") for line in infile),
                        delimiter=";")
    for row in reader:
        row_last = row
        m_genres = row[2].split("|")
        movies.append({"model": "Rater.Movie",
                       "pk": row[0],
                       "fields": {
                           "title": row[1],
                           "genre": m_genres
                       }})
        for g in m_genres:
            if g not in genre_list:
                genre_list.append(g)
    print(row_last)
    print(row_last[2].replace("|",","))
    print(" example: "+str(movies[0]))
    print(" ")

print("Converting genres...")
genres = []
print(genre_list)
for i in range(len(genre_list)):
    genres.append({"model": "Rater.Genre",
                   "pk": i,
                   "fields": {
                        "text": genre_list[i]
                   }})
print(" ")


def get_genre_pk(text, genre_list):
    for i in range(len(genre_list)):
        if text == genre_list[i]:
            return i + 1
    print(" genre lookup failed "+text)


with open("fixtures/genres.json", "w") as outfile:
    outfile.write(json.dumps(genres))


for movie in movies:
    g_set = movie["fields"]["genre"]
    for i in range(len(g_set)):
        movie["fields"]["genre"][i] = get_genre_pk(movie["fields"]["genre"][i], genre_list)


with open("fixtures/movies.json", "w") as outfile:
    outfile.write(json.dumps(movies))

print("Converting ratings...")
ratings = []
with open(source_base + "ratings.dat") as infile:
    reader = csv.reader((line.replace("::", ";") for line in infile),
                        delimiter=";")
    for idx, row in enumerate(reader):
        row_last = row
        ratings.append({"model": "Rater.Rating",
                        "pk": idx + 1,
                        "fields": {
                            "rater": row[0],
                            "movie": row[1],
                            "rating": row[2],
                            "posted": row[3]
                        }})
    print(row_last)
    print(" example: "+str(ratings[0]))
    print(" ")

with open("fixtures/ratings.json", "w") as outfile:
    outfile.write(json.dumps(ratings))
