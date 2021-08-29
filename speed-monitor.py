#%%

#!/usr/bin/env python
# coding: utf-8

import requests                 # Enable API request functionality
import subprocess               # Enable calling another process
import datetime                 # Enable date and time functionality
import os                       # Enable filesystem functionality
from pathlib import Path        # Enable filesystem path joining
import json                     # Enable JSON support
from pythonping import ping     # Enable pingtest
import speedtest                # Enable Speedtest
import time                     # Enable sleep

st = speedtest.Speedtest() # Define speedtest
servers = [] # Set specific servers for speedtest (none = use best)
threads = None # Threads for speedtest

# configDict = dict()
# configList = [line.strip().split(' = ') for line in open('config.txt')]  # pull run parameters from config.txt
testsPerRound = 3 # Number of tests before uploading to Gist (default 3)
numRounds = 2240 # Number of times to upload to Gist (2240 = 7 days of testing @ 90sec/test @ 3 tests/round)
testWaitSec = 90 # Wait time between tests (default 90 sec)

creds = [line.strip() for line in open('creds.txt')]  # pull API credentials from creds.txt
keY = creds[0]  # API key from creds.txt
headers1 = {'Accept' : 'application/vnd.github.v3+json'} # Headers for API request
auth1 = ('pete5x5', keY) # Login info

global allContent, gistID # global vars
allContent = [] # Make empty list for content
gistID = "" # set gistID to blank for first loop
gistADD = "" # set gistADD to blank for first loop

global gendate, fileName # global vars
gendate = (datetime.datetime.now()).strftime('%Y%m%d-%H%M%S') # date & time
fileName = 'speed-log-' + gendate + '.txt' # name of file to create
mainPath = Path.cwd() # Current directory
postPath = os.path.join(mainPath,'post') # Post folder for the text files

if Path(postPath).exists() is False or Path(postPath).is_dir() is False: # if the post folder doesn't exist or it's a file...
    Path(postPath).mkdir() # make it
    
filePath = os.path.join(postPath,fileName) # path with file name
postFile = open(filePath, 'w') # make the file

global gistName, gistPath # global vars
gistName = 'gist-' + gendate + '.txt'
gistPath = os.path.join(postPath,gistName) # path with gist name

#%%

def runTime(): # time entry for content
    global gendate2 # global vars
    gendate2 = (datetime.datetime.now()).strftime('%Y/%m/%d-%H:%M:%S')

def speedTest(): # speedtest entry for content
    global dn, up # global vars
    st.get_servers(servers) # get server list to use 
    st.get_best_server() # find best server
    dn = round(((st.download(threads=threads))/1000000),1) # download test, round to 1 decimal in Mbps
    up = round(((st.upload(threads=threads))/1000000),1) # upload test, round to 1 decimal in Mbps

def pingTest(): # ping entry for content
    global pingMS # global vars
    pingList = ping('google.ca', size=40, count=10) # ping Google 10 times
    print(pingList) #@
    pingMS = pingList.rtt_avg_ms # take the average ping in ms

def makeContent(): # put content together
    global pingMS, dn, up, allContent # global vars
    logEntry = [] # clear the log entry
    runTime() # generate current run time
    logEntry += ["Test run at: " + str(gendate2)] # add run time to list
    logEntry += ["Ping: " + str(pingMS) + "ms"] # add ping to list
    logEntry += ["Download speed: " + str(dn) + "Mbps"] # add download speed to list
    logEntry += ["Upload speed: " + str(up) + "Mbps"] # add upload speed to list
    logEntry += ["-----------------------------------"] # divider run time to list to make it easier to read
    for L1 in range(len(logEntry)): # for each line in the log entry
        print(logEntry[L1]) # print the line
    allContent += [logEntry] # add newly generated list to master list to be uploaded

def writeContent(): # write content to file
    global allContent # global vars
    postFile = open(filePath, 'w') # open file to write
    
    numCon = (len(allContent)) # number of tests done and logged
    for x1 in range(numCon): # for each test
        for x2 in range(len(allContent[numCon - 1 - x1])): # for each individual entry in a test
            writeMe = allContent[numCon - 1 - x1][(x2)] # get a list entry
            postFile.write(str(writeMe) + '\n') # write the content and a new line to the file
    postFile.close() # close the file

def readContent(): # read the file
    global filePath, readFile # global vars
    postFile = open(filePath, 'r') # open the file in read mode
    readFile = postFile.read() # read file contents

def makeGist(): # upload file contents to Gist
    global r1, payLoad, gistID, gistURL, gistADD # global vars
    payLoad={"description":"Network log " + gendate,"files":{"log-" + gendate:{"content":readFile}}} # payload to upload
    r1 = requests.post('https://api.github.com/gists'+gistADD, auth = auth1, headers=headers1, data = json.dumps(payLoad)) # API request
    resp = dict(r1.json()) # response from API
    print('')
    # print(resp) # print response

def gistInfo(): # get Gist info from API
    global gistURL, gistID, gistADD # global vars
    gistURL = r1.json()['html_url'] # URL of the created Gist
    gistID = r1.json()['id'] # ID of the created Gist
    gistADD = "/"+gistID # ID formatted to append to the API URL for updating the entry
    print(gistURL)
    # print(gistID)
    # print(gistADD)

def writeGist(): # get Gist info from API
    global gistURL # global vars
    postGist = open(gistPath, 'w') # open file to write
    postGist.write(str(gistURL) + '\n')
    postGist.close() # close the file


#%%
#---------------------------------#

# # First run to get a quick test and Gist URL:
# speedTest()
# pingTest()
# makeContent()
# writeContent()
# readContent()
# makeGist()
# gistInfo()
# writeGist()

# # Loop to run for desired time:
# for n1 in range(numRounds):
#     for n2 in range(testsPerRound):
#         speedTest()
#         pingTest()
#         makeContent()
#         writeContent()
#         time.sleep(testWaitSec)
#     readContent()
#     makeGist()
#     gistInfo()