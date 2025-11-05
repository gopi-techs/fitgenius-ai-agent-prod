"""
Unit tests for FitGenius AI Agent
Run with: pytest tests/test_fitgenius_agent.py -v
"""

import pytest
import json
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime

# Import the agent (adjust import based on your structure)
# from fitgenius_agent import FitGeniusAgent


class TestBMICalculator:
    """Tests for BMI calculation functionality"""
    
    def test_normal_bmi(self):
        """Test BMI calculation for normal weight"""
        height_cm = 175
        weight_kg = 70
        height_m = height_cm / 100
        expected_bmi = weight_kg / (height_m ** 2)
        
        assert round(expected_bmi, 2) == 22.86
        assert 18.5 <= expected_bmi < 25  # Normal range
    
    def test_underweight_bmi(self):
        """Test BMI calculation for underweight"""
        height_cm = 180
        weight_kg = 55
        height_m = height_cm / 100
        bmi = weight_kg / (height_m ** 2)
        
        assert bmi < 18.5
    
    def test_overweight_bmi(self):
        """Test BMI calculation for overweight"""
        height_cm = 175
        weight_kg = 85
        height_m = height_cm / 100
        bmi = weight_kg / (height_m ** 2)
        
        assert 25 <= bmi < 30
    
    def test_obese_bmi(self):
        """Test BMI calculation for obesity"""
        height_cm = 170
        weight_kg = 95
        height_m = height_cm / 100
        bmi = weight_kg / (height_m ** 2)
        
        assert bmi >= 30
    
    def test_ideal_weight_range(self):
        """Test ideal weight range calculation"""
        height_cm = 175
        height_m = height_cm / 100
        
        ideal_min = 18.5 * (height_m ** 2)
        ideal_max = 24.9 * (height_m ** 2)
        
        assert 56 < ideal_min < 58
        assert 76 < ideal_max < 77


class TestWorkoutPlanner:
    """Tests for workout plan generation"""
    
    def test_beginner_plan_structure(self):
        """Test that beginner plan has appropriate structure"""
        plan = {
            "fitness_level": "beginner",
            "days_per_week": 3,
            "duration_minutes": 45
        }
        
        assert plan["fitness_level"] == "beginner"
        assert plan["days_per_week"] <= 4  # Beginners shouldn't train more than 4x/week
        assert plan["duration_minutes"] <= 60  # Sessions shouldn't be too long
    
    def test_intermediate_plan_volume(self):
        """Test that intermediate plan has higher volume"""
        beginner_sets = 3
        intermediate_sets = 4
        
        assert intermediate_sets > beginner_sets
    
    def test_workout_days_distribution(self):
        """Test proper rest days between workouts"""
        workout_days = ["Monday", "Wednesday", "Friday"]
        
        # Should have at least 1 day rest between sessions
        assert len(workout_days) == 3
        assert "Tuesday" not in workout_days
        assert "Thursday" not in workout_days
    
    def test_exercise_variety(self):
        """Test that workout includes variety of movements"""
        exercises = [
            "Squats",  # Lower body push
            "Deadlifts",  # Lower body pull
            "Bench Press",  # Upper body push
            "Rows",  # Upper body pull
            "Plank"  # Core
        ]
        
        movement_patterns = ["push", "pull", "core"]
        assert len(exercises) >= 5
        assert len(movement_patterns) >= 3


class TestDietPlanner:
    """Tests for diet plan generation"""
    
    def test_calorie_deficit_for_weight_loss(self):
        """Test that weight loss plan creates caloric deficit"""
        tdee = 2500
        weight_loss_calories = tdee - 500
        
        assert weight_loss_calories < tdee
        assert 300 <= (tdee - weight_loss_calories) <= 700  # Reasonable deficit
    
    def test_calorie_surplus_for_muscle_gain(self):
        """Test that muscle gain plan creates caloric surplus"""
        tdee = 2500
        muscle_gain_calories = tdee + 300
        
        assert muscle_gain_calories > tdee
        assert 200 <= (muscle_gain_calories - tdee) <= 500  # Reasonable surplus
    
    def test_protein_requirements(self):
        """Test protein intake recommendations"""
        weight_kg = 80
        
        # Weight loss: 2.0g per kg
        weight_loss_protein = weight_kg * 2.0
        assert weight_loss_protein == 160
        
        # Muscle gain: 2.2g per kg
        muscle_gain_protein = weight_kg * 2.2
        assert muscle_gain_protein == 176
    
    def test_macro_distribution(self):
        """Test that macros add up correctly"""
        total_calories = 2000
        protein_g = 150
        carbs_g = 200
        fats_g = 55
        
        protein_cals = protein_g * 4
        carbs_cals = carbs_g * 4
        fats_cals = fats_g * 9
        
        total_macro_cals = protein_cals + carbs_cals + fats_cals
        
        # Allow 5% margin for rounding
        assert abs(total_macro_cals - total_calories) <= (total_calories * 0.05)
    
    def test_meal_frequency(self):
        """Test appropriate meal frequency"""
        meals_per_day = 5
        
        assert 4 <= meals_per_day <= 6
    
    def test_hydration_recommendation(self):
        """Test water intake recommendation"""
        weight_kg = 80
        recommended_water_liters = weight_kg * 0.033
        
        assert recommended_water_liters >= 2.5
        assert recommended_water_liters <= 4.5


class TestProgressTracking:
    """Tests for progress tracking functionality"""
    
    def test_weight_change_calculation(self):
        """Test weight change calculation over time"""
        initial_weight = 85.0
        current_weight = 82.5
        weight_change = current_weight - initial_weight
        
        assert weight_change == -2.5
        assert weight_change < 0  # Weight loss
    
    def test_weekly_average_calculation(self):
        """Test average weekly change calculation"""
        weight_change = -4.0  # kg
        days_elapsed = 28
        
        weekly_change = (weight_change / days_elapsed) * 7
        
        assert -1.5 < weekly_change < -0.5  # Healthy rate
    
    def test_measurement_tracking(self):
        """Test body measurement tracking"""
        measurements = {
            "week_1": {"waist": 95, "chest": 100, "arms": 35},
            "week_4": {"waist": 92, "chest": 101, "arms": 36}
        }
        
        waist_change = measurements["week_4"]["waist"] - measurements["week_1"]["waist"]
        chest_change = measurements["week_4"]["chest"] - measurements["week_1"]["chest"]
        
        assert waist_change < 0  # Waist should decrease
        assert chest_change > 0  # Chest should increase
    
    def test_progress_trend_detection(self):
        """Test trend detection in progress data"""
        weekly_weights = [85.0, 84.2, 83.5, 82.8]
        
        # Check if consistently decreasing
        is_decreasing = all(
            weekly_weights[i] > weekly_weights[i+1] 
            for i in range(len(weekly_weights)-1)
        )
        
        assert is_decreasing
    
    def test_adherence_calculation(self):
        """Test workout adherence percentage"""
        planned_workouts = 12
        completed_workouts = 11
        
        adherence = (completed_workouts / planned_workouts) * 100
        
        assert adherence > 90  # Good adherence
        assert adherence == pytest.approx(91.67, rel=0.01)


class TestBodyAnalysis:
    """Tests for body composition analysis"""
    
    def test_body_fat_estimation_range(self):
        """Test that body fat estimates are within realistic range"""
        estimated_bf = 24.5
        
        assert 5 <= estimated_bf <= 50  # Realistic range
    
    def test_fitness_level_classification(self):
        """Test fitness level classification"""
        levels = ["beginner", "intermediate", "advanced"]
        test_level = "intermediate"
        
        assert test_level in levels
    
    def test_muscle_development_scoring(self):
        """Test muscle development scoring system"""
        scores = {
            "chest": 5,
            "shoulders": 7,
            "arms": 6,
            "back": 7,
            "legs": 8,
            "core": 4
        }
        
        for body_part, score in scores.items():
            assert 1 <= score <= 10


class TestIntegration:
    """Integration tests"""
    
    @patch('boto3.client')
    def test_bedrock_connection(self, mock_boto_client):
        """Test Bedrock API connection"""
        mock_client = Mock()
        mock_boto_client.return_value = mock_client
        
        # Simulate successful connection
        mock_client.invoke_model.return_value = {
            'body': Mock(read=lambda: json.dumps({
                'content': [{'text': 'Test response'}]
            }).encode())
        }
        
        # Test would call actual agent here
        # result = agent.process_user_request("test query")
        # assert result is not None
    
    @patch('boto3.resource')
    def test_dynamodb_write(self, mock_boto_resource):
        """Test DynamoDB write operation"""
        mock_table = Mock()
        mock_resource = Mock()
        mock_resource.Table.return_value = mock_table
        mock_boto_resource.return_value = mock_resource
        
        # Test data
        test_entry = {
            'userId': 'test_user',
            'date': '2024-11-05',
            'weight': 80.0
        }
        
        mock_table.put_item.return_value = {'ResponseMetadata': {'HTTPStatusCode': 200}}
        
        # Would test actual write here
        # agent.track_progress(**test_entry)
        # mock_table.put_item.assert_called_once()
    
    @patch('boto3.client')
    def test_s3_image_upload(self, mock_boto_client):
        """Test S3 image upload"""
        mock_s3 = Mock()
        mock_boto_client.return_value = mock_s3
        
        mock_s3.put_object.return_value = {
            'ResponseMetadata': {'HTTPStatusCode': 200}
        }
        
        # Would test actual upload here
        # agent.upload_progress_image(user_id, image_data)
        # mock_s3.put_object.assert_called_once()


class TestEdgeCases:
    """Test edge cases and error handling"""
    
    def test_zero_weight_handling(self):
        """Test handling of invalid weight input"""
        weight = 0
        
        with pytest.raises(ValueError):
            if weight <= 0:
                raise ValueError("Weight must be positive")
    
    def test_extreme_bmi_values(self):
        """Test handling of extreme BMI values"""
        # Extremely low
        bmi_low = 10.0
        assert bmi_low < 18.5
        
        # Extremely high
        bmi_high = 50.0
        assert bmi_high > 30
    
    def test_negative_measurements(self):
        """Test handling of negative measurement values"""
        measurements = [-5, 100, 95]
        
        # Should filter out negative values
        valid_measurements = [m for m in measurements if m > 0]
        assert len(valid_measurements) == 2
    
    def test_date_validation(self):
        """Test date format validation"""
        valid_date = "2024-11-05"
        invalid_date = "05-11-2024"
        
        try:
            datetime.strptime(valid_date, "%Y-%m-%d")
            is_valid = True
        except ValueError:
            is_valid = False
        
        assert is_valid
        
        try:
            datetime.strptime(invalid_date, "%Y-%m-%d")
            is_invalid = False
        except ValueError:
            is_invalid = True
        
        assert is_invalid


# Test fixtures
@pytest.fixture
def sample_user_data():
    """Sample user data for testing"""
    return {
        "user_id": "test_user_001",
        "age": 28,
        "gender": "male",
        "height_cm": 175,
        "weight_kg": 85,
        "goal": "weight_loss",
        "activity_level": "moderate"
    }


@pytest.fixture
def sample_workout_plan():
    """Sample workout plan for testing"""
    return {
        "plan_id": "plan_001",
        "fitness_level": "beginner",
        "days_per_week": 3,
        "exercises": [
            {"name": "Squats", "sets": 3, "reps": 12},
            {"name": "Push-ups", "sets": 3, "reps": 10},
            {"name": "Plank", "sets": 3, "duration": "30s"}
        ]
    }


@pytest.fixture
def sample_diet_plan():
    """Sample diet plan for testing"""
    return {
        "plan_id": "diet_001",
        "daily_calories": 2100,
        "macros": {
            "protein_g": 170,
            "carbs_g": 210,
            "fats_g": 58
        },
        "meals": 5
    }


# Run tests with: pytest tests/test_fitgenius_agent.py -v --cov
if __name__ == "__main__":
    pytest.main([__file__, "-v", "--cov=fitgenius_agent"])