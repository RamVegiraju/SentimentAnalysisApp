import json
from sys import getsizeof
import re
import math
import collections, functools, operator 
from datetime import datetime
import boto3

#Clients to access S3 and Comprehend
client = boto3.client('comprehend')
s3_client = boto3.client('s3', region_name = 'us-east-1')
s3 = boto3.resource('s3', region_name = 'us-east-1')

#Creating S3 buckets and folders for input and output results
bucket1 = "inputbucketcompr"
bucket2 = "outputbucketcompr"

#Creating input and output buckets to store user inputs and comprehend results
s3.create_bucket(Bucket=bucket1)
s3.create_bucket(Bucket=bucket2)

#Timestamps to give keynames for objects we push to S3
now = datetime.now()
current_time = now.strftime("%H:%M:%S")

def comprehendCall(sampStr):
    """Determines which Comprehend call to use"""
    sizeStr = getsizeof(sampStr)
    if sizeStr < 5000:
        return True
    return False

def countSplits(sampStr):
    """Number of times we need to split input string for batch sentiment call"""
    sizeStr = getsizeof(sampStr)
    if sizeStr > 5000:
        numSplits = math.ceil(sizeStr/5000)
        if numSplits > 25:
            raise("This text is too large for analysis try something else")
    return numSplits

def tokenizeText(sampStr):
    """Tokenizing text into sentences to make sure data is split properly"""
    sentList = re.split(r'(?<=[^A-Z].[.?]) +(?=[A-Z])', sampStr)
    numSentences = len(sentList)
    numSplits = countSplits(sampStr)
    
    #Storing size of each sentence to check if over 5000 limit
    sizesStr = []
    for sent in sentList:
        sizesStr.append(getsizeof(sent))
        for size in sizesStr:
            if size > 5000:
                raise("This piece is too large for analysis")
            continue
    #print(sizesStr)
    if numSentences > 25:
        raise("Too many pieces for Comprehend to process, split text even more")
        #Combines two sentences into one list item
        sentList = [sentList[i] + sentList[i+1] if not numSentences %2 else 'odd index' for i in range(0,len(sentList),2)]
    return sentList


def lambda_handler(event, context):
    
    #User input
    res = event['text']
    #print(res)
    
    #Storing user input in S3 input bucket
    s3_client.put_object(Body = res, Bucket = bucket1, Key = current_time + ".txt")
    
    #Inputs less than 5000 bytes can use normal detect sentiment call 
    if comprehendCall(res):
        print("This is less than 5000 bytes, going to use normal detect sentiment call")
        #print(getsizeof(res))
        sentiment = client.detect_sentiment(Text = res, LanguageCode = 'en')
        sentRes = sentiment['Sentiment']
        sentScore = sentiment['SentimentScore']
        
    #otherwise use batch detect sentiment call
    else:
        print("Using the Batch Detect Sentiment Call")
        #print(getsizeof(res))
        inputSentList = tokenizeText(res)
        sentResults = client.batch_detect_sentiment(TextList = inputSentList, LanguageCode = 'en') #returns a dictionary with value as list of dictionaries
        #print(sentResults)
        sentResults = sentResults['ResultList'] #list of dictionaries 
        sentScores = [sentResult['SentimentScore'] for sentResult in sentResults] #Accessing scores for each of four categories
        numSent = len(sentScores) #Number of batches given to batch detect call
        sentScore = dict(functools.reduce(operator.add, map(collections.Counter, sentScores))) # sum the values with same keys
        sentScore = {key: (sentScore[key]/numSent) for key in sentScore.keys()}
        print(sentScore)
    
    #Storing Comprehend output   
    s3_client.put_object(Body = str(sentScore), Bucket = bucket2, Key = current_time + ".txt")
    
    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
        },
        'body': sentScore
    }