#!/usr/bin/env python

import sys, os, re, csv, operator

def filter_ticky_logs():
  dict = []
  with open("syslog.log", 'r') as syslog_file:
    for line in syslog_file:
      result = re.search(r"ticky: (\w+): ([\w\s]+).+\((\w+)\)$", line)
      if result is not None:
        dict.append({"name":result.group(1),"desc":result.group(2),"user":result.group(3)})
  return dict

def ranking(dict):
  error_ranking = {}
  user_error_ranking = {}
  user_info_ranking = {}

  for item in dict:
    desc = item["desc"]
    name = item["name"]
    user = item["user"]

    if name  == "ERROR":
      error_ranking[desc] = error_ranking.get(desc, 0) +1
      user_error_ranking[user] = user_error_ranking.get(user, 0) +1
    else:
      user_info_ranking[user] = user_info_ranking.get(user, 0) +1
  
  # Sort errors by quantity and user statistics for error and info by name
  error_ranking = sorted(error_ranking.items(), key=operator.itemgetter(1), reverse=True)
  user_error_ranking = sorted(user_error_ranking.items(), key=operator.itemgetter(0),reverse=True)
  user_info_ranking = sorted(user_info_ranking.items(), key=operator.itemgetter(0),reverse=True)

  users = []
  for user in range(len(user_error_ranking)):
    users.append([user_error_ranking[user][0], user_error_ranking[user][1],user_info_ranking[user][1]])

  with open("user_statistics.csv", 'w+') as user_statistics_file:
    writer = csv.writer(user_statistics_file)
    writer.writerow(["Username", "INFO", "ERROR"])
    writer.writerows(users)

  with open("error_message.csv", 'w+') as error_msg_file:
    writer = csv.writer(error_msg_file)
    writer.writerow(["Error","Count"])
    writer.writerows(error_ranking)

if __name__=="__main__":
  dict = filter_ticky_logs()
  ranking(dict)
