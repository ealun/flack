#!/usr/bin/env python

import argparse
import json
import requests
import random
import slack_logger
from slackclient import SlackClient
import time


_RESPONSES = json.load(open('responses.json'))


def make_reply(name, channel, user, token):
  shawn_logger = slack_logger.init(token,
                                   name,
                                   channel,
                                   name)
  # Make a sassy reply in the way that only Shawn can: with farts.
  response = random.choice(_RESPONSES)
  # TODO: Figure out how to send the reply properly.
  shawn_logger.info('@{} {}'.format(user, response) if user
                    else response)


def check_comments(slack_comments, name, token):
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
      make_reply(name, comment.get('channel'), user, token)


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
                      default='shawntaylor')
  parser.add_argument('--token')
  args = parser.parse_args()
  return args

if __name__ == '__main__':
  main(process_args())
