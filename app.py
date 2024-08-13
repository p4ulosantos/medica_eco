import streamlit as st
import pandas as pd

# Funções de cálculo
def calcular_corp(peso, altura):
    altura_m = altura / 100  # Converter altura para metros
    return peso / (altura_m ** 2)

def calcular_relacao_septo_parede(septo, parede_posterior):
    return septo / parede_posterior

def calcular_espessura_relativa_parede(parede_posterior, diametro_diastolico):
    return (2 * parede_posterior) / diametro_diastolico

def calcular_volume(diametro):
    return (7 / (2.4 + diametro / 10)) * ((diametro / 10) ** 3)  # Converter mm para cm

def calcular_massa_ventricular(diametro_diastolico, septo, parede_posterior):
    diametro_diastolico_cm = diametro_diastolico / 10  # Converter mm para cm
    septo_cm = septo / 10  # Converter mm para cm
    parede_posterior_cm = parede_posterior / 10  # Converter mm para cm
    return 0.8 * (1.04 * ((diametro_diastolico_cm + parede_posterior_cm + septo_cm) ** 3 - diametro_diastolico_cm ** 3)) + 0.6

def calcular_indice_massa(massa_ventricular, corp):
    return massa_ventricular / corp

def calcular_fracao_ejecao(volume_diastolico_final, volume_sistolico_final):
    return ((volume_diastolico_final - volume_sistolico_final) / volume_diastolico_final) * 100

def calcular_fracao_encurtamento(diametro_diastolico, diametro_sistolico):
    return ((diametro_diastolico - diametro_sistolico) / diametro_diastolico) * 100

def calcular_relacao_atrio_aorta(diametro_atrio_esquerdo, diametro_aorta):
    return diametro_atrio_esquerdo / diametro_aorta

# Título
st.title('Cálculos de Ecocardiograma')

# Entrada de dados do usuário
peso = st.number_input('Peso (kg)', min_value=0.0, format="%.2f")
altura = st.number_input('Altura (cm)', min_value=0.0, format="%.2f")
diametro_diastolico = st.number_input('Diâmetro diastólico do ventrículo esquerdo (mm)', min_value=0.0, format="%.2f")
diametro_sistolico = st.number_input('Diâmetro sistólico do ventrículo esquerdo (mm)', min_value=0.0, format="%.2f")
septo = st.number_input('Septo interventricular (mm)', min_value=0.0, format="%.2f")
parede_posterior = st.number_input('Parede posterior (mm)', min_value=0.0, format="%.2f")
diametro_basal_vd = st.number_input('Diâmetro basal do ventrículo direito (mm)', min_value=0.0, format="%.2f")
diametro_medio_vd = st.number_input('Diâmetro médio do ventrículo direito (mm)', min_value=0.0, format="%.2f")
diametro_aorta = st.number_input('Diâmetro da raiz da aorta (mm)', min_value=0.0, format="%.2f")
diametro_atrio_esquerdo = st.number_input('Diâmetro do átrio esquerdo (mm)', min_value=0.0, format="%.2f")
volume_indexado_atrio = st.number_input('Volume indexado do átrio esquerdo (ml/m²)', min_value=0.0, format="%.2f")

# Botão para calcular
if st.button('Calcular'):
    corp = calcular_corp(peso, altura)
    volume_diastolico_final = calcular_volume(diametro_diastolico)
    volume_sistolico_final = calcular_volume(diametro_sistolico)
    relacao_septo_parede = calcular_relacao_septo_parede(septo, parede_posterior)
    espessura_relativa_parede = calcular_espessura_relativa_parede(parede_posterior, diametro_diastolico)
    massa_ventricular = calcular_massa_ventricular(diametro_diastolico, septo, parede_posterior)
    indice_massa = calcular_indice_massa(massa_ventricular, corp)
    fracao_ejecao = calcular_fracao_ejecao(volume_diastolico_final, volume_sistolico_final)
    fracao_encurtamento = calcular_fracao_encurtamento(diametro_diastolico, diametro_sistolico)
    relacao_atrio_aorta = calcular_relacao_atrio_aorta(diametro_atrio_esquerdo, diametro_aorta)
    
    # Criação do DataFrame para exibir resultados em formato de tabela
    resultados_ve = {
        'Parâmetro': ['Diâmetro diastólico', 'Diâmetro sistólico', 'Volume diastólico final', 'Volume sistólico final',
                      'Septo interventricular', 'Parede posterior', 'Relação septo/parede posterior', 'Espessura relativa de parede',
                      'Massa ventricular', 'Índice de massa', 'Fração de ejeção (Teicholz)', 'Fração de encurtamento'],
        'Valor': [f'{diametro_diastolico:.2f} mm', f'{diametro_sistolico:.2f} mm', f'{volume_diastolico_final:.2f} ml', f'{volume_sistolico_final:.2f} ml',
                  f'{septo:.2f} mm', f'{parede_posterior:.2f} mm', f'{relacao_septo_parede:.2f}', f'{espessura_relativa_parede:.2f}',
                  f'{massa_ventricular:.2f} g', f'{indice_massa:.2f} g/m²', f'{fracao_ejecao:.2f} %', f'{fracao_encurtamento:.2f} %']
    }

    resultados_vd = {
        'Parâmetro': ['Diâmetro basal do ventrículo direito', 'Diâmetro médio do ventrículo direito'],
        'Valor': [f'{diametro_basal_vd:.2f} mm', f'{diametro_medio_vd:.2f} mm']
    }

    resultados_aorta = {
        'Parâmetro': ['Diâmetro da raiz da aorta'],
        'Valor': [f'{diametro_aorta:.2f} mm']
    }

    resultados_atrio = {
        'Parâmetro': ['Diâmetro do átrio esquerdo', 'Volume indexado', 'Relação átrio esquerdo/aorta'],
        'Valor': [f'{diametro_atrio_esquerdo:.2f} mm', f'{volume_indexado_atrio:.2f} ml/m²', f'{relacao_atrio_aorta:.2f}']
    }
    
    df_ve = pd.DataFrame(resultados_ve)
    df_vd = pd.DataFrame(resultados_vd)
    df_aorta = pd.DataFrame(resultados_aorta)
    df_atrio = pd.DataFrame(resultados_atrio)

    # Exibindo resultados em tabelas
    st.subheader('Resultados:')
    
    st.write('**VENTRÍCULO ESQUERDO:**')
    st.table(df_ve)
    
    st.write('**VENTRÍCULO DIREITO:**')
    st.table(df_vd)
    
    st.write('**AORTA:**')
    st.table(df_aorta)
    
    st.write('**ÁTRIO ESQUERDO:**')
    st.table(df_atrio)
