#!/usr/bin/env python3
"""
FitGenius AI Agent - Interactive Demo
Run this in your AWS lab environment to showcase the agent's capabilities
"""

import json
import sys
from datetime import datetime
from typing import Dict

# Color codes for terminal output
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def print_header(text: str):
    """Print formatted header"""
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'='*60}")
    print(f"{text:^60}")
    print(f"{'='*60}{Colors.END}\n")


def print_section(title: str):
    """Print section divider"""
    print(f"\n{Colors.CYAN}{Colors.BOLD}▶ {title}{Colors.END}")
    print(f"{Colors.CYAN}{'─'*60}{Colors.END}")


def print_success(text: str):
    """Print success message"""
    print(f"{Colors.GREEN}✓ {text}{Colors.END}")


def print_info(text: str):
    """Print info message"""
    print(f"{Colors.BLUE}ℹ {text}{Colors.END}")


def print_result(data: Dict):
    """Print formatted result"""
    print(f"{Colors.YELLOW}{json.dumps(data, indent=2)}{Colors.END}")


def demo_1_bmi_calculator():
    """Demo: BMI Calculation and Health Assessment"""
    print_section("Demo 1: BMI Calculator & Health Assessment")
    
    print_info("Calculating BMI for a 28-year-old male...")
    print("  Height: 175 cm")
    print("  Weight: 85 kg")
    
    # Simulate BMI calculation
    height_m = 175 / 100
    bmi = 85 / (height_m ** 2)
    
    result = {
        "bmi": round(bmi, 2),
        "category": "Overweight",
        "health_risk": "Moderate",
        "ideal_weight_range": {
            "min": 56.6,
            "max": 76.3
        },
        "recommendation": "Consider a balanced diet and regular exercise to reach ideal weight"
    }
    
    print_result(result)
    print_success("BMI analysis complete!")


def demo_2_workout_plan():
    """Demo: Generate Personalized Workout Plan"""
    print_section("Demo 2: Personalized Workout Plan Generator")
    
    print_info("Generating 4-day workout plan for weight loss...")
    print("  Fitness Level: Beginner")
    print("  Goal: Weight Loss")
    print("  Available Equipment: Gym equipment")
    print("  Duration: 45 minutes per session")
    
    result = {
        "plan": [
            {
                "day": "Monday",
                "focus": "Full Body Circuit",
                "duration": "45 min",
                "exercises": [
                    {"name": "Treadmill Warm-up", "duration": "5 min", "intensity": "moderate"},
                    {"name": "Bodyweight Squats", "sets": 3, "reps": 15},
                    {"name": "Push-ups (modified)", "sets": 3, "reps": 10},
                    {"name": "Dumbbell Rows", "sets": 3, "reps": 12},
                    {"name": "Plank", "sets": 3, "duration": "30 sec"},
                    {"name": "Jump Rope", "sets": 3, "duration": "1 min"},
                    {"name": "Cool-down Stretch", "duration": "5 min"}
                ],
                "estimated_calories": 320
            },
            {
                "day": "Wednesday",
                "focus": "Cardio & Core",
                "duration": "45 min",
                "exercises": [
                    {"name": "Elliptical", "duration": "20 min", "intensity": "moderate-high"},
                    {"name": "Mountain Climbers", "sets": 3, "reps": 20},
                    {"name": "Russian Twists", "sets": 3, "reps": 30},
                    {"name": "Leg Raises", "sets": 3, "reps": 15},
                    {"name": "Burpees", "sets": 3, "reps": 10},
                    {"name": "Cool-down Walk", "duration": "5 min"}
                ],
                "estimated_calories": 380
            },
            {
                "day": "Friday",
                "focus": "Strength Training",
                "duration": "45 min",
                "exercises": [
                    {"name": "Bike Warm-up", "duration": "5 min"},
                    {"name": "Goblet Squats", "sets": 4, "reps": 12},
                    {"name": "Bench Press", "sets": 4, "reps": 10},
                    {"name": "Lat Pulldown", "sets": 3, "reps": 12},
                    {"name": "Shoulder Press", "sets": 3, "reps": 10},
                    {"name": "Core Circuit", "duration": "10 min"}
                ],
                "estimated_calories": 300
            },
            {
                "day": "Sunday",
                "focus": "Active Recovery",
                "duration": "30 min",
                "exercises": [
                    {"name": "Light Yoga", "duration": "20 min"},
                    {"name": "Walking", "duration": "20 min"},
                    {"name": "Stretching", "duration": "10 min"}
                ],
                "estimated_calories": 150
            }
        ],
        "weekly_calories_burned": 1150,
        "tips": [
            "Stay hydrated throughout workouts",
            "Focus on form over speed",
            "Rest 60-90 seconds between sets",
            "Track your progress weekly",
            "Adjust intensity based on how you feel"
        ]
    }
    
    print_result(result)
    print_success("Workout plan generated successfully!")


def demo_3_diet_plan():
    """Demo: Generate Personalized Diet Plan"""
    print_section("Demo 3: Personalized Nutrition Plan")
    
    print_info("Creating diet plan for weight loss...")
    print("  Current Weight: 85 kg")
    print("  Target Weight: 75 kg")
    print("  Activity Level: Moderate")
    print("  Goal: Lose 0.5 kg per week")
    
    result = {
        "daily_targets": {
            "calories": 2100,
            "protein_g": 170,
            "carbs_g": 210,
            "fats_g": 58,
            "fiber_g": 30,
            "water_liters": 3.5
        },
        "meal_plan": {
            "breakfast": {
                "time": "7:00 AM",
                "meal": "Oatmeal with Protein",
                "items": [
                    "Oats: 60g",
                    "Whey Protein: 30g",
                    "Blueberries: 100g",
                    "Almonds: 15g",
                    "Cinnamon: 1 tsp"
                ],
                "calories": 420,
                "protein_g": 35
            },
            "mid_morning_snack": {
                "time": "10:00 AM",
                "meal": "Greek Yogurt Bowl",
                "items": [
                    "Greek Yogurt: 200g",
                    "Mixed nuts: 20g",
                    "Honey: 1 tsp"
                ],
                "calories": 280,
                "protein_g": 22
            },
            "lunch": {
                "time": "1:00 PM",
                "meal": "Grilled Chicken Salad",
                "items": [
                    "Chicken breast: 150g",
                    "Mixed greens: 150g",
                    "Quinoa: 80g (cooked)",
                    "Olive oil: 1 tbsp",
                    "Vegetables: 200g"
                ],
                "calories": 520,
                "protein_g": 48
            },
            "afternoon_snack": {
                "time": "4:00 PM",
                "meal": "Protein Smoothie",
                "items": [
                    "Banana: 1 medium",
                    "Protein powder: 25g",
                    "Almond milk: 250ml",
                    "Spinach: 30g"
                ],
                "calories": 250,
                "protein_g": 28
            },
            "dinner": {
                "time": "7:00 PM",
                "meal": "Baked Salmon with Vegetables",
                "items": [
                    "Salmon: 180g",
                    "Sweet potato: 150g",
                    "Broccoli: 200g",
                    "Olive oil: 1 tsp"
                ],
                "calories": 580,
                "protein_g": 42
            },
            "evening_snack": {
                "time": "9:00 PM (optional)",
                "meal": "Cottage Cheese",
                "items": [
                    "Cottage cheese: 150g",
                    "Berries: 50g"
                ],
                "calories": 150,
                "protein_g": 20
            }
        },
        "supplements": [
            "Multivitamin (morning)",
            "Omega-3 Fish Oil (morning)",
            "Vitamin D3 (morning)",
            "Magnesium (evening)"
        ],
        "tips": [
            "Meal prep on Sundays for the week",
            "Drink water before each meal",
            "Track your meals for the first 2 weeks",
            "Allow one cheat meal per week",
            "Adjust portions based on hunger and progress"
        ],
        "expected_results": {
            "weekly_weight_loss": "0.4-0.6 kg",
            "time_to_goal": "15-20 weeks",
            "muscle_preservation": "High (due to adequate protein)"
        }
    }
    
    print_result(result)
    print_success("Diet plan created successfully!")


def demo_4_body_analysis():
    """Demo: Body Composition Analysis"""
    print_section("Demo 4: AI Body Composition Analysis")
    
    print_info("Analyzing body composition from uploaded image...")
    print("  Note: This would use Claude Vision API in production")
    
    # Simulated analysis result
    result = {
        "timestamp": datetime.now().isoformat(),
        "overall_assessment": {
            "fitness_level": "Beginner-Intermediate",
            "estimated_body_fat": "24-26%",
            "body_type": "Endomorph",
            "posture_score": "7/10"
        },
        "muscle_development": {
            "shoulders": {"rating": 6, "notes": "Moderate development, could be wider"},
            "chest": {"rating": 5, "notes": "Below average, needs focused work"},
            "arms": {"rating": 6, "notes": "Average development"},
            "core": {"rating": 4, "notes": "Weak core, visible fat layer"},
            "back": {"rating": 6, "notes": "Decent foundation"},
            "legs": {"rating": 7, "notes": "Good development"}
        },
        "problem_areas": [
            {
                "area": "Abdominal Region",
                "issue": "Excess fat storage",
                "recommendation": "Focus on diet, add HIIT cardio 3x/week"
            },
            {
                "area": "Posture",
                "issue": "Slight forward shoulder roll",
                "recommendation": "Add face pulls, band pull-aparts, and doorway stretches"
            },
            {
                "area": "Chest Development",
                "issue": "Underdeveloped pectorals",
                "recommendation": "Increase chest volume - 15-20 sets per week"
            }
        ],
        "strengths": [
            "Good leg development shows training history",
            "Shoulder structure has good potential",
            "Overall body symmetry is balanced"
        ],
        "action_plan": {
            "priority_1": "Reduce body fat through caloric deficit (500 cal/day)",
            "priority_2": "Add 3x weekly HIIT sessions (20-30 min)",
            "priority_3": "Focus on chest and core development",
            "priority_4": "Improve posture through targeted exercises"
        },
        "estimated_timeline": {
            "visible_changes": "4-6 weeks",
            "significant_transformation": "12-16 weeks",
            "goal_physique": "24-36 weeks"
        }
    }
    
    print_result(result)
    print_success("Body analysis complete!")


def demo_5_progress_tracking():
    """Demo: Progress Tracking System"""
    print_section("Demo 5: Progress Tracking & Analytics")
    
    print_info("Tracking progress over 4 weeks...")
    
    result = {
        "user_id": "demo_user_001",
        "tracking_period": "4 weeks",
        "measurements": [
            {
                "week": 1,
                "date": "2024-10-07",
                "weight_kg": 85.0,
                "waist_cm": 95.0,
                "chest_cm": 100.0,
                "arms_cm": 35.0,
                "workout_completion": "100%"
            },
            {
                "week": 2,
                "date": "2024-10-14",
                "weight_kg": 84.2,
                "waist_cm": 94.0,
                "chest_cm": 100.5,
                "arms_cm": 35.2,
                "workout_completion": "100%"
            },
            {
                "week": 3,
                "date": "2024-10-21",
                "weight_kg": 83.5,
                "waist_cm": 93.0,
                "chest_cm": 101.0,
                "arms_cm": 35.5,
                "workout_completion": "85%"
            },
            {
                "week": 4,
                "date": "2024-10-28",
                "weight_kg": 82.8,
                "waist_cm": 92.0,
                "chest_cm": 101.5,
                "arms_cm": 36.0,
                "workout_completion": "100%"
            }
        ],
        "analysis": {
            "total_weight_loss_kg": 2.2,
            "avg_weekly_loss_kg": 0.55,
            "waist_reduction_cm": 3.0,
            "chest_gain_cm": 1.5,
            "arms_gain_cm": 1.0,
            "trend": "Excellent progress - losing fat while gaining muscle"
        },
        "achievements": [
            "✓ Consistent 0.5kg/week weight loss",
            "✓ 3cm waist reduction",
            "✓ Muscle gain in upper body",
            "✓ 96% workout adherence"
        ],
        "recommendations": {
            "continue": [
                "Current diet strategy is working perfectly",
                "Workout intensity is appropriate",
                "Recovery appears adequate"
            ],
            "adjust": [
                "Consider adding 1 additional arm day",
                "Increase core work by 20%"
            ],
            "celebrate": [
                "You're in the top 10% for consistency!",
                "Fat loss while muscle gain is exceptional",
                "Keep up the amazing work!"
            ]
        },
        "next_4_weeks_projection": {
            "expected_weight": "80.0 kg",
            "expected_body_fat": "20-22%",
            "confidence": "High (based on current adherence)"
        }
    }
    
    print_result(result)
    print_success("Progress analysis complete!")


def demo_6_complete_transformation():
    """Demo: Complete 12-Week Transformation Plan"""
    print_section("Demo 6: Complete Transformation Journey")
    
    print_info("Creating comprehensive 12-week transformation plan...")
    
    result = {
        "program_overview": {
            "duration": "12 weeks",
            "goal": "Lose 10kg fat, gain 2kg muscle",
            "approach": "Progressive overload + Structured nutrition"
        },
        "phases": {
            "phase_1": {
                "weeks": "1-4",
                "focus": "Fat Loss Foundation",
                "workout_split": "Full body 4x/week",
                "cardio": "LISS 3x/week, 30min",
                "calories": 2100,
                "expected_weight_loss": "3-4 kg"
            },
            "phase_2": {
                "weeks": "5-8",
                "focus": "Fat Loss + Muscle Building",
                "workout_split": "Upper/Lower 4x/week",
                "cardio": "HIIT 2x/week, LISS 2x/week",
                "calories": 2200,
                "expected_weight_loss": "3-4 kg"
            },
            "phase_3": {
                "weeks": "9-12",
                "focus": "Muscle Definition",
                "workout_split": "Push/Pull/Legs 2x/week",
                "cardio": "HIIT 3x/week, 20min",
                "calories": 2300,
                "expected_weight_loss": "2-3 kg"
            }
        },
        "weekly_schedule_example": {
            "monday": "Push Day + HIIT",
            "tuesday": "Pull Day",
            "wednesday": "Legs + Core",
            "thursday": "Rest or Active Recovery",
            "friday": "Push Day",
            "saturday": "Pull Day + LISS",
            "sunday": "Rest"
        },
        "nutrition_strategy": {
            "protein_target": "2.2g per kg bodyweight",
            "meal_timing": "6 meals spread throughout day",
            "pre_workout": "Carbs + Caffeine",
            "post_workout": "Protein + Fast carbs",
            "cheat_meals": "1 per week"
        },
        "success_factors": [
            "Sleep 7-9 hours nightly",
            "Track all meals and workouts",
            "Weekly progress photos",
            "Bi-weekly body measurements",
            "Stay hydrated (4L+ water daily)",
            "Stress management crucial"
        ],
        "expected_results": {
            "week_4": {"weight": "82kg", "body_fat": "23%"},
            "week_8": {"weight": "79kg", "body_fat": "20%"},
            "week_12": {"weight": "75kg", "body_fat": "16-17%"}
        },
        "investment_required": {
            "time_per_week": "8-10 hours (workouts + meal prep)",
            "financial": "Gym membership + quality food + supplements",
            "mental": "High discipline and consistency"
        }
    }
    
    print_result(result)
    print_success("12-week transformation plan ready!")


def main():
    """Run all demos"""
    print_header("FitGenius AI Agent - Interactive Demo")
    
    print(f"{Colors.BOLD}This demo showcases the capabilities of the FitGenius AI Agent{Colors.END}")
    print("Built with AWS Strands Agents SDK and powered by Claude 3")
    print("\nFeatures demonstrated:")
    print("  1. BMI Calculator & Health Assessment")
    print("  2. Personalized Workout Plan Generation")
    print("  3. Custom Diet & Nutrition Planning")
    print("  4. AI Body Composition Analysis")
    print("  5. Progress Tracking & Analytics")
    print("  6. Complete Transformation Journey")
    
    input(f"\n{Colors.YELLOW}Press Enter to start the demo...{Colors.END}")
    
    try:
        # Run all demos
        demo_1_bmi_calculator()
        input(f"\n{Colors.YELLOW}Press Enter for next demo...{Colors.END}")
        
        demo_2_workout_plan()
        input(f"\n{Colors.YELLOW}Press Enter for next demo...{Colors.END}")
        
        demo_3_diet_plan()
        input(f"\n{Colors.YELLOW}Press Enter for next demo...{Colors.END}")
        
        demo_4_body_analysis()
        input(f"\n{Colors.YELLOW}Press Enter for next demo...{Colors.END}")
        
        demo_5_progress_tracking()
        input(f"\n{Colors.YELLOW}Press Enter for next demo...{Colors.END}")
        
        demo_6_complete_transformation()
        
        # Summary
        print_header("Demo Complete!")
        print(f"{Colors.GREEN}{Colors.BOLD}✓ All features demonstrated successfully!{Colors.END}\n")
        print("Next steps:")
        print("  1. Integrate with actual AWS Bedrock API")
        print("  2. Add real image analysis using Claude Vision")
        print("  3. Connect to DynamoDB for persistence")
        print("  4. Build a web or mobile interface")
        print("  5. Deploy to production")
        
        print(f"\n{Colors.CYAN}Thank you for trying FitGenius AI Agent!{Colors.END}")
        print(f"{Colors.CYAN}Visit the GitHub repository for full documentation.{Colors.END}\n")
        
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}Demo interrupted by user{Colors.END}")
        sys.exit(0)


if __name__ == "__main__":
    main()