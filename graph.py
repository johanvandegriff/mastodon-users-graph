#!/usr/bin/python
import json
import requests
import datetime

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import StrMethodFormatter
from matplotlib.ticker import FuncFormatter


all_posts = []
# posts_separated = []

files = [ #new to old
  'mastodonusercount-5-mastodon.social.json',
  'mastodonusercount-4-manually-gathered.json',
  'mastodonusercount-3-bitcoinhackers.org.json',
  'mastodonusercount-0-lou.lt.json'
]

for file in files:
  with open(file, 'r') as f:
    file_contents = json.load(f)
    # posts_separated.append(file_contents)
    all_posts.extend(file_contents)


# posts = [
# {
# "created_at": "2022-11-18T10:00:17.000Z",
# "content": "<p>6,980,781 accounts <br>+10,739 in the last hour<br>+118,404 in the last day<br>+459,733 in the last week</p>"
# }
# ,
# {
# "created_at": "2022-11-18T11:00:17.000Z",
# "content": "<p>6,980,781 accounts <br>+10,739 in the last hour<br>+118,404 in the last day<br>+459,733 in the last week</p>"
# }
# ]

timestamps = []
data = []

for post in all_posts[::1]: #every 1 posts
# for post in all_posts[::100]: #every 100 posts
  created_at = post['created_at']
  content = post['content']
  # print(created_at, content)
  # "created_at": "2022-11-18T10:00:17.000Z",
  # "content": "<p>6,980,781 accounts <br>+10,739 in the last hour<br>+118,404 in the last day<br>+459,733 in the last week</p>"
  try:
    num_accounts = int(content.replace('<p>','').split(' accounts')[0].replace(',',''))
  except:
    continue
  timestamp = datetime.datetime.strptime(created_at, '%Y-%m-%dT%H:%M:%S.%fZ')
  timestamps.append(timestamp)
  data.append(num_accounts)
  # print(timestamp, num_accounts)

# timestamps = [timestamps]
# data = [data]

# print(len(timestamps), len(data))

# print(json.dumps(data, indent=2))
# print(timestamps)
# quit()

# plotting the data
plt.plot(timestamps, data)

# plt.plot(timestamps[:614], data[:614])
# plt.plot(timestamps[613:615], data[613:615], linestyle='dotted')
# plt.plot(timestamps[615:], data[615:])

# prev = 0
# for p in posts_separated:
#   start = prev
#   end = prev+len(p)-1
#   dotted_start = prev+len(p)-2
#   dotted_end = prev+len(p)+1
#   plt.plot(timestamps[start:end], data[start:end], color='tab:blue')
#   plt.plot(timestamps[dotted_start:dotted_end], data[dotted_start:dotted_end], color='tab:blue', linestyle='dotted')
#   prev = len(p)+1
#  print(len(p))

def millions(x, pos):
#  The two args are the value and tick position
#  return '%1.1fM' % (x * 1e-6)
  return int(x/1_000_000)

plt.gca().yaxis.set_major_formatter(FuncFormatter(millions))
plt.yticks(range(0, 10_000_001, 1_000_000))
plt.grid(visible=True, which='major', axis='both')
plt.xlim(datetime.date(2017, 1, 1), datetime.date(2023, 6, 1))
plt.ylim(0, 10_500_000)
#plt.format_xdata = mdates.DateFormatter('%Y-%m-%d')
#plt.xticks(rotation=45)

# Adding the title
plt.title('''data from @mastodonusercount@lou.lt,
@mastodonusercount@bitcoinhackers.org,
and @mastodonusercount@mastodon.social''', fontdict={'color': '#333'})
plt.suptitle('Total Mastodon Users over Time', fontsize='x-large')

# Adding the labels
plt.ylabel("number of users (millions)")
plt.xlabel("date")
plt.xticks(rotation=30)
plt.show()
