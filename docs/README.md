# Mapa do Medo

O **Mapa do Medo** é um sistema que permite aos usuários reportar ocorrências de segurança em sua região, como roubos, tiroteios e acidentes. Esses dados são armazenados em um banco de dados e podem ser visualizados em um dashboard interativo. Além disso, o sistema utiliza técnicas de Machine Learning para prever tendências de ocorrências.

## Como Rodar o Sistema

### Pré-requisitos

- Python 3.8 ou superior
- Bibliotecas listadas nos arquivos `requirements.txt` de cada módulo

### Instalação

1. Clone o repositório:
   ```bash
   git clone https://github.com/seu-usuario/Mapa_do_Medo.git
   cd Mapa_do_Medo

### Instale as dependências:

Para o bot:

bash
pip install -r bot/requirements.txt
Para o dashboard:

bash
pip install -r dashboard/requirements.txt
Para Machine Learning:

bash
pip install -r machine_learning/requirements.txt

### Configure o banco de dados:

O banco de dados SQLite será criado automaticamente ao rodar o bot.

### Executando o Bot

Navegue até o diretório do bot:

bash
cd bot
Execute o bot:

bash
python bot.py
Executando o Dashboard
Navegue até o diretório do dashboard:

bash
cd dashboard
Execute o dashboard:

bash
streamlit run dashboard.py
Executando o Modelo de Machine Learning
Navegue até o diretório de Machine Learning:

bash
cd machine_learning

### Treine o modelo:

bash
python model_training.py

### Faça previsões:

bash
python predictions.py

### Estrutura do Projeto

bot/: Código do bot Telegram para coleta de ocorrências.

dashboard/: Dashboard interativo para visualização de dados.

machine_learning/: Modelos de Machine Learning para previsão de ocorrências.

data/: Armazenamento de dados brutos e processados.

notebooks/: Análises exploratórias e experimentos.

docs/: Documentação do projeto.

### Contribuição
Contribuições são bem-vindas! Siga as diretrizes do CONTRIBUTING.md para enviar pull requests.