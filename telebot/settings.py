# coding: utf-8

class TSettings(object):
    def __init__(self, path):
        self.token = None
        self.db_path = None
        for line in open(path):
            if line.startswith('token'):
                self.token = line.split()[-1]
            elif line.startswith('db_path'):
                self.db_path = line.split()[-1]
        if not self.token:
            raise Exception("token is not provided by config")
        if not self.db_path:
            raise Exception("db_path is not provided by config")
