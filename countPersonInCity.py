import json

def sort_dict_by_city(dic):
      sorted_dict = sorted(dic.items(), key=lambda x: (len(x[1]['city']), x[1]['tweets_num']), reverse=True)[:10]
      return sorted_dict

def countPersonInCity(person_data_dic, tweet_data, sal_data):

  def find_gcc(location):
    city_name = location.split(',')[0].strip()
    for key, value in sal_data.items():
      if value['gcc'][1] == 'g':
        if key.lower() == city_name.lower():
          return value['gcc'][1:]

  for tweet in tweet_data:
    author_id = tweet["data"]["author_id"]
    if author_id not in person_data_dic:
      person_data_dic[author_id] = {"tweets_num": 0, "city": {}}
    person_data_dic[author_id]["tweets_num"] += 1
    
    valid_gcc = find_gcc(tweet['includes']['places'][0]['full_name'])
    if valid_gcc is not None :
      if valid_gcc not in person_data_dic[author_id]["city"].keys(): 
        person_data_dic[author_id]["city"][valid_gcc] = 0
      person_data_dic[author_id]["city"][valid_gcc] += 1 


