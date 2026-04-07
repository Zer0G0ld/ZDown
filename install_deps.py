# install_deps.py
import subprocess
import sys
import os
import platform

def verificar_python():
    """Verifica versão do Python"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 7):
        print("❌ Python 3.7 ou superior é necessário!")
        print(f"   Versão atual: Python {version.major}.{version.minor}")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} detectado")
    return True

def instalar_dependencias():
    """Instala todas as dependências necessárias"""
    
    print("=" * 50)
    print("🎥 Video Downloader Pro - Instalador de Dependências")
    print("=" * 50)
    
    if not verificar_python():
        return
    
    # Dependências principais
    dependencias = {
        'customtkinter': 'Interface gráfica moderna',
        'pytubefix': 'Download do YouTube (versão corrigida)',
        'yt-dlp': 'Download de outras plataformas',
        'Pillow': 'Criação de ícones',
        'requests': 'Requisições HTTP'
    }
    
    print("\n📦 Instalando dependências...\n")
    
    instalados = 0
    erros = 0
    
    for dep, desc in dependencias.items():
        print(f"📥 Instalando {dep} ({desc})...", end=" ")
        try:
            # Usar --upgrade para garantir a versão mais recente
            subprocess.check_call(
                [sys.executable, "-m", "pip", "install", "--upgrade", dep],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            print("✅")
            instalados += 1
        except Exception as e:
            print("❌")
            print(f"    Erro: {e}")
            erros += 1
    
    print("\n" + "=" * 50)
    print(f"✅ Dependências instaladas: {instalados}/{len(dependencias)}")
    if erros > 0:
        print(f"⚠️  Falhas: {erros}")
    
    # Verificar FFmpeg
    print("\n🎬 Verificando FFmpeg...")
    try:
        result = subprocess.run(['ffmpeg', '-version'], 
                               capture_output=True, 
                               text=True,
                               check=False)
        if result.returncode == 0:
            # Extrair versão
            version_line = result.stdout.split('\n')[0]
            print(f"✅ {version_line}")
        else:
            print("⚠️  FFmpeg não encontrado!")
            print("   Para baixar vídeos em 1080p+, instale o FFmpeg:")
            print("   📥 Download: https://www.gyan.dev/ffmpeg/builds/")
            print("   📖 Tutorial: https://youtu.be/xxxxx")
    except FileNotFoundError:
        print("⚠️  FFmpeg não encontrado!")
        print("   Para baixar vídeos em 1080p+, instale o FFmpeg:")
        print("   📥 Download: https://www.gyan.dev/ffmpeg/builds/")
    
    print("\n" + "=" * 50)
    print("✨ Instalação concluída!")
    print("\nPróximos passos:")
    print("1. Execute 'python create_icon.py' para criar o ícone")
    print("2. Execute 'python main.py' para testar o programa")
    print("3. Execute 'python setup.py' para criar o executável")
    print("=" * 50)

def desinstalar_dependencias():
    """Remove todas as dependências"""
    print("🗑️  Desinstalando dependências...")
    
    dependencias = ['customtkinter', 'pytubefix', 'yt-dlp', 'Pillow', 'requests']
    
    for dep in dependencias:
        try:
            subprocess.check_call(
                [sys.executable, "-m", "pip", "uninstall", dep, "-y"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            print(f"   ✓ {dep} removido")
        except:
            pass
    
    print("✅ Todas as dependências foram removidas!")

if __name__ == "__main__":
    # Verificar argumentos de linha de comando
    if len(sys.argv) > 1 and sys.argv[1] == "--uninstall":
        desinstalar_dependencias()
    else:
        instalar_dependencias()