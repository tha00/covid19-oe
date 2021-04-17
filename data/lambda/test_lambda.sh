aws lambda invoke \
  --function-name "$FUNCTION_NAME" \
  out --log-type Tail --query 'LogResult' --output text |  base64 -d
