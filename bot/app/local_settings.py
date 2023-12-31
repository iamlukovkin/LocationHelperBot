from .modules.read_files import read_settings


settings = read_settings()
credentials = settings['credentials']
scope = settings['scope']
methods_folder = settings['methods_folder']
PD_folder = settings['PD_folder']
users_folder_id = settings['users_folder_id']

API_TOKEN = settings['API_TOKEN']
SQL_ALCHEMY_URL = settings['SQL_ALCHEMY_URL']
