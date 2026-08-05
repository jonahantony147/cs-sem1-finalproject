# -*- coding: utf-8 -*-
"""
Created on Sat Nov  8 21:53:50 2025

@author: jonah
"""

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

































