# Proxy Server CLI Tool

## Project URL
<https://roadmap.sh/projects/caching-server>

## Installation

Clone the repository and navigate to the project directory:

```sh
git clone https://github.com/SangharshSeth/caching-server
cd caching-server
```

## Usage

Run the CLI tool using:

```sh
python main.py -p <port> -o <origin-url>
```

### Options:

| Flag             | Description                                     |
| ---------------- | ----------------------------------------------- |
| `-p`, `--port`   | Port to listen on (default: 8000)               |
| `-o`, `--origin` | Origin server to forward requests to (Required) |

### Example:

```sh
python main.py -p 8080 -o http://example.com
```

This starts a proxy server on port `8080` that forwards all requests to [`http://example.com`](http://example.com).

## Error Handling

- If an invalid origin URL is provided (not starting with `http://` or `https://`), an error is displayed.
- If the server fails to start, an error message is printed to `stderr`.
