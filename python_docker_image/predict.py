import pickle
import numpy as np

# Load the saved model
with open('linear_regression_model.pkl', 'rb') as file:
    loaded_model = pickle.load(file)

# Ask user for input (study hours)
new_data = float(input("Enter the number of study hours: "))

# Reshape the input to a 2D array (needed by the model)
new_data = np.array([[7.0]])  # Convert to a 2D array with shape (1, 1)

# Predict the score using the loaded model
predicted_score = loaded_model.predict(new_data)

#print(f'Predicted Score: {predicted_score[0]}')

