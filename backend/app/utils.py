import os
import zipfile
import asyncio
from datetime import datetime

def limpar_nome_arquivo(nome: str) -> str:
    """Remove caracteres inválidos para nomes de arquivos."""
    proibidos = '<>:"/\\|?*'
    for c in proibidos:
        nome = nome.replace(c, '-')
    return nome.strip()

def criar_zip(arquivos: list, pasta_destino="musicas") -> str:
    """Cria um arquivo ZIP com as músicas baixadas."""
    nome_zip = f"musicas_{datetime.now().strftime('%Y%m%d%H%M%S')}.zip"
    caminho_zip = os.path.join(pasta_destino, nome_zip)

    with zipfile.ZipFile(caminho_zip, 'w') as zipf:
        for arquivo in arquivos:
            zipf.write(arquivo, os.path.basename(arquivo))

    return caminho_zip

def musica_ja_baixada(nome: str, formato: str = "mp3", pasta_destino: str = "musicas") -> bool:
    """Verifica se a música já existe na pasta de destino."""
    nome_limpo = limpar_nome_arquivo(nome)
    caminho = os.path.join(pasta_destino, f"{nome_limpo}.{formato}")
    return os.path.exists(caminho)

async def remover_arquivos(*arquivos):
    """Remove arquivos após envio da resposta."""
    await asyncio.sleep(1)
    for arquivo in arquivos:
        if os.path.exists(arquivo):
            os.remove(arquivo)
