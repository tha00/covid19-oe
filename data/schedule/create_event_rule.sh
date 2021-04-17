#!/usr/bin/env bash

RULE_NAME="daily-rule"

# Daily schedule
aws events put-rule \
  --name $RULE_NAME \
  --schedule-expression "rate(1 day)"

# Perssion attached to the lambda function, so that event rule can invoke it
aws lambda add-permission \
  --function-name "$FUNCTION_NAME" \
  --statement-id "daily-event" \
  --action "lambda:InvokeFunction" \
  --principal events.amazonaws.com \
  --source-arn arn:aws:events:"$REGION":"$ACCOUNT_ID":rule/$RULE_NAME

# Add lambda function as event target
aws events put-targets \
  --rule $RULE_NAME \
  --targets "Id"="1","Arn"="arn:aws:lambda:${REGION}:${ACCOUNT_ID}:function:${FUNCTION_NAME}"
