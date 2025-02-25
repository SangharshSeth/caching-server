import functools
import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, ParseResult

import requests

CACHE_MEMORY = dict()


def proxy_request(origin: str, parsed_url: ParseResult):
    params = parsed_url.path.split('/')
    path_params = ''
    if len(params) > 0:
        for param in params:
            if param != '':
                path_params += f"/{param}"

    print(path_params)

    target_url = f'{origin}{path_params}'
    if path_params not in CACHE_MEMORY:
        print("Cache Miss")
        response = requests.get(target_url)
        print(response.headers.get('Content-Type'))
        if response.status_code != 200:
            print(f'Request to {target_url} failed with status code {response.status_code}')
        data = response.json()
        entry = {
            'data': data,
            'content_type': response.headers['Content-Type'],
        }
        CACHE_MEMORY[path_params] = entry
        return False, entry
    else:
        print("Cache Hit")
        return True, CACHE_MEMORY[path_params]


class BaseHandler(BaseHTTPRequestHandler):

    def __init__(self, origin, *args, **kwargs):
        self.origin = origin
        super().__init__(*args, **kwargs)

    def do_GET(self):
        print('Request received {}'.format(self))
        parsed_url = urlparse(self.path)

        cache_hit, response = proxy_request(self.origin, parsed_url)
        if cache_hit:
            self.headers['X-Cache-Hit'] = 'true'
            self.headers['X-Cache'] = 'HIT'
        else:
            self.headers['X-Cache-Hit'] = 'false'
            self.headers['X-Cache'] = 'MISS'

        print('Response received {}'.format(response))
        json_response = json.dumps(response.get('data'))
        self.send_response(200)
        self.send_header('Content-type', response['content_type'])
        self.end_headers()
        self.wfile.write(bytes(json_response, 'utf-8'))


def serve(port: int, origin: str):
    handler = functools.partial(BaseHandler, origin)
    server = HTTPServer(('localhost', port), handler)
    print('Starting proxy server on port {}'.format(port))
    server.serve_forever()
    server.server_close()
