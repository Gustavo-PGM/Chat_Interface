import tkinter as tk
from tkinter import scrolledtext, ttk
import requests
from bs4 import BeautifulSoup
import threading

# Função para buscar resposta na web usando a API do DuckDuckGo
def buscar_web_duckduckgo(pergunta):
    try:
        url = "https://api.duckduckgo.com"
        params = {
            "q": pergunta,
            "format": "json",
            "lang": "pt-br"  # Definindo o idioma da busca como Português Brasileiro
        }
        response = requests.get(url, params=params)
        if response.status_code == 200:
            resultados = response.json().get("AbstractText")
            if resultados:
                return resultados
        return None
    except Exception as e:
        print(f"Erro na busca web: {e}")
        return None

# Função para buscar resposta na web usando a API do Google
def buscar_web_google(pergunta):
    try:
        resposta_web = requests.get(f'https://www.google.com/search?q={pergunta}')
        soup = BeautifulSoup(resposta_web.text, 'html.parser')
        resultados = soup.find_all('div', class_='BNeawe')
        respostas = [resultado.get_text() for resultado in resultados if resultado.get_text() and 'Wikipédia' not in resultado.get_text()]
        return respostas
    except Exception as e:
        print(f"Erro na busca web: {e}")
        return None

# Função para enviar pergunta
def enviar_pergunta(event=None):
    pergunta = pergunta_entry.get().strip().lower()
    if pergunta:
        resposta_text.delete(1.0, tk.END)  # Limpa o campo de texto das respostas
        resposta_text.insert(tk.END, f"Você: {pergunta}\n", 'pergunta')
        
        resposta_text.insert(tk.END, "Chatbot: Pesquisando...\n\n", 'pesquisa')
        threading.Thread(target=buscar_e_responder, args=(pergunta,)).start()
            
        pergunta_entry.delete(0, tk.END)  # Limpa o campo de entrada

# Função para buscar e responder após pesquisa na web
def buscar_e_responder(pergunta):
    resposta_web = buscar_web_duckduckgo(pergunta)
    if not resposta_web:
        respostas_web = buscar_web_google(pergunta)
        if respostas_web:
            resposta_text.insert(tk.END, "Chatbot: Aqui estão algumas informações relevantes que encontrei:\n\n", 'resposta')
            for resposta in respostas_web:
                resposta_text.insert(tk.END, f"- {resposta}\n\n", 'resposta')
        else:
            resposta_text.insert(tk.END, "Chatbot: Desculpe, não consegui encontrar uma resposta para essa pergunta.\n\n", 'resposta')
    else:
        resposta_text.insert(tk.END, f"Chatbot: {resposta_web}\n\n", 'resposta')

# Função principal do chatbot
def chatbot():
    root = tk.Tk()
    root.title("Chatbot")

    style = ttk.Style()
    style.configure('TFrame', background='#333333')
    style.configure('TButton', background='#0078D7', foreground='white')
    style.configure('TLabel', background='#333333', foreground='white')
    style.configure('TScrolledText', background='#FFFFFF', foreground='#333333')

    frame = ttk.Frame(root)
    frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

    global pergunta_entry, resposta_text
    pergunta_entry = ttk.Entry(frame)
    pergunta_entry.grid(row=0, column=0, padx=10, pady=10, sticky=(tk.W, tk.E))
    pergunta_entry.focus()
    pergunta_entry.bind("<Return>", enviar_pergunta)  # Associa a tecla "Enter" à função enviar_pergunta

    enviar_button = ttk.Button(frame, text="Enviar", command=enviar_pergunta)
    enviar_button.grid(row=0, column=1, padx=10, pady=10, sticky=tk.E)

    resposta_text = scrolledtext.ScrolledText(frame, wrap=tk.WORD, width=60, height=20)
    resposta_text.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky=(tk.W, tk.E))

    resposta_text.tag_config('pergunta', foreground='#000000')  # Define a cor da pergunta como preto
    resposta_text.tag_config('pesquisa', foreground='#555555')  # Define a cor do texto de pesquisa como cinza escuro
    resposta_text.tag_config('resposta', foreground='#000000')  # Define a cor da resposta como preto

    root.mainloop()

chatbot()