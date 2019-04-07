FROM python:3.6.8
ADD . /code
WORKDIR /code
EXPOSE 5000
COPY . .
RUN pip install -r requirements.txt
RUN chmod +x manage.py
ARG APP_SETTINGS=config.ProductionConfig
ENV FLASK_ENV=production
ENV FLASK_APP=app
RUN bash db_setup.sh
CMD ["bash", "scripts/wsgi.sh"]
