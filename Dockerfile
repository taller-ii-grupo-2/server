FROM python:3.7.2
ADD . /code
WORKDIR /code
RUN pip install -r requirements.txt
CMD ["python", "src/hypechat/main.py"]