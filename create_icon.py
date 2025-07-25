# Script para criar um ícone simples para a aplicação
# Este script gera um ícone básico usando PIL se disponível

try:
    from PIL import Image, ImageDraw
    import os
    
    # Criar uma imagem 64x64 com fundo azul e um círculo vermelho (representando gravação)
    size = (64, 64)
    image = Image.new('RGBA', size, (70, 130, 180, 255))  # SteelBlue background
    draw = ImageDraw.Draw(image)
    
    # Desenhar círculo vermelho no centro (botão de gravação)
    circle_size = 20
    center = (size[0] // 2, size[1] // 2)
    left = center[0] - circle_size // 2
    top = center[1] - circle_size // 2
    right = center[0] + circle_size // 2
    bottom = center[1] + circle_size // 2
    
    draw.ellipse([left, top, right, bottom], fill=(220, 20, 60, 255))  # Crimson circle
    
    # Salvar como ICO para Windows
    image.save('icon.ico', format='ICO', sizes=[(16,16), (32,32), (48,48), (64,64)])
    
    # Salvar como PNG para backup
    image.save('icon.png', format='PNG')
    
    print("Ícone criado com sucesso!")
    
except ImportError:
    print("PIL não está disponível. Criando arquivo de ícone placeholder...")
    
    # Criar um arquivo placeholder
    with open('icon.ico', 'wb') as f:
        # Este é um ícone ICO mínimo válido (1x1 pixel transparente)
        ico_data = bytes([
            0x00, 0x00, 0x01, 0x00, 0x01, 0x00, 0x01, 0x01, 0x00, 0x00, 0x01, 0x00,
            0x20, 0x00, 0x30, 0x00, 0x00, 0x00, 0x16, 0x00, 0x00, 0x00, 0x28, 0x00,
            0x00, 0x00, 0x01, 0x00, 0x00, 0x00, 0x02, 0x00, 0x00, 0x00, 0x01, 0x00,
            0x20, 0x00, 0x00, 0x00, 0x00, 0x00, 0x04, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00
        ])
        f.write(ico_data)
    
    print("Arquivo de ícone placeholder criado!")

except Exception as e:
    print(f"Erro ao criar ícone: {e}")
