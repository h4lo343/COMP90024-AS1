import json
import sys
import threading
from countCity import countCity, check_city
from countPersonInCity import countPersonInCity, sort_dict_by_city
from countPersonTweet import countPersonTweet
import time
from collections import Counter
import heapq
from mpi4py import MPI

with open('./json/twitter-data-small.json', 'r', encoding='utf-8') as f:
    tweet_data_total = json.load(f)

with open('./json/sal.json', 'r', encoding='utf-8') as f:
    sal_data = json.load(f)


node = sys.argv[1]
core = sys.argv[2]

gcc_dict = {}
person_data_dic = {}
author_ids = []

def solve_data(gcc_dict, person_data_dic,chunk, sal_data, author_ids):
  countCity(gcc_dict, chunk, sal_data)
  countPersonInCity(person_data_dic, chunk, sal_data)
  countPersonTweet(chunk, author_ids)

start_time = time.time()  

if node == "1" and core == "1":
    solve_data(gcc_dict, person_data_dic,tweet_data_total, sal_data, author_ids)


if node == "1" and core == "8":
  total_records = len(tweet_data_total)
  records_per_thread = total_records // 8

  threads = []
  for i in range(8):
    start_index = i * records_per_thread
    length = records_per_thread if i < 7 else total_records - start_index

    t = threading.Thread(target=solve_data, args=(gcc_dict, person_data_dic,tweet_data_total[start_index:start_index + length], sal_data, author_ids))
    threads.append(t)
    t.start()

  for t in threads:
    t.join()

print(f"{'Greater Capital City':<40}{'Number of Tweets Made'}")
sorted_gcc_dict = sorted(gcc_dict.items(), key=lambda x: x[1], reverse=True)
for gcc, count in sorted_gcc_dict:
    city = check_city(gcc)
    city_output = f"{gcc}({city})"
    print(f"{city_output:<40}{count:<75}")

print('-----------------------------------------------------------------------------------')

sorted_data = sort_dict_by_city(person_data_dic) 
print(f"{'Rank':<5}{'Author Id':<20}{'Number of Unique City Locations and #Tweets':<40}")
for i, (author_id, value) in enumerate(sorted_data):
    city_info = ' '.join([f'({value["city"][k]}{k})' for k in value['city']])
    print(f'#{i+1:<5}{author_id:<20}{len(value["city"]):<2}#{value["tweets_num"]} tweets - {city_info}')

print('-----------------------------------------------------------------------------------')

count_dict = Counter(author_ids)
    
top_10 = heapq.nlargest(10, count_dict.items(), key=lambda x: x[1])

count_dict = Counter(author_ids)
top_10 = heapq.nlargest(10, count_dict.items(), key=lambda x: x[1])

print("Rank\tAuthor Id\t\tNumber of Tweets Made")
for i, (id, count) in enumerate(top_10):
  print(f"#{i+1}\t{id: <20}\t{count}")

print('-----------------------------------------------------------------------------------')

print("elapsed time:", time.time() - start_time )

