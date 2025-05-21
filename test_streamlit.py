import streamlit as st

st.title("Tes Streamlit")
st.write("Selamat datang di UI Chatbot!")
user_input = st.chat_input("Masukkan teks:")
if user_input:
    st.chat_message("user").markdown(user_input)
    st.chat_message("assistant").markdown(f"Kamu mengetik: {user_input}")