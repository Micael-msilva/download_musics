# 🎵 Music Downloader API

API RESTful para download de músicas do YouTube e extração de playlists do Spotify, construída com FastAPI e Docker.

## 📋 Sobre o Projeto

Este projeto é uma aplicação backend que permite:
- **Baixar músicas do YouTube** através de queries de busca ou URLs diretas
- **Extrair faixas de playlists do Spotify** usando web scraping
- **Download em lote** com suporte a múltiplas músicas simultaneamente
- **Conversão automática** para formato MP3
- **Empacotamento em ZIP** quando há múltiplos downloads

## 🏗️ Arquitetura

```
download_musics/
├── backend/
│   ├── api/                    # Rotas da API
│   │   └── routes.py          # Endpoints REST
│   ├── application/           # Lógica de aplicação
│   │   ├── music_downloader.py    # Gerenciamento de downloads
│   │   └── spotify_scrapper.py    # Scraping do Spotify
│   ├── services/              # Camada de serviços
│   │   ├── music_downloader_service.py
│   │   └── spotify_scrapper_service.py
│   ├── tools/                 # Utilitários
│   │   └── utils.py
│   ├── main.py                # Ponto de entrada
│   ├── Dockerfile
│   └── requirements.txt
├── musics/                    # Diretório de saída dos downloads
└── docker-compose.yml
```

## 🚀 Tecnologias Utilizadas

- **FastAPI** - Framework web moderno e de alta performance
- **yt-dlp** - Download de vídeos/áudios do YouTube
- **Playwright** - Automação de navegador para scraping do Spotify
- **Docker & Docker Compose** - Containerização
- **FFmpeg** - Conversão e processamento de áudio
- **Python 3.11** - Linguagem base

## 📦 Pré-requisitos

- Docker
- Docker Compose

## ⚡ Instalação e Execução

1. **Clone o repositório:**
```bash
git clone <url-do-repositorio>
cd download_musics
```

2. **Inicie o container:**
```bash
docker-compose up --build
```

3. **Acesse a aplicação:**
- API: `http://localhost:8000`
- Documentação interativa (Swagger): `http://localhost:8000/docs`
- Documentação alternativa (ReDoc): `http://localhost:8000/redoc`

## 🎯 Endpoints da API

### 1. Download de Músicas

**POST** `/music/download`

Baixa músicas do YouTube através de queries de busca ou URLs.

**Parâmetros:**
```json
{
  "musics": ["Nome da Música 1", "Nome da Música 2"],
  "format": "mp3"
}
```

**Resposta:**
- Música única: Retorna o arquivo de áudio diretamente
- Múltiplas músicas: Retorna um arquivo ZIP contendo todos os downloads

**Exemplo com cURL:**
```bash
curl -X POST "http://localhost:8000/music/download?format=mp3" \
  -H "Content-Type: application/json" \
  -d '["Bohemian Rhapsody", "Stairway to Heaven"]' \
  --output musicas.zip
```

### 2. Extrair Faixas de Playlist do Spotify

**POST** `/spotify/playlist`

Extrai os nomes das músicas de uma playlist pública do Spotify.

**Parâmetros:**
```json
{
  "playlist_url": "https://open.spotify.com/playlist/...",
  "count": 10  // opcional, padrão: todas as músicas
}
```

**Resposta:**
```json
{
  "playlist_url": "https://open.spotify.com/playlist/...",
  "tracks": ["Música 1", "Música 2", "..."],
  "count": 10
}
```

**Exemplo com cURL:**
```bash
curl -X POST "http://localhost:8000/spotify/playlist?count=10" \
  -H "Content-Type: application/json" \
  -d '{"playlist_url": "https://open.spotify.com/playlist/37i9dQZF1DXcBWIGoYBM5M"}'
```

### 3. Download de Playlist do Spotify

**POST** `/spotify/download`

Extrai as músicas da playlist do Spotify e faz o download de todas elas do YouTube.

**Parâmetros:**
```json
{
  "playlist_url": "https://open.spotify.com/playlist/...",
  "count": 5  // opcional, padrão: todas as músicas
}
```

**Resposta:**
- Retorna um arquivo ZIP contendo todas as músicas da playlist

**Exemplo com cURL:**
```bash
curl -X POST "http://localhost:8000/spotify/download" \
  -H "Content-Type: application/json" \
  -d '{"playlist_url": "https://open.spotify.com/playlist/37i9dQZF1DXcBWIGoYBM5M"}' \
  --output playlist.zip
```

## 🔧 Funcionalidades Técnicas

### Download Concorrente
- Utiliza `ThreadPoolExecutor` para downloads paralelos
- Máximo de 5 workers simultâneos por padrão
- Melhora significativa na performance para múltiplos downloads

### Web Scraping Inteligente
- Usa Playwright para renderizar páginas JavaScript do Spotify
- Scroll automático para carregar todas as faixas
- Detecção de duplicatas
- Limite de segurança para evitar loops infinitos

### Gerenciamento de Arquivos
- Criação automática de diretório de saída
- Conversão automática para MP3
- Empacotamento em ZIP para múltiplos arquivos
- Limpeza de nomes de arquivo

## 📁 Volumes Docker

O container mapeia o diretório `./musics` para persistir os downloads no host:

```yaml
volumes:
  - ./musics:/musics
```

Todos os arquivos baixados ficam disponíveis em `./musics/` no host.

## 🛠️ Desenvolvimento

### Estrutura de Dependências

```txt
yt-dlp          # Download de vídeos/áudios
fastapi         # Framework web
uvicorn         # Servidor ASGI
pydantic        # Validação de dados
playwright      # Automação de navegador
```

### Rodando Localmente (sem Docker)

```bash
cd backend
pip install -r requirements.txt
python -m playwright install --with-deps
python main.py
```

## 🐛 Debug

A aplicação possui logs detalhados. Para visualizar:

```bash
docker-compose logs -f backend
```

## ⚠️ Avisos Importantes

1. **Uso Educacional**: Este projeto é para fins educacionais e de aprendizado
2. **Direitos Autorais**: Respeite os direitos autorais das músicas
3. **Termos de Serviço**: O uso pode violar os termos de serviço do YouTube e Spotify
4. **Performance**: Downloads em lote podem levar tempo dependendo da quantidade de músicas

## 📝 Melhorias Futuras

- [ ] Adicionar autenticação e autorização
- [ ] Implementar fila de downloads com Redis
- [ ] Adicionar suporte a mais formatos de áudio (FLAC, WAV, etc.)
- [ ] Interface web para facilitar o uso
- [ ] Sistema de cache para evitar downloads duplicados
- [ ] Rate limiting para evitar bloqueios
- [ ] Suporte a playlists privadas do Spotify (com autenticação)
- [ ] Webhook para notificar conclusão de downloads longos

## 📄 Licença

Este projeto é disponibilizado para fins educacionais.

## 👨‍💻 Contribuindo

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou pull requests.

---

**Nota**: Este é um projeto de laboratório de web hacking criado para fins educacionais. Use com responsabilidade.
