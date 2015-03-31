import argparse
import requests
import slack_logger
from slackclient import SlackClient


def main(args):
  shawn_logger = slack_logger.init(args.token,
                                   'shawntaylor',
                                   args.channel,
                                   'shawntaylor')
  shawn_logger.info('Testing')


def process_args():
  parser = argparse.ArgumentParser()
  parser.add_argument('--channel',
                      default='#stf-testing')
  parser.add_argument('--token')
  parser.add_argument('mode',
                      choices=('q&a',
                               'quotes',
                               'responsive')
  args = parser.parse_args()
  return args

if __name__ == '__main__':
  main(process_args())
