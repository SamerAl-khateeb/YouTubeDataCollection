# generateGephiFiles.py
# By: Samer Al-khateeb

# this script will read the videoTitleByTagsNetwork.csv file 
# generated by processing_popular_vid_in_location.py
# and produce two output files called "edges.csv" and "nodes.csv" 
# these files can be imported directly to Gephi


import os
import csv


def read_CSV_file():
    # the output file name generated 
    # by popular_vid_in_location.py 
    filename = "videoTitleByTagsNetwork.csv"

    #open the file 
    #inputFile = open(filename, "r")
    # if you get an unicodeError try the line below instead
    inputFile = open(filename, "r", encoding='utf-8')

    #read the content of the file
    inputFileContents = csv.reader(inputFile)

    # skipping the first row in the csv input file
    next(inputFileContents)

    return inputFileContents


def write_nodes_to_CSV(biglist):
    # creating a file to save the output
    with open('nodes.csv', 'w', newline='', encoding='utf-8') as csv_output_file:
        #creating a csv writer object 
        csvwriter = csv.writer(csv_output_file, delimiter=',', lineterminator='\n')
        #write the columns headers
        csvwriter.writerow(["Id", "Name", "channelId", 
                            "channelTitle", "channelDescription", "videoCategoryId",
                             "videoDescription", "videoPublishedAt", "videoCommentCount",
                             "videoFavoriteCount", "videoLikeCount", "videoViewCount",
                             "videoPopularAt"])
        #writing/inserting the list to the output file 
        csvwriter.writerows(biglist)
    # close the output file
    csv_output_file.close()


def write_edges_to_CSV(biglist):
    # creating a file to save the output
    with open('edges.csv', 'w', newline='', encoding='utf-8') as csv_output_file:
        #creating a csv writer object 
        csvwriter = csv.writer(csv_output_file, delimiter=',', lineterminator='\n')
        #write the columns headers
        csvwriter.writerow(["Source", "Target"])
        #writing/inserting the list to the output file 
        csvwriter.writerows(biglist)
    # close the output file
    csv_output_file.close()


def main():
    # define the nodes output list
    nodesOutputList = []

    # define the edges output list
    edgesOutputList = []

    # read the CSV input file
    fileAsList = read_CSV_file()
    # varibale used to assign a unique ID 
    # to each node name (could be a video title or a tag)
    Id = 0

    # list to accumlate the unique nodes names 
    nodesList = []
    
    # counter to count how many rows are processed so far
    count = 0
    
    # go through the file to extract all 
    # the unique nodes and the info related to it
    for row in fileAsList:
        
        count = count + 1
        print("processing row number ", count)

        channelId = row[0]
        channelTitle = row[1]
        channelDescription = row[2]
        videoCategoryId = row[3]
        videoTitle = row[4]
        videoDescription = row[5]
        videoPublishedAt = row[6]
        videoCommentCount = row[7]
        videoFavoriteCount = row[8]
        videoLikeCount = row[9]
        videoViewCount = row[10]
        videoPopularAt = row[11]
        tagExtracted = row[12]

        # if the video title not in the list add it as a node
        if videoTitle not in nodesList:
            nodesList.append(videoTitle)
            Id = Id + 1
            newNodeRow = [Id, videoTitle, channelId, 
                            channelTitle, channelDescription, videoCategoryId,
                             videoDescription, videoPublishedAt, videoCommentCount,
                             videoFavoriteCount, videoLikeCount, videoViewCount,
                             videoPopularAt]
            nodesOutputList.append(newNodeRow)
        # if the extracted tag not in the list add it as a node
        if tagExtracted not in nodesList:
            nodesList.append(tagExtracted)
            Id = Id + 1
            newNodeRow = [Id, tagExtracted, channelId, 
                            channelTitle, channelDescription, videoCategoryId,
                             videoDescription, videoPublishedAt, videoCommentCount,
                             videoFavoriteCount, videoLikeCount, videoViewCount,
                             videoPopularAt]                           
            nodesOutputList.append(newNodeRow)
    # call the function to create nodes.csv file 
    write_nodes_to_CSV(nodesOutputList)

    # read the CSV input file
    fileAsList = read_CSV_file()
    # go through the file again to map each source and target to the nodes IDs
    for row in fileAsList:
        videoTitle = row[4]
        tagExtracted = row[12]
        source = nodesList.index(videoTitle) + 1
        target = nodesList.index(tagExtracted) + 1
        newEdgeRow = [source, target]
        edgesOutputList.append(newEdgeRow)
    # call the function to create edges.csv file 
    write_edges_to_CSV(edgesOutputList)

if __name__ == "__main__":
    main()
