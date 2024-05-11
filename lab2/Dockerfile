FROM python:3.12
WORKDIR /app

COPY ./app/requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

COPY ./app /app

ENTRYPOINT ["bash", "-c", "cd ./init && python3 upload_script.py && cd ../rest-api && uvicorn main:app --port 5005 --host 0.0.0.0"]