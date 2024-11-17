import streamlit as st
import pickle
import pandas as pd

# Cargar el modelo y el escalador desde archivos
with open('linear_model.pkl', 'rb') as model_file:
    model = pickle.load(model_file)

with open('scaler.pkl', 'rb') as scaler_file:
    scaler = pickle.load(scaler_file)

# Título de la aplicación
st.title('Predicció de Contraccio de Diposit (Regresión Logistica)')

# Entrada de datos del usuario
age = st.number_input('Age', min_value=18, max_value=120)
job = st.selectbox('Job', ['admin.', 'blue-collar', 'entrepreneur', 'housemaid', 'management', 'retired', 'self-employed', 'services', 'student', 'technician', 'unemployed', 'unknown'])
marital = st.selectbox('Marital', ['divorced', 'married', 'single', 'unknown'], index=2)
education = st.selectbox('Education', ['primary', 'secondary', 'tertiary','unknown'])
housing = st.selectbox('Housing', ['no', 'yes'])
loan = st.selectbox('Loan', ['no', 'yes'])
month = st.selectbox('Month', ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec'])
balance = st.number_input('Balance', min_value=0)
duration = st.number_input('Duration', min_value=0)
campaign = st.number_input('Campaign', min_value=0)
previous = st.selectbox('Previous', ['no', 'yes'])

# Crear un DataFrame con las entradas
user_data = pd.DataFrame({
    'age': [age],
    'job': [job],
    'marital': [marital],
    'education' : [education],
    'housing' : [housing],
    'loan' : [loan],
    'month' : [month],
    'balance' : [balance],
    'duration' : [duration],
    'campaign' : [campaign],
    'previous' : [previous]
})

# Estandarizar las entradas
user_data_standardized = scaler.transform(user_data)

# Realizar la predicción
prediction = model.predict(user_data_standardized)

# Mostrar la predicción
st.write(f'Predicción: {prediction[0]:.2f}')