# Start server

```
gunicorn -w 5 -t 90 -b 0.0.0.0:8000 server_config.wsgi:application & daphne -b 0.0.0.0 -p 8001 server_config.asgi:application
```

- **gunicorn**: Handle HTTP Request
- **daphne**: Handle asgi requests: Web Socket
