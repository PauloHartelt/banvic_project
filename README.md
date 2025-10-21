# Projeto ETL Banvic

## 📌 Descrição

Este projeto implementa um pipeline de **ETL (Extract, Transform, Load)** utilizando **Apache Airflow** em sua versão 2.8.1 como orquestrador, **PostgreSQL** como banco de dados fonte e Data Warehouse (DW), e **Docker Compose** para gerenciar os serviços.

O pipeline realiza:

- **Extração** de dados:
  - De um arquivo CSV (`transacoes.csv`);
  - De um banco PostgreSQL (dump `banvic.sql`).
- **Transformação** (apenas padronização e organização).
  - Armazenar os dados em um caminho padronizado com ano-mês-dia/fonte dos dados/nome da tabela.csv
  - Execução automática, todos os dias, às 04:35 da manhã.
- **Carga** dos dados extraídos em um **Data Warehouse PostgreSQL**.

Serviços docker utilizados:

- **DB**: Banco de dados Postgre fonte, carregado com o banvic.sql.
- **DW**: Banco de dados Postgre destino, produto do projeto.
- **Airflow DB**: Banco de dados interno do Airflow.
- **Airflow init**: Serviço de inicialização do Airflow.
- **Airflow webserver**: Interface web do Airflow, rodando na porta 8080.
- **Airflow scheduler**: Agendador de tarefas do Airflow.

Como executar a aplicação:

- Execute o comando de instalação das **bibliotecas Python** em seu terminal: pip install -r requirements.txt
- Inicialize o **Docker Desktop** em sua máquina.
- Com o docker inicializado, execute o comando para inicializar o **Docker Compose** em sua máquina: docker compose up
- Com o docker compose executando, aguarde até executar o **Airflow**.
- Ao airflow executar, abra o seu **navegador web** e cole o seguinte caminho: http://localhost:8080/login/
- Ao entrar na tela de usuário e senha do **Airflow**, coloque os seguintes dados para ter acesso à ferramenta:
  - Username: admin
  - Password: admin
- Com isso tudo feito, basta clicar no nome da **DAG** e clicar em Trigger DAG, no canto superior direito da tela.

---

## 🗂 Estrutura do Projeto

```bash
banvic-project/
├── airflow/                  # Configurações do Airflow
│   ├── dags/                 # DAGs do Airflow
│   │   └── banvic_dag.py     # DAG principal do ETL
│   ├── logs/                 # Logs do Airflow
│   ├── plugins/              # Plugins (se necessário)
│   └── scripts/              # Funções auxiliares
│       └── extract_helpers.py
├── airflow-db-data           # Volume do banco do Airflow
├── banvic.sql                # Script SQL com dados do banco fonte
├── data_sources/             # Fonte dos dados CSV e SQL
│   ├── transacoes.csv
│   └── banvic.sql
├── dbdata/                   # Volume do banco fonte
├── dwdata/                   # Volume do Data Warehouse
├── outputs/                  # Saída das extrações (arquivos .csv)
├── volumes/                  # Pasta de configuração dos logs do Airflow
├── docker-compose.yml        # Definição dos serviços (db, dw, airflow, etc.)
└── README.md                 # Esta documentação
├── requirements.txt          # Bibliotecas Python utilizadas
```
