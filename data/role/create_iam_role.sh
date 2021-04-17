#!/usr/bin/env bash

BASE_DIR=$(dirname "$0")

# Create lambda-s3 role
aws iam create-role \
  --role-name "$ROLE_NAME" \
  --assume-role-policy-document file://"$BASE_DIR"/trust-policy.json

# Attach lambda execution policy
aws iam attach-role-policy \
  --role-name "$ROLE_NAME" \
  --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole

# Attach s3 access policy
aws iam attach-role-policy \
  --role-name "$ROLE_NAME" \
  --policy-arn arn:aws:iam::aws:policy/AmazonS3FullAccess