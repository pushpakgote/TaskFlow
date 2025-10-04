# TaskFlow
TaskFlow| Project Tracking App

# Redis Server
Start Redis Server command: redis-server  (if it gives error, then first try stop redis server command: redis-cli shutdown)
Stop Redis Server command: redis-cli shutdown 

# Celery (For async tasks)
Command : celery -A taskflow worker -l info --pool=solo

# Celery Beat (For scheduled tasks)
Command : celery -A taskflow beat --loglevel=info