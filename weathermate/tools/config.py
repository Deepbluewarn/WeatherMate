import json

def getUserConfig():
    # Load the user configuration file
    USER_CONFIG_FILE = 'config.json'
    user_config = {}
    try:
        with open(USER_CONFIG_FILE, 'r') as file:
            user_config = json.load(file)
    except FileNotFoundError:
        print(f'User config file not found: {USER_CONFIG_FILE}')
    except json.JSONDecodeError:
        print(f'Error parsing user config file: {USER_CONFIG_FILE}')
    return user_config