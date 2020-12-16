from sys import getsizeof
import math
import re
import collections, functools, operator 

def comprehendCall(sampStr):
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
    sizesStr = []
    for sent in sentList:
        sizesStr.append(getsizeof(sent))
        for size in sizesStr:
            if size > 5000:
                raise("This piece is too large for analysis")
            continue
    print(sizesStr)
    if numSentences > 25:
        raise("Too many pieces for Comprehend to process, split text even more")
        #Combines two sentences into one list item
        sentList = [sentList[i] + sentList[i+1] if not numSentences %2 else 'odd index' for i in range(0,len(sentList),2)]
    return sentList


testList = ["This is a test", "I am just testing this"]

sampStrEx = """Paragraphs are the building blocks of papers. Many students define paragraphs in terms of length: a paragraph is a group of at least five sentences, a paragraph is half a page long, etc. In reality, though, the unity and coherence of ideas among sentences is what constitutes a paragraph. A paragraph is defined as “a group of sentences or a single sentence that forms a unit” (Lunsford and Connors 116). Length and appearance do not determine whether a section in a paper is a paragraph. For instance, in some styles of writing, particularly journalistic styles, a paragraph can be just one sentence long. Ultimately, a paragraph is a sentence or group of sentences that support one main idea. In this handout, we will refer to this as the “controlling idea,” because it controls what happens in the rest of the paragraph.

How do I decide what to put in a paragraph?
Before you can begin to determine what the composition of a particular paragraph will be, you must first decide on an argument and a working thesis statement for your paper. What is the most important idea that you are trying to convey to your reader? The information in each paragraph must be related to that idea. In other words, your paragraphs should remind your reader that there is a recurrent relationship between your thesis and the information in each paragraph. A working thesis functions like a seed from which your paper, and your ideas, will grow. The whole process is an organic one—a natural progression from a seed to a full-blown paper where there are direct, familial relationships between all of the ideas in the paper.

The decision about what to put into your paragraphs begins with the germination of a seed of ideas; this “germination process” is better known as brainstorming. There are many techniques for brainstorming; whichever one you choose, this stage of paragraph development cannot be skipped. Building paragraphs can be like building a skyscraper: there must be a well-planned foundation that supports what you are building. Any cracks, inconsistencies, or other corruptions of the foundation can cause your whole paper to crumble.

So, let’s suppose that you have done some brainstorming to develop your thesis. What else should you keep in mind as you begin to create paragraphs? Every paragraph in a paper should be:

Unified: All of the sentences in a single paragraph should be related to a single controlling idea (often expressed in the topic sentence of the paragraph).
Clearly related to the thesis: The sentences should all refer to the central idea, or thesis, of the paper (Rosen and Behrens 119).
Coherent: The sentences should be arranged in a logical manner and should follow a definite plan for development (Rosen and Behrens 119).
Well-developed: Every idea discussed in the paragraph should be adequately explained and supported through evidence and details that work together to explain the paragraph’s controlling idea (Rosen and Behrens 119)."""


sentList = tokenizeText(sampStrEx)
#print(sentList)

#print(splitText(sampStrEx, numSplits))
#print(comprehendCall(sampStrEx))

sentResults = {'ResultList': [{'Index': 0, 'Sentiment': 'NEUTRAL', 'SentimentScore': {'Positive': 0.011681548319756985, 'Negative': 0.06063302233815193, 'Neutral': 0.9272783398628235, 'Mixed': 0.0004070141294505447}}, {'Index': 1, 'Sentiment': 'NEGATIVE', 'SentimentScore': {'Positive': 0.0029982738196849823, 'Negative': 0.5769728422164917, 'Neutral': 0.41990339756011963, 'Mixed': 0.00012543801858555526}}, {'Index': 2, 'Sentiment': 'NEUTRAL', 'SentimentScore': {'Positive': 0.1131499856710434, 'Negative': 0.14023615419864655, 'Neutral': 0.7386338114738464, 'Mixed': 0.007980105467140675}}, {'Index': 3, 'Sentiment': 'NEUTRAL', 'SentimentScore': {'Positive': 0.0004288615600671619, 'Negative': 0.0011221497552469373, 'Neutral': 0.9984419941902161, 'Mixed': 7.046719474601559e-06}}, {'Index': 4, 'Sentiment': 'NEGATIVE', 'SentimentScore': {'Positive': 0.001489726360887289, 'Negative': 0.775030255317688, 'Neutral': 0.22065746784210205, 'Mixed': 0.0028225507121533155}}, {'Index': 5, 'Sentiment': 'NEUTRAL', 'SentimentScore': {'Positive': 0.04012716934084892, 'Negative': 0.30116117000579834, 'Neutral': 0.6572431921958923, 'Mixed': 0.00146845867857337}}, {'Index': 6, 'Sentiment': 'NEUTRAL', 'SentimentScore': {'Positive': 0.02333061955869198, 'Negative': 0.12271184474229813, 'Neutral': 0.8527335524559021, 'Mixed': 0.0012238927884027362}}, {'Index': 7, 'Sentiment': 'NEUTRAL', 'SentimentScore': {'Positive': 0.03945013880729675, 'Negative': 0.004295798949897289, 'Neutral': 0.955801248550415, 'Mixed': 0.0004527719283942133}}, {'Index': 8, 'Sentiment': 'NEUTRAL', 'SentimentScore': {'Positive': 0.005719235632568598, 'Negative': 0.14484599232673645, 'Neutral': 0.8348576426506042, 'Mixed': 0.014577070251107216}}, {'Index': 9, 'Sentiment': 'NEUTRAL', 'SentimentScore': {'Positive': 0.015935378149151802, 'Negative': 0.014818429946899414, 'Neutral': 0.9672188758850098, 'Mixed': 0.0020273446571081877}}, {'Index': 10, 'Sentiment': 'NEUTRAL', 'SentimentScore': {'Positive': 0.02537616714835167, 'Negative': 0.009846421889960766, 'Neutral': 0.9609721302986145, 'Mixed': 0.0038053260650485754}}, {'Index': 11, 'Sentiment': 'NEUTRAL', 'SentimentScore': {'Positive': 0.024596408009529114, 'Negative': 0.14768283069133759, 'Neutral': 0.8178223967552185, 'Mixed': 0.009898331016302109}}, {'Index': 12, 'Sentiment': 'NEUTRAL', 'SentimentScore': {'Positive': 0.15570788085460663, 'Negative': 0.14202800393104553, 'Neutral': 0.7014215588569641, 'Mixed': 0.0008425438427366316}}, {'Index': 13, 'Sentiment': 'POSITIVE', 'SentimentScore': {'Positive': 0.5495188236236572, 'Negative': 0.010222344659268856, 'Neutral': 0.4374014735221863, 'Mixed': 0.0028573928866535425}}, {'Index': 14, 'Sentiment': 'NEUTRAL', 'SentimentScore': {'Positive': 0.20765651762485504, 'Negative': 0.001014437060803175, 'Neutral': 0.7911648154258728, 'Mixed': 0.00016426382353529334}}, {'Index': 15, 'Sentiment': 'NEUTRAL', 'SentimentScore': {'Positive': 0.16856582462787628, 'Negative': 0.05743616819381714, 'Neutral': 0.7736886739730835, 'Mixed': 0.0003093627165071666}}, {'Index': 16, 'Sentiment': 'POSITIVE', 'SentimentScore': {'Positive': 0.814439058303833, 'Negative': 0.03027229569852352, 'Neutral': 0.15306109189987183, 'Mixed': 0.002227654680609703}}, {'Index': 17, 'Sentiment': 'NEUTRAL', 'SentimentScore': {'Positive': 0.1446247398853302, 'Negative': 0.1353081911802292, 'Neutral': 0.6976632475852966, 'Mixed': 0.0224039014428854}}, {'Index': 18, 'Sentiment': 'NEGATIVE', 'SentimentScore': {'Positive': 0.1716945618391037, 'Negative': 0.6434348225593567, 'Neutral': 0.15719453990459442, 'Mixed': 0.027675990015268326}}, {'Index': 19, 'Sentiment': 'NEUTRAL', 'SentimentScore': {'Positive': 0.016616340726614, 'Negative': 0.04292582720518112, 'Neutral': 0.9371781945228577, 'Mixed': 0.0032796612940728664}}, {'Index': 20, 'Sentiment': 'NEUTRAL', 'SentimentScore': {'Positive': 0.008413147181272507, 'Negative': 0.13769400119781494, 'Neutral': 0.792053759098053, 'Mixed': 0.06183909997344017}}, {'Index': 21, 'Sentiment': 'NEUTRAL', 'SentimentScore': {'Positive': 0.01074897963553667, 'Negative': 0.25769057869911194, 'Neutral': 0.731290340423584, 'Mixed': 0.0002700533077586442}}, {'Index': 22, 'Sentiment': 'NEUTRAL', 'SentimentScore': {'Positive': 0.04209870845079422, 'Negative': 0.11173070222139359, 'Neutral': 0.8442538976669312, 'Mixed': 0.001916671870276332}}, {'Index': 23, 'Sentiment': 'NEUTRAL', 'SentimentScore': {'Positive': 0.21718205511569977, 'Negative': 0.004649543669074774, 'Neutral': 0.7497596144676208, 'Mixed': 0.028408829122781754}}, {'Index': 24, 'Sentiment': 'POSITIVE', 'SentimentScore': {'Positive': 0.8677494525909424, 'Negative': 0.0026179247070103884, 'Neutral': 0.12912599742412567, 'Mixed': 0.0005065735895186663}}], 'ErrorList': [], 'ResponseMetadata': {'RequestId': '74383430-b9af-48c8-9bb8-7c83c26a9488', 'HTTPStatusCode': 200, 'HTTPHeaders': {'x-amzn-requestid': '74383430-b9af-48c8-9bb8-7c83c26a9488', 'content-type': 'application/x-amz-json-1.1', 'content-length': '4388', 'date': 'Wed, 16 Dec 2020 04:09:15 GMT'}, 'RetryAttempts': 0}}
sentResults = sentResults['ResultList'] #list of dictionaries 
sentScores = [sentResult['SentimentScore'] for sentResult in sentResults] #Accessing scores for each of four categories
numSent = len(sentScores) #Number of batches given to batch detect call
sentScores = dict(functools.reduce(operator.add, map(collections.Counter, sentScores))) # sum the values with same keys
#print(sentScores)
sentScores = {key: (sentScores[key]/numSent) for key in sentScores.keys()}
print(sentScores)