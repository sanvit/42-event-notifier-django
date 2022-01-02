FROM python:3.9
ENV PYTHONUNBUFFERED=1
RUN mkdir /app
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
RUN python manage.py collectstatic --noinput
RUN chmod +x docker-entrypoint.sh
EXPOSE 8000
CMD ["/app/docker-entrypoint.sh"]