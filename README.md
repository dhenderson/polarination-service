# Environment variables

```bash
NEWSAPI_KEY=
```

# Lambda

Install requests dependency

```bash
$ pip install -t . requests
```

Create the zip file:

```bash
$ zip -r lambda.zip . -x "env" "requirements.txt" ".vscode"
```
