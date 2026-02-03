import os
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from typing import List, Optional
from application.music_downloader import MusicDownloader
from application.spotify_scrapper import SpotifyScraper

router = APIRouter()

@router.post("/music/download")
def download_music(musics: List[str], format: str = "mp3"):
    print(f"[DEBUG] /music/download called with musics={musics}, format={format}")
    
    if not musics:
        raise HTTPException(status_code=400, detail="Lista de músicas vazia")

    downloader = MusicDownloader(format=format)
    results = downloader.download(musics, format=format)

    print(f"[DEBUG] Download results in endpoint: {results}")

    # check success / output_path before using it
    if not results.get("success"):
        detail = results.get("message") or results.get("error") or "Download failed"
        print(f"[DEBUG] Download failed: {detail}")
        raise HTTPException(status_code=500, detail=detail)

    output_path = results.get("output_path")
    if not output_path:
        print(f"[DEBUG] No output_path in results")
        raise HTTPException(status_code=500, detail="No output file produced")

    print(f"[DEBUG] Returning FileResponse with path: {output_path}")
    
    return FileResponse(
        path=output_path,
        filename=os.path.basename(output_path),
        media_type="audio/mpeg" if len(musics) == 1 else "application/zip"
    )

@router.post("/spotify/playlist")
def get_spotify_playlist_tracks(playlist_url: str, count: Optional[int] = None):
    print(f"[DEBUG] /spotify/playlist called with url={playlist_url}")
    
    if not playlist_url:
        raise HTTPException(status_code=400, detail="URL da playlist não fornecida")

    scraper = SpotifyScraper()
    try:
        tracks = scraper.get_playlist_track_names(playlist_url, count or "all")
        print(f"[DEBUG] Scraped {len(tracks)} tracks from playlist")
        return {
            "playlist_url": playlist_url,
            "tracks": tracks,
            "count": len(tracks)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao extrair playlist: {str(e)}")

@router.post("/spotify/download")
def download_spotify_playlist(playlist_url: str, count: Optional[int] = None):
    print(f"[DEBUG] /spotify/download called with url={playlist_url}")
    
    if not playlist_url:
        raise HTTPException(status_code=400, detail="URL da playlist não fornecida")

    try:
        # Extrai as músicas da playlist
        scraper = SpotifyScraper()
        tracks = scraper.get_playlist_track_names(playlist_url, count or "all")

        if not tracks:
            raise HTTPException(status_code=404, detail="Nenhuma música encontrada na playlist")

        # Faz o download das músicas extraídas
        downloader = MusicDownloader()
        download_results = downloader.download(tracks)

        print(f"[DEBUG] Download results for Spotify playlist: {download_results}")

        return FileResponse(
            path=download_results["output_path"],
            filename=os.path.basename(download_results["output_path"]),
            media_type="application/zip" if len(tracks) > 1 else "audio/mpeg"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao processar a playlist: {str(e)}")
