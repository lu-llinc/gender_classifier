#!/usr/bin/env python2.7
# encoding: utf-8
'''Simple wrapper around MySQLdb object. Contains some convenience methods for querying.
'''
import re
import MySQLdb

class Model(object):

    def __init__(self, mysql):
        self.mysql = mysql
        self._conn = None
        self._cursor = None # Do not access this, use the execute and commit methods on Model

        # Sometimes changes need to be committed immediately (when working interactively).
        # Other times, it is much faster to perform in bulk, and make a single transaction.
        # This flag will disable calls to self.commit(), such that we can prevent slow bulk operations.
        self._in_transaction = False

        self.connect()

    def connect(self):
        '''(Re)connect using the credentials given in the constructor'''
        self._conn = self.mysql.connect()
        self._cursor = self._conn.cursor(MySQLdb.cursors.DictCursor)

    def execute(self, *args, **kwargs):
        try:
            result = self._cursor.execute(*args, **kwargs)
        except MySQLdb.ProgrammingError as e:
            raise MySQLdb.ProgrammingError(e.args[0], e.args[1] + '.\nSTATEMENT: {}'.format(self._cursor._last_executed))
        except MySQLdb.OperationalError as e:
            # Sometimes a MySQL session times out. In this case, we wish to reconnect, and reissue the query.
            if e[0] == 2006:
                self.connect()
                result = self._cursor.execute(*args, **kwargs)
            else:
                raise MySQLdb.OperationalError(e.args[0], e.args[1] + '.\nSTATEMENT: {}'.format(self._cursor._last_executed))
        return result

    def empty(self, *args, **kwargs):
        '''Returns true if the result set for the given query is empty'''
        self.execute(*args, **kwargs)
        return self.fetchone() is None

    def fetchone(self, *args, **kwargs):
        return self._cursor.fetchone(*args, **kwargs)

    def fetchall(self, filter_attr=None):
        '''`filter_attr` is used for convenience to create a list of single attribute values.

        Example:
            if the result of `fetchall()` would be:
                [{"id": 10}, {"id": 12}],
            then the result of `fetchall('id')` would be:
                [10, 12]
        '''
        results = self._cursor.fetchall()
        if filter_attr is not None:
            if results is None:
                return []
            else:
                return [result[filter_attr] for result in results]
        else:
            return results

    def fetch_attr(self, attr, default=None):
        '''Returns the attribute of the first fetch if there is one, otherwise `default`
        '''
        row = self.fetchone()
        if not row:
            return default
        else:
            return row[attr]

    def use_db(self, dbname):
        try:
            self.execute('USE `{}`'.format(dbname))
        except:
            return False
        return True

    def create_db(self, dbname):
        self.execute('CREATE DATABASE `{}` CHARACTER SET utf8 COLLATE utf8_bin'.format(dbname))

    def drop_db(self, dbname):
        self.execute('DROP DATABASE `{}`'.format(dbname))

    def execute_file(self, fname, verbose=False):
        '''Execute MySQL from a file

        Note that many shell built-ins are not supported, which do work when running from shell.
        Special code is added to support the `delimiter` shell built-in.
        '''
        buff = []
        delim = ';'
        for line in open(fname):
            # Buffer lines
            line = line.strip()

            # Check for change in delimiter
            m = re.match(r'delimiter (.+)$', line, re.IGNORECASE)
            if m:
                delim = m.group(1)
                continue # Do not execute change delimiter: this is not supported

            # Ignore lines with comments
            if line.startswith('--'):
                continue

            # If delimiter, replace the delimiter, and flush the buffer
            if line.endswith(delim):
                buff.append(line[:-len(delim)])
                if verbose:
                    print 'Executing:', '-'*80, '\n', '\n'.join(buff), '\n', '-'*80, '\n'
                self.execute('\n'.join(buff))
                buff = []
            else:
                buff.append(line)

    def insert_id(self):
        return self._conn.insert_id()

    def commit(self):
        if not self._in_transaction:
            self._conn.commit()

    def insert_dict(self, table, data):
        '''Insert a dict into the table. Assume that the keys of the dict are equal to the columns.
        Note: you must commit yourself.
        '''
        # Want to simply use the keys of the data for inserting,
        # but we can not necessarily trust these keys.
        for k in data:
            self.ensure_safe(k)
        self.ensure_safe(table)

        query = 'INSERT INTO {} ({}) VALUES ({})'.format(
            table, ', '.join(data), ', '.join('%s' for d in data)
        )
        self.execute(query, data.values())
        id = self.insert_id()
        return id

    @classmethod
    def filter_if_null(self, data, attributes):
        '''Modify data in place. Used to remove attributes that are None,
        so their default values can be inserted by MySQL.'''
        for attr in attributes:
            if attr in data and data[attr] is None:
                data.pop(attr)
        return data

    def start_transaction(self):
        self._in_transaction = True

    def stop_transaction(self):
        self._in_transaction = False
        self.commit()

    @staticmethod
    def ensure_safe(str):
        assert ';' not in str, '{} is unsafe'.format(str)
        return str
