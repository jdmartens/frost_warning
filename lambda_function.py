import os
import json
import requests
import boto3
from datetime import datetime, timedelta

# AWS clients
ses_client = boto3.client('ses')
sns_client = boto3.client('sns')

# Environment variables
OPENWEATHER_API_KEY = os.environ['OPENWEATHER_API_KEY']
LAT = os.getenv('LAT', "44.42085921856718")  # Default to central Wisconsin
LON = os.getenv('LON', "-89.8140888229648")  # Default to central Wisconsin
SES_SENDER_EMAIL = os.environ['SES_SENDER_EMAIL']
SES_RECIPIENT_EMAIL = os.environ['SES_RECIPIENT_EMAIL']
SNS_TOPIC_ARN = os.environ['SNS_TOPIC_ARN']
BUFFER_TEMP = int(os.environ.get('BUFFER_TEMP', 0))  # Default buffer is 0°F if not set

# OpenWeather API URL
WEATHER_API_URL = "https://api.openweathermap.org/data/2.5/forecast"

def get_weather_forecast():
    """Fetches the weather forecast for the next 8 hours using Fahrenheit."""
    params = {
        'lat': LAT,
        'lon': LON,
        'appid': OPENWEATHER_API_KEY,
        'units': 'imperial'  # Fahrenheit
    }
    
    response = requests.get(WEATHER_API_URL, params=params)
    print("response:", response.json())
    if response.status_code != 200:
        raise Exception(f"Failed to fetch weather data: {response.text}")
    
    return response.json()

def check_frost_warning(weather_data):
    """Checks if freezing temperatures (≤ 32°F + buffer) are forecasted in the next 8 hours."""
    now = datetime.utcnow()
    cutoff_time = now + timedelta(hours=8)
    warning_temp = 32 + BUFFER_TEMP  # Apply buffer to freezing temperature

    for forecast in weather_data['list']:
        forecast_time = datetime.utcfromtimestamp(forecast['dt'])
        temperature = forecast['main']['temp']
        
        if forecast_time <= cutoff_time and temperature <= warning_temp:
            return forecast_time, temperature
    
    return None, None

def send_ses_email(alert_message):
    """Sends an email alert using AWS SES."""
    ses_client.send_email(
        Source=SES_SENDER_EMAIL,
        Destination={'ToAddresses': [SES_RECIPIENT_EMAIL]},
        Message={
            'Subject': {'Data': 'Frost/Freezing Weather Alert'},
            'Body': {'Text': {'Data': alert_message}}
        }
    )

def send_sns_notification(alert_message):
    """Publishes a notification to an SNS topic."""
    sns_client.publish(
        TopicArn=SNS_TOPIC_ARN,
        Message=alert_message,
        Subject="Frost/Freezing Weather Alert"
    )

def lambda_handler(event, context):
    """AWS Lambda entry point."""
    try:
        weather_data = get_weather_forecast()
        alert_time, alert_temp = check_frost_warning(weather_data)
        
        if alert_time:
            alert_message = (
                f"Warning: Freezing temperature ({alert_temp}°F) forecasted at {alert_time} UTC. "
                f"Buffer applied: {BUFFER_TEMP}°F."
            )
            send_ses_email(alert_message)
            send_sns_notification(alert_message)
            
            return {"statusCode": 200, "body": json.dumps("Alert sent successfully.")}
        
        return {"statusCode": 200, "body": json.dumps("No freezing weather detected in the next 8 hours.")}
    
    except Exception as e:
        return {"statusCode": 500, "body": json.dumps(f"Error: {str(e)}")}
