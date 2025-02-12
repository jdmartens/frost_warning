Here’s a **README.md** for your AWS Lambda function that sends **SES email notifications** when freezing weather is forecasted.  

---

### **README.md**
```markdown
# Freezing Weather Alert AWS Lambda

## Overview
This AWS Lambda function monitors weather forecasts using the OpenWeather API. If freezing temperatures (32°F or below) are expected within the next 8 hours, it sends an email notification via **Amazon SES**. The function also supports a configurable buffer to send warnings **before** freezing conditions occur.

## Features
- Fetches weather forecast data for a given location
- Detects temperatures at or below **32°F + buffer** in the next **8 hours**
- Sends an **email alert via AWS SES**
- Configurable buffer to trigger warnings at a higher temperature (e.g., alert at 34°F)
- Runs serverless with AWS Lambda

## Prerequisites
Before deploying this function, ensure you have:
- An **AWS account**
- An **OpenWeather API key**
- A **verified sender email in Amazon SES**
- The necessary **IAM permissions** for AWS Lambda to send emails via SES

## Environment Variables
Set the following environment variables in AWS Lambda:

| Variable             | Description |
|----------------------|-------------|
| `OPENWEATHER_API_KEY` | OpenWeather API key for retrieving weather data |
| `LAT` | Latitude of the location to monitor |
| `LON` | Longitude of the location to monitor |
| `SES_SENDER_EMAIL` | **Verified** sender email in Amazon SES |
| `SES_RECIPIENT_EMAIL` | Email address to receive alerts |
| `BUFFER_TEMP` | (Optional) Buffer above freezing (default: `0`). If set to `2`, alerts trigger at `34°F`. |

## Setup Instructions

### 1. Create the Lambda Function
1. Navigate to AWS Lambda in the AWS Console.
2. Create a new function using **Python 3.x**.
3. Copy and paste the Lambda function code into the editor.

### 2. Configure Environment Variables
Set the environment variables as listed above.

### 3. Configure a Lambda Layer for Requests Package
1. Package the `requests` library as a ZIP file.
2. Upload it as a Lambda layer.
3. Attach the layer to the Lambda function.

### 4. Configure IAM Permissions
The Lambda function needs permission to send emails via **Amazon SES**. Attach a policy with the following permissions:
```json
{
    "Effect": "Allow",
    "Action": "ses:SendEmail",
    "Resource": "*"
}
```

### 5. Deploy the Lambda Function
1. Save the function in AWS Lambda.
2. Set up a **CloudWatch Event Rule** to trigger the function periodically (e.g., every hour).

## How It Works
1. The Lambda function retrieves the **8-hour** weather forecast from OpenWeather.
2. It checks if any temperature is **at or below 32°F + buffer**.
3. If freezing conditions are expected, it **sends an email alert via AWS SES**.
4. If no freezing weather is detected, the function exits without sending an email.

## Example Email Alert
```
Subject: Frost/Freezing Weather Alert
Message: Warning: Freezing temperature (30°F) forecasted at 2025-02-10 02:00 UTC.
Buffer applied: 2°F.
```

## Future Enhancements
- Support additional notification methods (e.g., AWS SNS if costs allow)
- Allow multiple locations to be monitored in a single function
- Improve logging and error handling

## License
This project is licensed under the MIT License.
```

