#!/usr/bin/env python3
"""Load sample data for testing"""
import boto3
from datetime import datetime, timedelta

def load_sample_progress():
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table('FitGeniusProgress')
    
    base_date = datetime.now() - timedelta(days=30)
    
    for i in range(30):
        date = base_date + timedelta(days=i)
        entry = {
            'userId': 'demo_user_001',
            'date': date.strftime('%Y-%m-%d'),
            'weight': 85.0 - (i * 0.1),
            'measurements': {
                'waist': 95 - (i * 0.1),
                'chest': 100 + (i * 0.05),
                'arms': 35 + (i * 0.02)
            }
        }
        table.put_item(Item=entry)
        print(f"✓ Loaded: {date.strftime('%Y-%m-%d')}")

if __name__ == "__main__":
    load_sample_progress()