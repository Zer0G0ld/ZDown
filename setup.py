# setup.py
import PyInstaller.__main__
import sys
import os
import shutil
import urllib.request
import zipfile
from pathlib import Path

def baixar_ffmpeg():
    """Baixa o FFmpeg automaticamente se não existir"""
    ffmpeg_path = Path("ffmpeg_bin/ffmpeg.exe")
    
    if ffmpeg_path.exists():
        print("✅ FFmpeg já está na pasta!")
        return True
    
    print("📥 Baixando FFmpeg...")
    os.makedirs("ffmpeg_bin", exist_ok=True)
    
    # Usar um build pequeno do FFmpeg (apenas o executável)
    # Fonte: https://www.gyan.dev/ffmpeg/builds/
    url = "https://www.gyan.dev/ffmpeg/builds/packages/ffmpeg-6.1.1-full_build.7z"
    
    # Alternativa: usar um build menor do BtbN
    url_alternativa = "https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip"
    
    try:
        # Baixar zip
        zip_path = Path("ffmpeg_bin/ffmpeg.zip")
        urllib.request.urlretrieve(url_alternativa, zip_path)
        
        # Extrair apenas o ffmpeg.exe
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            for file in zip_ref.namelist():
                if file.endswith("ffmpeg.exe"):
                    # Extrair para a pasta
                    with zip_ref.open(file) as source, open(ffmpeg_path, 'wb') as target:
                        target.write(source.read())
                    break
        
        # Limpar zip
        zip_path.unlink()
        print("✅ FFmpeg baixado com sucesso!")
        return True
    except Exception as e:
        print(f"⚠️ Erro ao baixar FFmpeg: {e}")
        print("   Você precisará instalar manualmente")
        return False

def limpar_arquivos_antigos():
    """Remove arquivos de builds anteriores"""
    pastas_remover = ['build', 'dist']
    arquivos_remover = ['*.spec']
    
    for pasta in pastas_remover:
        if os.path.exists(pasta):
            shutil.rmtree(pasta)
            print(f"🗑️  Removido: {pasta}/")
    
    for padrao in arquivos_remover:
        for arquivo in Path('.').glob(padrao):
            arquivo.unlink()
            print(f"🗑️  Removido: {arquivo}")

def verificar_icone():
    """Verifica se o ícone existe, se não, cria um"""
    if not os.path.exists('icon.ico'):
        print("⚠️  Ícone não encontrado! Criando um...")
        try:
            # Tentar importar e criar o ícone
            from create_icon import criar_icone
            criar_icone()
        except ImportError:
            print("❌ Não foi possível criar o ícone automaticamente")
            print("   Execute 'python create_icon.py' primeiro")
            return False
    print("✅ Ícone encontrado!")
    return True

def criar_executavel():
    """Cria o executável com FFmpeg embutido"""
    
    print("=" * 60)
    print("🎬 Gerando executável do Video Downloader Pro")
    print("=" * 60)
    
    # Baixar FFmpeg se necessário
    baixar_ffmpeg()
    
    # Limpar arquivos antigos
    limpar_arquivos_antigos()
    
    if not verificar_icone():
        return
    
    if not os.path.exists('main.py'):
        print("❌ Arquivo main.py não encontrado!")
        return
    
    print("\n📦 Configurando PyInstaller...\n")
    
    if sys.platform == 'win32':
        # Adicionar FFmpeg ao executável
        ffmpeg_bin = Path("ffmpeg_bin")
        
        cmd = [
            'main.py',
            '--onefile',
            '--windowed',
            '--name=VideoDownloaderPro',
            '--icon=icon.ico',
            '--noconsole',
            '--clean',
            '--uac-admin',
            '--collect-all=customtkinter',
            '--collect-all=pytubefix',
            '--collect-all=yt_dlp',
            '--hidden-import=yt_dlp',
            '--hidden-import=customtkinter',
            '--hidden-import=PIL',
            '--hidden-import=urllib.request',
            '--hidden-import=zipfile',
        ]
        
        # Adicionar FFmpeg como arquivo extra
        if ffmpeg_bin.exists():
            # Adicionar a pasta ffmpeg_bin como dado extra
            cmd.append(f'--add-data=ffmpeg_bin{os.pathsep}ffmpeg_bin')
        
        if os.path.exists('README.md'):
            cmd.append('--add-data=README.md;.')
        
        try:
            PyInstaller.__main__.run(cmd)
            print("\n✅ Executável criado com FFmpeg embutido!")
            print(f"📁 Localização: {os.path.abspath('dist/VideoDownloaderPro.exe')}")
        except Exception as e:
            print(f"\n❌ Erro: {e}")
    else:
        print("⚠️  Script otimizado para Windows!")

def criar_versao_portable():
    """Cria uma versão portátil (com pasta de dados)"""
    print("\n📦 Criando versão portátil...")
    
    cmd = [
        'main.py',
        '--onedir',                     # Pasta com arquivos (mais compatível)
        '--windowed',
        '--name=VideoDownloaderPro_Portable',
        '--icon=icon.ico',
        '--noconsole',
        '--clean',
        '--collect-all=customtkinter',
        '--collect-all=pytubefix',
        '--collect-all=yt_dlp',
    ]
    
    try:
        PyInstaller.__main__.run(cmd)
        print("✅ Versão portátil criada em 'dist/VideoDownloaderPro_Portable/'")
    except Exception as e:
        print(f"❌ Erro: {e}")

if __name__ == "__main__":
    # Verificar argumentos
    if len(sys.argv) > 1:
        if sys.argv[1] == "--portable":
            criar_versao_portable()
        elif sys.argv[1] == "--clean":
            limpar_arquivos_antigos()
            print("✅ Limpeza concluída!")
        else:
            print(f"Argumento desconhecido: {sys.argv[1]}")
            print("Uso: python setup.py [--portable] [--clean]")
    else:
        criar_executavel()