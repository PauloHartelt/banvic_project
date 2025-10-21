import os, shutil, psycopg2
import pandas as pd
from sqlalchemy import create_engine

def extract_csv(**context): # Cria um ajudante para extrair csv
    ds = context['ds']  # 'ano-mês-dia'
    src = '/opt/airflow/data_sources/transacoes.csv' # Caminho da pasta fonte, no Docker
    dest_dir = os.path.join('/opt/airflow/outputs', ds, 'csv') # Caminho da pasta destino, no Docker
    os.makedirs(dest_dir, exist_ok=True)
    tmp = os.path.join(dest_dir, 'transacoes.tmp')
    shutil.copyfile(src, tmp)
    os.replace(tmp, os.path.join(dest_dir, 'transacoes.csv'))

def extract_sql_db(**context): # Cria um ajudante para extrair sql
    ds = context['ds']
    out_root = '/opt/airflow/outputs' # Caminho da pasta fonte, no Docker
    out_dir_base = os.path.join(out_root, ds, 'sql')
    os.makedirs(out_dir_base, exist_ok=True)

    conn = psycopg2.connect (
        host='db', port=5432, dbname='banvic',
        user='data_engineer', password='v3rysecur&pas5w0rd'
    )
    cur = conn.cursor()
    cur.execute("""
      SELECT table_name
      FROM information_schema.tables
      WHERE table_schema='public' AND table_type='BASE TABLE';
    """)
    tables = [r[0] for r in cur.fetchall()]

    for table in tables:
        df = pd.read_sql_query(f'SELECT * FROM "{table}"', conn)
        tmp = os.path.join(out_dir_base, f'{table}.tmp')
        df.to_csv(tmp, index=False)
        os.replace(tmp, os.path.join(out_dir_base, f'{table}.csv'))

    cur.close()
    conn.close()

def load_to_dw(**context): # Cria um ajudante para carregar no DW
    ds = context['ds']
    out_root = '/opt/airflow/outputs' # Caminho da pasta destino, no Docker
    src_dir_sql = os.path.join(out_root, ds, 'sql')
    src_dir_csv = os.path.join(out_root, ds, 'csv')

    engine = create_engine('postgresql://dw_user:dw_pass@dw:5432/dw')

    # carregar todas as tabelas do SQL-export
    for fname in os.listdir(src_dir_sql):
        if not fname.endswith('.csv'): continue
        table = fname[:-4]
        df = pd.read_csv(os.path.join(src_dir_sql, fname))
        df.to_sql(table, engine, if_exists='replace', index=False)
    # carregar transacoes.csv
    df_tx = pd.read_csv(os.path.join(src_dir_csv, 'transacoes.csv'))
    df_tx.to_sql('transacoes', engine, if_exists='replace', index=False)