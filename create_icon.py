# create_icon.py
from PIL import Image, ImageDraw
import os

def criar_icone():
    """Cria um ícone para o aplicativo"""
    size = 256
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Fundo gradiente (azul escuro para azul claro)
    for i in range(size):
        # Gradiente vertical
        r = int(30 + (i / size) * 50)
        g = int(100 + (i / size) * 50)
        b = int(200 + (i / size) * 55)
        draw.line([(0, i), (size, i)], fill=(r, g, b))
    
    # Desenhar um retângulo arredondado
    margin = size // 8
    draw.rectangle([margin, margin, size - margin, size - margin], 
                   outline=(255, 255, 255), width=size//20)
    
    # Desenhar um triângulo (play) mais elegante
    center_x = size // 2
    center_y = size // 2
    
    # Ajustar pontos para um triângulo mais equilibrado
    triangle_size = size * 0.35
    points = [
        (center_x - triangle_size//2, center_y - triangle_size//1.5),
        (center_x - triangle_size//2, center_y + triangle_size//1.5),
        (center_x + triangle_size//1.2, center_y)
    ]
    draw.polygon(points, fill=(255, 255, 255))
    
    # Salvar como ICO com múltiplos tamanhos
    img.save('icon.ico', format='ICO', sizes=[(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (16, 16)])
    
    print("✅ Ícone criado com sucesso!")
    print("   Arquivo: icon.ico")
    return True

if __name__ == "__main__":
    criar_icone()