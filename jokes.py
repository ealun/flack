#!/usr/bin/env python

import argparse
import json
import random
import sys
import time


_QA_JOKES = json.load(open('qa_jokes.json'))
_RESPONSES = json.load(open('responses.json'))

_LAUGHS = [
    'Hahaha!',
    'Lol!!',
    ':laughing:',
    'Heh',
    'hahaha'
]


class NewlineWrapper(object):

  def __init__(self, stream):
    self.stream = stream

  def write(self, *args, **kwargs):
    self.stream.write(*args, **kwargs)
    self.stream.write('\n')


class QAJoke(object):
  
  def __init__(self, qa_joke, username=None, qa_delay_seconds=0, laugh_delay_seconds=0):
    question = qa_joke['q']
    answer = qa_joke['a']
    if username:
      question = 'Hey {}! {}'.format(username, question)
    self.question = question
    self.answer = answer
    self.laughter = random.choice(_LAUGHS)
    self.qa_delay_second = qa_delay_seconds
    self.laugh_delay_second = laugh_delay_seconds


  def tell_joke(self, stream):
    stream.write(self.question)
    time.sleep(self.qa_delay_second)
    stream.write(self.answer)
    time.sleep(self.laugh_delay_second)
    stream.write(self.laughter)


class ResponseJoke(object):

  def __init__(self, response_joke, username=None):
    self.username = username
    self.response_joke = response_joke

  def tell_joke(self, stream):
    stream.write('{} {}'.format(self.username, self.response_joke))


def get_joke(joke_type=None, username=None):
  joke_type = joke_type or random.choice((
      'qa',
      'response'))
  if joke_type == 'qa':
    return QAJoke(random.choice(_QA_JOKES),
                  username=username,
                  qa_delay_seconds=random.randint(5, 10),
                  laugh_delay_seconds=random.randint(4, 7))
  elif joke_type == 'response':
    return ResponseJoke(random.choice(_RESPONSES),
                        username=username)

def main(args):
  if args.type == 'qa':
    joke = QAJoke(random.choice(_QA_JOKES),
                  delay_seconds=args.delay,
                  username=args.username)
    joke.tell_joke(NewlineWrapper(sys.stdout))


def process_args():
  parser = argparse.ArgumentParser()
  parser.add_argument('--type', default='qa', choices=('qa',))
  parser.add_argument('--delay', default=0, type=int)
  parser.add_argument('--username', default=None)
  args = parser.parse_args()
  return args


if __name__ == '__main__':
  main(process_args())
