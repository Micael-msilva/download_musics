#!/bin/bash

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Criar ambiente virtual se não existir
if [ ! -d "backend/venv" ]; then
    echo -e "${YELLOW}[INFO] Criando ambiente virtual...${NC}"
    python3 -m venv backend/venv
fi

# Ativar o ambiente virtual
echo -e "${GREEN}[INFO] Ativando ambiente virtual...${NC}"
source backend/venv/bin/activate

# Instalar dependências se não instaladas
if [ ! -f "backend/venv/installed.flag" ]; then
    echo -e "${GREEN}[INFO] Instalando dependências do backend...${NC}"
    pip install -r backend/requirements.txt && touch backend/venv/installed.flag
fi

# Encerrar processos que ocupam as portas
for PORT in 8000 8080; do
    if lsof -i:$PORT >/dev/null; then
        echo -e "${YELLOW}[WARN] Porta $PORT em uso. Encerrando processo...${NC}"
        kill -9 $(lsof -t -i:$PORT)
    fi
done

# Iniciar o backend
echo -e "${GREEN}[INFO] Iniciando Backend na porta 8000...${NC}"
uvicorn app.main:app --reload --port 8000 --app-dir backend > backend.log 2>&1 &

# Iniciar o frontend
echo -e "${GREEN}[INFO] Iniciando Frontend na porta 8080...${NC}"
cd frontend
python3 -m http.server 8080 > ../frontend.log 2>&1 &
cd ..

# Mensagem final
sleep 2
echo -e "${GREEN}[INFO] Servidores rodando com sucesso!${NC}"
echo "- Backend:  http://127.0.0.1:8000"
echo "- Frontend: http://127.0.0.1:8080"

wait
