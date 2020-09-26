# iPadAir4_lambda
The iPad Air 4 is currenlty 'Avialable in October' on the [apple website](https://www.apple.com/ie/ipad-air/).  
This is an AWS lambda function that checks the apple website for iPad Air 4 availability changes.

# System Overview
* A scheduled trigger kicks off the lambda function every 2 hours.  
* The lamdba function scrapes the [apple ipad web page](https://www.apple.com/ie/ipad-air/).   
* If the availability staus has changed, it sends an email to the recepient email address in the [lambda_function.py](./lambda_function.py) file.  
  
![System Diagram](system__diagram.png)

# Configuration

  ### Personalize the python file:
  Edit the python file [lambda_function.py](./lambda_function.py) with your personal info.    
  **Note** : You need an Amazon SES veriefied email addreess in order to send emails. Learn more [here](https://docs.aws.amazon.com/ses/latest/DeveloperGuide/verify-email-addresses.html).
  
  ### The Lambda function: 
  Create a new lambda function at [https://aws.amazon.com/lambda/](https://aws.amazon.com/lambda/)  
  Upload the python file -> [lambda_function.py](./lambda_function.py)  
  Note: runtime is currently Python 3.7  
  
  ### Layers: 
  These are the python dependency packages (mentioned in the [requirements.txt](./requirements.txt) file)    
  The dependencies are downloaded and placed in the following directory structure `python/lib/python3.7/site-packages/` and uploaded as a zip file.   
  The zip file is available as [lambda_layer.zip](./lambda_layer.zip) on the repo.  
  Create a new layer and upload the [lambda_layer.zip](./lambda_layer.zip) file.  
  
  ### EventBridge event
  A cron job is used to kick off the lambda function every two hours.  
  Cron expression used is: cron(0 */2 * * ? *)  
  
  ##### Disclaimer:
  - Please observe best practices while scraping a web site (use a reasonable limit per hour to avoid getting blocked)
  - Use the [AWS Secrets manager](https://aws.amazon.com/secrets-manager/) instead of hard-coding your keys in the source code.
  - This project is created for educational purposed only. 
  - Lets hope iPad pre-orders open next week! 

