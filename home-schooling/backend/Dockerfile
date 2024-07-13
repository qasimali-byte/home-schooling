FROM python:3.11-slim
USER root

# Set the working directory in the container
ARG FUNCTION_DIR=/app
WORKDIR ${FUNCTION_DIR}

# Install the required dependencies using caching
COPY requirements.txt ${FUNCTION_DIR}
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn

ARG mysqlhost
ARG mysqldatabasename
ARG mysqluser
ARG mysqlpassword
ARG mysqlcharset
ARG mysqlport
ARG client_key
ARG aws_access_key
ARG aws_secret_key
ARG aws_end_point
ARG aws_bucket_name
ARG sentry_dsn_key
ARG sentry_prod_enabled

ENV host=$mysqlhost
ENV databasename=$mysqldatabasename
ENV user=$mysqluser
ENV password=$mysqlpassword
ENV charset=$mysqlcharset
ENV port=$mysqlport
ENV client_secret=$client_key
ENV ACCESS_KEY=$aws_access_key
ENV SECRET_KEY=$aws_secret_key
ENV END_POINT=$aws_end_point
ENV BUCKET_NAME=$aws_bucket_name
ENV dsn=$sentry_dsn_key
ENV sentry_enabled=$sentry_prod_enabled


# Copy the Lambda function code into the container
WORKDIR ${FUNCTION_DIR}
COPY /*.py ${FUNCTION_DIR}
COPY Database ${FUNCTION_DIR}/Database
COPY Email_Templates ${FUNCTION_DIR}/Email_Templates
COPY arial.ttf ${FUNCTION_DIR}
#Set a default value, you can override it during the Docker build
EXPOSE 5000

CMD ["gunicorn", "--workers", "3", "--bind", "0.0.0.0:5000", "--timeout", "600", "run:app"]
