import yt_dlp

class MusicDownloaderService:

    def get_data(self, format: str, query_or_url: str, output_folder: str) -> dict:
        if query_or_url.startswith("http"):
            url = query_or_url
        else:
            url = f"ytsearch:{query_or_url}"

        name = query_or_url if not url.startswith("http") else "music"
        output_path = f"{output_folder}/{name}"

        ydl_opts = {
            "format": "bestaudio/best",
            "outtmpl": output_path,
            "quiet": True,
            "noplaylist": True,
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": format,
                    "preferredquality": "192",
                }
            ],
        }
        data = {
            "ydl_opts": ydl_opts,
            "url": url,
            "name": name,
            "output_path": output_path,
        }
        return data
