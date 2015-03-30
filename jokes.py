#!/usr/bin/env python

import argparse
import json
import random
import sys
import time


_QA_JOKES = json.load(open('qa_jokes.json'))

_LAUGHS = [
    'Hahaha!',
    'Lol!!',
    ':laughing:',
]


class NewlineWrapper(object):

  def __init__(self, stream):
    self.stream = stream

  def write(self, *args, **kwargs):
    self.stream.write(*args, **kwargs)
    self.stream.write('\n')


class QAJoke(object):
  
  def __init__(self, qa_joke, username=None, delay_seconds=0):
    question = qa_joke['q']
    answer = qa_joke['a']
    if username:
      question = 'Hey {}! {}'.format(username, question)
    self.question = question
    self.answer = '{} {}'.format(answer, random.choice(_LAUGHS))
    self.delay_second = delay_seconds

  def tell_joke(self, stream):
    stream.write(self.question)
    time.sleep(self.delay_second)
    stream.write(self.answer)


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
