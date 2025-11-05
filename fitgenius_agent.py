"""
FitGenius AI Agent - Comprehensive Fitness Assistant
Built with AWS Strands Agents SDK

This agent provides:
- Body composition analysis
- Personalized workout plans
- Custom diet recommendations
- Daily progress tracking
- Adaptive fitness coaching
"""

import json
import boto3
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import base64

# Strands Agent Configuration
from strands import Agent, Tool, ToolResponse

class FitGeniusAgent:
    """Main Fitness AI Agent using Strands SDK"""
    
    def __init__(self):
        self.bedrock = boto3.client('bedrock-runtime')
        self.s3 = boto3.client('s3')
        self.dynamodb = boto3.resource('dynamodb')
        
        # Initialize tools
        self.tools = [
            self.create_bmi_calculator_tool(),
            self.create_body_analyzer_tool(),
            self.create_workout_planner_tool(),
            self.create_diet_planner_tool(),
            self.create_progress_tracker_tool(),
            self.create_web_search_tool()
        ]
        
        # Initialize agent
        self.agent = Agent(
            name="FitGenius",
            description="Personal fitness AI agent for body analysis, workout planning, and progress tracking",
            tools=self.tools,
            model_id="anthropic.claude-3-sonnet-20240229-v1:0"
        )
    
    def create_bmi_calculator_tool(self) -> Tool:
        """Tool to calculate BMI and body composition metrics"""
        def calculate_bmi(weight_kg: float, height_cm: float) -> Dict:
            height_m = height_cm / 100
            bmi = weight_kg / (height_m ** 2)
            
            # BMI categories
            if bmi < 18.5:
                category = "Underweight"
                health_risk = "Low to Moderate"
            elif 18.5 <= bmi < 25:
                category = "Normal Weight"
                health_risk = "Low"
            elif 25 <= bmi < 30:
                category = "Overweight"
                health_risk = "Moderate"
            else:
                category = "Obese"
                health_risk = "High"
            
            return {
                "bmi": round(bmi, 2),
                "category": category,
                "health_risk": health_risk,
                "ideal_weight_range": {
                    "min": round(18.5 * (height_m ** 2), 1),
                    "max": round(24.9 * (height_m ** 2), 1)
                }
            }
        
        return Tool(
            name="bmi_calculator",
            description="Calculate BMI and determine health category",
            function=calculate_bmi,
            parameters={
                "weight_kg": {"type": "number", "description": "Weight in kilograms"},
                "height_cm": {"type": "number", "description": "Height in centimeters"}
            }
        )
    
    def create_body_analyzer_tool(self) -> Tool:
        """Tool to analyze body structure from images"""
        def analyze_body_image(image_data: str, user_info: Dict) -> Dict:
            """
            Uses Claude Vision to analyze body composition
            image_data: base64 encoded image
            user_info: dict with age, gender, height, weight
            """
            
            prompt = f"""Analyze this body image and provide a detailed assessment:
            
            User Info:
            - Age: {user_info.get('age')}
            - Gender: {user_info.get('gender')}
            - Height: {user_info.get('height_cm')}cm
            - Weight: {user_info.get('weight_kg')}kg
            
            Please analyze:
            1. Overall body composition (estimated body fat %)
            2. Muscle development by body part (shoulders, chest, arms, core, legs)
            3. Posture assessment
            4. Areas needing improvement
            5. Current fitness level estimate (beginner/intermediate/advanced)
            
            Provide specific, actionable insights."""
            
            # Call Bedrock with Claude Vision
            response = self.bedrock.invoke_model(
                modelId='anthropic.claude-3-sonnet-20240229-v1:0',
                body=json.dumps({
                    "anthropic_version": "bedrock-2023-05-31",
                    "max_tokens": 2000,
                    "messages": [{
                        "role": "user",
                        "content": [
                            {
                                "type": "image",
                                "source": {
                                    "type": "base64",
                                    "media_type": "image/jpeg",
                                    "data": image_data
                                }
                            },
                            {
                                "type": "text",
                                "text": prompt
                            }
                        ]
                    }]
                })
            )
            
            result = json.loads(response['body'].read())
            analysis = result['content'][0]['text']
            
            return {
                "analysis": analysis,
                "timestamp": datetime.now().isoformat(),
                "user_info": user_info
            }
        
        return Tool(
            name="body_analyzer",
            description="Analyze body composition from image using AI vision",
            function=analyze_body_image,
            parameters={
                "image_data": {"type": "string", "description": "Base64 encoded body image"},
                "user_info": {"type": "object", "description": "User demographics and measurements"}
            }
        )
    
    def create_workout_planner_tool(self) -> Tool:
        """Tool to generate personalized workout plans"""
        def generate_workout_plan(
            fitness_level: str,
            goals: List[str],
            available_equipment: List[str],
            days_per_week: int,
            duration_minutes: int,
            focus_areas: List[str]
        ) -> Dict:
            """
            Generate a personalized workout plan
            fitness_level: beginner, intermediate, advanced
            goals: weight_loss, muscle_gain, strength, endurance, flexibility
            """
            
            workout_templates = {
                "beginner": {
                    "weight_loss": [
                        {"day": "Monday", "focus": "Full Body", "exercises": [
                            "Bodyweight Squats: 3x12",
                            "Push-ups (modified): 3x8-10",
                            "Lunges: 3x10 each leg",
                            "Plank: 3x30 seconds",
                            "Jumping Jacks: 3x20"
                        ]},
                        {"day": "Wednesday", "focus": "Cardio & Core", "exercises": [
                            "Brisk Walking: 20 minutes",
                            "Mountain Climbers: 3x15",
                            "Bicycle Crunches: 3x15",
                            "Burpees: 3x8",
                            "Leg Raises: 3x12"
                        ]},
                        {"day": "Friday", "focus": "Full Body", "exercises": [
                            "Bodyweight Squats: 3x15",
                            "Incline Push-ups: 3x10",
                            "Step-ups: 3x12 each leg",
                            "Side Plank: 3x20s each side",
                            "High Knees: 3x30 seconds"
                        ]}
                    ],
                    "muscle_gain": [
                        {"day": "Monday", "focus": "Upper Body", "exercises": [
                            "Push-ups: 4x8-12",
                            "Dumbbell Rows: 4x10",
                            "Shoulder Press: 3x10",
                            "Bicep Curls: 3x12",
                            "Tricep Dips: 3x10"
                        ]},
                        {"day": "Wednesday", "focus": "Lower Body", "exercises": [
                            "Goblet Squats: 4x10",
                            "Romanian Deadlifts: 4x10",
                            "Lunges: 3x12 each",
                            "Calf Raises: 4x15",
                            "Glute Bridges: 3x15"
                        ]},
                        {"day": "Friday", "focus": "Full Body", "exercises": [
                            "Squats: 4x10",
                            "Push-ups: 4x10",
                            "Bent Over Rows: 4x10",
                            "Overhead Press: 3x10",
                            "Planks: 3x45s"
                        ]}
                    ]
                },
                "intermediate": {
                    "muscle_gain": [
                        {"day": "Monday", "focus": "Chest & Triceps", "exercises": [
                            "Barbell Bench Press: 4x8-10",
                            "Incline Dumbbell Press: 3x10",
                            "Cable Flyes: 3x12",
                            "Tricep Pushdowns: 4x12",
                            "Overhead Tricep Extension: 3x12"
                        ]},
                        {"day": "Tuesday", "focus": "Back & Biceps", "exercises": [
                            "Pull-ups: 4x6-8",
                            "Barbell Rows: 4x8",
                            "Lat Pulldowns: 3x10",
                            "Barbell Curls: 4x10",
                            "Hammer Curls: 3x12"
                        ]},
                        {"day": "Thursday", "focus": "Legs", "exercises": [
                            "Back Squats: 4x8",
                            "Leg Press: 4x12",
                            "Romanian Deadlifts: 3x10",
                            "Leg Curls: 3x12",
                            "Leg Extensions: 3x15"
                        ]},
                        {"day": "Friday", "focus": "Shoulders & Arms", "exercises": [
                            "Military Press: 4x8",
                            "Lateral Raises: 4x12",
                            "Face Pulls: 3x15",
                            "Barbell Curls: 3x10",
                            "Close-Grip Bench: 3x10"
                        ]}
                    ]
                }
            }
            
            # Select appropriate template
            primary_goal = goals[0] if goals else "muscle_gain"
            plan = workout_templates.get(fitness_level, {}).get(primary_goal, [])
            
            return {
                "plan": plan[:days_per_week],
                "duration_per_session": f"{duration_minutes} minutes",
                "fitness_level": fitness_level,
                "goals": goals,
                "tips": [
                    "Always warm up for 5-10 minutes before starting",
                    "Focus on proper form over heavy weights",
                    "Rest 60-90 seconds between sets",
                    "Cool down and stretch after each session",
                    f"Increase weights by 5-10% when you can complete all sets with good form"
                ]
            }
        
        return Tool(
            name="workout_planner",
            description="Generate personalized workout plans based on goals and fitness level",
            function=generate_workout_plan,
            parameters={
                "fitness_level": {"type": "string", "description": "beginner, intermediate, or advanced"},
                "goals": {"type": "array", "description": "List of fitness goals"},
                "available_equipment": {"type": "array", "description": "Available gym equipment"},
                "days_per_week": {"type": "integer", "description": "Number of workout days"},
                "duration_minutes": {"type": "integer", "description": "Session duration"},
                "focus_areas": {"type": "array", "description": "Body parts to focus on"}
            }
        )
    
    def create_diet_planner_tool(self) -> Tool:
        """Tool to create personalized diet plans"""
        def generate_diet_plan(
            goal: str,
            current_weight: float,
            target_weight: float,
            activity_level: str,
            dietary_restrictions: List[str],
            meals_per_day: int
        ) -> Dict:
            """
            Generate personalized diet plan
            goal: weight_loss, muscle_gain, maintenance
            activity_level: sedentary, moderate, active, very_active
            """
            
            # Calculate BMR (Basal Metabolic Rate) - simplified
            # Using Mifflin-St Jeor Equation approximation
            activity_multipliers = {
                "sedentary": 1.2,
                "moderate": 1.55,
                "active": 1.725,
                "very_active": 1.9
            }
            
            # Simplified TDEE calculation (you'd need gender, age, height for accuracy)
            base_calories = current_weight * 22  # Rough estimate
            tdee = base_calories * activity_multipliers.get(activity_level, 1.55)
            
            # Adjust calories based on goal
            if goal == "weight_loss":
                target_calories = tdee - 500  # 500 cal deficit
                protein_multiplier = 2.0  # g per kg bodyweight
                carb_percentage = 0.30
                fat_percentage = 0.30
            elif goal == "muscle_gain":
                target_calories = tdee + 300  # 300 cal surplus
                protein_multiplier = 2.2
                carb_percentage = 0.40
                fat_percentage = 0.25
            else:  # maintenance
                target_calories = tdee
                protein_multiplier = 1.8
                carb_percentage = 0.35
                fat_percentage = 0.30
            
            # Calculate macros
            protein_g = current_weight * protein_multiplier
            protein_calories = protein_g * 4
            fat_calories = target_calories * fat_percentage
            fat_g = fat_calories / 9
            carb_calories = target_calories - protein_calories - fat_calories
            carb_g = carb_calories / 4
            
            # Sample meal plans
            meal_examples = {
                "weight_loss": {
                    "breakfast": "Oatmeal with berries and protein powder (350 cal)",
                    "snack1": "Greek yogurt with almonds (200 cal)",
                    "lunch": "Grilled chicken salad with olive oil dressing (450 cal)",
                    "snack2": "Apple with peanut butter (180 cal)",
                    "dinner": "Baked salmon with roasted vegetables (500 cal)"
                },
                "muscle_gain": {
                    "breakfast": "Scrambled eggs with whole grain toast and avocado (550 cal)",
                    "snack1": "Protein shake with banana (300 cal)",
                    "lunch": "Chicken breast with brown rice and broccoli (650 cal)",
                    "snack2": "Trail mix with dried fruits (250 cal)",
                    "dinner": "Lean beef with sweet potato and green beans (700 cal)",
                    "snack3": "Cottage cheese with berries (200 cal)"
                }
            }
            
            return {
                "daily_calories": round(target_calories),
                "macros": {
                    "protein_g": round(protein_g),
                    "carbs_g": round(carb_g),
                    "fats_g": round(fat_g)
                },
                "meal_plan": meal_examples.get(goal, meal_examples["weight_loss"]),
                "hydration": "Drink at least 3-4 liters of water daily",
                "tips": [
                    "Eat protein with every meal",
                    "Include vegetables in lunch and dinner",
                    "Prepare meals in advance",
                    "Track your food intake for first 2 weeks",
                    "Adjust portions based on weekly progress"
                ],
                "supplements_suggested": [
                    "Multivitamin",
                    "Omega-3 Fish Oil",
                    "Vitamin D3",
                    "Whey Protein (if needed to hit protein goals)"
                ]
            }
        
        return Tool(
            name="diet_planner",
            description="Generate personalized diet and nutrition plans",
            function=generate_diet_plan,
            parameters={
                "goal": {"type": "string", "description": "weight_loss, muscle_gain, or maintenance"},
                "current_weight": {"type": "number", "description": "Current weight in kg"},
                "target_weight": {"type": "number", "description": "Target weight in kg"},
                "activity_level": {"type": "string", "description": "Activity level"},
                "dietary_restrictions": {"type": "array", "description": "Dietary restrictions"},
                "meals_per_day": {"type": "integer", "description": "Number of meals per day"}
            }
        )
    
    def create_progress_tracker_tool(self) -> Tool:
        """Tool to track and compare progress over time"""
        def track_progress(
            user_id: str,
            date: str,
            weight: float,
            body_measurements: Dict,
            progress_image: Optional[str] = None
        ) -> Dict:
            """
            Store and analyze progress data
            """
            table = self.dynamodb.Table('FitGeniusProgress')
            
            progress_entry = {
                'userId': user_id,
                'date': date,
                'weight': weight,
                'measurements': body_measurements,
                'timestamp': datetime.now().isoformat()
            }
            
            # Store in DynamoDB
            table.put_item(Item=progress_entry)
            
            # Get historical data
            response = table.query(
                KeyConditionExpression='userId = :uid',
                ExpressionAttributeValues={':uid': user_id},
                ScanIndexForward=False,
                Limit=30
            )
            
            history = response.get('Items', [])
            
            # Calculate progress
            if len(history) > 1:
                first_entry = history[-1]
                weight_change = weight - first_entry['weight']
                days_elapsed = (datetime.fromisoformat(date) - 
                               datetime.fromisoformat(first_entry['date'])).days
                
                analysis = {
                    "total_weight_change": round(weight_change, 2),
                    "days_tracked": days_elapsed,
                    "avg_weekly_change": round((weight_change / days_elapsed) * 7, 2) if days_elapsed > 0 else 0,
                    "trend": "gaining" if weight_change > 0 else "losing" if weight_change < 0 else "maintaining",
                    "entries_count": len(history)
                }
            else:
                analysis = {
                    "message": "First entry recorded. Keep tracking!",
                    "entries_count": 1
                }
            
            return {
                "current_entry": progress_entry,
                "analysis": analysis,
                "history_summary": {
                    "total_entries": len(history),
                    "date_range": f"{history[-1]['date']} to {history[0]['date']}" if len(history) > 1 else date
                }
            }
        
        return Tool(
            name="progress_tracker",
            description="Track daily progress with measurements and images",
            function=track_progress,
            parameters={
                "user_id": {"type": "string", "description": "Unique user identifier"},
                "date": {"type": "string", "description": "Date of measurement (YYYY-MM-DD)"},
                "weight": {"type": "number", "description": "Current weight in kg"},
                "body_measurements": {"type": "object", "description": "Body measurements dict"},
                "progress_image": {"type": "string", "description": "Optional base64 progress photo"}
            }
        )
    
    def create_web_search_tool(self) -> Tool:
        """Tool to search for nutrition info, exercises, etc."""
        def search_fitness_info(query: str, category: str) -> Dict:
            """
            Search for fitness-related information
            category: nutrition, exercises, supplements, research
            """
            # This would integrate with actual search API
            # For demo purposes, returning structured data
            
            return {
                "query": query,
                "category": category,
                "results": [
                    {
                        "title": f"Information about {query}",
                        "summary": "Detailed information would be retrieved from search API",
                        "source": "Fitness Database"
                    }
                ]
            }
        
        return Tool(
            name="fitness_search",
            description="Search for fitness information, exercises, nutrition data",
            function=search_fitness_info,
            parameters={
                "query": {"type": "string", "description": "Search query"},
                "category": {"type": "string", "description": "Search category"}
            }
        )
    
    def process_user_request(self, user_input: str, context: Dict = None) -> str:
        """Main method to process user requests through the agent"""
        
        # Add context if provided
        if context:
            user_input = f"User Context: {json.dumps(context)}\n\nUser Request: {user_input}"
        
        # Process through Strands agent
        response = self.agent.process(user_input)
        
        return response


# Example usage and testing
def main():
    """Example usage of FitGenius Agent"""
    
    # Initialize agent
    agent = FitGeniusAgent()
    
    # Example 1: Initial Assessment
    print("=== Example 1: Initial Fitness Assessment ===")
    user_context = {
        "name": "John",
        "age": 28,
        "gender": "male",
        "height_cm": 175,
        "weight_kg": 85,
        "goal": "weight_loss"
    }
    
    response = agent.process_user_request(
        "I want to lose weight and get fit. Can you analyze my current state and create a plan?",
        context=user_context
    )
    print(response)
    
    # Example 2: Generate workout plan
    print("\n=== Example 2: Workout Plan ===")
    response = agent.process_user_request(
        "Create a 4-day per week workout plan for weight loss. I'm a beginner with basic gym equipment."
    )
    print(response)
    
    # Example 3: Diet plan
    print("\n=== Example 3: Diet Plan ===")
    response = agent.process_user_request(
        "Generate a diet plan to help me lose 10kg. I'm moderately active and have no dietary restrictions."
    )
    print(response)
    
    # Example 4: Progress tracking
    print("\n=== Example 4: Track Progress ===")
    response = agent.process_user_request(
        "Track my progress: Today I weigh 83kg, waist is 90cm, chest is 100cm"
    )
    print(response)


if __name__ == "__main__":
    main()