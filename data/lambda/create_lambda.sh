#!/usr/bin/env bash

DIR=$(dirname "$0")

aws lambda create-function \
  --function-name "$FUNCTION_NAME" \
  --zip-file fileb://"$DIR"/../build/lambda_function.zip \
  --handler lambda_function.lambda_handler \
  --runtime python3.7 \
  --role arn:aws:iam::"$ACCOUNT_ID":role/"$ROLE_NAME" \
  --timeout 900 \
  --environment "Variables={BUCKET_NAME=$BUCKET_NAME, FILE_NAME=${FILE_NAME}, DATA_URL=${DATA_URL}}"
