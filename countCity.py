def countCity(gcc_dict, tweet_data, sal_data): 
  for tweet in tweet_data:
        full_name = tweet['includes']['places'][0]['full_name']
        city_name = full_name.split(',')[0].strip()
      
        for key, value in sal_data.items():
          if value['gcc'][1] == 'g':
            if key.lower() == city_name.lower():  
                gcc = value['gcc']
                if gcc not in gcc_dict:
                    gcc_dict[gcc] = 0
                gcc_dict[gcc] += 1

def check_city(city):
  if city == "1gsyd":
    return "Greater Sydney"
  if city == "2gmel":
    return "Greater Melbourne"
  if city == "3gbri":
    return "Greater Brisbane"
  if city == "4gade":
    return "Greater Adelaide"
  if city == "5gper":
    return "Greater Perth"
  if city == "6ghob":
    return "Greater Hobart"
  if city == "7gdar":
    return "Greater Darwin"