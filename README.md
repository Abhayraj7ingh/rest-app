# Image Upload Service (LocalStack Setup)

This project runs locally using **S3** and **DynamoDB** via **LocalStack**.

Follow the steps below to set up your local development environment.

---

## ✔️ How to Use (LocalStack)

### 1️ Start LocalStack

```bash
docker run -d -p 4566:4566 localstack/localstack


### 2 Create S3 Bucket

```Cli
aws --endpoint-url=http://localhost:4566 s3 mb s3://images-bucket
aws --endpoint-url=http://localhost:4566 s3 ls


### 3 Create DynamoDB Table

```Cli
aws --endpoint-url=http://localhost:4566 dynamodb create-table \
--table-name images-table \
--attribute-definitions \
    AttributeName=user_id,AttributeType=S \
    AttributeName=image_id,AttributeType=S \
--key-schema \
    AttributeName=user_id,KeyType=HASH \
    AttributeName=image_id,KeyType=RANGE \
--billing-mode PAY_PER_REQUEST

aws --endpoint-url=http://localhost:4566 dynamodb list-tables
