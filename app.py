import pandas as pd
import scipy.stats
import streamlit as st
import time

# Estas son variables de estado que se conservan cuando Streamlit vuelve a ejecutar este script
if 'experiment_no' not in st.session_state:
    st.session_state['experiment_no'] = 0

if 'df_experiment_results' not in st.session_state:
    st.session_state['df_experiment_results'] = pd.DataFrame(columns=['número de volado', 'iteraciones o repeticiones', 'media o promedio'])

st.header('Volado')

chart = st.line_chart([0.5])

def toss_coin(n):
    # Realiza los lanzamientos de la moneda y calcula los promedios en tiempo real
    trial_outcomes = scipy.stats.bernoulli.rvs(p=0.5, size=n)
    cumulative_sum = 0
    means = []

    for i, outcome in enumerate(trial_outcomes, 1):
        cumulative_sum += outcome
        mean = cumulative_sum / i
        means.append(mean)
        chart.add_rows([mean])
        time.sleep(0.05)
    
    return mean

number_of_trials = st.slider('¿Número de intentos?', 1, 1000, 10)
start_button = st.button('Ejecutar')

if start_button:
    st.write(f'Experimento con {number_of_trials} intentos en curso.')
    st.session_state['experiment_no'] += 1
    mean = toss_coin(number_of_trials)
    st.session_state['df_experiment_results'] = pd.concat([
        st.session_state['df_experiment_results'],
        pd.DataFrame(data=[[st.session_state['experiment_no'],
                            number_of_trials,
                            mean]],
                     columns=['número de volado', 'iteraciones o repeticiones', 'media o promedio'])
        ],
        axis=0)
    st.session_state['df_experiment_results'] = st.session_state['df_experiment_results'].reset_index(drop=True)

st.write(st.session_state['df_experiment_results'])
