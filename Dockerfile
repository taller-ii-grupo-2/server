FROM python:3.6.8
ADD . /code
WORKDIR /code
RUN pip install -r requirements.txt
ENV FLASK_ENV=development
CMD ["/bin/bash", "docker-entry-point.sh"]
