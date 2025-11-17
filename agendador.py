import streamlit as st
from datetime import datetime
import json

def carregar_dados():
    try:
        with open('compromisso.json', 'r') as arquivo:
            st.session_state.compromisso = json.load(arquivo)
    except (FileNotFoundError, json.JSONDecodeError):
        st.session_state.compromisso = {}

def salvar_dados():
    with open('compromisso.json', 'w') as arquivo:
        json.dump(st.session_state.compromisso, arquivo, indent=4)

st.title("Agendador de Compromissos")

if 'compromisso' not in st.session_state:
    carregar_dados()

tab1, tab2, tab3 = st.tabs(
    ["Adicionar compromisso", "Visualizar compromissos", "Cancelar/editar compromissos"])

with tab1:
    st.header("Adicionar compromisso")
    nome = st.text_input("Nome do compromisso:")
    data = st.date_input("Data do compromisso:")
    hora = st.time_input("Hora do compromisso:")
    if st.button("Agendar"):
        if nome and data and hora:
            st.session_state.compromisso[nome]= {
            "data": str(data), "hora": str(hora)}
            salvar_dados()
            st.success(f"Compromisso '{nome}' agendado!")
        else:
            st.error("Preencha todos os campos corretamente.")
            
with tab2:
    st.header("Visualizar compromissos")
    if not st.session_state.compromisso:
        st.info("Nenhum compromisso agendado")
    else:
        compromissos_para_exibir = []
        for compromisso, dados in st.session_state.compromisso.items():
            compromissos_para_exibir.append({
                "Compromisso": compromisso,
                "Data": dados['data'],
                "Horário": dados['hora']
            })
        st.dataframe(compromissos_para_exibir, use_container_width=True)
        
with tab3:
    st.header("Cancelar/editar compromissos")
    if not st.session_state.compromisso:
        st.info("Nenhum compromisso agendado")
    else:
        compromissos_para_exibir = []
        for nome, dados in st.session_state.compromisso.items():
            compromissos_para_exibir.append({"Compromisso": nome, "Data": dados["data"], "Hora": dados["hora"]})
        st.dataframe(compromissos_para_exibir)
        nome_cancelar = st.text_input("Nome do compromisso a cancelar/editar:")
        if st.button("Cancelar compromisso"):
            if nome_cancelar in st.session_state.compromisso:
                del st.session_state.compromisso[nome_cancelar]
                salvar_dados()
                st.success(f"Compromisso '{nome_cancelar}' cancelado!")
            else:
                st.error("Compromisso não encontrado.")
        novo_nome = st.text_input("Novo nome do compromisso (deixe vazio para não alterar):")
        nova_data = st.date_input("Nova data do compromisso (deixe igual para não alterar):")
        nova_hora = st.time_input("Nova hora do compromisso (deixe igual para não alterar):")
        if st.button("Editar compromisso"):
            if nome_cancelar in st.session_state.compromisso:
                if novo_nome:
                    st.session_state.compromisso[novo_nome] = st.session_state.compromisso.pop(nome_cancelar)
                    nome_cancelar = novo_nome
                st.session_state.compromisso[nome_cancelar]["data"] = str(nova_data)
                st.session_state.compromisso[nome_cancelar]["hora"] = str(nova_hora)
                salvar_dados()
                st.success(f"Compromisso '{nome_cancelar}' editado!")
            else:
                st.error("Compromisso não encontrado.")