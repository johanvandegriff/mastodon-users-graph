#!/usr/bin/python
import json
import requests

url = 'https://mastodon.social/api/v1/accounts/lookup?acct=mastodonusercount'
#url = 'https://lou.lt/api/v1/accounts/lookup?acct=mastodonusercount'
response = requests.get(url).json()
id = response['id']
url = f'https://mastodon.social/api/v1/accounts/{id}'
#url = f'https://lou.lt/api/v1/accounts/{id}'

#url = 'https://bitcoinhackers.org/api/v1/accounts/6079' #@mastodonusercount@bitcoinhackers.org

response = requests.get(url).json()
total_num_posts = response['statuses_count']

url = url+'/statuses'


posts = []
response = requests.get(url).json()

while len(response) > 0:
  posts.extend(response)
  max_id = posts[-1]['id']
  response = requests.get(f'{url}?limit=99999&max_id={max_id}').json()
  print(f'{len(posts)}/{total_num_posts}')

with open('mastodonusercount.json', 'w') as f:
  json.dump(posts, f)
