# FitGenius AI Agent - Complete Setup Guide

## Table of Contents
1. [AWS Account Setup](#aws-account-setup)
2. [IAM Permissions](#iam-permissions)
3. [Bedrock Model Access](#bedrock-model-access)
4. [DynamoDB Configuration](#dynamodb-configuration)
5. [S3 Bucket Setup](#s3-bucket-setup)
6. [Local Development Setup](#local-development-setup)
7. [Environment Configuration](#environment-configuration)
8. [Testing the Agent](#testing-the-agent)
9. [Troubleshooting](#troubleshooting)

## AWS Account Setup

### Step 1: Create AWS Account
1. Go to [AWS Console](https://aws.amazon.com/)
2. Click "Create an AWS Account"
3. Follow the registration process
4. Verify your email and payment method

### Step 2: Enable Amazon Bedrock
1. Navigate to Amazon Bedrock in AWS Console
2. Request access to Claude 3 models
3. Wait for approval (usually within 24 hours)

## IAM Permissions

Create an IAM user with the following permissions:

### Option 1: Using AWS CLI

```bash
# Create IAM policy
cat > fitgenius-policy.json << EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "bedrock:InvokeModel",
                "bedrock:InvokeModelWithResponseStream"
            ],
            "Resource": [
                "arn:aws:bedrock:*::foundation-model/anthropic.claude-3-sonnet-20240229-v1:0",
                "arn:aws:bedrock:*::foundation-model/anthropic.claude-3-opus-20240229-v1:0"
            ]
        },
        {
            "Effect": "Allow",
            "Action": [
                "dynamodb:PutItem",
                "dynamodb:GetItem",
                "dynamodb:Query",
                "dynamodb:Scan",
                "dynamodb:UpdateItem",
                "dynamodb:DeleteItem"
            ],
            "Resource": "arn:aws:dynamodb:*:*:table/FitGeniusProgress"
        },
        {
            "Effect": "Allow",
            "Action": [
                "s3:PutObject",
                "s3:GetObject",
                "s3:DeleteObject"
            ],
            "Resource": "arn:aws:s3:::fitgenius-images/*"
        }
    ]
}
EOF

# Create the policy
aws iam create-policy \
    --policy-name FitGeniusAgentPolicy \
    --policy-document file://fitgenius-policy.json

# Create IAM user
aws iam create-user --user-name fitgenius-agent

# Attach policy to user
aws iam attach-user-policy \
    --user-name fitgenius-agent \
    --policy-arn arn:aws:iam::YOUR_ACCOUNT_ID:policy/FitGeniusAgentPolicy

# Create access keys
aws iam create-access-key --user-name fitgenius-agent
```

### Option 2: Using AWS Console

1. Go to IAM → Users → Create User
2. User name: `fitgenius-agent`
3. Attach policies directly → Create policy
4. Copy the JSON from `fitgenius-policy.json` above
5. Create and attach the policy
6. Create access keys for the user

## Bedrock Model Access

### Request Model Access

```bash
# Check if Claude 3 Sonnet is available
aws bedrock list-foundation-models \
    --region us-east-1 \
    --query "modelSummaries[?contains(modelId, 'claude-3')]"

# If not available, request access through console:
# 1. Go to Bedrock → Model access
# 2. Request access to Claude 3 Sonnet
# 3. Wait for approval
```

### Test Bedrock Access

```python
import boto3
import json

bedrock = boto3.client('bedrock-runtime', region_name='us-east-1')

response = bedrock.invoke_model(
    modelId='anthropic.claude-3-sonnet-20240229-v1:0',
    body=json.dumps({
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 100,
        "messages": [
            {"role": "user", "content": "Say hello!"}
        ]
    })
)

print(json.loads(response['body'].read()))
```

## DynamoDB Configuration

### Create Progress Tracking Table

```bash
# Create table
aws dynamodb create-table \
    --table-name FitGeniusProgress \
    --attribute-definitions \
        AttributeName=userId,AttributeType=S \
        AttributeName=date,AttributeType=S \
    --key-schema \
        AttributeName=userId,KeyType=HASH \
        AttributeName=date,KeyType=RANGE \
    --billing-mode PAY_PER_REQUEST \
    --region us-east-1

# Add Global Secondary Index for date queries
aws dynamodb update-table \
    --table-name FitGeniusProgress \
    --attribute-definitions \
        AttributeName=date,AttributeType=S \
    --global-secondary-index-updates \
    '[{
        "Create": {
            "IndexName": "DateIndex",
            "KeySchema": [
                {"AttributeName": "date", "KeyType": "HASH"}
            ],
            "Projection": {"ProjectionType": "ALL"},
            "ProvisionedThroughput": {
                "ReadCapacityUnits": 5,
                "WriteCapacityUnits": 5
            }
        }
    }]'

# Verify table creation
aws dynamodb describe-table \
    --table-name FitGeniusProgress \
    --query 'Table.[TableName,TableStatus]'
```

### Create User Profiles Table (Optional)

```bash
aws dynamodb create-table \
    --table-name FitGeniusUsers \
    --attribute-definitions \
        AttributeName=userId,AttributeType=S \
    --key-schema \
        AttributeName=userId,KeyType=HASH \
    --billing-mode PAY_PER_REQUEST \
    --region us-east-1
```

## S3 Bucket Setup

### Create Image Storage Bucket

```bash
# Create bucket
aws s3 mb s3://fitgenius-images-YOUR_UNIQUE_ID --region us-east-1

# Enable versioning
aws s3api put-bucket-versioning \
    --bucket fitgenius-images-YOUR_UNIQUE_ID \
    --versioning-configuration Status=Enabled

# Set lifecycle policy to delete old images
cat > lifecycle.json << EOF
{
    "Rules": [
        {
            "Id": "DeleteOldProgressImages",
            "Status": "Enabled",
            "Prefix": "progress/",
            "Expiration": {
                "Days": 180
            }
        }
    ]
}
EOF

aws s3api put-bucket-lifecycle-configuration \
    --bucket fitgenius-images-YOUR_UNIQUE_ID \
    --lifecycle-configuration file://lifecycle.json

# Set CORS for web access (if building web app)
cat > cors.json << EOF
{
    "CORSRules": [
        {
            "AllowedOrigins": ["*"],
            "AllowedMethods": ["GET", "PUT", "POST"],
            "AllowedHeaders": ["*"],
            "MaxAgeSeconds": 3000
        }
    ]
}
EOF

aws s3api put-bucket-cors \
    --bucket fitgenius-images-YOUR_UNIQUE_ID \
    --cors-configuration file://cors.json
```

## Local Development Setup

### 1. Clone and Setup Python Environment

```bash
# Clone repository
git clone https://github.com/yourusername/fitgenius-ai-agent.git
cd fitgenius-ai-agent

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt
```

### 2. Install Strands Agents SDK

```bash
# Follow AWS documentation to install Strands SDK
# The SDK may need to be installed from AWS-specific sources

pip install strands-agents-sdk
```

### 3. Configure AWS Credentials

```bash
# Configure AWS CLI
aws configure

# Enter your credentials:
# AWS Access Key ID: YOUR_ACCESS_KEY
# AWS Secret Access Key: YOUR_SECRET_KEY
# Default region name: us-east-1
# Default output format: json

# Verify configuration
aws sts get-caller-identity
```

## Environment Configuration

### Create .env File

```bash
cat > .env << EOF
# AWS Configuration
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key

# Bedrock Configuration
BEDROCK_MODEL_ID=anthropic.claude-3-sonnet-20240229-v1:0
BEDROCK_MAX_TOKENS=4096

# DynamoDB Configuration
DYNAMODB_PROGRESS_TABLE=FitGeniusProgress
DYNAMODB_USERS_TABLE=FitGeniusUsers

# S3 Configuration
S3_BUCKET_NAME=fitgenius-images-YOUR_UNIQUE_ID
S3_IMAGE_PREFIX=progress/

# Agent Configuration
AGENT_NAME=FitGenius
AGENT_VERSION=1.0.0
MAX_IMAGE_SIZE_MB=5
MAX_HISTORY_DAYS=90

# Feature Flags
ENABLE_VISION_ANALYSIS=true
ENABLE_PROGRESS_TRACKING=true
ENABLE_WEB_SEARCH=true

# Logging
LOG_LEVEL=INFO
LOG_FORMAT=json
EOF
```

### Update config.yaml

```yaml
aws:
  region: us-east-1
  bedrock:
    model_id: anthropic.claude-3-sonnet-20240229-v1:0
    max_tokens: 4096
    temperature: 0.7
  
database:
  progress_table: FitGeniusProgress
  users_table: FitGeniusUsers
  
storage:
  bucket_name: fitgenius-images-YOUR_UNIQUE_ID
  image_prefix: progress/
  max_image_size_mb: 5
  
agent:
  name: FitGenius
  version: 1.0.0
  features:
    vision_analysis: true
    progress_tracking: true
    web_search: true
  limits:
    max_history_days: 90
    max_workout_plans: 10
    max_diet_plans: 10
  
logging:
  level: INFO
  format: json
  file: logs/fitgenius.log
```

## Testing the Agent

### Run Unit Tests

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=fitgenius_agent --cov-report=html

# Run specific test file
pytest tests/test_body_analyzer.py -v
```

### Manual Testing

```python
# test_agent.py
from fitgenius_agent import FitGeniusAgent

def test_basic_functionality():
    agent = FitGeniusAgent()
    
    # Test BMI calculation
    response = agent.process_user_request(
        "Calculate my BMI. I'm 175cm tall and weigh 80kg."
    )
    print("BMI Test:", response)
    
    # Test workout plan generation
    response = agent.process_user_request(
        "Create a 3-day beginner workout plan for weight loss."
    )
    print("Workout Plan:", response)
    
    # Test diet planning
    response = agent.process_user_request(
        "Generate a diet plan for muscle gain. I weigh 75kg and want to gain 5kg."
    )
    print("Diet Plan:", response)

if __name__ == "__main__":
    test_basic_functionality()
```

Run the test:
```bash
python test_agent.py
```

### Test with Sample Data

```bash
# Create test user
python scripts/create_test_user.py

# Load sample progress data
python scripts/load_sample_data.py

# Run end-to-end test
python scripts/e2e_test.py
```

## Troubleshooting

### Common Issues

#### 1. Bedrock Access Denied

**Error**: `AccessDeniedException: User is not authorized to perform: bedrock:InvokeModel`

**Solution**:
```bash
# Verify IAM permissions
aws iam get-user-policy \
    --user-name fitgenius-agent \
    --policy-name FitGeniusAgentPolicy

# Request Bedrock model access in console
# Bedrock → Model access → Request access
```

#### 2. DynamoDB Table Not Found

**Error**: `ResourceNotFoundException: Requested resource not found`

**Solution**:
```bash
# List tables
aws dynamodb list-tables

# Recreate table if missing
aws dynamodb create-table \
    --table-name FitGeniusProgress \
    --attribute-definitions AttributeName=userId,AttributeType=S AttributeName=date,AttributeType=S \
    --key-schema AttributeName=userId,KeyType=HASH AttributeName=date,KeyType=RANGE \
    --billing-mode PAY_PER_REQUEST
```

#### 3. S3 Bucket Permission Denied

**Error**: `AccessDenied: Access Denied`

**Solution**:
```bash
# Check bucket policy
aws s3api get-bucket-policy --bucket fitgenius-images-YOUR_UNIQUE_ID

# Update IAM policy to include S3 permissions
```

#### 4. Image Size Too Large

**Error**: `PayloadTooLargeException`

**Solution**:
- Resize images before uploading
- Maximum size is 5MB for Claude Vision
- Use image compression:

```python
from PIL import Image

def compress_image(input_path, output_path, max_size_mb=5):
    img = Image.open(input_path)
    
    # Calculate compression quality
    quality = 95
    img.save(output_path, "JPEG", quality=quality, optimize=True)
    
    # Check file size and reduce quality if needed
    while os.path.getsize(output_path) > max_size_mb * 1024 * 1024 and quality > 10:
        quality -= 5
        img.save(output_path, "JPEG", quality=quality, optimize=True)
```

#### 5. Rate Limiting

**Error**: `ThrottlingException: Rate exceeded`

**Solution**:
- Implement exponential backoff
- Add retry logic:

```python
import time
from botocore.exceptions import ClientError

def invoke_with_retry(bedrock_client, **kwargs):
    max_retries = 3
    for attempt in range(max_retries):
        try:
            return bedrock_client.invoke_model(**kwargs)
        except ClientError as e:
            if e.response['Error']['Code'] == 'ThrottlingException':
                wait_time = 2 ** attempt
                time.sleep(wait_time)
            else:
                raise
    raise Exception("Max retries exceeded")
```

### Getting Help

If you encounter issues not covered here:

1. Check AWS CloudWatch Logs
2. Enable debug logging in the agent
3. Review AWS Service Health Dashboard
4. Open an issue on GitHub
5. Check AWS Bedrock documentation

### Useful Commands

```bash
# Check AWS service quotas
aws service-quotas list-service-quotas \
    --service-code bedrock

# Monitor DynamoDB table
aws dynamodb describe-table \
    --table-name FitGeniusProgress

# View CloudWatch logs
aws logs tail /aws/bedrock/fitgenius --follow

# Test S3 connectivity
aws s3 ls s3://fitgenius-images-YOUR_UNIQUE_ID/
```

## Next Steps

1. Complete the setup checklist
2. Run the test suite
3. Try the example scripts
4. Build your first fitness plan
5. Customize the agent for your needs

For more information, see:
- [README.md](README.md) - Main documentation
- [EXAMPLES.md](EXAMPLES.md) - Usage examples
- [API.md](API.md) - API reference
- [CONTRIBUTING.md](CONTRIBUTING.md) - Contribution guidelines