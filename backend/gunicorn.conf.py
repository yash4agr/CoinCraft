# Gunicorn configuration for CoinCraft Backend
bind = "127.0.0.1:8000"
workers = 4
worker_class = "uvicorn.workers.UvicornWorker"
worker_connections = 1000
max_requests = 1000
max_requests_jitter = 100
timeout = 30
keepalive = 5

# Logging
accesslog = "/var/log/coincraft/access.log"
errorlog = "/var/log/coincraft/error.log"
loglevel = "info"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'

# Process naming
proc_name = "coincraft-api"

# Security
limit_request_line = 4096
limit_request_fields = 100
limit_request_field_size = 8190
