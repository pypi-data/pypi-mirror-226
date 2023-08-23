# -*- coding: utf-8 -*-
"""
####################################################
###########         dependency          ############
####################################################
# Option 1: requires mysql client installed
pip install mysqlclient DBUtils

# Option 2: green pure python client, slower than `mysqlclient`
pip install pymysql DBUtils

####################################################
###########         config.yml          ############
####################################################
mysql:
  default:
    host: default-host
    port: 3306
    user: username
    password: password
    db: default_db_name
  some-other:
    host: some-other-host
    port: 3306
    user: username
    password: password
    db: default_db_name


####################################################
###########          usage              ############
####################################################
from hao.mysql import MySQL
with MySQL() as db:
    db.cursor.execute('select * from t_dummy_table')
    records = db.cursor.fetchall()

with MySQL('some-other', cursor_class='dict') as db:
    ...
"""

from typing import Optional, Union

from . import config, logs

try:
    from dbutils.pooled_db import PooledDB
except ImportError:
    from DBUtils.PooledDB import PooledDB

try:
    import pymysql as mysqlclient
    from pymysql.connections import Connection
    from pymysql.cursors import Cursor, DictCursor, SSCursor, SSDictCursor
except ImportError:
    import MySQLdb as mysqlclient
    from MySQLdb.connections import Connection
    from MySQLdb.cursors import Cursor, DictCursor, SSCursor, SSDictCursor


LOGGER = logs.get_logger(__name__)


class MySQL:
    _POOLS = {}
    _CURSOR_CLASSES = {
        'default': Cursor,
        'ss': SSCursor,
        'dict': DictCursor,
        'ss-dict': SSDictCursor,
    }

    def __init__(self, profile='default', cursor_class='default') -> None:
        super().__init__()
        self.profile = profile
        self.cursor_class = cursor_class or 'default'
        self._ensure_pool()

    def _get_cursor_class(self):
        return self._CURSOR_CLASSES.get(self.cursor_class, Cursor)

    def _ensure_pool(self):
        if self.profile in MySQL._POOLS:
            return
        conf_profile = config.get(f"mysql.{self.profile}", {})
        if len(conf_profile) == 0:
            raise ValueError(f'mysql profile not configured: {self.profile}')
        conf = {
            'mincached': 1,
            'maxcached': 2,
            'maxshared': 2,
            'maxconnections': 20,
            'use_unicode': True,
            'charset': "utf8",
            'cursorclass': self._get_cursor_class(),
            'autocommit': True,
        }
        conf.update(conf_profile)
        LOGGER.debug(f"connecting [{self.profile}], host: {conf.get('host')}, db: {conf.get('db')}")

        pool = PooledDB(
            mysqlclient,
            mincached=conf.pop('mincached', 1),
            maxcached=conf.pop('maxcached', 2),
            maxshared=conf.pop('maxshared', 2),
            maxconnections=conf.pop('maxconnections', 20),
            blocking=conf.pop('blocking', False),
            maxusage=conf.pop('maxusage', None),
            setsession=conf.pop('setsession', None),
            reset=conf.pop('reset', True),
            failures=conf.pop('failures', None),
            ping=conf.pop('ping', 1),
            **conf
        )
        MySQL._POOLS[self.profile] = pool

    def __enter__(self):
        self.conn = self.connect()
        self.cursor = self.conn.cursor()
        return self

    def connect(self) -> Connection:
        return self._POOLS.get(self.profile).connection()

    def execute(self, sql: str, params: Optional[Union[list, tuple]] = None):
        self.cursor.execute(sql, params)
        return self.cursor

    def fetchone(self, sql: str, params: Optional[Union[list, tuple]] = None):
        self.cursor.execute(sql, params)
        return self.cursor.fetchone()

    def fetchall(self, sql: str, params: Optional[Union[list, tuple]] = None):
        self.cursor.execute(sql, params)
        return self.cursor.fetchall()

    def fetch(self, sql: str, params: Optional[Union[list, tuple]] = None, batch=2000):
        self.cursor.execute(sql, params)
        while True:
            records = self.cursor.fetchmany(size=batch)
            if not records:
                break
            for record in records:
                yield record

    def commit(self, sql: str, params: Optional[Union[list, tuple]] = None):
        rowcount = self.cursor.execute(sql, params)
        self.conn.commit()
        return rowcount

    def rollback(self):
        self.conn.rollback()

    def __exit__(self, _type, _value, _trace):
        self.cursor.close()
        self.conn.close()
