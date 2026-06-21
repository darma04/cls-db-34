# -*- encoding: utf-8 -*-
# Gunicorn production configuration for Central-License-Server-Isolated-Database-36

bind = '127.0.0.1:8009'
workers = 3
worker_class = 'sync'
timeout = 120
accesslog = '/var/log/gunicorn/Central-License-Server-Isolated-Database-36/access.log'
errorlog = '/var/log/gunicorn/Central-License-Server-Isolated-Database-36/error.log'
loglevel = 'info'
capture_output = True
enable_stdio_inheritance = True
