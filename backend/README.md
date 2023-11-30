# Pandemic - Reign of Cthulhu
The codebase here includes the backend server of the game

## Technology Stack
- Python v3.12.0
- [Poetry](https://github.com/python-poetry/poetry) v1.6.1 for package management
- [Socket.io](https://socket.io/) for real-time communication among clients and server
- [Ruff](https://github.com/astral-sh/ruff) for linting
- [Black](https://github.com/psf/black) for code formatting

Check out all other dependencies required by running the command below :
```bash
poetry run pip list
```


## Setup
### Install dependencies
```bash
poetry  update
```

### Build project
```bash
poetry  build
poetry  install
```

### Run
```bash
poetry run webapp-dev
```

Once the server started, you can send HTTP request to the server.

For example:
```bash
curl  --request POST --http2 \
      --header "Accept: application/json" \
      --header "Content-Type: application/json" \
      --data "{\"players\":[{\"id\":\"8du0ey\", \"nickname\":\"Frog\"}]}" \
      -v  "http://localhost:8081/games"
```

### Test
The command below includes unit test and e2e test
```bash
poetry run pytest -v ./tests
```

### Linter
```bash
poetry run ruff check ./app/
```

### Formatter
```bash
poetry run black  ./app/
```
