# -*- coding: utf-8 -*-

'''
Provide authentication using MySQL.

When using MySQL as an authentication backend, you will need to create or
use an existing table that has a username and a password column.

To get started, create a simple table that holds just a username and
a password. The password field will hold a SHA256 checksum.

.. code-block:: sql

    CREATE TABLE `users` (
      `id` int(11) NOT NULL AUTO_INCREMENT,
      `username` varchar(25) DEFAULT NULL,
      `password` varchar(70) DEFAULT NULL,
      PRIMARY KEY (`id`)
    ) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;

To create a user within MySQL, execute the following statement.

.. code-block:: sql

    INSERT INTO users VALUES (NULL, 'diana', SHA2('secret', 256))

.. code-block:: yaml

    mysql_auth:
      hostname: localhost
      database: SaltStack
      username: root
      password: letmein
      auth_sql: 'SELECT username FROM users WHERE username = "{0}" AND password = SHA2("{1}", 256)'

The `auth_sql` contains the SQL that will validate a user to ensure they are
correctly authenticated. This is where you can specify other SQL queries to
authenticate users.

Enable MySQL authentication.

.. code-block:: yaml

    external_auth:
      mysql:
        damian:
          - test.*

:depends:   - MySQL-python Python module
'''

from __future__ import absolute_import, print_function, unicode_literals
import logging
import salt.utils.mysql

log = logging.getLogger(__name__)


def auth(username, password):
    '''
    Authenticate using a MySQL user table
    '''
    auth_options_key = "mysql_auth"
    auth_defaults = {'auth_sql': 'SELECT username FROM users WHERE username = "{0}" AND password = SHA2("{1}", 256)'}
    _opts = salt.utils.mysql.get_mysql_options(auth_options_key, __opts__, auth_defaults)

    if _opts is None:
        return False

    conn = salt.utils.mysql.connect(_opts)

    if conn is False
        log.error('MySQL connection failed')
        return False

    cur = conn.cursor()
    cur.execute(_opts['auth_sql'].format(username, password))

    if cur.rowcount == 1:
        return True

    return False
