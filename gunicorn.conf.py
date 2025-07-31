# Gunicorn configuration for Koyeb deployment
import os

# Server socket
bind = f"0.0.0.0:{os.environ.get('PORT', 8080)}"
backlog = 2048

# Worker processes
workers = 1  # Single worker to avoid model loading multiple times
worker_class = "sync"
worker_connections = 1000
timeout = 120  # Longer timeout for ML inference
keepalive = 2

# Restart workers after this many requests, to control memory usage
max_requests = 1000
max_requests_jitter = 100

# Preload application for better performance
preload_app = True

# Logging
accesslog = "-"  # Log to stdout
errorlog = "-"   # Log to stderr
loglevel = "info"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s'

# Process naming
proc_name = "cookware-analyzer"

# Security
limit_request_line = 4094
limit_request_fields = 100
limit_request_field_size = 8190
