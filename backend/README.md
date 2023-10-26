### Settings
#### Install dependencies
```bash
poetry  update
```

#### Build project
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
```bash
poetry run pytest -v ./tests/e2e/test_game.py
```

### Linter
```bash
poetry run ruff check ./app/
```

### Formatter
```bash
poetry run black  ./app/
```

