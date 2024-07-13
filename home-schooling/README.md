# Home-Schooling

## About This Project
Web application designed to facilitate home education by enabling parents to keep track of their children's progress. This project utilizes React for the frontend and Vite as the build tool to ensure a fast and efficient development experience.

### Language

- **Python**: The primary programming language used for this project.

## Infrastructure

Our project relies on REST APIs for efficient data interaction and analytical data extraction.

## Security Notice

**Important**: Never store API keys, credentials, or any secrets in your code. Instead, use environment variables.

## Configuration

Configure your environment variables in a file named `.env`. This file should never be committed to your repository for security reasons.

Example `.env` file:

```plaintext
host="DEMO_HOST"
databasename="DEMO_DATABASE"
user="DEMO_DB_USER"
password="DEMO_PASSWORD"
charset="DEMO_CHARSET"
port="DEMO_POST"
client_secret="DEMO_CLIENT_SECRET"
ACCESS_KEY="DEMO_AWS_ACCESS_KEY"
SECRET_KEY="DEMO_AWS_SECRET_KEY"
END_POINT="DEMO_AWS_ENDPOINT"
BUCKET_NAME="DEMO_AWS_BUCKETNAME"
```

## Docker File

docker build --build-arg mysqlhost=host --build-arg mysqldatabasename=mydatabase --build-arg mysqluser=myuser --build-arg mysqlpassword=mypassword --build-arg mysqlcharset=utf8 --build-arg mysqlport=myport --build-arg client_key=myclientkey --build-arg aws_access_key=myawsaccesskey --build-arg aws_secret_key=myawssecretkey --build-arg aws_end_point=myawsendpoint --build-arg aws_bucket_name=myawsbucketname .

docker run dev
