FROM python:3.10
EXPOSE 8000
RUN uvicorn run main:app --host 0.0.0.0 --port 8000 --reload