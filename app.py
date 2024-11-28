import streamlit as st
import pandas as pd
import pickle
df = pd.DataFrame()

# Load the trained model and scaler
model = pickle.load(open('linear_model.pkl', 'rb'))
scaler = pickle.load(open('scaler.pkl', 'rb'))
encoder = pickle.load(open('encoder.pkl','rb'))

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
#categorical_features = ['job', 'marital', 'contact', 'poutcome']
#encoder = OneHotEncoder(sparse_output=False, handle_unknown='ignore')  # sparse=False for streamlit compatibility
#encoded_features = encoder.transform(df[categorical_features])
#encoded_df = pd.DataFrame(encoded_features, columns=encoder.get_feature_names_out(categorical_features))
#encoded_df = encoded_df.drop(['job', 'marital','contact','poutcome'], axis=1)


new_data = {'job': df['job'], 'marital': df['marital'], 'contact': df['contact'], 'poutcome': df['poutcome']}  
new_data_df = pd.DataFrame(new_data)

# Transform the categorical features in the new data
encoded_features = encoder.transform(new_data_df[['job', 'marital', 'contact', 'poutcome']])

# Create a DataFrame from the encoded features
encoded_features_df = pd.DataFrame(encoded_features.toarray(), 
                                     columns=encoder.get_feature_names_out(['job', 'marital', 'contact', 'poutcome']))

# Concatenate the encoded features with the rest of the new data
# Assuming your original new_data_df has other numerical features
encoded_df= pd.concat([new_data_df, encoded_features_df], axis=1)


# Concatenate numerical and encoded features
input_df = pd.concat([df, encoded_df], axis=1)
input_df  = input_df.drop(['job', 'marital', 'contact', 'poutcome'], axis=1)
input_df.columns
input_df.shape

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
