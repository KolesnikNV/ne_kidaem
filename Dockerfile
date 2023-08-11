FROM python:3.9

WORKDIR /app

COPY requirements.txt ./
RUN pip3 install -r requirements.txt --no-cache-dir

COPY ne_kidaem/ ./
COPY docker-entrypoint.sh .
RUN chmod +x docker-entrypoint.sh

ENTRYPOINT ["./docker-entrypoint.sh"]
CMD ["gunicorn", "--bind", "ne_kidaem.wsgi:application", "backend.wsgi"] 
