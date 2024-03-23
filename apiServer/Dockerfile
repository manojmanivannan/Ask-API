FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

WORKDIR /app
COPY ./apiServer/main.py /app/main.py
COPY ./docs/mock_crime_records.csv /app/mock_crime_records.csv

RUN pip install pandas
