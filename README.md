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

## Using Postman to make a request to your API

In Postman:

1. Create a new request
2. Switch to the "Authorization" tab
3. For "Type", select "OAuth 2.0" from the dropdown
4. Then in the "Configuration Options" tab, set the following settings:
   - **Grant Type**: Authorization Code
   - **Callback URL**: `https://oauth.pstmn.io/v1/callback` (this should be the default)
     - check the box "Authorize using browser"
   - **Auth URL**: `https://auth.{DomainName}/oauth2/authorize`
     - refer to https://docs.aws.amazon.com/cognito/latest/developerguide/authorization-endpoint.html
   - **Access Token URL**: `https://auth.{DomainName}/oauth2/token`
     - refer to https://docs.aws.amazon.com/cognito/latest/developerguide/token-endpoint.html
   - **Client ID**: retrieve your Client ID from the Amazon Cognito web console -> User pools -> select your user pool -> App integration tab -> Scroll down to the App client list -> select your app client -> copy the Client ID from the "App client information" section
   - **Client Secret**: retrieve your Client Secret from the same place you retrieved the Client ID
   - **Scope**: the same scope you set in [template.yaml](./template.yaml) e.g. `resource_name/action_name`
   - **State**: leave blank
   - **Client Authentication**: Send as Basic Auth Header
   
   Then click "Get New Access Token"

In the browser:

1. Use the username specified in [template.yaml](./template.yaml) (default is `firstname.lastname`)
2. Use the password that was automatically emailed to the email that you specified for the `UserPoolUserEmail` parameter
3. After you sign in then Cognito will ask you to set a new password

---

# Learning about OAuth2

OAuth2 is confusing 🫠

Here are the articles that helped me get a clear grasp of all the pieces and technical details:

- [An Illustrated Guide to OAuth and OpenID Connect | Okta Developer](https://developer.okta.com/blog/2019/10/21/illustrated-guide-to-oauth-and-oidc)
- [What the Heck is OAuth? | Okta Developer](https://developer.okta.com/blog/2017/06/21/what-the-heck-is-oauth)
- [Auth0 Blog | OAuth ID Token and Access Token: What Is the Difference?](https://auth0.com/blog/id-token-access-token-what-is-the-difference/)
- [Understanding Amazon Cognito user pool OAuth 2.0 grants | Front-End Web & Mobile](https://aws.amazon.com/blogs/mobile/understanding-amazon-cognito-user-pool-oauth-2-0-grants/)
- [Part 1: Securing AWS API Gateway using AWS Cognito OAuth2 Scopes | by Cloud Guru | Medium](https://awskarthik82.medium.com/part-1-securing-aws-api-gateway-using-aws-cognito-oauth2-scopes-410e7fb4a4c0)
- [Implement the OAuth 2.0 Authorization Code with PKCE Flow | Okta Developer](https://developer.okta.com/blog/2019/08/22/okta-authjs-pkce)
- [How to secure the Cognito login flow with a state nonce and PKCE - Advanced Web Machinery](https://advancedweb.hu/how-to-secure-the-cognito-login-flow-with-a-state-nonce-and-pkce/)
- [Auth0 Blog | Identity, Unlocked...Explained | Episode 1](https://auth0.com/blog/identity-unlocked-explained-episode-1/)
- [Amazon Premium Support | Decode and verify the signature of a Cognito JSON Web Token](https://aws.amazon.com/premiumsupport/knowledge-center/decode-verify-cognito-json-token/)
- [How to add Cognito login to a website - Advanced Web Machinery](https://advancedweb.hu/how-to-add-cognito-login-to-a-website/)
