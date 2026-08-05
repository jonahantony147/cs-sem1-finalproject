# -*- coding: utf-8 -*-
"""
Created on Thu Nov 20 15:29:02 2025

@author: jonah
"""


import matplotlib.pyplot as plt
import math
import random


def createUserList(filename="ml-100k/u.user"):
    numUsers = []  #list to store all user dictionaries
    f = open(filename, "r", encoding="latin-1")  #open the file to read data
    for line in f:  # go through each user
        user_id, age, gender, occupation, zip_code = line.strip().split("|")
        numUsers.append({
            "age": int(age),
            "gender": gender,
            "occupation": occupation,
            "zip": zip_code
        })
    f.close()  
    return numUsers  


def createMovieList(filename="ml-100k/u.item"):
    numItems = []  #list to store movie info
    f = open(filename, "r", encoding="latin-1")  #open the movie file
    for line in f:
        parts = line.strip().split("|")  #split each line by "|"
        movie = {
            "title": parts[1],
            "release date": parts[2],
            "video release date": parts[3],
            "IMDB url": parts[4],
            "genre": [int(x) for x in parts[5:24]]  #last 19 columns are 0/1s
        }
        numItems.append(movie)  #add the dictionary to the list
    f.close()  
    return numItems


def readRatings(filename="ml-100k/u.data"):
    ratingTuples = []  #list to store (user, movie, rating) tuples
    f = open(filename, "r", encoding="latin-1")
    for line in f:
        parts = line.strip().split()  #split automatically handles any amount of space or tabs
        user_id, movie_id, rating, timestamp = parts
        ratingTuples.append((int(user_id), int(movie_id), int(rating)))
    f.close()
    return ratingTuples


def createRatingsDataStructure(numUsers, numItems, ratingTuples):
    rLu = [{} for i in range(numUsers)]   #each user gets a dict
    rLm = [{} for i in range(numItems)]   #each movie gets a dict
    #go through every (user, movie, rating) tuple
    for (user, movie, rating) in ratingTuples:
        rLu[user - 1][movie] = rating   #add movie + rating to that user’s dict
        rLm[movie - 1][user] = rating   #add user + rating to that movie’s dict
    return [rLu, rLm]


def createGenreList(filename="ml-100k/u.genre"):
    genres = []  #list to store all genre names
    f = open(filename, "r", encoding="latin-1")  
    for line in f:
        line = line.strip()
        if line != "":  #skip empty lines if any
            name, num = line.split("|")  
            genres.append(name)  #store just the name
    f.close()
    return genres


userList = createUserList()
movieList = createMovieList()
ratingTuples = readRatings()
numUsers = len(userList)
numItems = len(movieList)
rLu, rLm = createRatingsDataStructure(numUsers, numItems, ratingTuples)


def demGenreRatingFractions(userList, movieList, rLu, gender, ageRange, ratingRange):
    #set ranges
    age1, age2 = ageRange
    r1, r2 = ratingRange
    #count of ratings for 19 genres
    genreCounts = [0] * 19
    genreInRange = [0] * 19
    totalRatings= 0
    
    user_id = 1  #user IDs start from 1
    for user in userList:
        #filter by gender
        if gender != "A" and user["gender"] != gender:
            user_id += 1
            continue

        #filter by age range
        if not (age1 <= user["age"] < age2):
            user_id += 1
            continue

        userRatings = rLu[user_id - 1]  #ratings for this user

        for movie_id, rating in userRatings.items():
            movie = movieList[movie_id - 1]
            totalRatings += 1

            for i in range(19):
                if movie["genre"][i] == 1:
                    genreCounts[i] += 1
                    if r1 <= rating <= r2:
                        genreInRange[i] += 1
        user_id += 1  

    if totalRatings == 0:
        return [None] * 19  #return list of Nones if invalid age range
    
    genreFractions = []
    for i in range(19):
        if genreCounts[i] > 0:
            genreFractions.append(genreInRange[i] / totalRatings)
        else:
            genreFractions.append(0.0) 
    #change None to 0.0 to avoid round error
    genreFractions = [0.0 if x is None else x for x in genreFractions]   
    
    return genreFractions



userList = createUserList()
movieList = createMovieList()
rawRatings = readRatings()
rLu, rLm = createRatingsDataStructure(len(userList), len(movieList), rawRatings)


def randomPrediction(u, m):
    return random.randint(1, 5)


def meanUserRatingPrediction(u, m, rLu):
    user_index = u - 1
    if user_index < 0 or user_index >= len(rLu):
        return None
    userRatings = rLu[user_index]   #dict: movie_id → rating
    if len(userRatings) == 0:
        return None
    return sum(userRatings.values())/len(userRatings)


def meanMovieRatingPrediction(u, m, rLm):
    movie_index = m - 1
    if movie_index < 0 or movie_index >= len(rLm):
        return None
    movieRatings = rLm[movie_index]   #dict: user_id → rating
    if len(movieRatings) == 0:
        return None
    return sum(movieRatings.values()) / len(movieRatings)


def demRatingPrediction(u, m, userList, rLu):
    u_index = u - 1
    m = int(m)
    userGender = userList[u_index]["gender"]
    userAge = userList[u_index]["age"]
    lower = userAge - 5
    upper = userAge + 5
    ratings = []
    #loop neighbors
    for other_u in range(1, len(userList) + 1):
        other_index = other_u - 1
        #skip self
        if other_u == u:
            continue
        other = userList[other_index]
        #gender + age filter
        if other["gender"] == userGender and lower <= other["age"] <= upper:
            if m in rLu[other_index]:
                ratings.append(rLu[other_index][m])
    #if no neighbors -> REQUIRED return None
    if len(ratings) == 0:
        return None
    return sum(ratings) / len(ratings)



def movieGenres(movieList, movie_id):  #helper function 1  
    return movieList[movie_id - 1]["genre"]

def sharesGenre(g1, g2):  #helper function 2
    #both are lists of 0/1 flags of length 19
    for i in range(len(g1)):
        if g1[i] == 1 and g2[i] == 1:
            return True
    return False

def genreRatingPrediction(u, m, movieList, rLu):
    user_index = u - 1
    m_genres = movieGenres(movieList, m)
    userRatings = rLu[user_index]
    genre_ratings = []
    for movie_id, rating in userRatings.items():
        if movie_id == m:
            continue  #skip the movie we are predicting
        if sharesGenre(m_genres, movieGenres(movieList, movie_id)):
            genre_ratings.append(rating)
    if len(genre_ratings) == 0:
        return None
    return sum(genre_ratings) / len(genre_ratings)




#function 6&7
def partitionRatings(rawRatings, testPercent):
    #calculate number of test ratings
    total = len(rawRatings)
    testCount = int((testPercent / 100) * total)
    #randomly select unique indices for test set
    testIndices = set(random.sample(range(total), testCount))
    trainingSet = []
    testSet = []
    #split based on chosen indices
    for i in range(total):
        if i in testIndices:
            testSet.append(rawRatings[i])
        else:
            trainingSet.append(rawRatings[i])
    return trainingSet, testSet



def rmse(actualRatings, predictedRatings):
    #skip none predictions
    s = 0  #sum of squared diffs
    count = 0
    for i in range(len(actualRatings)):
        p = predictedRatings[i]
        if p is None:
            continue
        if isinstance(p, float) and (p != p):  #skip NaN
            continue
        diff = actualRatings[i] - p
        s += diff * diff
        count += 1
    if count == 0:
        return None  #no valid predictions
    return math.sqrt(s / count)



#load data
userList = createUserList()
movieList = createMovieList()
rawRatings = readRatings()

#rmse lists for 5 algorithms
rmse_random = []
rmse_user = []
rmse_movie = []
rmse_dem = []
rmse_genre = []

#repeat experiment 10 times
for i in range(10):
    #step 1: split data
    trainingSet, testSet = partitionRatings(rawRatings, 20)

    #step 2: build data structures from training set only
    numUsers = len(userList)
    numMovies = len(movieList)
    trainingRLu, trainingRLm = createRatingsDataStructure(numUsers, numMovies, trainingSet)

    #lists to store predicted and actual ratings
    actual = []
    pred_random = []
    pred_user = []
    pred_movie = []
    pred_dem = []
    pred_genre = []

    #step 3: loop through test set
    for (u, m, r) in testSet:
        actual.append(r)
        pred_random.append(randomPrediction(u, m))
        pred_user.append(meanUserRatingPrediction(u, m, trainingRLu))
        pred_movie.append(meanMovieRatingPrediction(u, m, trainingRLm))
        pred_dem.append(demRatingPrediction(u, m, userList, trainingRLu))
        pred_genre.append(genreRatingPrediction(u, m, movieList, trainingRLu))

    #step 4: compute rmse for this repetition
    rmse_random.append(rmse(actual, pred_random))
    rmse_user.append(rmse(actual, pred_user))
    rmse_movie.append(rmse(actual, pred_movie))
    rmse_dem.append(rmse(actual, pred_dem))
    rmse_genre.append(rmse(actual, pred_genre))

#step 5: plot results
data = [rmse_random, rmse_user, rmse_movie, rmse_dem, rmse_genre]
plt.boxplot(data, patch_artist=True)
plt.xticks([1,2,3,4,5], ['random','user','movie','dem','genre'])
plt.ylabel('RMSE')
plt.title('RMSE comparison of prediction algorithms')
plt.show()
