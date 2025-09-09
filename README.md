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

basicamente o arquivo principal tem uma função para o download de audio e uma função para chamar e inicar o codigo todo

a função `download_audio` verifica se o `repos` existe e se não existe ele cria para guardar os downloads e logo em seguinda as configurações do `yt-dlp` 

depois chamamos e iniciamos com as informações adicionais os `inputs` e formatos padrões

não vamos versionar o venv e nem o repos pois irá deixar o repositorio do github pesado

