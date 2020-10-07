# backend

The MetaDB API server

## Developement quickstart

```bash
pip3 install --user -r requirements.txt
uvicorn themetadb.backend.main:app --reload --port=8080
```

Then go to [http://127.0.0.1:8080/docs](http://127.0.0.1:8080/docs)

### Check code before commiting

```bash
flake8 .
mypy .
```
