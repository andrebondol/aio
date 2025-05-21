import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup

# Fungsi untuk memuat data lokal
def load_data(filename="dataset.csv"):
    try:
        df = pd.read_csv(filename)
        return df["text"].dropna().tolist()
    except:
        return []

# Fungsi untuk memuat riwayat percakapan
def load_conversation(filename="conversation_history.csv"):
    try:
        df = pd.read_csv(filename)
        return df[["user_input", "response"]].dropna().to_dict("records")
    except:
        return []

# Fungsi untuk scraping online
def scrape_website(url):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        paragraphs = soup.find_all('p')
        texts = [para.get_text() for para in paragraphs if para.get_text()]
        return texts
    except:
        return []

# Fungsi untuk menyimpan percakapan
def save_conversation(user_input, response, filename="conversation_history.csv"):
    df = pd.DataFrame({"user_input": [user_input], "response": [response]})
    try:
        df.to_csv(filename, mode='a', header=not pd.io.common.file_exists(filename), index=False)
    except:
        pass

# Fungsi utama untuk memproses input
def process_user_input(user_input):
    # 1. Cari di riwayat percakapan
    conversations = load_conversation()
    for conv in conversations:
        if user_input.lower() in conv["user_input"].lower():
            return conv["response"]

    # 2. Cari di dataset lokal
    texts = load_data()
    for text in texts:
        if user_input.lower() in text.lower():
            response = f"Ditemukan di data lokal: {text[:100]}"
            save_conversation(user_input, response)
            return response

    # 3. Scraping online
    url = "https://en.wikipedia.org/wiki/" + user_input.replace(" ", "_")
    scraped_data = scrape_website(url)
    if scraped_data:
        response = f"Ditemukan online: {scraped_data[0][:100]}"
        df = pd.DataFrame({"text": scraped_data})
        df.to_csv("dataset.csv", mode='a', header=not pd.io.common.file_exists("dataset.csv"), index=False)
        save_conversation(user_input, response)
        return response

    # 4. Default
    response = "Maaf, saya tidak menemukan informasi tentang itu."
    save_conversation(user_input, response)
    return response

# UI Streamlit mirip ChatGPT
st.title("AI Chatbot Cappuccino")
st.write("Tanyakan sesuatu, misalnya: 'Saya mau buat cappuccino'")

# Simpan riwayat percakapan di session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Tampilkan riwayat percakapan
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input pengguna
user_input = st.chat_input("Masukkan pertanyaan:")
if user_input:
    # Tampilkan input pengguna
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Proses input dan tampilkan respons
    response = process_user_input(user_input)
    with st.chat_message("assistant"):
        st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})