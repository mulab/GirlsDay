FROM python:3.5.1-onbuild

ENV DEBUG=False

EXPOSE 80

CMD python manage.py runserver 0.0.0.0:80
