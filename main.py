# main.py
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import customtkinter as ctk
from pytubefix import YouTube, Playlist
from pytubefix.cli import on_progress
import yt_dlp
import os
import threading
from pathlib import Path
import re
from datetime import datetime
import subprocess
import sys

class VideoDownloader:
    def __init__(self):
        # Configurar tema do customtkinter
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Janela principal
        self.janela = ctk.CTk()
        self.janela.title("Video Downloader Pro")
        self.janela.geometry("700x700")
        self.janela.resizable(True, True)
        self.janela.minsize(600, 550)
        
        # Variáveis
        self.url_var = tk.StringVar()
        self.status_var = tk.StringVar(value="Aguardando...")
        self.plataforma = tk.StringVar(value="YouTube")
        self.qualidade = tk.StringVar(value="Melhor Qualidade")
        self.formato = tk.StringVar(value="MP4")
        self.pasta_download = tk.StringVar(value=str(Path.home() / "Downloads_Videos"))
        
        # CORRIGIDO: Ordem correta
        self.criar_pasta_download()  # 1º Criar pasta
        self.verificar_ffmpeg()      # 2º Verificar FFmpeg (cria a variável)
        self.criar_interface()       # 3º Criar interface (usa a variável)

        
    def verificar_ffmpeg(self):
        """Verifica se o FFmpeg está instalado"""
        try:
            subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
            self.ffmpeg_disponivel = True
        except (subprocess.CalledProcessError, FileNotFoundError):
            self.ffmpeg_disponivel = False
            print("FFmpeg não encontrado. Para baixar vídeos em 1080p+, instale o FFmpeg")
        
    def criar_pasta_download(self):
        """Cria a pasta de downloads se não existir"""
        Path(self.pasta_download.get()).mkdir(parents=True, exist_ok=True)
        
    def criar_interface(self):
        # Título
        titulo = ctk.CTkLabel(self.janela, text="🎥 Video Downloader Pro", 
                              font=("Arial", 28, "bold"))
        titulo.pack(pady=20)
        
        # Frame principal
        frame = ctk.CTkFrame(self.janela)
        frame.pack(padx=20, pady=10, fill="both", expand=True)
        
        # Grid layout
        frame.grid_columnconfigure(1, weight=1)
        
        # Seleção da plataforma
        plataforma_label = ctk.CTkLabel(frame, text="Plataforma:", font=("Arial", 14))
        plataforma_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        
        plataforma_menu = ctk.CTkOptionMenu(frame, values=["YouTube", "Instagram", "Twitter/X", "TikTok", "Facebook"],
                                           variable=self.plataforma,
                                           command=self.mudar_plataforma)
        plataforma_menu.grid(row=0, column=1, padx=10, pady=10, sticky="w")
        
        # URL do vídeo
        url_label = ctk.CTkLabel(frame, text="URL do Vídeo:", font=("Arial", 14))
        url_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")
        
        self.url_entry = ctk.CTkEntry(frame, width=400, textvariable=self.url_var,
                                      placeholder_text="Cole a URL aqui...")
        self.url_entry.grid(row=1, column=1, padx=10, pady=10, sticky="ew")
        
        # Frame de opções
        opcoes_frame = ctk.CTkFrame(frame)
        opcoes_frame.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="ew")
        opcoes_frame.grid_columnconfigure((0,1,2,3), weight=1)
        
        # Qualidade
        qualidade_label = ctk.CTkLabel(opcoes_frame, text="Qualidade:", font=("Arial", 12))
        qualidade_label.grid(row=0, column=0, padx=5, pady=5)
        
        qualidade_menu = ctk.CTkOptionMenu(opcoes_frame, 
                                          values=["Melhor Qualidade", "1080p", "720p", "480p", "360p", "Apenas Áudio"],
                                          variable=self.qualidade,
                                          command=self.mudar_qualidade)
        qualidade_menu.grid(row=1, column=0, padx=5, pady=5)
        
        # Formato
        formato_label = ctk.CTkLabel(opcoes_frame, text="Formato:", font=("Arial", 12))
        formato_label.grid(row=0, column=1, padx=5, pady=5)
        
        formato_menu = ctk.CTkOptionMenu(opcoes_frame, 
                                        values=["MP4", "MP3 (áudio)"],
                                        variable=self.formato,
                                        command=self.mudar_formato)
        formato_menu.grid(row=1, column=1, padx=5, pady=5)
        
        # Pasta de destino
        pasta_label = ctk.CTkLabel(opcoes_frame, text="Pasta:", font=("Arial", 12))
        pasta_label.grid(row=0, column=2, padx=5, pady=5)
        
        self.pasta_entry = ctk.CTkEntry(opcoes_frame, textvariable=self.pasta_download, width=150)
        self.pasta_entry.grid(row=1, column=2, padx=5, pady=5)
        
        pasta_btn = ctk.CTkButton(opcoes_frame, text="📁", width=40, 
                                 command=self.selecionar_pasta)
        pasta_btn.grid(row=1, column=3, padx=5, pady=5)
        
        # Checkbox para baixar playlist
        self.playlist_var = tk.BooleanVar()
        playlist_check = ctk.CTkCheckBox(frame, text="Baixar playlist completa", 
                                        variable=self.playlist_var)
        playlist_check.grid(row=3, column=0, columnspan=2, pady=10)
        
        # Checkbox para manter arquivos temporários
        self.manter_temp_var = tk.BooleanVar()
        manter_temp_check = ctk.CTkCheckBox(frame, text="Manter arquivos temporários (vídeo/áudio separados)", 
                                           variable=self.manter_temp_var)
        manter_temp_check.grid(row=4, column=0, columnspan=2, pady=5)
        
        # Botão de download
        self.download_btn = ctk.CTkButton(frame, text="⬇️ BAIXAR VÍDEO", 
                                         command=self.iniciar_download,
                                         height=45, width=250,
                                         font=("Arial", 15, "bold"))
        self.download_btn.grid(row=5, column=0, columnspan=2, pady=20)
        
        # Barra de progresso
        self.progresso = ttk.Progressbar(frame, length=500, mode='determinate')
        self.progresso.grid(row=6, column=0, columnspan=2, pady=10)
        
        # Status
        status_label = ctk.CTkLabel(frame, textvariable=self.status_var,
                                   font=("Arial", 12))
        status_label.grid(row=7, column=0, columnspan=2, pady=10)
        
        # Frame de informações
        info_frame = ctk.CTkFrame(self.janela)
        info_frame.pack(padx=20, pady=10, fill="x")
        
        ffmpeg_status = "✅ FFmpeg instalado" if self.ffmpeg_disponivel else "⚠️ FFmpeg NÃO instalado (necessário para 1080p+)"
        ffmpeg_color = "green" if self.ffmpeg_disponivel else "orange"
        
        info_text = ctk.CTkLabel(info_frame, 
                                text=f"📌 Suporte a múltiplas plataformas: YouTube, Instagram, Twitter, TikTok, Facebook\n"
                                     f"📌 Baixe vídeos em alta qualidade ou apenas áudio (MP3)\n"
                                     f"📌 Suporte a playlists do YouTube\n"
                                     f"📌 Escolha a pasta de destino\n"
                                     f"📌 Download em múltiplas threads (não trava a interface)\n"
                                     f"{ffmpeg_status}\n"
                                     f"⚠️ Instagram: Certifique-se que o perfil é público",
                                font=("Arial", 11), justify="left")
        info_text.pack(pady=10)
        
        # Rodapé
        rodape = ctk.CTkLabel(self.janela, text="Video Downloader Pro v2.0 | Requer FFmpeg para vídeos 1080p+", 
                             font=("Arial", 10), text_color="gray")
        rodape.pack(pady=5)
    
    def mudar_qualidade(self, choice):
        """Quando muda a qualidade, verifica necessidade do FFmpeg"""
        if choice in ["Melhor Qualidade", "1080p"] and not self.ffmpeg_disponivel:
            self.status_var.set("⚠️ Para 1080p+ é necessário instalar o FFmpeg!")
            
    def mudar_plataforma(self, choice):
        """Ajusta opções baseado na plataforma"""
        if choice == "YouTube":
            self.qualidade.set("Melhor Qualidade")
            self.formato.set("MP4")
        else:
            # Para outras plataformas, apenas MP3 e MP4 são suportados
            self.formato.set("MP4")
            
    def mudar_formato(self, choice):
        """Ajusta qualidade baseado no formato"""
        if choice == "MP3 (áudio)":
            self.qualidade.set("Apenas Áudio")
            
    def selecionar_pasta(self):
        """Abre diálogo para selecionar pasta"""
        pasta = filedialog.askdirectory(title="Selecione a pasta para salvar os vídeos")
        if pasta:
            self.pasta_download.set(pasta)
            self.criar_pasta_download()
            
    def atualizar_progresso(self, stream, chunk, bytes_remaining):
        """Atualiza barra de progresso para YouTube"""
        if hasattr(stream, 'filesize') and stream.filesize:
            total_size = stream.filesize
            bytes_downloaded = total_size - bytes_remaining
            percentage = (bytes_downloaded / total_size) * 100
            self.progresso['value'] = percentage
            self.status_var.set(f"Baixando... {percentage:.1f}%")
            self.janela.update_idletasks()
            
    def progresso_hook(self, d):
        """Hook de progresso para yt-dlp"""
        if d['status'] == 'downloading':
            if 'total_bytes' in d and d['total_bytes']:
                percentage = (d['downloaded_bytes'] / d['total_bytes']) * 100
                self.progresso['value'] = percentage
                self.status_var.set(f"Baixando... {percentage:.1f}%")
                self.janela.update_idletasks()
            elif 'total_bytes_estimate' in d:
                percentage = (d['downloaded_bytes'] / d['total_bytes_estimate']) * 100
                self.progresso['value'] = percentage
                self.status_var.set(f"Baixando... {percentage:.1f}%")
                self.janela.update_idletasks()
        elif d['status'] == 'finished':
            self.status_var.set("Processando arquivo...")
            self.janela.update_idletasks()
            
    def limpar_nome_arquivo(self, nome):
        """Remove caracteres inválidos do nome do arquivo"""
        nome = re.sub(r'[<>:"/\\|?*]', '', nome)
        nome = nome.strip()
        return nome[:200]
    
    def mesclar_video_audio(self, video_path, audio_path, output_path):
        """Mescla vídeo e áudio usando FFmpeg"""
        try:
            self.status_var.set("Mesclando vídeo e áudio...")
            # Comando FFmpeg para mesclar
            cmd = [
                'ffmpeg', '-i', video_path, '-i', audio_path,
                '-c:v', 'copy', '-c:a', 'aac', '-strict', 'experimental',
                output_path, '-y'  # -y para sobrescrever se existir
            ]
            subprocess.run(cmd, capture_output=True, check=True)
            return True
        except subprocess.CalledProcessError as e:
            print(f"Erro ao mesclar: {e}")
            return False
        
    def baixar_youtube(self, url):
        try:
            self.status_var.set("Conectando ao YouTube...")

            if self.playlist_var.get() and 'playlist' in url:
                return self.baixar_playlist_youtube(url)
            
            yt = YouTube(url, on_progress_callback=self.atualizar_progresso)
            
            # Verificar se é apenas áudio
            if self.qualidade.get() == "Apenas Áudio" or self.formato.get() == "MP3 (áudio)":
                video = yt.streams.filter(only_audio=True).first()
                if video:
                    titulo = self.limpar_nome_arquivo(yt.title)
                    nome_arquivo = f"{titulo}.mp3"
                    video.download(output_path=self.pasta_download.get(), filename=nome_arquivo)
                    self.progresso['value'] = 100
                    self.status_var.set(f"✅ Áudio baixado! Salvo em: {self.pasta_download.get()}")
                    messagebox.showinfo("Sucesso", f"Áudio baixado com sucesso!\n\nTítulo: {titulo}")
                return
            
            # Para vídeo: tentar baixar com áudio incluso primeiro
            qualidade_map = {
                "1080p": "1080p",
                "720p": "720p",
                "480p": "480p", 
                "360p": "360p",
            }
            
            video_stream = None
            precisa_mesclar = False
            
            # Tentar encontrar stream progressivo (com áudio incluso)
            if self.qualidade.get() in qualidade_map:
                video_stream = yt.streams.filter(
                    res=qualidade_map[self.qualidade.get()],
                    progressive=True,
                    file_extension='mp4'
                ).first()
            
            # Se não achou progressivo, tenta o melhor
            if not video_stream and self.qualidade.get() == "Melhor Qualidade":
                video_stream = yt.streams.filter(progressive=True, file_extension='mp4').first()
            
            # Se ainda não achou ou a qualidade é alta (1080p+), precisa mesclar
            if not video_stream or self.qualidade.get() in ["1080p", "Melhor Qualidade"]:
                # Pega o melhor stream de vídeo (sem áudio)
                video_stream = yt.streams.filter(adaptive=True, file_extension='mp4').order_by('resolution').desc().first()
                # Pega o melhor stream de áudio
                audio_stream = yt.streams.filter(only_audio=True).first()
                
                if video_stream and audio_stream:
                    precisa_mesclar = True
                    if not self.ffmpeg_disponivel:
                        messagebox.showerror("Erro", 
                            "Para baixar vídeos em 1080p ou melhor qualidade, é necessário instalar o FFmpeg!\n\n"
                            "Download: https://ffmpeg.org/download.html\n"
                            "Ou use qualidade 720p ou inferior.")
                        return
            
            if not video_stream:
                messagebox.showerror("Erro", "Não foi possível encontrar um stream de vídeo adequado")
                return
            
            titulo = self.limpar_nome_arquivo(yt.title)
            
            if precisa_mesclar:
                # Baixar vídeo e áudio separados
                self.status_var.set("Baixando vídeo (sem áudio)...")
                video_path = Path(self.pasta_download.get()) / f"{titulo}_video_temp.mp4"
                audio_path = Path(self.pasta_download.get()) / f"{titulo}_audio_temp.mp4"
                output_path = Path(self.pasta_download.get()) / f"{titulo}.mp4"
                
                video_stream.download(output_path=self.pasta_download.get(), filename=f"{titulo}_video_temp.mp4")
                
                self.status_var.set("Baixando áudio...")
                audio_stream.download(output_path=self.pasta_download.get(), filename=f"{titulo}_audio_temp.mp4")
                
                # Mesclar
                if self.mesclar_video_audio(str(video_path), str(audio_path), str(output_path)):
                    # Remover arquivos temporários se não foi marcado para manter
                    if not self.manter_temp_var.get():
                        os.remove(video_path)
                        os.remove(audio_path)
                    
                    self.progresso['value'] = 100
                    self.status_var.set(f"✅ Download completo! Salvo em: {self.pasta_download.get()}")
                    messagebox.showinfo("Sucesso", f"Vídeo baixado com sucesso!\n\nTítulo: {titulo}")
                else:
                    messagebox.showerror("Erro", "Falha ao mesclar vídeo e áudio")
            else:
                # Download direto (já tem áudio)
                nome_arquivo = f"{titulo}.mp4"
                video_stream.download(output_path=self.pasta_download.get(), filename=nome_arquivo)
                
                self.progresso['value'] = 100
                self.status_var.set(f"✅ Download completo! Salvo em: {self.pasta_download.get()}")
                messagebox.showinfo("Sucesso", f"Vídeo baixado com sucesso!\n\nTítulo: {titulo}")
                
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao baixar do YouTube:\n{str(e)}")
            self.status_var.set("Erro no download")
            
    def baixar_playlist_youtube(self, url):
        """Baixa playlist completa do YouTube"""
        try:
            self.status_var.set("Carregando playlist...")
            playlist = Playlist(url)
            
            total_videos = len(playlist.video_urls)
            self.status_var.set(f"Playlist encontrada: {playlist.title} ({total_videos} vídeos)")
            
            resposta = messagebox.askyesno("Confirmar", 
                                          f"Baixar playlist '{playlist.title}'?\n\n"
                                          f"Total de vídeos: {total_videos}\n"
                                          f"Pasta: {self.pasta_download.get()}")
            
            if not resposta:
                return
                
            for i, video_url in enumerate(playlist.video_urls, 1):
                self.status_var.set(f"Baixando vídeo {i}/{total_videos}...")
                self.progresso['value'] = (i-1)/total_videos * 100
                
                # Usar o mesmo método melhorado para cada vídeo
                yt = YouTube(video_url)
                
                # Tentar pegar stream com áudio
                video = yt.streams.filter(progressive=True, file_extension='mp4').first()
                if not video:
                    video = yt.streams.get_highest_resolution()
                
                if video:
                    titulo = self.limpar_nome_arquivo(yt.title)
                    video.download(output_path=self.pasta_download.get(), 
                                  filename=f"{i:03d} - {titulo}.mp4")
                    
            self.progresso['value'] = 100
            self.status_var.set(f"✅ Playlist completa baixada! Total: {total_videos} vídeos")
            messagebox.showinfo("Sucesso", f"Playlist baixada com sucesso!\nTotal de vídeos: {total_videos}")
            
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao baixar playlist:\n{str(e)}")

    def baixar_outras_plataformas(self, url, plataforma):
        """Download para Instagram, Twitter, TikTok, Facebook usando yt-dlp"""
        try:
            self.status_var.set(f"Conectando ao {plataforma}...")
            
            # Configurações base do yt-dlp
            ydl_opts = {
                'outtmpl': str(Path(self.pasta_download.get()) / '%(title)s.%(ext)s'),
                'quiet': True,
                'no_warnings': True,
                'progress_hooks': [self.progresso_hook],
                'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            }
            
            # Configurações específicas para Instagram
            if plataforma == "Instagram":
                ydl_opts['headers'] = {
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                    'Accept-Language': 'pt-BR,pt;q=0.8,en-US;q=0.5,en;q=0.3',
                }
            
            # Configurações para áudio
            if self.qualidade.get() == "Apenas Áudio" or self.formato.get() == "MP3 (áudio)":
                ydl_opts.update({
                    'format': 'bestaudio/best',
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    }],
                })
            else:
                ydl_opts['format'] = 'best'
                
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                self.status_var.set(f"Processando link do {plataforma}...")
                info = ydl.extract_info(url, download=True)
                
                self.progresso['value'] = 100
                self.status_var.set(f"✅ Download completo! Salvo em: {self.pasta_download.get()}")
                messagebox.showinfo("Sucesso", f"Vídeo do {plataforma} baixado com sucesso!\nPasta: {self.pasta_download.get()}")
                
        except Exception as e:
            error_msg = str(e)
            if "ffmpeg" in error_msg.lower():
                error_msg += "\n\nNota: Para converter para MP3, é necessário instalar o FFmpeg.\nDownload: https://ffmpeg.org/download.html"
            messagebox.showerror("Erro", f"Falha ao baixar do {plataforma}:\n{error_msg}")
            self.status_var.set("Erro no download")
    
    def iniciar_download(self):
        url = self.url_var.get().strip()
        
        if not url:
            messagebox.showwarning("Aviso", "Por favor, insira a URL do vídeo!")
            return
        
        # Validar URL
        if not url.startswith(('http://', 'https://')):
            messagebox.showwarning("Aviso", "URL inválida! Certifique-se de incluir http:// ou https://")
            return
        
        # Desabilitar botão durante download
        self.download_btn.configure(state="disabled", text="⬇️ BAIXANDO...")
        self.progresso['value'] = 0
        
        # Criar thread para não travar a interface
        def download_thread():
            try:
                plataforma = self.plataforma.get()
                
                if plataforma == "YouTube":
                    self.baixar_youtube(url)
                else:
                    self.baixar_outras_plataformas(url, plataforma)
            except Exception as e:
                messagebox.showerror("Erro", f"Erro inesperado:\n{str(e)}")
            finally:
                # Reabilitar botão
                self.download_btn.configure(state="normal", text="⬇️ BAIXAR VÍDEO")
                self.progresso['value'] = 0
                self.status_var.set("Aguardando...")
        
        thread = threading.Thread(target=download_thread)
        thread.daemon = True
        thread.start()
    
    def run(self):
        self.janela.mainloop()

# Executar o programa
if __name__ == "__main__":
    app = VideoDownloader()
    app.run()