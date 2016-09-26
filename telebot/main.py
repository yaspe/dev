# coding: utf-8

from bot import TBot
from settings import TSettings
from link_db import TLinkDb
from utils import page_title


class TLinkBot(TBot):
    @property
    def help_message(self):
        return (
            'This is a cool link bot\n'
            'Commands:\n'
            '  /all - shows all your stored links\n'
            '  /get - shows your newest link\n'
            '  /get N - shows your newest N links\n'
            '  /del N - deletes your link with id=N\n'
            'Just send a link to store it\n'
        )

    @property
    def start_message(self):
        return self.help_message

    def __init__(self, settings):
        TBot.__init__(self, settings.token)
        self.db = TLinkDb(settings.db_path)

    def send_links(self, uid, chat_id, limit=None):
        links = self.db.links(uid, limit)
        reply = []
        for link in links:
            reply.append('%s. %s' % (link['id'], link['link']))
        self.send_message(chat_id, '\n'.join(reply), disable_preview=len(links) != 1)

    def remove_link(self, uid, link_id, chat_id):
        self.db.remove(link_id, uid)
        self.send_message(chat_id, 'Link #%s has been removed' % link_id)

    def process_command(self, event):
        if event.command == '/all':
            return self.send_links(event.uid, event.chat_id)
        if event.command.startswith('/get'):
            return self.send_links(event.uid, event.chat_id, event.args[0] if event.args else 1)
        if event.command.startswith('/del'):
            if not event.args:
                return self.send_message(event.chat_id, 'Link id is required')
            return self.remove_link(event.uid, event.args[0], event.chat_id)

        self.send_help_message(event.chat_id)

    def process_event(self, event):
        if event.is_command:
            return self.process_command(event)

        if event.message.startswith('http'):
            if ' ' not in event.message and '\t' not in event.message:
                try:
                    title = page_title(event.message)
                    event.message += ' %s' % title
                except Exception as e:
                    print str(e)
            self.db.store(event.uid, event.message)
            self.send_message(event.chat_id, 'Your link has been stored')
        else:
            self.send_message(event.chat_id, 'Invalid link, valid link should starts with http or https')


if __name__ == '__main__':
    TLinkBot(TSettings('/Users/ya-spe/github/dev/telebot/settings.txt')).run()
