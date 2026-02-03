import os
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
import yt_dlp
from services.music_downloader_service import MusicDownloaderService


class MusicDownloader:
    def __init__(self, format: str = "mp3", max_workers: int = 5):
        self.format = format.lower()
        self.service = MusicDownloaderService()
        self.output_folder = Path("../musics")
        self.output_folder.mkdir(exist_ok=True)
        self.max_workers = max_workers
        print(f"[DEBUG] MusicDownloader initialized with output_folder: {self.output_folder.absolute()}")

    def download(self, queries_or_url: list, format: str = None) -> dict:
        if format is None:
            format = self.format

        print(f"[DEBUG] Starting download for {len(queries_or_url)} query(ies): {queries_or_url}")
        results = []
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = [executor.submit(self._download_single, q, format) for q in queries_or_url]
            for future in as_completed(futures):
                results.append(future.result())
        
        print(f"[DEBUG] Download results: {results}")
        
        if len(queries_or_url) != 1:
            from tools.utils import generate_zip
            zip_path = generate_zip(files_path=str(self.output_folder))
            print(f"[DEBUG] Generated zip at: {zip_path}")
            return {
                "success": True,
                "query": "all_files",
                "output_path": zip_path,
                "message": f"All files zipped at: {zip_path}"
            }
        # Retorna o dicionário do primeiro (e único) resultado em vez de uma lista
        return results[0] if results else {
            "success": False,
            "query": None,
            "output_path": None,
            "message": "No download result"
        }
    
    def _download_single(self, query_or_url: str, format: str) -> dict:
        try:
            print(f"[DEBUG] _download_single started for: {query_or_url}, format: {format}")
            download_data = self.service.get_data(format, query_or_url, str(self.output_folder))
            print(f"[DEBUG] download_data received: {download_data}")
            
            with yt_dlp.YoutubeDL(download_data["ydl_opts"]) as ydl:
                ydl.download([download_data["url"]])
            
            print(f"[DEBUG] yt-dlp download completed")
            
            # Lista todos os arquivos na pasta após o download
            all_files = list(self.output_folder.glob("*"))
            print(f"[DEBUG] Files in output folder: {[str(f) for f in all_files]}")
            
            # procura o arquivo real gerado (com extensão) na pasta de saída
            from pathlib import Path
            base_name = download_data.get("name") or Path(download_data.get("output_path", "")).stem
            print(f"[DEBUG] Searching for files with base_name: {base_name}")
            
            found_files = list(self.output_folder.glob(f"{base_name}*"))
            print(f"[DEBUG] Found files matching pattern: {[str(f) for f in found_files]}")
            
            if found_files:
                real_path = str(found_files[0])
            else:
                # fallback: usa output_path fornecido se existir e for um arquivo
                real_path = download_data.get("output_path")
                print(f"[DEBUG] No files found, using fallback path: {real_path}")
                if real_path and not Path(real_path).exists():
                    raise FileNotFoundError(f"Downloaded file not found for base name: {base_name}")

            print(f"[DEBUG] Final real_path: {real_path}, exists: {Path(real_path).exists()}")
            
            return {
                "success": True,
                "query": query_or_url,
                "output_path": real_path,
                "message": f"Successfully downloaded: {download_data.get('name')}"
            }
        except Exception as e:
            print(f"[DEBUG] Exception in _download_single: {type(e).__name__}: {str(e)}")
            import traceback
            traceback.print_exc()
            return {
                "success": False,
                "query": query_or_url,
                "error": str(e),
                "message": f"Failed to download: {query_or_url}"
            }
