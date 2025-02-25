import argparse
import sys
from server import serve

def init_cli():
    parser = argparse.ArgumentParser(description='A simple proxy server cli tool')
    parser.add_argument(
        '-p', '--port',
        type=int,
        default=8000,
        help='Port to listen on (default: 8000)'
    )
    parser.add_argument(
        '-o', '--origin',
        type=str,
        required=True,
        help='Origin server to forward requests to (e.g. http://api.example.com)'
    )
    
    args = parser.parse_args()
    
    # Validate origin URL format
    if not args.origin.startswith(('http://', 'https://')):
        parser.error('Origin must start with http:// or https://')
    
    try:
        serve(args.port, args.origin)
    except Exception as e:
        print(f"Error starting server: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    init_cli()
