import json
import sys
import threading
from countCity import countCity
from countPersonInCity import countPersonInCity
from countPersonTweet import countPersonTweet
import time
from collections import Counter
from mpi4py import MPI
from print import printResult

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
    printResult(gcc_dict, person_data_dic, author_ids, time, start_time)


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

  printResult(gcc_dict, person_data_dic, author_ids, time, start_time)

if node == "2" and core == "8": 
  comm = MPI.COMM_WORLD
  rank = comm.Get_rank()
  size = comm.Get_size()
  
  if size != 2:
    print("Error: program must run on 2 processes")
    sys.exit(1)

  if rank == 0:
    # process 0 reads first half of the data
    tweet_data_chunk = tweet_data_total[:len(tweet_data_total)//2]
    solve_data(gcc_dict, person_data_dic, tweet_data_chunk, sal_data, author_ids)
    comm.send((gcc_dict, person_data_dic, author_ids), dest=1)

  elif rank == 1:
    # process 1 reads second half of the data
    tweet_data_chunk = tweet_data_total[len(tweet_data_total)//2:]
    solve_data(gcc_dict, person_data_dic, tweet_data_chunk, sal_data, author_ids)
    data = comm.recv(source=0)
    # combine results from both processes
    for key in data[0]:
      if key in gcc_dict:
        gcc_dict[key] += data[0][key]
      else:
        gcc_dict[key] = data[0][key]

    for key in data[1]:
      if key in person_data_dic:
        person_data_dic[key]['tweets_num'] += data[1][key]['tweets_num']
        for k in data[1][key]['city']:
          if k in person_data_dic[key]['city']:
            person_data_dic[key]['city'][k] += data[1][key]['city'][k]
          else:
            person_data_dic[key]['city'][k] = data[1][key]['city'][k]
      else:
        person_data_dic[key] = data[1][key]

    author_ids += data[2]
    
    printResult(gcc_dict, person_data_dic, author_ids, time, start_time)



    








