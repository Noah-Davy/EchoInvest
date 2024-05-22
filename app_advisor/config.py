import os

DJANGO_ENV = os.getenv('DJANGO_ENV', 'development')

if DJANGO_ENV == 'production':
    import redis
    from rq import Queue
    redis_url = os.getenv('REDIS_URL', 'redis://localhost:6379')
    conn = redis.from_url(redis_url)
    q = Queue(connection=conn)
else:
    q = None