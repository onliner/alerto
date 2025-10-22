worker_class = "aiohttp.GunicornWebWorker"
bind = "0.0.0.0:8080"

workers = 1
threads = 1

accesslog = "-"
errorlog = "-"

keepalive = 5
graceful_timeout = 30
timeout = 60

worker_tmp_dir = "/dev/shm"
