# -*- coding: utf-8 -*-
"""
"""
#Import packages
import os
import pandas as pd
import numpy as np
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import time

# Spotify Credentials
client_id = 'YOUR CLIENT ID HERE'
client_secret = 'YOUR CLIENT SECRET HERE'
redirect_uri = 'http://localhost:8080'
scope = 'user-library-read'

# Initialize Spotipy with OAuth Authentication
auth_manager = SpotifyOAuth(client_id=client_id,
                            client_secret=client_secret,
                            redirect_uri=redirect_uri,
                            scope=scope)
spotify = spotipy.Spotify(auth_manager=auth_manager)


#Function to delay API calls if the rate limit is hit (an issue I had when repeatedly making batch calls).
def rate_limited_call(call):
    
    #Try the api call.
    try:
        return call()
    
    #If 429 error is returned, wait the amount in the Retry-After header before trying again.
    except spotipy.exceptions.SpotifyException as e:
        if e.http_status == 429:
            retry_after = int(e.headers["Retry-After"])
            time.sleep(retry_after)
            return rate_limited_call(call)
        raise

#Function to get tracks' duration,key,liveness and mode from audio features endpoint.
def get_audio_features(uris):
    
    #Use anonymous function to call rate_limited_call with audio_features_endpoint for multiples songs.
    audio_features_list = rate_limited_call(lambda: spotify.audio_features(uris))
    #Returns a list of dictionaries for each track.
    
    #Initialise empty audio features dictionary.
    audio_features_dict = {}
    
    #Place values from API into audio features dict
    for features in audio_features_list:
        audio_features_dict[features['id']] = {
            "duration_ms": features['duration_ms'],
            "key": features['key'],
            "liveness": features['liveness'],
            "mode": features['mode']
            }
        
    return audio_features_dict

#Function to get tracks' duration,key,liveness and mode from tracks endpoint.
def get_nonaudio_features(uris):
    
    #Make rate limited call on tracks endpoint for multiple songs. 
    tracks_list = rate_limited_call(lambda: spotify.tracks(uris))
    
    #Initialise empty track details dict.
    track_details_dict = {}
    
    for track in tracks_list['tracks']:
        #Save explicit tag and artist uri to track details dict.
        track_details_dict[track['id']] = {
            "explicit": track['explicit'],
        } 
    return track_details_dict

# Function to process a batches of URIs at once, to avoid rate limit issues with doing them one by one
# and issues with doing all of them at once.
def process_batch(uris):
    
    #Empty list to store data from batches.
    batch_data = []
    
    #Get audio and track features for list of uris.
    audio_features = get_audio_features(uris)
    track_details = get_nonaudio_features(uris)
    
    #Unpack data for each uri into barch_data list and return.
    for uri in uris:
        batch_data.append({
            "id": uri,
            **audio_features[uri], #unpack audio features
            **track_details[uri] #unpack track details
        })
    return batch_data


#Import dataset
Spotify_API_data = pd.read_csv("Spotify_Dataset_V3.csv", delimiter = ";")

# Some songs with identical titles appear in the dataset with different ids, so I will make all 
# songs with the same title use the same URI.
# Find the first id to appear for every song title.
title_to_uri = Spotify_API_data.groupby('Title')['id'].first()
# Update all entries in the original DataFrame to use the common URI
Spotify_API_data['id'] = Spotify_API_data['Title'].map(title_to_uri)

#Find unique URIs in the dataset
unique_URIs = Spotify_API_data['id'].unique()


# Initialize list to hold output data
output_data = []

# Process URIs in batches of 50
batch_size = 50
for i in range(0, len(unique_URIs), batch_size):
    batch_uris = unique_URIs[i: i + batch_size] #Get the 50 uris from unique_URIs
    batch_data = process_batch(batch_uris) #Get the data from process_batch
    output_data.extend(batch_data) #Append data from batch into output_data list
    
# Create Output DataFrame
Spotify_API_Features = pd.DataFrame(output_data)

# Write to csv.
Spotify_API_Features.to_csv("Spotify_API_Features.csv", index=False)