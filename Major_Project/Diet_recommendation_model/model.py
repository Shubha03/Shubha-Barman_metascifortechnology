import streamlit as st  
import pandas as pd  
import numpy as np  
from sklearn.model_selection import train_test_split  
from sklearn.preprocessing import StandardScaler, LabelEncoder  
from sklearn.ensemble import RandomForestClassifier  
import joblib  
import plotly.express as px  
import plotly.graph_objects as go  

class DietRecommendationSystem:  
    def __init__(self):  
        self.model = None  
        self.scaler = StandardScaler()  
        self.label_encoder = LabelEncoder()  

    def prepare_dataset(self):  
        # Synthetic dataset creation  
        np.random.seed(42)  
        data = {  
            'age': np.random.randint(18, 65, 1000),  
            'weight': np.random.uniform(50, 100, 1000),  
            'height': np.random.uniform(150, 190, 1000),  
            'activity_level': np.random.choice(['Sedentary', 'Moderate', 'Active'], 1000),  
            'health_goal': np.random.choice(['Weight Loss', 'Muscle Gain', 'Weight Maintenance'], 1000),  
            'gender': np.random.choice(['Male', 'Female'], 1000),  
            'diet_type': [  
                'Low Carb' if goal == 'Weight Loss' and activity == 'Moderate' else  
                'High Protein' if goal == 'Muscle Gain' and activity == 'Active' else  
                'Balanced' for goal, activity in zip(  
                    np.random.choice(['Weight Loss', 'Muscle Gain', 'Weight Maintenance'], 1000),  
                    np.random.choice(['Sedentary', 'Moderate', 'Active'], 1000)  
                )  
            ]  
        }  
        return pd.DataFrame(data)  

    def preprocess_data(self, data):  
        # Separate features and target  
        X = data.drop('diet_type', axis=1)  
        y = self.label_encoder.fit_transform(data['diet_type'])  

        # One-hot encode categorical variables  
        X = pd.get_dummies(X, columns=['activity_level', 'health_goal', 'gender'])  

        # Scale numerical features  
        numerical_cols = ['age', 'weight', 'height']  
        X[numerical_cols] = self.scaler.fit_transform(X[numerical_cols])  

        return X, y  

    def train_model(self):  
        # Create dataset  
        data = self.prepare_dataset()  

        # Preprocess data  
        X, y = self.preprocess_data(data)  

        # Split data  
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)  

        # Train Random Forest Classifier  
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)  
        self.model.fit(X_train, y_train)  

        # Model evaluation  
        accuracy = self.model.score(X_test, y_test)  
        st.write(f"Model Accuracy: {accuracy:.2f}")  

    def predict_diet(self, user_data):  
        # Preprocess user data  
        user_data_processed = pd.get_dummies(user_data)  

        # Ensure all columns from training are present  
        missing_cols = set(self.model.feature_names_in_) - set(user_data_processed.columns)  
        for col in missing_cols:  
            user_data_processed[col] = 0  

        # Reorder columns to match training data  
        user_data_processed = user_data_processed[self.model.feature_names_in_]  

        # Make prediction  
        prediction_encoded = self.model.predict(user_data_processed)  
        prediction = self.label_encoder.inverse_transform(prediction_encoded)  

        return prediction[0]  

def create_diet_plan(diet_type):  
    diet_plans = {  
        'Low Carb': {  
            'description': 'Focus on reducing carbohydrate intake',  
            'recommended_foods': ['Lean proteins', 'Vegetables', 'Healthy fats'],  
            'avoid_foods': ['Sugary foods', 'Bread', 'Pasta']  
        },  
        'High Protein': {  
            'description': 'Emphasis on protein-rich foods for muscle development',  
            'recommended_foods': ['Chicken', 'Fish', 'Eggs', 'Protein shakes'],  
            'avoid_foods': ['Processed foods', 'Excessive carbs']  
        },  
        'Balanced': {  
            'description': 'Balanced approach to nutrition',  
            'recommended_foods': ['Whole grains', 'Fruits', 'Vegetables', 'Lean proteins'],  
            'avoid_foods': ['Junk food', 'Excessive sugar']  
        }  
    }  
    return diet_plans.get(diet_type, {})  

def main():  
    st.set_page_config(page_title="Diet Recommendation", page_icon="🥗")  
    
    # Title and description  
    st.title("Diet Recommendation System")  
    st.write("Get personalized diet recommendations based on your profile!")  

    # Sidebar for user inputs  
    st.sidebar.header("Your Profile")  
    age = st.sidebar.slider("Age", 18, 65, 30)  
    weight = st.sidebar.slider("Weight (kg)", 40, 150, 70)  
    height = st.sidebar.slider("Height (cm)", 140, 220, 170)  
    
    gender = st.sidebar.selectbox("Gender", ["Male", "Female"])  
    activity_level = st.sidebar.selectbox(  
        "Activity Level",   
        ["Sedentary", "Moderate", "Active"]  
    )  
    health_goal = st.sidebar.selectbox(  
        "Health Goal",   
        ["Weight Loss", "Muscle Gain", "Weight Maintenance"]  
    )  

    # Create diet recommendation system  
    diet_system = DietRecommendationSystem()  
    diet_system.train_model()  

    # Prepare user data for prediction  
    user_data = pd.DataFrame({  
        'age': [age],  
        'weight': [weight],  
        'height': [height],  
        'gender': [gender],  
        'activity_level': [activity_level],  
        'health_goal': [health_goal]  
    })  

    # Prediction button  
    if st.sidebar.button("Get Diet Recommendation"):  
        try:  
            # Get diet recommendation  
            recommended_diet = diet_system.predict_diet(user_data)  
            
            # Display recommendation  
            st.success(f"Recommended Diet Plan: {recommended_diet}")  
            
            # Get detailed diet plan  
            diet_plan = create_diet_plan(recommended_diet)  
            
            # Create columns for diet details  
            col1, col2 = st.columns(2)  
            
            with col1:  
                st.subheader("Diet Description")  
                st.write(diet_plan.get('description', 'No description available'))  
                
                st.subheader("Recommended Foods")  
                for food in diet_plan.get('recommended_foods', []):  
                    st.markdown(f"✅ {food}")  
            
            with col2:  
                st.subheader("Foods to Avoid")  
                for food in diet_plan.get('avoid_foods', []):  
                    st.markdown(f"❌ {food}")  
            
            # Additional visualizations can be added here  
        
        except Exception as e:  
            st.error(f"Error generating recommendation: {e}")  

    # Optional: Add some educational content  
    st.sidebar.markdown("### 💡 Diet Tips")  
    st.sidebar.info(  
        "Remember:\n"  
        "- Stay hydrated\n"  
        "- Eat balanced meals\n"  
        "- Regular exercise\n"  
        "- Consult a nutritionist"  
    )  

if __name__ == "__main__":  
    main()