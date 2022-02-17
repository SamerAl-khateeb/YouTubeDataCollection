# This script return a csv file with trending videos information in a specific Location
# It is a modified version of the sample code posted by YouTube Data API 
# which can be found here https://developers.google.com/youtube/v3/docs/videos/list?apix=true
# Sample Python code for youtube.videos.list

# To be able to run the code using IDLE you have to do the following:
# For Mac users, open terminal and type:
#   python3 -m pip install --upgrade pip==19.0.3
#   python3 -m pip install google-auth-oauthlib
#   python3 -m pip install --upgrade google-api-python-client

# For Windows users, open CMD and type:
#   py -m pip install --upgrade pip==19.0.3
#   py -m pip install google-auth-oauthlib
#   py -m pip install --upgrade google-api-python-client

import os
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import json
import csv
import time

scopes = ["https://www.googleapis.com/auth/youtube.readonly"]

def make_request(location, accessToken):
    api_service_name = "youtube"
    api_version = "v3"
    API_KEY = "PasteYourAPIKeyHere!"

    youtube = googleapiclient.discovery.build(api_service_name, api_version, developerKey=API_KEY)

    request = youtube.videos().list(
        part="snippet,contentDetails,statistics",
        chart="mostPopular",
        maxResults=10,
        regionCode=location,
        pageToken=accessToken
    )
    
    json_response = request.execute()
    return json_response


def write_output_to_CSV(biglist):
    # creating a file to save the output
    with open('output.csv', 'w', newline='', encoding='utf-8') as csv_output_file:
        #creating a csv writer object 
        csvwriter = csv.writer(csv_output_file, delimiter=',', lineterminator='\n')
        #write the columns headers
        csvwriter.writerow(["channelId", "channelTitle", "channelDescription", 
                                "videoCategoryId", "videoTitle", "videoDescription", 
                                "videoPublishedAt", "videoTags", "videoCommentCount",
                                "videoFavoriteCount", "videoLikeCount", "videoViewCount", "videoPopularAt"])
        #writing/inserting the list to the output file 
        csvwriter.writerows(biglist)
    # close the output file
    csv_output_file.close()

        
def main():
    # creating a list to hold the output
    CSV_output_list =[]

    # counter to keep count of how many requests made
    # so far so we do not exceed the 10,000 requests per day limit
    numberOfRequestes = 0

    # list of country codes can be used here, 
    # you can find these at https://countrycode.org
    list_of_locations =["US", "CA"]
    
    # collect data for each locaiton in the list
    for location in list_of_locations:
        # for the first request keep the page token to nothing
        accessToken =""

        # make a request and get a response
        json_response = make_request(location,accessToken)
        print(json.dumps(json_response, indent=4, sort_keys=True))
        
        numberOfRequestes = numberOfRequestes + 1

        # keep extracting the values from the response of the current page of result
        # if there is not more results exit and start the same process for the next location 
        while (True):
            # extract the values from the response of the current page of result
            for record in range(len(json_response['items'])):
                videoCategoryId = json_response['items'][record]['snippet']['categoryId']
                
                channelId = json_response['items'][record]['snippet']['channelId']
                channelTitle = json_response['items'][record]['snippet']['channelTitle']
                channelDescription = json_response['items'][record]['snippet']['description']

                videoDescription = json_response['items'][record]['snippet']['localized']['description']
                videoTitle = json_response['items'][record]['snippet']['localized']['title']

                videoPublishedAt = json_response['items'][record]['snippet']['publishedAt']
                
                # not all videos are taggged
                try: 
                    videoTags = json_response['items'][record]['snippet']['tags']
                except KeyError as e:
                    videoTags ="none"

                # not all videos has comments count available
                try:
                    videoCommentCount = json_response['items'][record]["statistics"]['commentCount']
                except KeyError as e:
                    videoCommentCount = 0

                try:
                    videoFavoriteCount = json_response['items'][record]["statistics"]['favoriteCount']
                except KeyError as e:
                    videoFavoriteCount = 0

                try:
                    videoLikeCount = json_response['items'][record]["statistics"]['likeCount']
                except KeyError as e:
                    videoLikeCount = 0

                try:
                    videoViewCount = json_response['items'][record]["statistics"]['viewCount']
                except KeyError as e:
                    videoViewCount = 0

                videoPopularAt = location

                
                # create one CSV row
                CSV_output_row = [channelId, channelTitle, channelDescription, 
                                    videoCategoryId, videoTitle, videoDescription, 
                                    videoPublishedAt, videoTags, videoCommentCount,
                                     videoFavoriteCount, videoLikeCount, videoViewCount, videoPopularAt]
                
                # append the row to the CSV list
                CSV_output_list.append(CSV_output_row)

        
            if ('nextPageToken' in json_response):
                accessToken = json_response['nextPageToken']
                print(accessToken)
                json_response = make_request(location, accessToken)
                print(json.dumps(json_response, indent=4, sort_keys=True))
                numberOfRequestes = numberOfRequestes + 1
            else:
                break
            # sleep for 1 day (86,400 seconds) once you reach  
            # the 10,000 requests per 1 day limit. 
            if (numberOfRequestes == 10000):
                time.sleep(86400)
                #Then reset the number of requests
                numberOfRequestes = 0
        
        # send the list to the function to create a CSV file
        write_output_to_CSV(CSV_output_list)

if __name__ == "__main__":
    main()
