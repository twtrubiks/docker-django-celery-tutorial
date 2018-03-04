from celery import Celery

app = Celery('demo', broker='amqp://celery:password123@rabbitmq:5672/my_vhost')
app.config_from_object('celery_app.celery_config')
