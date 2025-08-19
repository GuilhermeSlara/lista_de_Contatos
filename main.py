import streamlit as st
import sqlite3
import pandas as pd
import re

# BANCO DE DADOS ----------------------------------------------------------------------------------------------------
con = sqlite3.connect("contatos.db")
banco = con.cursor()

# Criação da tabela (se não existir)
banco.execute("""
CREATE TABLE IF NOT EXISTS contatos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT,
    telefone TEXT,
    email TEXT
)
""")
con.commit()

# BARRA LATERAL -----------------------------------------------------------------------------------------------------
menu = st.sidebar.selectbox("Menu", ["Descrição","Adicionar", "Lista", "Atualizar", "Excluir",])


# DESCRIÇÃO --------------------------------------------------------------------------------------------------------------------

if menu == "Descrição":
    st.header("📱 Site Lista de Contatos")
    st.text("O Lista de Contatos é um aplicativo desenvolvido em Python com Streamlit e SQLite que tem como objetivo facilitar a organização de informações de pessoas de forma prática e intuitiva. Com ele, é possível: Adicionar contatos informando nome, telefone e e-mail, Listar contatos cadastrados, visualizando todos em ordem, Atualizar contatos existentes, alterando seus dados sem perder o histórico, Excluir contatos que não são mais necessários.")

# ADICINONAR ------------------------------------------------------------------------------------------------------------
Padrao_telefone = r"^\(?\d{2}\)?\s?\d{4,5}-?\d{4}$"

padrao_email = r"^\S+@\S+\.\S+$"

if menu == "Adicionar":
    st.header("📱 Adicionar Contato")
    st.subheader("Adicione os Dados seguintes para listar")
    nome = st.text_input("Nome")
    telefone = st.text_input("Telefone ex: xx xxxx-xxxx")
    email = st.text_input("Email")

    if st.button("Salvar"): 
        if not nome or not telefone or not email:
            st.warning("Preencha todos os dados")
        elif not re.match(Padrao_telefone,telefone):
            st.warning('Preencha o telefone de acordo com o padrão: xx xxxx-xxxx')
        elif not re.match(padrao_email, email):
            st.warning('Preencha o telefone de acordo com o padrão: usuario@dominio.com')
        else:
            banco.execute("INSERT INTO contatos (nome, telefone, email) VALUES (?, ?, ?)",
                    (nome, telefone, email))
            con.commit()
            st.success("Contato adicionado!")
    


# LISTA ---------------------------------------------------------------------------------------------------------------
elif menu == "Lista":
    st.header("📱 Lista de Contatos")
    dados = banco.execute("SELECT * FROM contatos").fetchall()
    df = pd.DataFrame(dados, columns=["ID", "Nome", "Telefone", "Email"])
    st.table(df)

# ATUALIZAR ----------------------------------------------------------------------------------------------------------------
elif menu == "Atualizar":
    st.header("📱 Atualizar Contato")
    st.subheader("Selecione o ID que queria atualizar")
    dados = banco.execute("SELECT * FROM contatos").fetchall()

    if dados:
        ids = [d[0] for d in dados]
        id_escolhido = st.selectbox("Escolha o ID", ids)
        contato = [d for d in dados if d[0] == id_escolhido][0]
        novo_nome = st.text_input("Nome", contato[1])
        novo_tel = st.text_input("Telefone", contato[2])
        novo_email = st.text_input("Email", contato[3])

        if st.button("Atualizar"):
            banco.execute("UPDATE contatos SET nome=?, telefone=?, email=? WHERE id=?",
                        (novo_nome, novo_tel, novo_email, id_escolhido))
            con.commit()
            st.success("Contato atualizado!")

# EXCLUIR --------------------------------------------------------------------------------------------------------------
elif menu == "Excluir":
    st.header("📱 Excluir Contato")
    st.subheader("Selecione o ID que queria Excluir")
    dados = banco.execute("SELECT * FROM contatos").fetchall()

    if dados:
        ids = [d[0] for d in dados]
        id_escolhido = st.selectbox("Escolha o ID", ids)

        if st.button("Excluir"):
            banco.execute("DELETE FROM contatos WHERE id=?", (id_escolhido,))
            con.commit()
            st.warning("Contato excluído!")
