def matchState(val1, val2):
   return (val1 == "New South Wales" and "nsw" in val2) or \
          (val1 == "Victoria" and "vic" in val2) or \
          (val1 == "Queensland" and "qld" in val2) or \
          (val1 == "Western Australia" and "wa" in val2) or \
          (val1 == "South Australia" and "sa" in val2) or \
          (val1 == "Tasmania" and "tas" in val2) or \
          (val1 == "Northern Territory" and "nt" in val2) or \
          (val1 == "Australian Capital Territory" and "act" in val2)


def countCity(gcc_dict, tweet_data, sal_data): 
  for tweet in tweet_data:
        full_name = tweet['includes']['places'][0]['full_name']
        if not "," in full_name: 
           continue
        city_name = full_name.split(',')[0].strip()
        state_name = full_name.split(',')[1].strip()

        for key, value in sal_data.items():
          if value['gcc'][1] == 'g':
            if "(" in key:
              if "-" in key: 
                shorthand_state_name = key.split('-')[1].strip()
              elif "(" in key:
                shorthand_state_name = key.split('(')[1].strip()
              key_city_name = key.split('(')[0].strip().lower()
              if matchState(state_name, shorthand_state_name) and key_city_name == city_name.lower(): 
                gcc = value['gcc']
                if gcc not in gcc_dict:
                    gcc_dict[gcc] = 0
                gcc_dict[gcc] += 1
                break
              continue
            else:
              if key.lower() == city_name.lower():  
                  gcc = value['gcc']
                  if gcc not in gcc_dict:
                      gcc_dict[gcc] = 0
                  gcc_dict[gcc] += 1
                  break
              
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
  
