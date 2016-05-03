#!/usr/bin/env python2.7
# encoding: utf-8
'''If executed as a script, prints an export of the database config.
'''
import ConfigParser
import sys


def read_server_config(config_files):
    config = ConfigParser.ConfigParser()
    read = config.read(config_files)
    if not read:
        raise ValueError('None of the config files ({}) could be opened'.format(config_files))

    server = extract_server_config(config)
    db = extract_db_config(config)
    twitter = extract_twitter_config(config)
    faceplusplus = extract_faceplusplus_config(config)

    return dict(
        server=server,
        database=db,
        twitter=twitter,
        faceplusplus=faceplusplus
    )


def extract_db_config(config):
    conf = dict(config.items('database'))
    conf['port'] = config.getint('database', 'port')
    return conf


def extract_twitter_config(config):
    conf = dict(config.items('twitter'))
    return conf


def extract_faceplusplus_config(config):
    conf = dict(config.items('faceplusplus'))
    return conf


def extract_server_config(config):
    # Allow easy extension of config extraction for specific servers.
    # server_specific_func_name = 'extract_{}_server'.format(config.get('server', 'server').lower())
    # specific_conf = getattr(sys.modules[__name__], server_specific_func_name, lambda x: dict())(config)

    # Fetch ALL configuration for the server
    conf = dict(config.items('server'))
    # Be more specific for others (otherwise datatype does not match)
    # conf['reloader'] = config.getboolean('server', 'reloader')
    conf['debug'] = config.getboolean('server', 'debug')
    conf['port'] = config.getint('server', 'port')

    # conf.update(specific_conf)
    return conf


def extract_geventsocketio_server(config):
    from gevent import monkey
    monkey.patch_all()
    return dict(resource='socket.io')


def export_db_config(config_files):
    '''Export the database config to the current environment.
    Found this helpful to communicate with bash, while still keeping a single configuration file.
    '''
    conf = read_server_config(config_files)
    db = conf['db']
    print 'export MYSQL_USERNAME={} MYSQL_PASSWORD={} AUTH_DB={} MYSQL_PORT={}'.format(db['user'], db['password'],
                                                                                       db['auth'], db['port'])
    return None


if __name__ == '__main__':
    config_files = sys.argv[1:]
    export_db_config(config_files)
