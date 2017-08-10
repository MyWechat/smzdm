# -*- coding: utf-8 -*-

import sqlite3
import json
import os

# sqlite storage
class Storage(object):
    PUSHED_TB = 'pushed'
    USER_TB = 'user'

    def __init__(self, db='store.db'):
        ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
        os.chdir(ROOT_PATH)

        self.conn = sqlite3.connect(db)
        self.cursor = self.conn.cursor()

        self._init_check()

    def __del__(self):
        self.cursor.close()
        self.conn.close()

    def _dict_to_table_syntax(self, d):
        return ','.join(['%s %s' % (i, d[i]) for i in d])

    def _init_check(self):
        push_table = {
            'id': 'vchar(64) primary key',
            'data': 'text',
            'timestamp': 'datetime default current_timestamp'
        }

        user_table = {
            'user': 'vchar(255) primary key',
            'data': 'text'
        }

        tables = {self.PUSHED_TB: push_table, self.USER_TB: user_table}
        for table in tables:
            table_syntax = self._dict_to_table_syntax(tables[table])

            sql = 'create table if not exists %s (%s)' % (table, table_syntax)
            self.cursor.execute(sql)

    def pushed(self, id):
        self.cursor.execute('select * from %s where id=?' % (self.PUSHED_TB), (id,))
        res = self.cursor.fetchone()
        return res

    def add_push(self, id, data):
        self.cursor.execute('insert into %s (id, data) VALUES (%s, \'%s\')' % (self.PUSHED_TB, id, json.dumps(data)))
        self.conn.commit()
        return self.cursor.lastrowid

    def drop_push(self):
        self.cursor.execute('drop table %s' % (self.PUSHED_TB))
        self.conn.commit()

    def flush_push(self):
        self.cursor.execute('delete from %s' % (self.PUSHED_TB))
        self.conn.commit()

    def user_status(self, user):
        self.cursor.execute('select user, data from %s where user=?' % (self.USER_TB), [user])
        res = self.cursor.fetchone()
        return res

    def set_user(self, user, data):
        u = self.user_status(user)
        if not u:
            self.cursor.execute('insert into %s (user, data) VALUES (\'%s\', \'%s\')' % (self.USER_TB, user, json.dumps(data)))
        else:
            self.cursor.execute('update %s set data=\'%s\' where user=?' % (self.USER_TB, json.dumps(data)), [user])
        self.conn.commit()

    def all_active_users(self):
        self.cursor.execute('select user, data from %s' % (self.USER_TB))
        res = self.cursor.fetchall()
        ret = []
        try:
            for i in res:
                user = i[0]
                data = json.loads(i[1])
                if data['state'] == 'smzdm/start':
                    ret.append(user)
        except Exception as e:
            pass

        return ret

    def __getattr__(self, attr):
        for child in [self.cursor, self.conn]:
            if hasattr(child, attr):
                def wrapper(*args, **kw):
                    print('called with %r and %r' % (args, kw))
                    return getattr(child, attr)(*args, **kw)

                return wrapper
        raise AttributeError(attr)


if __name__ == '__main__':
    s = Storage()
    s.set_user('1', [11])
    print s.user_status('1')
