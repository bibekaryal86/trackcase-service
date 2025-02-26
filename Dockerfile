FROM python:3.13.2-alpine
WORKDIR /code
COPY ./src /code/src
COPY .env /code
COPY pyproject.toml /code
RUN pip install --no-cache-dir --upgrade .
# instead of `.` use -r requirements.txt if using such
ENV APP_PORT=8080
# CMD ["uvicorn", "src.trackcase_service.main:app", "--host", "0.0.0.0", "--port", "80"]
ENTRYPOINT ["python", "src/trackcase_service/main.py"]
# build as : docker build -t trackcase-service .
# run as : docker run --name trackcase-service -e -p 8080:8080 -d trackcase-service
