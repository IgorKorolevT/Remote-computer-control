FROM python:3.13

EXPOSE 8000
WORKDIR /app
COPY requirements.txt /app
RUN pip install -r requirements.txt --no-cache-dir
COPY . /app
RUN python manage.py collectstatic
#CMD ["manage.py", "runserver", "0.0.0.0:8000"]
#CMD ["sh", "-c", "python manage.py migrate && daphne -b 0.0.0.0 -p 8000 Django_course_project.asgi:application"]
CMD ["sh", "-c", "python manage.py migrate && daphne -b 0.0.0.0 -p 8000 Django_course_project.asgi:application"]
