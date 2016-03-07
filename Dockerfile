FROM python:3.5.1-onbuild

ENV DEBUG=False

EXPOSE 80

CMD ["/usr/local/bin/uwsgi", "--ini", "uwsgi.ini"]
