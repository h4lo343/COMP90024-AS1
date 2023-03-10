from collections import Counter
import heapq
from countCity import check_city
from countPersonInCity import sort_dict_by_city


def printResult(gcc_dict, person_data_dic, author_ids, time, start_time): 
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