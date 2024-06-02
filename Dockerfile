FROM python:3.12-slim

WORKDIR /code

COPY ./requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . ./

ENV FLASK_APP=app.py
EXPOSE 5005

CMD ["flask", "run", "--debug", "--host", "0.0.0.0", "--port", "5005"]