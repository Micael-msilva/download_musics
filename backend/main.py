from fastapi import FastAPI, UploadFile, File, Query
from fastapi.responses import FileResponse
import os
import asyncio
from concurrent.futures import ThreadPoolExecutor
from .downloader import baixar_musica, baixar_lista
from .models import Music, MusicList
from .utils import criar_zip, remover_arquivos

app = FastAPI()

@app.post("/baixar-uma/")
async def baixar_uma(music: Music):
    caminho = baixar_musica(music)

    if not caminho or not os.path.exists(caminho):
        return {"erro": "Falha ao baixar a música."}

    response = FileResponse(
        caminho,
        media_type="audio/mpeg",
        filename=os.path.basename(caminho)
    )

    asyncio.create_task(remover_arquivos(caminho))
    return response

@app.post("/baixar-lista/")
async def baixar_varias(lista: MusicList):
    arquivos = []

    for url in lista.urls:
        caminho = baixar_musica(Music(url=url, format=lista.format))
        if caminho:
            arquivos.append(caminho)

    if not arquivos:
        return {"erro": "Nenhuma música foi baixada."}

    caminho_zip = criar_zip(arquivos)

    response = FileResponse(
        caminho_zip,
        media_type="application/zip",
        filename=os.path.basename(caminho_zip)
    )

    # asyncio.create_task(remover_arquivos(caminho_zip, *arquivos))
    return response

@app.post("/baixar-txt/")
async def baixar_txt(file: UploadFile = File(...), formato: str = Query("mp3")):
    conteudo = await file.read()
    urls = conteudo.decode('utf-8').splitlines()
    arquivos = []

    for url in urls:
        caminho = baixar_musica(Music(url=url, format=formato))
        if caminho:
            arquivos.append(caminho)

    if not arquivos:
        return {"erro": "Nenhuma música foi baixada."}

    caminho_zip = criar_zip(arquivos)

    response = FileResponse(
        caminho_zip,
        media_type="application/zip",
        filename=os.path.basename(caminho_zip)
    )

    # asyncio.create_task(remover_arquivos(caminho_zip, *arquivos))
    return response
