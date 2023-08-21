_CONFIG = {
    'local': {
        'http_protocol': 'http',
        'ws_protocol': 'ws',
        'host': 'localhost:8080',
    },
    'remote': {
        'http_protocol': 'https',
        'ws_protocol': 'wss',
        'host': 'urt.swit.fun',
    }
}

def _get_config(is_local: bool):
    return _CONFIG['local' if is_local else 'remote']

def http_base_url(is_local: bool):
    return _get_config(is_local)['http_protocol'] + '://' + _get_config(is_local)['host']

def ws_base_url(is_local: bool):
    return _get_config(is_local)['ws_protocol'] + '://' + _get_config(is_local)['host']

