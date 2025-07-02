import pandas as pd
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import numpy as np
import os

# --- 1. Load the data using pandas (External Information) ---
# Assuming the data is saved as 'cmdb_ci_computer.txt' in the same directory
# The first line of your source is the header, which is correctly identified.
try:
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))
    csv_path = os.path.join(BASE_DIR, 'app_modules', 'assets', 'data', 'cmdb_ci_computer.csv')
    df = pd.read_csv(csv_path, header=0)
    print("Data loaded successfully. First 5 rows:")
    print(df.head())
    print("\nColumn names:")
    print(df.columns.tolist())

except FileNotFoundError:
    print("Error: 'cmdb_ci_computer.txt' not found. Please make sure the file is in the correct directory.")
    # Exit or handle the error appropriately if the file isn't found
    exit()

# --- 2. Data Preprocessing (often done with pandas/scikit-learn before TensorFlow) (External Information) ---
# For a TensorFlow model, you'd typically need a clear input (features) and output (target).
# Let's imagine a hypothetical task: predict 'install_status' based on other features.

# Identify categorical and numerical features
categorical_features = ['asset', 'assigned_to', 'department', 'location',
                       'u_build_business_owner', 'u_build_deployment_type',
                       'u_build_primary_user', 'u_build_machine_use',
                       'u_build_site', 'u_build_use', 'hardware_substatus', 'u_primary_pc']
numerical_features = [] # No obvious numerical features in this dataset for direct calculation,
                       # but if there were, they would be listed here.

# The target variable we want to predict
target_variable = 'install_status'

# Fill 'Value Not Found' or empty strings with actual NaN for easier processing
df.replace('Value Not Found', np.nan, inplace=True)
df.replace('', np.nan, inplace=True) # Replace empty strings with NaN

# For simplicity, let's drop rows where the target is missing or if other key features are missing
# In a real scenario, you'd impute missing values or use more sophisticated handling.
df.dropna(subset=[target_variable] + categorical_features, inplace=True)


# Convert object columns to string type to handle mixed types gracefully
for col in df.columns:
    if df[col].dtype == 'object':
        df[col] = df[col].astype(str)

# Prepare features (X) and target (y)
X = df.drop(columns=['name', 'asset_tag', target_variable]) # 'name' and 'asset_tag' are usually identifiers, not features
y = df[target_variable]

# Encode categorical target variable (y)
label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(y)

# Use ColumnTransformer for one-hot encoding of categorical features
# Handle potential new categories in test set by setting handle_unknown='ignore'
preprocessor = ColumnTransformer(
    transformers=[
        ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)
    ],
    remainder='passthrough' # Keep other columns if any, though none are expected here
)

# Create a pipeline that first preprocesses, then potentially scales (not needed here)
# and then would feed into a model.
pipeline = Pipeline(steps=[('preprocessor', preprocessor)])

# Fit the preprocessor and transform X
X_processed = pipeline.fit_transform(X)

# Convert sparse matrix to dense array if necessary for TensorFlow
if hasattr(X_processed, 'toarray'):
    X_processed = X_processed.toarray()

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X_processed, y_encoded, test_size=0.2, random_state=42)

print(f"\nShape of processed features (X_train): {X_train.shape}")
print(f"Shape of target (y_train): {y_train.shape}")

# --- 3. Building a Simple TensorFlow Model (External Information) ---
# Now, you have numerical data (tensors in concept, here NumPy arrays) that TensorFlow can work with.
# The following is a basic example of a simple neural network for classification.

# Define the model using Keras (TensorFlow's high-level API)
model = tf.keras.Sequential([
    # Input layer with the number of features
    tf.keras.layers.Input(shape=(X_train.shape[1],)),
    # A dense (fully connected) hidden layer with ReLU activation
    tf.keras.layers.Dense(128, activation='relu'),
    # Another dense hidden layer
    tf.keras.layers.Dense(64, activation='relu'),
    # Output layer:
    # Use 'softmax' for multi-class classification
    # Use 'sigmoid' for binary classification
    # The number of units equals the number of unique classes in your target variable
    tf.keras.layers.Dense(len(label_encoder.classes_), activation='softmax')
])

# Compile the model
# 'adam' is a popular optimizer
# 'sparse_categorical_crossentropy' is used because y_train is integer-encoded, not one-hot encoded
model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

# Print a summary of the model architecture
print("\nTensorFlow Model Summary:")
model.summary()

# --- 4. Train the TensorFlow Model (External Information) ---
print("\nTraining the TensorFlow model (this might take a moment)...")
history = model.fit(X_train, y_train, epochs=10, validation_split=0.1, verbose=0) # verbose=0 to suppress per-epoch output

print("Model training complete.")
print(f"Final training accuracy: {history.history['accuracy'][-1]:.4f}")
print(f"Final validation accuracy: {history.history['val_accuracy'][-1]:.4f}")

# --- 5. Evaluate the Model (External Information) ---
loss, accuracy = model.evaluate(X_test, y_test, verbose=0)
print(f"\nModel evaluation on test set:")
print(f"Test Loss: {loss:.4f}")
print(f"Test Accuracy: {accuracy:.4f}")

# --- 6. Make Predictions (External Information) ---
# You can use the trained model to make predictions on new data.
# Let's predict on the first few test samples
predictions = model.predict(X_test[:5])
predicted_classes = np.argmax(predictions, axis=1)

print("\nSample Predictions:")
for i in range(len(predicted_classes)):
    original_status = label_encoder.inverse_transform([y_test[i]])
    predicted_status = label_encoder.inverse_transform([predicted_classes[i]])
    print(f"Actual: {original_status}, Predicted: {predicted_status}")