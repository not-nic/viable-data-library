FROM python:latest

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

COPY init.sh /app/init.sh

RUN chmod +x /app/init.sh

ENTRYPOINT ["/app/init.sh"]
