# aws-apigateway-oauth-with-cognito
Demo SAM template that launches an ApiGateway REST API protected by OAuth using Cognito User Pools

## Build + Deploy

### Build

```
sam build --use-container
```

### Deploy

We are using the `us-east-1` region because Cognito automatically creates a CloudFront distribution for the `UserPoolDomain` resource and CloudFront distributions can only use ACM certificates that are in the us-east-1 region.

If you would like to deploy this stack in another region then you will need to move the `AuthDomainCertificate` resource into a separate CloudFormation template, and deploy that CloudFormation stack (which only contains the ACM certificate) in the us-east-1 region first before deploying the main stack in your region of choice.

```
sam deploy \
  --stack-name apigw-cognito-oauth-example \
  --parameter-overrides \
    ParameterKey=Environment,ParameterValue=dev \
  #   ParameterKey=DomainName,ParameterValue=www.example.com \
  #   ParameterKey=HostedZoneId,ParameterValue=Z12345678AB9C0D12EFGH \
  #   ParameterKey=UserPoolUserEmail,ParameterValue=test@gmail.com \
  --s3-bucket <s3_bucket_name> \ # or use --resolve-s3 \ to use sam cli managed s3 bucket
  --s3-prefix cloudformation/apigw-cognito-oauth-example \
  --capabilities CAPABILITY_NAMED_IAM CAPABILITY_AUTO_EXPAND \
  --no-fail-on-empty-changeset \
  --region us-east-1 \
  --profile <profile_name>
```
