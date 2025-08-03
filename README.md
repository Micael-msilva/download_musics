# 🎵 YouTube Music Downloader

Um sistema completo para download de músicas do YouTube, composto por uma API FastAPI no backend e uma interface web moderna no frontend.

## 📋 Descrição do Projeto

Este projeto permite baixar músicas do YouTube de forma simples e eficiente através de uma interface web intuitiva. Oferece as seguintes funcionalidades:

- **Download individual**: Baixe uma música específica fornecendo sua URL
- **Download em lote**: Baixe múltiplas músicas de uma só vez (formato JSON ou arquivo TXT)
- **Múltiplos formatos**: Suporte para MP3 e MP4
- **Interface moderna**: Frontend responsivo com Tailwind CSS
- **API robusta**: Backend em FastAPI com endpoints RESTful

## 🚀 Como Configurar e Executar

### Pré-requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)

### Configuração Automática

O projeto inclui um script de inicialização que configura tudo automaticamente:

```bash
# Torne o script executável
chmod +x init.sh

# Execute o script de inicialização
./init.sh
```

O script irá:
- Criar um ambiente virtual Python
- Instalar todas as dependências necessárias
- Iniciar o backend na porta 8000
- Iniciar o frontend na porta 8080

### Configuração Manual

Se preferir configurar manualmente:

#### Backend
```bash
# Navegar para o diretório backend
cd backend

# Criar ambiente virtual
python3 -m venv venv

# Ativar ambiente virtual
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt

# Iniciar o servidor
uvicorn app.main:app --reload --port 8000
```

#### Frontend
```bash
# Em outro terminal, navegar para o diretório frontend
cd frontend

# Iniciar servidor HTTP simples
python3 -m http.server 8080
```

### Acessando a Aplicação

Após a inicialização:
- **Frontend**: http://127.0.0.1:8080
- **Backend API**: http://127.0.0.1:8000
- **Documentação da API**: http://127.0.0.1:8000/docs

## 🏗️ Estrutura do Projeto

```
download_musics/
├── README.md                    # Documentação do projeto
├── init.sh                      # Script de inicialização automática
├── backend.log                  # Log do servidor backend
├── frontend.log                 # Log do servidor frontend
│
├── backend/                     # Servidor API FastAPI
│   ├── main.py                  # Ponto de entrada da aplicação
│   ├── requirements.txt         # Dependências Python
│   └── app/                     # Módulos da aplicação
│       ├── __init__.py          # Inicializador do pacote
│       ├── downloader.py        # Lógica de download (yt-dlp)
│       ├── models.py            # Modelos Pydantic
│       └── utils.py             # Funções utilitárias
│
└── frontend/                    # Interface web
    └── index.html               # Página principal (HTML + JS + Tailwind)
```

### Componentes Principais

#### Backend (`/backend`)
- **FastAPI**: Framework web moderno e rápido
- **yt-dlp**: Biblioteca para download de vídeos/áudios do YouTube
- **Pydantic**: Validação de dados e serialização
- **Uvicorn**: Servidor ASGI de alta performance

#### Frontend (`/frontend`)
- **HTML5**: Estrutura da página
- **Tailwind CSS**: Framework CSS para estilização moderna
- **JavaScript Vanilla**: Interação com a API backend

## 📡 Endpoints da API

### `POST /baixar-uma/`
Baixa uma música individual
```json
{
  "url": "https://youtube.com/watch?v=...",
  "format": "mp3"
}
```

### `POST /baixar-lista/`
Baixa múltiplas músicas
```json
{
  "urls": ["url1", "url2", "url3"],
  "format": "mp3"
}
```

## 🎯 Funcionalidades

- ✅ Download de música única
- ✅ Download em lote via JSON
- ✅ Upload de arquivo TXT com URLs
- ✅ Suporte a formatos MP3 e MP4
- ✅ Interface responsiva
- ✅ Logs de sistema
- ✅ Gerenciamento automático de arquivos temporários

## 🛠️ Tecnologias Utilizadas

- **Backend**: Python, FastAPI, yt-dlp, Pydantic, Uvicorn
- **Frontend**: HTML5, CSS3 (Tailwind), JavaScript
- **Infraestrutura**: Shell Script, HTTP Server

---

**Desenvolvido com ❤️ para facilitar o download de músicas do YouTube**