#!/usr/bin/env python

import argparse
import json
import requests
import random
from slackclient import SlackClient
import time

from jokes import get_joke


_RESPONSES = json.load(open('responses.json'))


class SlackStream(object):

  def __init__(self, data):
    self.data = data

  def write(self, text):
    data = dict(self.data)
    data['text'] = text
    requests.post('https://slack.com/api/chat.postMessage',
                  data=data)


def make_reply(bot_name, channel, user, token):
  # Make a sassy reply in the way that only Shawn can: with farts.
  response = random.choice(_RESPONSES)
  data = {'token': token,
          'channel': 'G046U1HRJ', #channel,
          'username': bot_name,
          'text': '@{} {}'.format(user, response) if user else response}
  requests.post('https://slack.com/api/chat.postMessage',
                data=data)


def check_comments(slack_comments, bot_name, token):
  for comment in slack_comments:
    if (comment.get('type') == 'message' and
        '@%s' % bot_name in comment.get('text')):
      # This will have the user's id; use it to look up the name.
      try:
        response = requests.post('https://slack.com/api/users.info',
                                 data={'token': token,
                                       'user': comment.get('user')}).json()
        user = response['user']['name']
      except:
        user = None
      joke = get_joke(username='@{}'.format(user))
      if False:
        stream = SlackStream(dict(
            token=token,
            channel=comment.get('channel'),
            username=bot_name))
      else:
        stream = SlackStream(dict(
            token=token,
            channel='G046U1HRJ',
            username=bot_name))
      joke.tell_joke(stream)
      #make_reply(bot_name, comment.get('channel'), user, token)


def main(args):
  # Start an RTM session and read conversations to listen
  # for someone mentioning the bot's name.
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
