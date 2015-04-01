#!/usr/bin/env python

import argparse
import json
import requests
import random
from slackclient import SlackClient
import time

from jokes import get_joke


_ICON_URL = 'https://media.licdn.com/mpr/mpr/shrinknp_400_400/p/5/000/26b/340/1a04f41.jpg'
_BANNED_CHANNELS = {'C02950TDE', 'C02950TDJ', 'C03HU2AKW', 'C029RK17W'}

class SlackStream(object):

  def __init__(self, data):
    self.data = data

  def write(self, text):
    data = dict(self.data)
    data['text'] = text
    requests.post('https://slack.com/api/chat.postMessage',
                  data=data)


def check_comments(slack_comments, bot_name, token):
  for comment in slack_comments:
    if comment.get('type') == 'message' and comment.get('subtype') != 'bot_message':
      try:
        response = requests.post('https://slack.com/api/users.info',
                                 data={'token': token,
                                       'user': comment.get('user')}).json()
        user = response['user']['name']
      except:
        user = None
      response_joke = '@%s' % bot_name in comment.get('text', '')
      channel = comment.get('channel')
      if channel in _BANNED_CHANNELS or not response_joke and random.randint(1, 3) != 1:
        continue
      joke = get_joke(joke_type='response' if response_joke else None,
                      username='@{}'.format(user))
      stream = SlackStream(dict(
          token=token,
          icon_url=_ICON_URL,
          channel=channel,
          username=bot_name))
      joke.tell_joke(stream)


def main(args):
  sc = SlackClient(args.token)
  if sc.rtm_connect():
    while True:
      comments = sc.rtm_read()
      print comments
      check_comments(comments, args.bot_name, args.token)
      time.sleep(1)


def process_args():
  parser = argparse.ArgumentParser()
  parser.add_argument('--bot-name',
                      default='tester')
  parser.add_argument('--token')
  args = parser.parse_args()
  return args

if __name__ == '__main__':
  main(process_args())
