# ZDown

sistema simples de download de musica, usando `yt-dlp`e `ffmpeg`

## Funções
- Baixar o audio de qualquerr video 
- Permite escolher o formato de saida (`mp3` ou `wav`)
- Salva os arquivos automaticamente na pasta `repos/`


## Pré-requisitos

Antes de rodar o projeto, precisamos de

- Python 3+
- pip
- ffmep

estou usando o wsl no windows então siga estes passos:

Atualiza o sitema e instale as dependencias
```bash
sudo apt update -y && sudo apt upgrade -y
sudo apt install ffmpeg
sudo apt install python3 python3-pip -y
```

crie o ambiente virtual (venv)
```bash
python -m venv venv
source venv/bin/activate
```

instalar o `yt-dlp` tem duas formas

1. usando o pip:

```bash
pip3 install -U yt-dlp
```

2. direto do requirements

```bash
python install -m requirements.txt
```

## Main

