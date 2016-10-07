# coding: utf-8

import json
import urllib
import urllib2
import time
import requests

from utils import is_admin


class TEvent(object):
    def __init__(self, raw_event):
        self.uid = raw_event['message']['from']['id']
        self.chat_id = raw_event['message']['chat']['id']
        self.message = raw_event['message']['text']
        self.is_command = self.message.startswith('/')
        msg_parts = self.message.split()
        self.command, self.args = msg_parts[0], msg_parts[1:]


class TBot(object):
    def __init__(self, token):
        self.token = token
        self.offset = self._get_offset()

    def _get_req(self, cmd, params=None):
        if not params:
            params = {}
        api_url = 'https://api.telegram.org/bot{}/{}?{}'.format(self.token, cmd, urllib.urlencode(params))
        result = urllib2.urlopen(api_url).read()
        result_json = json.loads(result)
        if result_json['ok']:
            return result_json
        raise "Bad answer: {}".format(result)

    def _post_req(self, cmd, params=None, file_path=None):
        if not params:
            params = {}
        api_url = 'https://api.telegram.org/bot{}/{}'.format(self.token, cmd)
        files = {"document": open(file_path, "rb")} if file else None
        result = requests.post(api_url, data=params, files=files)
        result_json = json.loads(result.content)
        if result_json['ok']:
            return result_json
        raise "Bad answer: {}".format(result)

    def _get_offset(self):
        updates = self._get_req('getUpdates')
        events = updates['result']
        if not events:
            return 0
        last_event = events[-1]
        return int(last_event['update_id']) + 1

    @staticmethod
    def make_keyboard_markup(strings, one_time_keyboard=True):
        return json.dumps({
            'keyboard': strings,
            'resize_keyboard': True,
            'one_time_keyboard': one_time_keyboard,
        })

    @property
    def help_message(self):
        raise NotImplementedError

    def send_help_message(self, chat_id):
        self.send_message(chat_id, self.help_message)

    @property
    def start_message(self):
        raise NotImplementedError

    def send_start_message(self, chat_id):
        self.send_message(chat_id, self.start_message)

    def get_me(self):
        return self._get_req('getMe')

    def get_updates(self):
        result = self._get_req('getUpdates', {'offset': self.offset})
        self.offset = self._get_offset()
        return result

    def send_message(self, chat_id, message, markup=None, disable_preview=False):
        params = {
            'chat_id': chat_id,
            'text': message,
        }
        if markup:
            params['reply_markup'] = markup
        if disable_preview:
            params['disable_web_page_preview'] = 'true'
        self._post_req('sendMessage', params)

    def send_document(self, chat_id, file_path):
        params = {
            'chat_id': chat_id,
        }
        self._post_req('sendDocument', params, file_path=file_path)

    def process_event(self, event):
        raise NotImplementedError

    def run(self):
        while True:
            try:
                updates = self.get_updates()
                for raw_event in updates['result']:
                    event = TEvent(raw_event)
                    if event.is_command:
                        if event.command == '/help':
                            self.send_help_message(event.chat_id)
                            continue
                        elif event.command == '/start':
                            self.send_start_message(event.chat_id)
                            continue
                        elif event.command == '/kill' and is_admin(event.uid):
                            self.send_message(event.chat_id, "Stopping")
                            return

                    self.process_event(event)
            except Exception as e:
                print('Error:', str(e))
            time.sleep(3)
