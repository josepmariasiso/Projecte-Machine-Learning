import streamlit as st
import pandas as pd
import pickle
from sklearn.preprocessing import OneHotEncoder
df = pd.DataFrame()

# Load the trained model and scaler
model = pickle.load(open('linear_model.pkl', 'rb'))
scaler = pickle.load(open('scaler.pkl', 'rb'))
encoder = pickle.load(open('encoder.pkl','rb'))

# Create the Streamlit app
st.title('Bank Deposit Prediction ML BarcelonaActiva')
col1, col2 = st.columns(2)
age = col1.number_input("Age", min_value=18, max_value=120)
job = col2.selectbox("Job", ['unknown','admin.', 'technician', 'services', 'management', 'retired',
       'blue-collar', 'unemployed', 'entrepreneur', 'housemaid',
        'self-employed', 'student'])
marital = col1.selectbox("Marital", ['married', 'single', 'divorced'])
education = col2.selectbox("Education",['unknown', 'primary', 'secondary', 'tertiary'])
balance = col1.number_input("Balance",value=0.00)
prev = col2.number_input("Previous",value=0)
day = col1.number_input("Day", min_value=1, max_value=31)
month = col2.selectbox("Month", ['jan', 'feb','mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep','oct', 'nov', 'dec'] )
housing = col1.selectbox("Housing", ['yes','no'])
loan = col2.selectbox("Loan", ['yes','no'])
campaign= col1.number_input("Campaign", min_value=1)
duration = col2.number_input("Duration", min_value=1)
contact = col1.selectbox("Contact", ['unknown', 'cellular', 'telephone'])
poutcome = col2.selectbox("Prev Outcome", ['unknown', 'failure', 'success', 'other'])


# Crear un DataFrame con las entradas
user_data = pd.DataFrame({
    'age': [age],
    'education': [education],
    'balance': [balance],
    'housing': [housing],
    'loan': [loan],
    'day': [day],
    'month': [month],
    'duration': [duration],
    'campaign': [campaign],
    'previous': [prev],
    'job': [job],
    'marital': [marital],
    'contact': [contact],
    'poutcome': [poutcome],
})

df = user_data.copy()

#reduim la dimensionalitat en totes les variable categoriques

#reduim les dimensions de job
valors= df['job'].isin(['admin.', 'management'])
df.loc[valors, 'job'] = 'qualified'
valors= df['job'].isin(['blue-collar', 'services','technician'])
df.loc[valors, 'job'] = 'semi-q'
valors= df['job'].isin(['entrepreneur', 'housemaid','self-employed'])
df.loc[valors, 'job'] = 'freelance'
valors= df['job'].isin(['unemployed', 'unknown', 'retired', 'student'])
df.loc[valors, 'job'] = 'others'
df['job'] = df['job'].astype('category')

# “calificado,” “semicalificado,” “no calificado,” “freelance/autónomos,” y “otros” (incluyendo desempleados, retirados, estudiantes y “unknown”)

#reduim les dimensions de marital
df['marital']=df['marital'].astype('category')

#reduim les dimensions de education // mapeigem ordenant per nivells
education_={'unknown':0,'primary':1,'secondary':2,'tertiary':3}
df['education']=df['education'].map(education_)

housing_={'yes':1,'no':0}
df['housing']=df['housing'].map(housing_)

loan_={'yes':1,'no':0}
df['loan']=df['loan'].map(loan_)

month_={'jan':1,'feb':2,'mar':3,'apr':4,'may':5,'jun':6,'jul':7,'aug':8,'sep':9,'oct':10,'nov':11,'dec':12}
df['month']=df['month'].map(month_)

#reduim les dimensions de contact
valor_others = df['contact'].isin(['unknown','telephone'])
df.loc[valor_others, 'contact'] = 'others'
df['contact']=df['contact'].astype('category')

#reduir les dimensions de poutcome
valor_others = df['poutcome'].isin(['unknown','other'])
df.loc[valor_others, 'poutcome'] = 'others'
df['poutcome']=df['poutcome'].astype('category')

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


# Scale numerical features
numerical_features = ['age', 'balance', 'day', 'duration', 'campaign', 'previous']
input_df[numerical_features] = scaler.transform(input_df[numerical_features])



# Make prediction
prediction = model.predict(input_df)[0]

# Display the prediction
if prediction == 1:
    st.success('El mes probable es que aquest client subscrigui el diposit.')
else:
    st.error('El mes probable es que aquest client NO subscrigui el diposit.')