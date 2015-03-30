import argparse
import slack_logger


def main(args):
  shawn_logger = slack_logger.init(logger_name='shawntaylor',
                                   channel=args.channel,
                                   bot_name='shawntaylor')
  shawn_logger.info('Testing')

def process_args():
  parser = argparse.ArgumentParser()
  parser.add_argument('--channel')
  parser.add_argument('mode',
                      choices=('q&a',
                               'quotes',
                               'responsive')
  args = parser.parse_args()
  return args

if __name__ == '__main__':
  main(process_args())
