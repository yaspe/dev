# coding: utf-8

import os
import tempfile

from bot import TBot
from settings import TSettings
from link_db import TLinkDb
from utils import page_title, is_admin


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

    def send_stat(self, chat_id):
        msg = 'Total links: {stat[links]}\nTotal users: {stat[users]}'.format(stat=self.db.total_stat())
        self.send_message(chat_id, msg)

    def _dump_csv(self, chat_id, links):
        reply = []
        for link in links:
            if 'uid' in link:
                reply.append('{},{},{}'.format(link['id'], link['uid'], link['link'].replace(',', '\,')))
            else:
                reply.append('{},{}'.format(link['id'], link['link'].replace(',', '\,')))

        tmp = tempfile.NamedTemporaryFile(suffix='.csv', delete=False)
        tmp.write('\n'.join(reply))
        tmp.close()
        self.send_document(chat_id, tmp.name)
        os.unlink(tmp.name)

    def dump_csv(self, chat_id, uid):
        return self._dump_csv(chat_id, self.db.links(uid, limit=10000))

    def dump_csv_full(self, chat_id):
        return self._dump_csv(chat_id, self.db.all_links())

    def process_command(self, event):
        if event.command == '/all':
            return self.send_links(event.uid, event.chat_id)
        if event.command.startswith('/get'):
            return self.send_links(event.uid, event.chat_id, event.args[0] if event.args else 1)
        if event.command.startswith('/del'):
            if not event.args:
                return self.send_message(event.chat_id, 'Link id is required')
            return self.remove_link(event.uid, event.args[0], event.chat_id)
        if event.command == '/stat':
            return self.send_stat(event.chat_id)
        if event.command == '/dump':
            return self.dump_csv(event.chat_id, event.uid)
        if event.command == '/dump_full' and is_admin(event.uid):
            return self.dump_csv_full(event.chat_id)

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
