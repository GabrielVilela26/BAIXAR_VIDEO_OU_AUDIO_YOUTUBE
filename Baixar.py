import tkinter as tk
import customtkinter as ctk
from pytube import YouTube
from tkinter import filedialog
import urllib.request
import io
from PIL import Image, ImageTk
import os

# Crie a janela principal da aplicação
app = ctk.CTk()
app.geometry('800x600')
app.title("Baixar Vídeo e Áudio")
app.resizable(False, False)

# Defina uma classe para organizar os frames na aplicação
class Frames:
    def __init__(self, app):
        # Crie frames para diferentes seções da aplicação
        self.frame1 = tk.Frame(app, bg='#242424')
        self.frame2 = tk.Frame(app, bd=1, bg='#000001', highlightbackground='#FFFFFF', highlightthickness=4)
        self.frame3 = tk.Frame(app, bd=4, bg='#242424')
        self.frame4 = tk.Frame(app, bg='#242424')
        self.frame5 = tk.Frame(app, bg='#242424')
        # Posicione os frames na janela da aplicação
        self.frame1.place(relx=0.005, rely=0.005, relwidth=0.99, relheight=0.15)
        self.frame2.place(relx=0.185, rely=0.17, width=609, height=343)
        self.frame3.place(relx=0.005, rely=0.635, relwidth=0.99, relheight=0.049)
        self.frame4.place(relx=0.005, rely=0.72, relwidth=0.99, relheight=0.10)
        self.frame5.place(relx=0.005, rely=0.825, relwidth=0.99, relheight=0.15)

# Inicialize os frames
frames = Frames(app)
filename = None  # Inicialize o nome do arquivo
video = None     # Inicialize o objeto de vídeo
warning_label = None  # Inicialize um rótulo de aviso (se necessário)

# Defina funções para criar botões, campos de entrada e rótulos
def criar_botoes(frames):
    # Crie o botão "Buscar"
    bt_buscar = tk.Button(frames.frame1, text='BUSCAR', font=('Arial', 10), command=buscar_video)
    bt_buscar.place(relx=0.43, rely=0.7, relwidth=0.15, relheight=0.3)

    # Crie o botão "Baixar Áudio"
    bt_mp3 = tk.Button(frames.frame5, text='Baixar Áudio', font=('Arial', 12), command=baixar_audio)
    bt_mp3.place(relx=0.182, rely=0.1, relwidth=0.13, relheight=0.4)

    # Crie o botão "Baixar Vídeo"
    bt_mp4 = tk.Button(frames.frame5, text='Baixar Vídeo', font=('Arial', 12), command=baixar_video)
    bt_mp4.place(relx=0.67, rely=0.1, relwidth=0.13, relheight=0.4)

    # Crie o botão "Diretório"
    bt_dir = tk.Button(frames.frame4, text='...', command=escolher_caminho)
    bt_dir.place(relx=0.77, rely=0.5, relwidth=0.03, relheight=0.45)

def criar_campos(frames):
    # Campo de entrada para o link
    global lblLink
    lblLink = tk.Entry(frames.frame1, width=67,  font=(20), bd=0.2, highlightbackground='#A4A5A6', highlightthickness=1)
    lblLink.focus()
    lblLink.place(relx=0.182, rely=0.35, relheight=0.26)

    # Campo de entrada para o diretório
    global lblDir
    lblDir = tk.Entry(frames.frame4, width=65, font=(20), bd=0.1, highlightbackground='#A4A5A6', highlightthickness=1)
    lblDir.place(relx=0.182, rely=0.5, relheight=0.45)

def criar_textos(frames):
    # Rótulos de texto
    tk.Label(frames.frame1, text="Insira o link do vídeo abaixo:", font=('Arial', 16),foreground='white', bg='#242424').place(relx=0.182, rely=0.01)
    tk.Label(frames.frame4, text="Escolha o diretório de destino:", font=('Arial', 16),foreground='white', bg='#242424').place(relx=0.182, rely=0.01)

def exibir_miniatura(video):
    # Exibir miniatura e nome
    try:
        thumbnail_url = video.thumbnail_url.replace("https://i.ytimg.com", "https://img.youtube.com")
        raw_data = urllib.request.urlopen(thumbnail_url).read()
        im = Image.open(io.BytesIO(raw_data))
        im = im.resize((609, 343))  # Redimensiona para o tamanho desejado
        img = ImageTk.PhotoImage(im)
        panel = tk.Label(frames.frame2, image=img)
        panel.image = img
        panel.pack(fill="both", expand=True)
    except Exception as e:
        print(e)

def limpar_widgets():
    # Destruir o conteúdo do frame2 (onde a imagem é exibida)
    for widget in frames.frame2.winfo_children():
        widget.destroy()

    # Destruir o título no frame3
    for widget in frames.frame3.winfo_children():
        widget.destroy()

    # Limpar o campo de diretório
    lblDir.delete(0, tk.END)

    # Destruir qualquer aviso anterior
    global warning_label
    if warning_label:
        warning_label.destroy()

def buscar_video():
    # Buscar vídeo
    limpar_widgets()
    global video, filename, warning_label
    try:
        video = YouTube(lblLink.get())
        exibir_miniatura(video)
        titulo = tk.Label(frames.frame3, text=f"{video.title}", font=('Arial', 18, 'bold'),foreground='white', bg='#474747', width=83)
        titulo.pack()

        # Remover caracteres inválidos do nome do arquivo
        filename = f'{video.title}'
        filename = filename.replace('|', '')  # Remove o caractere '|'

        if warning_label:
            warning_label.destroy()
    except Exception as e:
        mensagem_erro = "O vídeo não foi encontrado. Verifique o link e tente novamente."
        erro_label = tk.Label(frames.frame3, text=mensagem_erro, font=('Arial', 12, 'bold'), foreground='white', bg='#474747', width=83)
        erro_label.pack()
        warning_label = erro_label
        print(e)

def escolher_caminho():
    # Escolher diretório
    vDiretorio = filedialog.askdirectory(initialdir="/", title="Escolha a pasta")
    lblDir.delete(0, tk.END)
    lblDir.insert(0, vDiretorio)

def baixar_video():
    #Download do vídeo
    global video, warning_label
    try:
        vCaminho = lblDir.get()
        output_path = os.path.join(vCaminho, f'{filename}.mp4')

        # Verifica se o arquivo já existe no diretório
        if os.path.exists(output_path):
            if warning_label:
                warning_label.destroy()
            warning_label = tk.Label(frames.frame5, text="O arquivo de vídeo já existe.", font=('Arial', 12, 'bold'), foreground='white', bg='#474747')
            warning_label.place(relx=0.49, rely=0.6, anchor='center')
        else:
            video.streams.get_highest_resolution().download(output_path=vCaminho, filename=f'{filename}.mp4')

            if warning_label:
                warning_label.destroy()
            download_label = tk.Label(frames.frame5, text="Download de Vídeo Concluído!", font=('Arial', 12, 'bold'), foreground='white', bg='#474747')
            download_label.place(relx=0.49, rely=0.6, anchor='center')
    except Exception as e:
        if warning_label:
            warning_label.destroy()
        warning_label = tk.Label(frames.frame5, text="Não foi possível concluir o download! Verifique.", font=('Arial', 12, 'bold'), foreground='white', bg='#474747')
        warning_label.place(relx=0.5, rely=0.6, anchor='center')
        print(e)

def baixar_audio():
    # Download do áudio
    global video, warning_label
    try:
        vCaminho = lblDir.get()
        output_path = os.path.join(vCaminho, f'{filename}.mp3')

        # Verifica se o arquivo já existe no diretório
        if os.path.exists(output_path):
            if warning_label:
                warning_label.destroy()
            warning_label = tk.Label(frames.frame5, text="O arquivo de áudio já existe.", font=('Arial', 12, 'bold'), foreground='white', bg='#474747')
            warning_label.place(relx=0.49, rely=0.6, anchor='center')
        else:
            # Baixando áudio
            ys = video.streams.filter(only_audio=True, file_extension='mp4').first()
            if ys:
                ys.download(output_path=vCaminho, filename=f'{filename}.mp3')

                # Renomear o arquivo baixado para ter extensão .mp3
                downloaded_file_path = os.path.join(vCaminho, f'{filename}.mp3')
                new_file_path = os.path.join(vCaminho, f'{filename}.mp3')
                os.rename(downloaded_file_path, new_file_path)

                if warning_label:
                    warning_label.destroy()
                download_label = tk.Label(frames.frame5, text="Download de Áudio Concluído!", font=('Arial', 12, 'bold'), foreground='white', bg='#474747')
                download_label.place(relx=0.49, rely=0.6, anchor='center')
                warning_label = download_label
            else:
                if warning_label:
                    warning_label.destroy()
                warning_label = tk.Label(frames.frame5, text="Não foi possível concluir o download! Verifique.", font=('Arial', 12, 'bold'), foreground='white', bg='#474747')
                warning_label.place(relx=0.5, rely=0.6, anchor='center')
    except Exception as e:
        print(e)

# Crie os elementos da interface
criar_campos(frames)
criar_textos(frames)
criar_botoes(frames)

# Inicie a aplicação
app.mainloop()
