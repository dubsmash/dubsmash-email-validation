<p align="center">
  <img src="https://d2nr8mwohhwyyc.cloudfront.net/static/images/logo.png"/>
</p>


# Dubsmash Email Validation Sample service
This is a small sample service that can be used to verify email addresses by deploying a small [Zappa](https://github.com/Miserlou/Zappa) application to [AWS Lambda](https://aws.amazon.com/lambda).

# How to use this project
1. Install requirements: `pip install -r requirements.txt`
2. Copy `zappa_settings.json.dist` to `zappa_settings.json`
3. Put in your S3 bucket name and make sure to have the `aws-cli` configured properly. For more information on how to configure Zappa please check [the documentation](https://github.com/Miserlou/Zappa#advanced-settings). If you should have problems authenticating with AWS [this should help you](http://docs.aws.amazon.com/cli/latest/userguide/cli-config-files.html).
4. Run `zappa deploy staging` to deploy the application to AWS.
5. Use the endpoint of the created API gateway that Zappa provided to access your service! 🎉

# How it works
In order to verify that email addresses really exist one must make sure that the SMTP server run by the targets provider would accept a mail being sent to the address under test (so-called email-pinging). In order to do so the MX records of the target host are retrieved first, afterwards a SMTP connection is opened up. After sending the initial `HELO` command to the remote SMTP server a "fake" mail being sent is started. Once the `RECPT` header is sent the remote server is returning an error code if the given email doesn't exist.

_Please note: This very simple service should just serve as a small demonstration of how to use serverless frameworks & provide basic insights into email-pinging. The implementation is not to be considered complete and especially the constant reinitialization of the SMTP client being used is taking up a lot of time._

_There are many ways to improve this. If you know them we probably would love to work with you: [Jobs @ Dubsmash](https://dubsmash.com/jobs)_
