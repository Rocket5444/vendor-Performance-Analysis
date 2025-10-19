import pandas as pd 
import os 
from sqlalchemy import create_engine 
import logging 
import time

# Create logs directory if it doesn't exist
os.makedirs('logs', exist_ok=True)  # This ensures the logs directory exists

logging.basicConfig(
    filename="logs/ingestion.log",  # Changed from .log to app.log for clarity
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filemode="a"
)

engine = create_engine('sqlite:///inventory.db')

''' This function will ingest the dataframe into database table'''
def ingest_db(df, table_name, engine):
    df.to_sql(table_name, con = engine, if_exists = 'replace', index = False)

'''this function will load the CSVs as dataframe and ingest info db'''
def load_raw_data():
    start = time.time()
    for file in os.listdir('data'):
        if '.csv' in file:
            df = pd.read_csv('data/'+file)
            logging.info(f'Ingesting {file} in db')
            ingest_db(df, file[:-4], engine)
    end = time.time()
    total_time = (end - start)/60
    logging.info('--------Ingestion Complete--------')
    
    logging.info(f'\nTotal Time Taken: {total_time} minutes')

if __name__ == '__main__':
    load_raw_data()