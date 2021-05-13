# COVID-19 in Austria

## Data

The data is obtained from [Open Data Austria](https://www.data.gv.at/katalog/dataset/4b71eb3d-7d55-4967-b80d-91a3f220b60c) 
as a .csv file. An [AWS Lambda function](https://aws.amazon.com/lambda/) that downloads the file to an [S3 bucket](https://aws.amazon.com/de/s3/)
along with scripts to deploy it using the [AWS CLI](https://aws.amazon.com/cli/) are provided. After having set the
required environment variables

- `REGION`: AWS region the Lambda function should be created in
- `BUCKET_NAME`: target bucket name where the function will place the file
- `FILE_KEY`: key (path) under which the function will place the downloaded file
- `DATA_URL`: URL of the file to download
- `ACCOUNT_ID`: AWS account number (needed to construct ARNs)
- `ROLE_NAME`: name of the role to be created for and used by the Lambda function
- `FUNCTION_NAME`: name of the Lambda function that will be created

under `./data`, run

- `role/create_iam_role.sh` to create the role that will give S3 access to the Lambda function
- `lambda/make_package.sh` to create a .zip file containing the lambda Python code and its dependencies
- `lambda/create_lambda.sh` to deploy the Lambda function on AWS and  `lambda/test_lambda.sh` to test it
- `schedule/create_event_rule.sh` to create a daily trigger event and attach the Lambda function as a target

## Streamlit app

Under `./streamlit`, there is a Streamlit application loading and presenting the data. A small setup
script to host the app on [AWS EC2](https://aws.amazon.com/ec2/) is also included.

<p align="center"><img src="/streamlit/screenshot.png" alt="screenshot" width="700"></p> 

## Resources

- [COVID-19 Austrian district data over time](https://www.data.gv.at/katalog/dataset/4b71eb3d-7d55-4967-b80d-91a3f220b60c)
- [Create and Deploy an AWS Lambda Function with the AWS CLI](https://medium.com/swlh/create-and-deploy-an-aws-lambda-function-for-data-collection-with-the-aws-cli-ad718ec61f8a)
- [How to deploy a stremlit app using Amazon free EC2](https://towardsdatascience.com/how-to-deploy-a-streamlit-app-using-an-amazon-free-ec2-instance-416a41f69dc3)