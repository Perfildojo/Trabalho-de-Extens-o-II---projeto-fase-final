#!/bin/bash

# Iniciar o banco de dados
echo "Iniciando o banco de dados..."
docker-compose up -d db

# Aguardar o banco de dados estar pronto
sleep 5

# Iniciar o bot
echo "Iniciando o bot..."
docker-compose up -d bot

# Iniciar o dashboard
echo "Iniciando o dashboard..."
docker-compose up -d dashboard

echo "Todos os serviços estão rodando!"
echo "- Bot: Verifique os logs com 'docker logs mapa_do_medo_bot'"
echo "- Dashboard: Acesse http://localhost:8501"