import pandas as pd

import json
actor_name_map = {}
movie_actor_map = {}
actor_genre_map = {}


with open("../data/imdb_movies_2000to2022.prolific.json", "r") as in_file:
    for line in in_file:
        
        # Read the movie on this line and parse its json
        this_movie = json.loads(line)
                    
        # Add all actors to the id->name map
        for actor_id,actor_name in this_movie['actors']:
            actor_name_map[actor_id] = actor_name
            
        # For each actor, add this movie's genres to that actor's list
        for actor_id,actor_name in this_movie['actors']:
            this_actors_genres = actor_genre_map.get(actor_id, {})
            
            # Increment the count of genres for this actor
            for g in this_movie["genres"]:
                this_actors_genres[g] = this_actors_genres.get(g, 0) + 1
                
            # Update the map
            actor_genre_map[actor_id] = this_actors_genres
            
        # Finished with this film
        movie_actor_map[this_movie["imdb_id"]] = ({
            "movie": this_movie["title"],
            "actors": set([item[0] for item in this_movie['actors']]),
            "genres": this_movie["genres"]
        })
        
        # Get all actors as an index for a dataframe
index = actor_genre_map.keys()

# Get the genre-counts for each actor in the index
rows = [actor_genre_map[k] for k in index]

# Create the data frame from these rows, with the actors as index
df = pd.DataFrame(rows, index=index)

# Fill NAs with zero, as NA means the actor has not starred in that genre
df = df.fillna(0)

df

target_actor_id = "nm1165110"
from scipy.sparse import lil_matrix # Needed for building the matrix of user ratings
import scipy.spatial.distance # Needed for calculating pairwise distances
#Setting the actor we will be comparing to
target_actor_id = 'nm1165110'
#Gathering the genres for that actor
target_actor_ratings = df.loc[target_actor_id]

#Generating distances from that actor to all the others
distances = scipy.spatial.distance.cdist(df, [target_actor_ratings], metric="cosine")[:,0]

query_distances = list(zip(df.index, distances))

#Printing the top ten most similar actors to our target
for similar_actor_id, similar_genre_score in sorted(query_distances, key=lambda x: x[1], reverse=False)[:10]:
    similar_actor = actor_genre_map[similar_actor_id]
    print(similar_actor_id, actor_name_map[similar_actor_id], similar_genre_score)
    
target_actor_id = "nm1165110"
from sklearn.metrics import DistanceMetric
from sklearn.metrics.pairwise import cosine_distances
dist = DistanceMetric.get_metric("euclidean")
#dist = cosine_distances
#Gathering the genres for that actor
target_actor_ratings = df.loc[target_actor_id]

#Generating distances from that actor to all the others
distances = dist.pairwise(df, [target_actor_ratings])[:,0]
#distances = dist(df, [target_actor_ratings])[:,0]

query_distances = list(zip(df.index, distances))

#Printing the top ten most similar actors to our target
for similar_actor_id, similar_genre_score in sorted(query_distances, key=lambda x: x[1], reverse=False)[:10]:
    similar_actor = actor_genre_map[similar_actor_id]
    print(similar_actor_id, actor_name_map[similar_actor_id], similar_genre_score)

