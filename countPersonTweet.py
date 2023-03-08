import json
from collections import Counter
import heapq


def countPersonTweet(tweet_data, author_ids):
 
    author_ids += [item['data']['author_id'] for item in tweet_data]
    # return author_ids
    
    count_dict = Counter(author_ids)
    
    top_10 = heapq.nlargest(10, count_dict.items(), key=lambda x: x[1])
    
    