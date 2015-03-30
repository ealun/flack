import logging
import logging.handlers
import requests


# https://api.slack.com/methods/chat.postMessage

# How should this stolen code be credited?
class SlackLogger(logging.Handler):
  def __init__(self, token, channel, bot_name='bot', *args, **kwargs):
    super(SlackLogger, self).__init__(*args, **kwargs)
    self.channel = channel
    self.token = token
    self.bot_name = bot_name

  def emit(self, record):
    data = {'token': self.token,
            'channel': self.channel,
            'username': self.bot_name,
            'text': record.getMessage()}
    requests.post('https://slack.com/api/chat.postMessage', data=data)
    return


def init(token='xoxp-2311027440-2314797283-2371321703-52806a',
         channel='#stf-testing',
         logger_name='shawntaylor',
         bot_name='shawntaylor'):
  log = logging.getLogger(logger_name)
  log.addHandler(SlackLogger(token, channel, bot_name))
  log.setLevel(logging.DEBUG)
  return log
