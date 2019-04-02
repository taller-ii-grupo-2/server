FROM python:3.6.8
ADD . /code
WORKDIR /code
RUN pip install -r requirements.txt
CMD ["python", "src/hypechat/app.py"]
