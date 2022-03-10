FROM python:3.10.2-alpine3.15

WORKDIR /web

COPY requirements.txt requirements.txt
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "run.py"]