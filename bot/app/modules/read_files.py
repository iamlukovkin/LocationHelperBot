def read_settings():
    import json
    print('Loading settings...')
    with open('settings.json', 'r') as f:
        settings = json.load(f)
    print('Settings loaded!')
    return settings