FROM python:3.10.9
ENV PYTHONUNBUFFERED=1

WORKDIR /code
COPY requirements.txt /code/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /code/
ENV PYTHONPATH=/code/app


CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]