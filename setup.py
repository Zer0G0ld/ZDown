# setup.py
import PyInstaller.__main__
import sys
import os
import shutil
from pathlib import Path

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
    """Cria o executável do programa"""
    
    print("=" * 60)
    print("🎬 Gerando executável do Video Downloader Pro")
    print("=" * 60)
    
    # Limpar arquivos antigos
    limpar_arquivos_antigos()
    
    # Verificar ícone
    if not verificar_icone():
        return
    
    # Verificar se main.py existe
    if not os.path.exists('main.py'):
        print("❌ Arquivo main.py não encontrado!")
        return
    
    print("\n📦 Configurando PyInstaller...\n")
    
    # Configuração para Windows
    if sys.platform == 'win32':
        # Comando base
        cmd = [
            'main.py',
            '--onefile',                    # Único arquivo executável
            '--windowed',                   # Sem console (GUI)
            '--name=VideoDownloaderPro',    # Nome do executável
            '--icon=icon.ico',              # Ícone do aplicativo
            '--noconsole',                  # Não mostrar console
            '--clean',                      # Limpar cache
            '--uac-admin',                  # Solicitar admin (se necessário)
            '--collect-all=customtkinter',  # Incluir customtkinter completo
            '--collect-all=pytubefix',      # Incluir pytubefix
            '--collect-all=yt_dlp',         # Incluir yt-dlp
            # Ocultar imports específicos
            '--hidden-import=yt_dlp',
            '--hidden-import=customtkinter',
            '--hidden-import=PIL',
            '--hidden-import=PIL._tkinter_finder',
            # Adicionar dados extras se existirem
        ]
        
        # Adicionar README se existir
        if os.path.exists('README.md'):
            cmd.append('--add-data=README.md;.')
        
        # Executar PyInstaller
        try:
            PyInstaller.__main__.run(cmd)
            
            print("\n" + "=" * 60)
            print("✅ Executável criado com sucesso!")
            print(f"📁 Localização: {os.path.abspath('dist/VideoDownloaderPro.exe')}")
            print("\n📝 Notas:")
            print("   - O executável está na pasta 'dist/'")
            print("   - Tamanho aproximado: ~50-80MB")
            print("   - Primeira execução pode ser mais lenta")
            print("=" * 60)
            
        except Exception as e:
            print(f"\n❌ Erro ao criar executável: {e}")
            
    else:
        print("⚠️  Este script é otimizado para Windows!")
        print("   Para outros sistemas, use: pyinstaller main.py --onefile")

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