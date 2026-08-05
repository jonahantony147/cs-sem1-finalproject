# -*- coding: utf-8 -*-
"""
Created on Thu Nov 30 17:13:28 2025

@author: jonah
"""

import random
import math

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


#phase3 functinos

#helper: mean rating of a user over all movies they rated
def userMeanRating(u, rLu):
    u_index = u - 1
    ratings_dict = rLu[u_index]
    if len(ratings_dict) == 0:
        return None
    return sum(ratings_dict.values()) / len(ratings_dict)


def similarity(u, v, rLu):
    u_index = u - 1
    v_index = v - 1

    #get rating dicts
    ratings_u = rLu[u_index]
    ratings_v = rLu[v_index]

    #if either user has no ratings, similarity is 0
    if len(ratings_u) == 0 or len(ratings_v) == 0:
        return 0.0

    #movies both users have rated
    common_movies = set(ratings_u.keys()) & set(ratings_v.keys())
    if len(common_movies) == 0:
        return 0.0

    #user mean ratings (over all their ratings)
    mean_u = userMeanRating(u, rLu)
    mean_v = userMeanRating(v, rLu)
    if mean_u is None or mean_v is None:
        return 0.0

    #compute numerator and denominator terms
    num = 0.0
    sum_sq_u = 0.0
    sum_sq_v = 0.0

    for m in common_movies:
        du = ratings_u[m] - mean_u
        dv = ratings_v[m] - mean_v
        num += du * dv
        sum_sq_u += du * du
        sum_sq_v += dv * dv

    #if denominator is 0, define similarity as 0
    if sum_sq_u == 0 or sum_sq_v == 0 or num == 0:
        return 0.0

    return num / math.sqrt(sum_sq_u * sum_sq_v)





#helper function for sorting neighbors
def neighborSortKey(pair):
    user_id, sim = pair
    return (-sim, user_id)  #higher similarity first, tie-breaker: smaller user id

def kNearestNeighbors(u, rLu, k):
    neighbors = []
    numUsers = len(rLu)
    #go through all users
    for v in range(1, numUsers + 1):
        if v == u:
            continue  #skip the user themself
        sim_uv = similarity(u, v, rLu)  #assumes you already defined similarity(u, v, rLu)
        neighbors.append((v, sim_uv))
    #sort by similarity (desc) then user id (asc)
    neighbors.sort(key=neighborSortKey)
    #return first k neighbors
    return neighbors[:k]





def CFRatingPrediction(u, m, rLu, friends):
    u_index = u - 1
    user_ratings = rLu[u_index]

    #if user has no ratings, nothing to base prediction on
    if len(user_ratings) == 0:
        return None

    #user's mean rating r_i
    mean_u = userMeanRating(u, rLu)

    num = 0.0
    denom = 0.0

    #friends is list of (friend_id, similarity)
    for (friend_id, sim_uv) in friends:
        f_index = friend_id - 1
        f_ratings = rLu[f_index]

        #skip friends who haven't rated movie m
        if m not in f_ratings:
            continue

        mean_f = userMeanRating(friend_id, rLu)
        if mean_f is None:
            continue

        num += (f_ratings[m] - mean_f) * sim_uv
        denom += abs(sim_uv)

    #if no friend contributed, fall back to user's mean rating
    if denom == 0:
        return mean_u

    return mean_u + (num / denom)



































