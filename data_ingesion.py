# libraries needed
import pandas as pd
import os
from sqlalchemy import create_engine
import logging
import time

# Tracking logg info about the project
logging.basicConfig(
    filename = 'loggs/ingesion_db.log',
    level = logging.DEBUG,
    format = '%(asctime)s - %(levelname)s - %(message)s',
    filemode = 'a'
)

# create mysql engine
engine = create_engine(f"mysql+mysqlconnector://root:root@localhost:3306/inventory")


# data insertion function
def ingest_db(data, table_name, engine):
    '''This function connect database'''
    data.to_sql(table_name, con=engine, if_exists='replace', index=False, chunksize=1000, method='multi')


# data load function
def load_raw_data():

    '''This function load the csv into dataframe and ingest dataframe into database in mysql'''
    
    start = time.time()
    for file in os.listdir('datasets'):
        df = pd.read_csv(f'datasets\{file}')
        logging.info(f'ingesting {file} in db.')
        print('data transfering...........')
        ingest_db(df, file[:-4], engine)
        print('data insert successfully ' + file)

    end = time.time()
    total_time = (end-start)/60
    logging.info('-------------ingession complete!---------------')
    logging.info(f'\n Total time taken {total_time} minutes.')

# call the function
if __name__ == '__main__':
    load_raw_data()