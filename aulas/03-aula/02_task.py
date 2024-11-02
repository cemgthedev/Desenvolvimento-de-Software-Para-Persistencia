import configparser as cp;

config = cp.ConfigParser();

config.read('config.ini');

database = config['DEFAULT'].get('database');
user = config['DEFAULT'].get('user');
password = config['DEFAULT'].get('password');

print(database, user, password);