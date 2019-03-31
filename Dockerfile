FROM python:3.7.2
ADD . /code
WORKDIR /code
EXPOSE 5000
COPY . .
RUN pip install -r requirements.txt
RUN chmod +x src/hypechat/manage.py
ARG APP_SETTINGS=config.ProductionConfig

# Make Entrypoint executable
RUN chmod +x docker-entrypoint.sh

# Run the app when the container launches
CMD ["/bin/bash", "/code/docker-entrypoint.sh"]