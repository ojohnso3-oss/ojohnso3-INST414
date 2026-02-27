#%matplotlib inline

import json
import random

import numpy as np
import pandas as pd
import networkx as nx

g = nx.Graph() # Build the graph

with open("imdb_movies_2000to2022.prolific.json", "r") as in_file:
    for line in in_file:
        
        # Load the movie from this line
        this_movie = json.loads(line)
            
        # Create a node for every actor
        for actor_id,actor_name in this_movie['actors']:
            # add the actor to the graph
             g.add_node(actor_id, name = actor_name)
            
        # Iterate through the list of actors, generating all pairs
        #. Starting with the first actor in the list, generate pairs with all subsequent actors
        #. then continue to second actor in the list and repeat
        i = 0 # Counter in the list
        for left_actor_id,left_actor_name in this_movie['actors']:
            for right_actor_id,right_actor_name in this_movie['actors'][i+1:]:

                # Get the current weight, if it exists
               #curr_weight = g[left_actor_id][right_actor_id]['weight'] if g.has_edge[left_actor_id, right_actor_id] else 0
                
                # Add an edge for these actors
                g.add_edge(left_actor_id, right_actor_id)
                
                # Print edges
                print(left_actor_name, "<->", right_actor_name)
                
            i += 1 # increment the counter
            
        # TODO: Remove the break below to run all code
    
    
# If you want to explore this graph in Gephi or some other
#. graph analysis tool, NetworkX makes it easy to export data.
#. Here, we use the GraphML format, which Gephi can read 
#. natively, to keep node attributes like Actor Name
nx.write_graphml(g, "actors.graphml")

top_k = 10 # how many of the most central nodes to print

# Calculate degree centrality for all nodes (FIRST)
centrality_degree = nx.degree_centrality(g)
# sort node-centrality dictionary by metric, and reverse to get top elements first
for u in sorted(centrality_degree, key=centrality_degree.get, reverse=True)[:top_k]:
    print(u, g.nodes[u]['name'], centrality_degree[u])
    
centrality_degree = nx.katz_centrality(g, alpha = 0.01)
# sort node-centrality dictionary by metric, and reverse to get top elements first
for u in sorted(centrality_degree, key=centrality_degree.get, reverse=True)[:top_k]:
    print(u, g.nodes[u]['name'], centrality_degree[u])
    

centrality_degree = nx.eigenvector_centrality(g)
# sort node-centrality dictionary by metric, and reverse to get top elements first
for u in sorted(centrality_degree, key=centrality_degree.get, reverse=True)[:top_k]:
    print(u, g.nodes[u]['name'], centrality_degree[u])