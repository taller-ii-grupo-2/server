FROM python:3.6.8
ADD . /code
WORKDIR /code
RUN pip install -r requirements.txt
ENV FLASK_ENV=development
ENV FLASK_APP=app
CMD ["bash", "db_setup.sh"]
CMD ["bash", "scripts/wsgi.sh"]
