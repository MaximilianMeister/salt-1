# -*- coding: utf-8 -*-
'''
MySQL Common Utils
=================

Establishes a connection to MySQL Server.

Example Usage:

    .. code-block:: python

        import salt.utils.mysql

        # options_key is the highest level key in the sls file, it varies between implementations
        # e.g. 'mysql_auth' for auth, 'mysql' for pillars
        options_key = 'mysql_auth'

        # custom_defaults is a custom dictionary that should be merged with the default options
        custom_defaults = {'auth_sql': 'SELECT username FROM users WHERE username = "{0}" AND password = SHA2("{1}", 256)'}

        # get the options data to perform the connection
        opts = salt.utils.mysql.get_mysql_options(options_key, __opts__, custom_defaults)

        # connect
        conn = salt.utils.mysql.connect(opts)

        # use the connection
        cur = conn.cursor()
        cur.execute(opts['auth_sql'].format(username, password))

.. versionadded:: 2018.3.0
'''

# Import Python libs
from __future__ import absolute_import, print_function, unicode_literals
import logging

# Import third party mysql libs
try:
    # Trying to import MySQLdb
    import MySQLdb
    import MySQLdb.cursors
    import MySQLdb.converters
    from MySQLdb.connections import OperationalError
except ImportError:
    try:
        # MySQLdb import failed, try to import PyMySQL
        import pymysql
        pymysql.install_as_MySQLdb()
        import MySQLdb
        import MySQLdb.cursors
        import MySQLdb.converters
        from MySQLdb.err import OperationalError
    except ImportError:
        MySQLdb = None

log = logging.getLogger(__name__)


def __virtual__():
    '''
    Confirm that a python mysql client is installed.
    '''
    return bool(MySQLdb), 'No python mysql client installed.' if MySQLdb is None else ''


def _get_mysql_defaults(custom_defaults=None):
    '''
    Returns the mysql defaults merged with the library specific defaults
    '''
    defaults = {'hostname': 'localhost',
                'username': 'salt',
                'password': 'salt',
                'database': 'salt',
                'port': 3306,
                'unix_socket': '/tmp/mysql.sock',
                'charset': 'utf8',
                'ssl': {}}

    if custom_defaults is not None:
        defaults.update(custom_defaults)

    return defaults


def get_mysql_options(options_key=None, options=None, custom_defaults=None):
    '''
    Returns options used by the specific library (auth, modules, returners, etc...) for the MySQL connection.
    '''
    defaults = _get_mysql_defaults(custom_defaults)
    _options = {}
    _opts = __opts__.get(options_key, {})
    for attr in defaults:
        if attr not in _opts:
            log.debug('Using default for MySQL %s', attr)
            _options[attr] = defaults[attr]
            continue
        _options[attr] = _opts[attr]
    return _options


def connect(options=None):
    '''
    Connect to MySQL database
    '''
    if options is None:
        log.debug('No options passed for connection')
        return False

    try:
        conn = MySQLdb.connect(options['hostname'],
                               options['username'],
                               options['password'],
                               options['database'],
                               options['port'],
                               options['unix_socket'],
                               options['ssl'])
        return conn
    except OperationalError as e:
        log.error(e)
        return False
