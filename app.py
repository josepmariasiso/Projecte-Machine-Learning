import streamlit as st
import pandas as pd
import pickle
df = pd.DataFrame()

# Load the trained model and scaler
model = pickle.load(open('linear_model.pkl', 'rb'))
scaler = pickle.load(open('scaler.pkl', 'rb'))
encoder = pickle.load(open('enconder.pkl', 'rb'))

# Define the input features
features = ['age', 'job', 'marital', 'education', 'balance', 'housing', 'loan',
            'contact', 'day', 'month', 'duration', 'campaign', 'pdays',
            'previous', 'poutcome']

# Create the Streamlit app
st.title('Bank Deposit Prediction')

# Create input fields for each feature
input_data = {}
for feature in features:
    if feature in ['job', 'marital', 'education', 'contact', 'poutcome']:
        input_data[feature] = st.selectbox(feature, df[feature].unique())
    else:
        input_data[feature] = st.number_input(feature)

# Preprocess the input data
input_df = pd.DataFrame([input_data])

# Apply one-hot encoding to categorical features
categorical_features = ['job', 'marital', 'contact', 'poutcome']
##encoder = OneHotEncoder(sparse_output=False, handle_unknown='ignore')  # sparse=False for streamlit compatibility
encoded_features = encoder.transform(df[categorical_features])
encoded_df = pd.DataFrame(encoded_features, columns=encoder.get_feature_names_out(categorical_features))
encoded_df = encoded_df.drop(['job', 'marital','contact','poutcome'], axis=1)

# Concatenate numerical and encoded features
input_df = pd.concat([input_df, encoded_df], axis=1)

# Scale numerical features
numerical_features = ['age', 'balance', 'day', 'duration', 'campaign', 'previous']
input_df[numerical_features] = scaler.transform(input_df[numerical_features])

# Make prediction
prediction = model.predict(input_df)[0]

# Display the prediction
if prediction == 1:
    st.success('This customer is likely to subscribe to a term deposit.')
else:
    st.error('This customer is unlikely to subscribe to a term deposit.')
