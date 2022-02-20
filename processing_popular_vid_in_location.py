# processing_popular_vid_in_location.py 
# By: Samer Al-khateeb

# this script will read the output.csv file 
# generated by popular_vid_in_location.py
# and produce an output file called "videoTitleByTagsNetwork.csv" 
# of videoTitle X Tags network file which can be analyzed and 
# visualized using Gephi

# Before running this script you need to remove 
# the header/first row of the output.csv file 

import os
import csv

def read_CSV_file():
    # the output file name generated 
    # by popular_vid_in_location.py 
    filename = "output.csv"

    #open the file 
    inputFile = open(filename, "r")

    #read the content of the file
    inputFileContents = csv.reader(inputFile)

    return inputFileContents


def write_output_to_CSV(biglist):
    # creating a file to save the output
    with open('videoTitleByTagsNetwork.csv', 'w', newline='', encoding='utf-8') as csv_output_file:
        #creating a csv writer object 
        csvwriter = csv.writer(csv_output_file, delimiter=',', lineterminator='\n')
        #write the columns headers
        csvwriter.writerow(["channelId", "channelTitle", "channelDescription", 
                                "videoCategoryId", "videoTitle", "videoDescription", 
                                "videoPublishedAt", "videoCommentCount",
                                "videoFavoriteCount", "videoLikeCount", "videoViewCount", "videoPopularAt", "tagExtracted"])
        #writing/inserting the list to the output file 
        csvwriter.writerows(biglist)
    # close the output file
    csv_output_file.close()

def main():
    #define an output list
    CSVOutputList = []

    # read the CSV input file
    fileAsList = read_CSV_file()
    
    # for each row in the file extract all the info
    for row in fileAsList:
        channelId = row[0]
        channelTitle = row[1]
        channelDescription = row[2]
        videoCategoryId = row[3]
        videoTitle = row[4]
        videoDescription = row[5]
        videoPublishedAt = row[6]

        videoCommentCount = row[8]
        videoFavoriteCount = row[9]
        videoLikeCount = row[10]
        videoViewCount = row[11]
        videoPopularAt = row[12]

        # removing the quotes, opeing, and closing square brakets from the string
        videoTags = row[7].replace("'", "").lstrip('[').rstrip(']')
        #converting the string into a list
        videoTags = videoTags.split(',')

        # for each hashtag in the videoTags 
        # create a new row with all the info 
        # plus the hashtag extracted 
        for i in range(len(videoTags)):
            tagExtracted = videoTags[i].lstrip("'").rstrip("'")
            print(tagExtracted)
            newRow = [channelId, channelTitle, channelDescription, 
                        videoCategoryId, videoTitle, videoDescription, 
                        videoPublishedAt, videoCommentCount, videoFavoriteCount,
                        videoLikeCount, videoViewCount, videoPopularAt, tagExtracted]
            CSVOutputList.append(newRow)

    # send the list to a function to create a CSV file
    write_output_to_CSV(CSVOutputList)

if __name__ == "__main__":
    main()