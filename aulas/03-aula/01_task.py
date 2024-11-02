import configparser as cp;

config = cp.ConfigParser();

config['DEFAULT'] = {
    'database': 'localhost',
    'user': 'root',
    'password': 'admin'
}

with open('config.ini', 'w') as configfile:
    config.write(configfile);