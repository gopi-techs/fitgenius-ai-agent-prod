# FitGenius AI Agent 🏋️‍♂️

> An intelligent fitness assistant built with AWS Strands Agents SDK that provides personalized workout plans, diet recommendations, and progress tracking using AI-powered body analysis.

[![AWS](https://img.shields.io/badge/AWS-Bedrock-FF9900?style=for-the-badge&logo=amazon-aws)](https://aws.amazon.com/bedrock/)
[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge)](LICENSE)

## 🌟 Features

### 1. **AI-Powered Body Analysis**
- Analyzes body composition from uploaded images using Claude Vision
- Estimates body fat percentage and muscle development
- Provides posture assessment and improvement recommendations
- Determines current fitness level (beginner/intermediate/advanced)

### 2. **Personalized Workout Plans**
- Custom workout routines based on fitness level and goals
- Supports multiple goals: weight loss, muscle gain, strength, endurance
- Adapts to available equipment and time constraints
- Progressive overload recommendations

### 3. **Smart Diet Planning**
- Calculates personalized calorie and macro targets
- Generates meal plans based on dietary restrictions
- Provides supplement recommendations
- Includes hydration and meal timing guidance

### 4. **Progress Tracking**
- Daily weight and measurement logging
- Visual progress comparisons over time
- Trend analysis and insights
- Motivational feedback based on achievements

### 5. **Intelligent Coaching**
- Answers fitness and nutrition questions
- Provides form corrections and exercise alternatives
- Adapts plans based on progress
- Searches latest fitness research when needed

## 🏗️ Architecture

```
┌─────────────────────────────────────────────┐
│           User Interface Layer              │
│  (CLI / Web App / Mobile App / API)        │
└──────────────────┬──────────────────────────┘
                   │
┌──────────────────▼──────────────────────────┐
│        FitGenius AI Agent (Strands)         │
│  ┌─────────────────────────────────────┐   │
│  │   Agent Orchestrator (Claude 3)     │   │
│  └─────────────────────────────────────┘   │
│                                             │
│  ┌──────────────────────────────────────┐  │
│  │          Tool Registry                │  │
│  ├──────────────────────────────────────┤  │
│  │ • BMI Calculator                     │  │
│  │ • Body Analyzer (Vision)             │  │
│  │ • Workout Planner                    │  │
│  │ • Diet Planner                       │  │
│  │ • Progress Tracker                   │  │
│  │ • Fitness Search                     │  │
│  └──────────────────────────────────────┘  │
└──────────────────┬──────────────────────────┘
                   │
┌──────────────────▼──────────────────────────┐
│          AWS Services Layer                 │
│  ┌─────────────┐  ┌──────────┐  ┌────────┐ │
│  │   Bedrock   │  │ DynamoDB │  │   S3   │ │
│  │  (Claude 3) │  │(Progress)│  │(Images)│ │
│  └─────────────┘  └──────────┘  └────────┘ │
└─────────────────────────────────────────────┘
```

## 🚀 Quick Start

### Prerequisites

- Python 3.9 or higher
- AWS Account with Bedrock access
- AWS CLI configured with appropriate credentials
- Required IAM permissions for Bedrock, DynamoDB, and S3

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/fitgenius-ai-agent.git
cd fitgenius-ai-agent
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Set up AWS credentials**
```bash
aws configure
```

4. **Create DynamoDB table**
```bash
aws dynamodb create-table \
    --table-name FitGeniusProgress \
    --attribute-definitions \
        AttributeName=userId,AttributeType=S \
        AttributeName=date,AttributeType=S \
    --key-schema \
        AttributeName=userId,KeyType=HASH \
        AttributeName=date,KeyType=RANGE \
    --billing-mode PAY_PER_REQUEST
```

5. **Run the agent**
```bash
python fitgenius_agent.py
```

## 💻 Usage Examples

### Example 1: Initial Assessment

```python
from fitgenius_agent import FitGeniusAgent

agent = FitGeniusAgent()

# User context
user_info = {
    "name": "Sarah",
    "age": 30,
    "gender": "female",
    "height_cm": 165,
    "weight_kg": 70,
    "goal": "weight_loss"
}

# Get assessment and plan
response = agent.process_user_request(
    "I want to lose 10kg in 3 months. Can you help me with a complete plan?",
    context=user_info
)

print(response)
```

### Example 2: Body Analysis with Image

```python
import base64

# Load and encode image
with open("body_photo.jpg", "rb") as image_file:
    encoded_image = base64.b64encode(image_file.read()).decode()

# Analyze body composition
response = agent.process_user_request(
    f"Analyze my body composition and suggest focus areas. Image: {encoded_image}",
    context=user_info
)
```

### Example 3: Daily Progress Tracking

```python
# Track daily progress
response = agent.process_user_request(
    """Track my progress for today:
    - Weight: 68.5kg
    - Waist: 85cm
    - Chest: 95cm
    - Arms: 32cm
    - Completed workout: Yes
    """,
    context={"user_id": "user123"}
)
```

### Example 4: Get Workout Plan

```python
response = agent.process_user_request(
    """Create a 5-day workout plan for muscle gain. 
    I'm intermediate level with full gym access. 
    60 minutes per session. 
    Focus on upper body development."""
)
```

## 📊 Sample Output

### Body Analysis Report
```
=== Body Composition Analysis ===
Current Stats:
- BMI: 25.7 (Overweight)
- Estimated Body Fat: 28%
- Fitness Level: Beginner

Muscle Development:
✓ Shoulders: Moderate development
✓ Chest: Below average, needs focus
✓ Arms: Average development
✓ Core: Weak, significant work needed
✓ Legs: Good foundation

Recommendations:
1. Focus on compound movements
2. Add 30min cardio 3x/week
3. Strengthen core with dedicated ab work
4. Improve posture - slight forward lean detected
```

### Workout Plan Sample
```
=== 4-Day Muscle Gain Plan ===

Monday - Chest & Triceps
1. Barbell Bench Press: 4x8-10
2. Incline Dumbbell Press: 3x10
3. Cable Flyes: 3x12
4. Tricep Pushdowns: 4x12
5. Overhead Extension: 3x12

Tuesday - Back & Biceps
1. Pull-ups: 4x6-8
2. Barbell Rows: 4x8
...
```

### Diet Plan Sample
```
=== Personalized Nutrition Plan ===

Daily Targets:
- Calories: 2,200 kcal
- Protein: 165g (30%)
- Carbs: 220g (40%)
- Fats: 73g (30%)

Meal Schedule:
Breakfast (7:00 AM): Oatmeal with protein powder and berries
Snack 1 (10:00 AM): Greek yogurt with almonds
Lunch (1:00 PM): Grilled chicken with brown rice and vegetables
...
```

## 🧪 Testing

Run the test suite:
```bash
python -m pytest tests/
```

Run specific tests:
```bash
python -m pytest tests/test_body_analyzer.py -v
```

## 🛠️ Configuration

Create a `config.yaml` file:

```yaml
aws:
  region: us-east-1
  bedrock_model: anthropic.claude-3-sonnet-20240229-v1:0
  
database:
  table_name: FitGeniusProgress
  
features:
  enable_vision_analysis: true
  enable_progress_tracking: true
  enable_web_search: true
  
limits:
  max_image_size_mb: 5
  max_history_days: 90
```

## 📈 Roadmap

- [ ] Add video analysis for exercise form checking
- [ ] Integration with fitness wearables (Fitbit, Apple Watch)
- [ ] Meal photo analysis for calorie counting
- [ ] Community features and challenges
- [ ] Mobile app development
- [ ] Multi-language support
- [ ] Integration with recipe databases
- [ ] Virtual PT sessions with real-time feedback

## 🤝 Contributing

Contributions are welcome! Please read our [Contributing Guidelines](CONTRIBUTING.md) first.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [AWS Strands Agents SDK](https://docs.aws.amazon.com/bedrock/latest/userguide/agents.html)
- Powered by [Anthropic Claude 3](https://www.anthropic.com/claude)
- Inspired by AWS Agentic AI Foundations Course

## 📧 Contact

Your Name - Gopinatha R (gopiroux@gmail.com)

Project Link: https://github.com/gopi-techs/fitgenius-ai-agent-prod/

---

**Note**: This agent is for educational and informational purposes only. Always consult with healthcare professionals before starting any fitness or diet program.

⭐ If you found this project helpful, please give it a star!
