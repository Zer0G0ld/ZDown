import yt_dlp # ingnora o erro já foi feito a instalação
import os

# Função para baixar áudio
def download_audio(url, formato="mp3", repo="."):
    # Garantir que o diretório de repositório existe
    os.makedirs(repo, exist_ok=True)

    # Configurações do yt-dlp
    config = {
        "format": "bestaudio/best",
        "outtmpl": os.path.join(repo, "%(title)s.%(ext)s"), # Salva dentro de /repos
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": formato,
                "preferredquality": "192", # Qualidade do áudio
            }
        ],
    }

    with yt_dlp.YoutubeDL(config) as ydl:
        ydl.download([url])

# Chamando função
if __name__ == "__main__":
    repo = "repos" # Diretorio onde deseja salvar
    link = input("Digite o link do vídeo/música: ").strip()
    formato = input("Digite o formato que deseja (mp3/wav) D:[mp3]: ").strip().lower()
    if formato not in ["mp3", "wav"]:
        formato = "mp3"
    download_audio(link, formato, repo)
    print(f"✅ Download concluído! Arquivo salvo em ./{repo}")