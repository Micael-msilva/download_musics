import yt_dlp
from concurrent.futures import ThreadPoolExecutor
import os
import re
import logging
from .models import Music, MusicList
from .utils import limpar_nome_arquivo, criar_zip, musica_ja_baixada as musica_ja_baixada_utils

PASTA_DESTINO = "musicas"  # Corrigido: caminho relativo válido
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# -----------------------------
# Funções utilitárias
# -----------------------------

def musica_ja_baixada(nome: str, formato: str = "mp3") -> bool:
    """Verifica se a música já existe na pasta de destino."""
    nome_limpo = limpar_nome_arquivo(nome)
    caminho = os.path.join(PASTA_DESTINO, f"{nome_limpo}.{formato}")
    return os.path.exists(caminho)

# -----------------------------
# Função principal
# -----------------------------

def baixar_musica(music: Music) -> str:
    """Baixa música ou vídeo usando URL ou termo de busca."""
    os.makedirs(PASTA_DESTINO, exist_ok=True)
    is_url = re.match(r'^(https?://|www\.)', music.url)

    # Primeiro, vamos obter informações do vídeo
    try:
        with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
            if is_url:
                info = ydl.extract_info(music.url, download=False)
            else:
                info = ydl.extract_info(f"ytsearch:{music.url}", download=False)['entries'][0]

            titulo = info.get('title', 'musica')
            nome_limpo = limpar_nome_arquivo(titulo)
            
            # Verificar se já existe
            if musica_ja_baixada(titulo, music.format):
                caminho_existente = os.path.join(PASTA_DESTINO, f"{nome_limpo}.{music.format}")
                logger.info(f"[⏭] Pulando, já existe: {titulo}")
                return caminho_existente if os.path.exists(caminho_existente) else None
    except Exception as e:
        logger.error(f"[✖] Erro ao verificar {music.url}: {e}")
        return None

    # Configurar opções de download
    opcoes = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(PASTA_DESTINO, f'{nome_limpo}.%(ext)s'),
        'quiet': True,
        'no_warnings': True,
    }

    audio_formats = ["mp3", "wav", "m4a", "aac", "flac"]
    if music.format.lower() in audio_formats:
        opcoes['postprocessors'] = [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': music.format,
            'preferredquality': '192',
        }]
        opcoes['outtmpl'] = os.path.join(PASTA_DESTINO, f'{nome_limpo}.{music.format}')

    # Fazer o download
    try:
        with yt_dlp.YoutubeDL(opcoes) as ydl:
            if is_url:
                ydl.download([music.url])
            else:
                ydl.download([f"ytsearch:{music.url}"])
        
        # Verificar se o arquivo foi criado
        caminho_arquivo = os.path.join(PASTA_DESTINO, f"{nome_limpo}.{music.format}")
        if os.path.exists(caminho_arquivo):
            logger.info(f"[✔] Download concluído: {titulo}")
            return caminho_arquivo
        else:
            # Procurar arquivo com nome similar (caso o yt-dlp tenha mudado o nome)
            for arquivo in os.listdir(PASTA_DESTINO):
                if arquivo.startswith(nome_limpo) and arquivo.endswith(f".{music.format}"):
                    caminho_real = os.path.join(PASTA_DESTINO, arquivo)
                    logger.info(f"[✔] Download concluído: {arquivo}")
                    return caminho_real
            
            logger.error(f"[✖] Arquivo não encontrado após download: {caminho_arquivo}")
            return None
            
    except Exception as e:
        logger.error(f"[✖] Erro ao baixar {music.url}: {e}")
        return None

# -----------------------------
# Funções para lista
# -----------------------------

def baixar_lista(music_list: MusicList, max_threads: int = 3):
    """Baixa várias músicas em paralelo."""
    os.makedirs(PASTA_DESTINO, exist_ok=True)
    musicas = [Music(url=url, format=music_list.format) for url in music_list.urls]

    logger.info(f"Encontradas {len(musicas)} músicas. Iniciando download...")

    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        # Para a função baixar_lista, não precisamos dos retornos
        futures = []
        for musica in musicas:
            future = executor.submit(baixar_musica, musica)
            futures.append(future)
        
        # Aguardar conclusão de todos os downloads
        for future in futures:
            future.result()

def baixar_lista_com_zip(music_list: MusicList, max_threads: int = 3, criar_arquivo_zip: bool = False) -> str:
    """Baixa várias músicas em paralelo e opcionalmente cria um ZIP."""
    os.makedirs(PASTA_DESTINO, exist_ok=True)
    musicas = [Music(url=url, format=music_list.format) for url in music_list.urls]

    logger.info(f"Encontradas {len(musicas)} músicas. Iniciando download...")

    # Lista para armazenar arquivos baixados
    arquivos_baixados = []

    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        # Mapear downloads e coletar resultados
        futures = []
        for musica in musicas:
            future = executor.submit(baixar_musica_com_retorno, musica)
            futures.append(future)
        
        # Coletar arquivos baixados
        for future in futures:
            arquivo = future.result()
            if arquivo:
                arquivos_baixados.append(arquivo)

    logger.info(f"Downloads concluídos: {len(arquivos_baixados)} arquivos")

    # Criar ZIP se solicitado
    if criar_arquivo_zip and arquivos_baixados:
        caminho_zip = criar_zip(arquivos_baixados, PASTA_DESTINO)
        logger.info(f"ZIP criado: {caminho_zip}")
        return caminho_zip
    
    return PASTA_DESTINO

def baixar_musica_com_retorno(music: Music) -> str:
    """Baixa música e retorna o caminho do arquivo baixado."""
    os.makedirs(PASTA_DESTINO, exist_ok=True)
    is_url = re.match(r'^(https?://|www\.)', music.url)

    opcoes = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(PASTA_DESTINO, f'%(title)s.{music.format}'),
        'quiet': True,
        'no_warnings': True,
    }

    audio_formats = ["mp3", "wav", "m4a", "aac", "flac"]
    if music.format.lower() in audio_formats:
        opcoes['postprocessors'] = [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': music.format,
            'preferredquality': '192',
        }]

    try:
        with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
            if is_url:
                info = ydl.extract_info(music.url, download=False)
            else:
                info = ydl.extract_info(f"ytsearch:{music.url}", download=False)['entries'][0]

            titulo = info.get('title', 'musica')
            nome_limpo = limpar_nome_arquivo(titulo)
            caminho_arquivo = os.path.join(PASTA_DESTINO, f"{nome_limpo}.{music.format}")
            
            if musica_ja_baixada(titulo, music.format):
                logger.info(f"[⏭] Pulando, já existe: {titulo}")
                return caminho_arquivo if os.path.exists(caminho_arquivo) else None
    except Exception as e:
        logger.error(f"[✖] Erro ao verificar {music.url}: {e}")
        return None

    try:
        with yt_dlp.YoutubeDL(opcoes) as ydl:
            if is_url:
                ydl.download([music.url])
            else:
                ydl.download([f"ytsearch:{music.url}"])
        
        logger.info(f"[✔] Download concluído: {titulo}")
        return caminho_arquivo
    except Exception as e:
        logger.error(f"[✖] Erro ao baixar {music.url}: {e}")
        return None

