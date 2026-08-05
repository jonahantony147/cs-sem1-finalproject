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
    rLu = [{} for _ in range(numUsers)]   #each user gets a dict
    rLm = [{} for _ in range(numItems)]   #each movie gets a dict
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



import matplotlib.pyplot as plt

def plotDemographicComparisons(userList, movieList, rLu):
    #the 5 genres want
    selected_genres = ["Action", "Comedy", "Drama", "Horror", "Romance"]
    genre_indices = [1, 5, 8, 10, 14]  #indexes of these in u.genre order

    #high ratings (4-5)
    female_high = demGenreRatingFractions(userList, movieList, rLu, "F", [0, 100], [4, 5])
    male_high = demGenreRatingFractions(userList, movieList, rLu, "M", [0, 100], [4, 5])

    #low ratings (1–2)
    female_low = demGenreRatingFractions(userList, movieList, rLu, "F", [0, 100], [1, 2])
    male_low = demGenreRatingFractions(userList, movieList, rLu, "M", [0, 100], [1, 2])

    #extract only the 5 selected genres
    female_high = [female_high[i] for i in genre_indices]
    male_high = [male_high[i] for i in genre_indices]
    female_low = [female_low[i] for i in genre_indices]
    male_low = [male_low[i] for i in genre_indices]

    x = range(len(selected_genres))
    width = 0.35

    #high ratings: female vs male
    plt.figure(figsize=(8, 5))
    plt.bar([p - width/2 for p in x], female_high, width, label='Female', color='lightcoral')
    plt.bar([p + width/2 for p in x], male_high, width, label='Male', color='skyblue')
    plt.xticks(x, selected_genres)
    plt.ylabel("Fraction of Ratings (4–5)")
    plt.title("High Ratings (4–5): Female vs Male")
    plt.legend()
    plt.show()

    #low ratings: female vs male
    plt.figure(figsize=(8, 5))
    plt.bar([p - width/2 for p in x], female_low, width, label='Female', color='lightcoral')
    plt.bar([p + width/2 for p in x], male_low, width, label='Male', color='skyblue')
    plt.xticks(x, selected_genres)
    plt.ylabel("Fraction of Ratings (1–2)")
    plt.title("Low Ratings (1–2): Female vs Male")
    plt.legend()
    plt.show()

    #high ratings (4–5)
    young_high = demGenreRatingFractions(userList, movieList, rLu, "A", [20, 30], [4, 5])
    old_high = demGenreRatingFractions(userList, movieList, rLu, "A", [50, 60], [4, 5])

    #low ratings (1–2)
    young_low = demGenreRatingFractions(userList, movieList, rLu, "A", [20, 30], [1, 2])
    old_low = demGenreRatingFractions(userList, movieList, rLu, "A", [50, 60], [1, 2])

    #extract only the 5 selected genres
    young_high = [young_high[i] for i in genre_indices]
    old_high = [old_high[i] for i in genre_indices]
    young_low = [young_low[i] for i in genre_indices]
    old_low = [old_low[i] for i in genre_indices]

    #high ratings: younger vs older
    plt.figure(figsize=(8, 5))
    plt.bar([p - width/2 for p in x], young_high, width, label='Younger (20–30)', color='limegreen')
    plt.bar([p + width/2 for p in x], old_high, width, label='Older (50–60)', color='orange')
    plt.xticks(x, selected_genres)
    plt.ylabel("Fraction of Ratings (4–5)")
    plt.title("High Ratings (4–5): Younger vs Older Adults")
    plt.legend()
    plt.show()

    #low ratings: younger vs older
    plt.figure(figsize=(8, 5))
    plt.bar([p - width/2 for p in x], young_low, width, label='Younger (20–30)', color='limegreen')
    plt.bar([p + width/2 for p in x], old_low, width, label='Older (50–60)', color='orange')
    plt.xticks(x, selected_genres)
    plt.ylabel("Fraction of Ratings (1–2)")
    plt.title("Low Ratings (1–2): Younger vs Older Adults")
    plt.legend()
    plt.show()


if __name__ == "__main__":
    plotDemographicComparisons(userList, movieList, rLu)

































