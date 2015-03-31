#!/usr/bin/env python

import argparse
import requests
import slack_logger
from slackclient import SlackClient
import time


def make_reply(name, channel, token):
  shawn_logger = slack_logger.init(token,
                                   name,
                                   channel,
                                   name)
  # Make a sassy reply in the way that only Shawn can: with farts.
  # TODO: Add these responses
  shawn_logger.info('Test fart')


def check_comments(slack_comments, name, token):
  for comment in slack_comments:
    if (comment.get('type') == 'message' and
        '@%s' % bot_name in comment.get('text')):
      make_reply(name, comment.get('channel'), token)

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
