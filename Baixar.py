import tkinter as tk
import customtkinter as ctk
from tkinter import filedialog
import yt_dlp  # Importando a biblioteca yt-dlp
import os
from PIL import Image, ImageTk  # Importando para manipulação de imagens
import requests  # Importando a biblioteca requests

# Criação da janela principal da aplicação
app = ctk.CTk()
app.geometry('800x600')
app.title("Baixar Vídeo e Áudio")
app.resizable(False, False)

# Classe para organizar os frames da aplicação
class Frames:
    def __init__(self, app):
        self.frame1 = tk.Frame(app, bg='#242424')
        self.frame2 = tk.Frame(app, bd=1, bg='#000001', highlightbackground='#FFFFFF', highlightthickness=4)
        self.frame3 = tk.Frame(app, bd=4, bg='#242424')
        self.frame4 = tk.Frame(app, bg='#242424')
        self.frame5 = tk.Frame(app, bg='#242424')
        # Posicionamento dos frames
        self.frame1.place(relx=0.005, rely=0.005, relwidth=0.99, relheight=0.15)
        self.frame2.place(relx=0.185, rely=0.17, width=609, height=343)
        self.frame3.place(relx=0.005, rely=0.635, relwidth=0.99, relheight=0.049)
        self.frame4.place(relx=0.005, rely=0.72, relwidth=0.99, relheight=0.10)
        self.frame5.place(relx=0.005, rely=0.825, relwidth=0.99, relheight=0.15)

# Inicialização dos frames
frames = Frames(app)
filename = None
thumbnail_label = None
warning_label = None

# Definição dos botões, campos e rótulos
def criar_botoes(frames):
    bt_buscar = tk.Button(frames.frame1, text='BUSCAR', font=('Arial', 10), command=buscar_video)
    bt_buscar.place(relx=0.43, rely=0.7, relwidth=0.15, relheight=0.3)

    bt_mp3 = tk.Button(frames.frame5, text='Baixar Áudio', font=('Arial', 12), 
                       command=lambda: baixar_audio(lblLink.get(), lblDir.get()))
    bt_mp3.place(relx=0.182, rely=0.1, relwidth=0.13, relheight=0.4)

    bt_mp4 = tk.Button(frames.frame5, text='Baixar Vídeo', font=('Arial', 12), 
                       command=lambda: baixar_video(lblLink.get(), lblDir.get()))
    bt_mp4.place(relx=0.67, rely=0.1, relwidth=0.13, relheight=0.4)

    bt_dir = tk.Button(frames.frame4, text='...', command=escolher_caminho)
    bt_dir.place(relx=0.76, rely=0.5, relwidth=0.04, relheight=0.45)

def criar_campos(frames):
    global lblLink
    lblLink = tk.Entry(frames.frame1, width=55, font=(20), bd=0.2, highlightbackground='#A4A5A6', highlightthickness=1)
    lblLink.focus()
    lblLink.place(relx=0.182, rely=0.35, relheight=0.26)

    global lblDir
    lblDir = tk.Entry(frames.frame4, width=52, font=(20), bd=0.1, highlightbackground='#A4A5A6', highlightthickness=1)
    lblDir.place(relx=0.182, rely=0.5, relheight=0.45)

def criar_textos(frames):
    tk.Label(frames.frame1, text="Insira o link do vídeo abaixo:", font=('Arial', 16), foreground='white', bg='#242424').place(relx=0.182, rely=0.01)
    tk.Label(frames.frame4, text="Escolha o diretório de destino:", font=('Arial', 16), foreground='white', bg='#242424').place(relx=0.182, rely=0.01)

def limpar_widgets():
    for widget in frames.frame2.winfo_children():
        widget.destroy()

    for widget in frames.frame3.winfo_children():
        widget.destroy()

    global thumbnail_label
    if thumbnail_label:
        thumbnail_label.destroy()

    lblDir.delete(0, tk.END)

    global warning_label
    if warning_label:
        warning_label.destroy()

def buscar_video():
    limpar_widgets()
    global filename, warning_label, thumbnail_label
    url = lblLink.get().strip()
    if not url:
        exibir_mensagem("Por favor, insira um link válido.", frames.frame3)
        return

    try:
        with yt_dlp.YoutubeDL() as ydl:
            info = ydl.extract_info(url, download=False)
            filename = info['title'].replace('|', '').replace('/', '').replace('\\', '')
            titulo = tk.Label(frames.frame3, text=filename, font=('Arial', 18, 'bold'), foreground='white', bg='#474747', width=83)
            titulo.pack()

            # Obtendo a URL da miniatura
            thumbnail_url = info.get('thumbnail')
            if thumbnail_url:
                exibir_miniatura(thumbnail_url)

    except Exception as e:
        exibir_mensagem("Vídeo não encontrado. Verifique o link e tente novamente.", frames.frame3)
        print(e)

def exibir_mensagem(mensagem, frame):
    global warning_label
    if warning_label:
        warning_label.destroy()
    warning_label = tk.Label(frame, text=mensagem, font=('Arial', 12, 'bold'), foreground='white', bg='#474747')
    warning_label.place(relx=0.5, rely=0.5, anchor='center')  # Nova posição para a mensagem

def exibir_miniatura(url):
    global thumbnail_label
    if thumbnail_label:
        thumbnail_label.destroy()

    # Baixando a miniatura
    image = Image.open(requests.get(url, stream=True).raw)
    thumbnail = ImageTk.PhotoImage(image)

    thumbnail_label = tk.Label(frames.frame2, image=thumbnail)
    thumbnail_label.image = thumbnail  # Referência para evitar coleta de lixo
    thumbnail_label.pack()

def escolher_caminho():
    vDiretorio = filedialog.askdirectory(initialdir="/", title="Escolha a pasta")
    lblDir.delete(0, tk.END)
    lblDir.insert(0, vDiretorio)

def baixar_video(url, caminho):
    global warning_label
    try:
        output_path = os.path.join(caminho, f'{filename}.mp4')

        if os.path.exists(output_path):
            exibir_mensagem("O arquivo de vídeo já existe.", frames.frame5)
            return
        else:
            ydl_opts = {
                'format': 'bestvideo+bestaudio/best',
                'outtmpl': output_path,
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            exibir_mensagem("Download de Vídeo Concluído!", frames.frame5)
    except Exception as e:
        exibir_mensagem("Não foi possível concluir o download! Verifique.", frames.frame5)
        print(e)

def baixar_audio(url, caminho):
    global warning_label
    try:
        output_path = os.path.join(caminho, f'{filename}.mp3')

        if os.path.exists(output_path):
            exibir_mensagem("O arquivo de áudio já existe.", frames.frame5)
            return
        else:
            ydl_opts = {
                'format': 'bestaudio/best',
                'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': '192'}],
                'outtmpl': output_path
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            exibir_mensagem("Download de Áudio Concluído!", frames.frame5)
    except Exception as e:
        exibir_mensagem("Não foi possível concluir o download! Verifique.", frames.frame5)
        print(e)

# Chamadas para criar os botões, campos e textos
criar_botoes(frames)
criar_campos(frames)
criar_textos(frames)

# Inicie a interface gráfica
app.mainloop()
