import ccxt
import pandas as pd
from datetime import datetime, timedelta

# write a sqlalchemy script to upload data to a postgresql database
from sqlalchemy import create_engine
from psql import PSQL
import argparse




def fetch_price(pair_name: str='BTC/USDT'):
    '''Fetch data from binance and return df as dataframe'''
    exchange = ccxt.binance()
    current_time = datetime.now()
    past_time = current_time - timedelta(days=1)
    since = int(past_time.timestamp() * 1000)
    ohlcv = exchange.fetch_ohlcv(pair_name, timeframe='1h', since=since)
    df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    df.set_index('timestamp', inplace=True)
    df['name'] = pair_name
    # Reindex columns to move 'name' to the first position
    df = df.reindex(columns=['name'] + [col for col in df.columns if col != 'name'])
    return df



def crypto_upload_all(con_string: str = 'postgresql://lucaslee@localhost:5432/crypto'):
    # Create a database connection
    engine = create_engine(con_string)
    target_list = ['ETH/USDT', 'BTC/USDT', 'DOGE/USDT', 'SOL/USDT', 'BCH/USDT', 'WLD/USDT']

    query = "truncate table crypto_price"
    psql = PSQL(url=con_string)
    psql.execute(query)
    for v in target_list:
        df = fetch_price(pair_name=v)
        df.reset_index(inplace=True)
        df.to_sql('crypto_price', con=engine, if_exists='append', index=False)
    psql.conn.close()
    print('Done!!')
    
def update_one_pair(pair_name: str, con_string: str = 'postgresql://lucaslee@localhost:5432/crypto'):
    ava_list = ['ETH/USDT', 'BTC/USDT', 'DOGE/USDT', 'SOL/USDT', 'BCH/USDT', 'WLD/USDT']
    if pair_name not in ava_list:
        print(f'{pair_name} is not available!')
        return
    else:
        psql = PSQL(url=con_string)
        query = "delete from crypto_price where name = '%s'" % pair_name
        psql.execute(query)
        psql.conn.close()
        df = fetch_price(pair_name=pair_name)
        df.reset_index(inplace=True)
        df.to_sql('crypto_price', con=create_engine(con_string), if_exists='append', index=False)
    
    print(f'{pair_name} updated!')

def read_crypto_from_db(con_string: str = 'postgresql://lucaslee@localhost:5432/crypto'):
    query = "select * from crypto_price"
    df = pd.read_sql_query(query, con=con_string)
    return df
    
if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description="Doing the dba stuff.")
    parser.add_argument(
        "-c", "--cls", required=False, help="The pgpool host class name to insert."
    )
    parser.add_argument(
        "-dev", "--developer", action='store_true', required=False, help="VIP interfacce of pgpool nodes"
    )

    args = parser.parse_args()
    
    if args.developer:
        input_name = input('Type your host username to continue: ')
        input_hostname = input('Type your host name IP to continue: ')
        con_string = f'postgresql://{input_name}@{input_hostname}:5432/crypto'
        print('connecting to:', con_string)
        input_pair = input('Type the pair name to update(if all means update all): ')
        if input_pair == 'all':
            crypto_upload_all(con_string=con_string)
        else:
            update_one_pair(input_pair, con_string=con_string)
        print("Done!!")
    else:
        con_string = 'postgresql://lucaslee@localhost:5432/crypto'
        crypto_upload_all(con_string=con_string)
    
        # df = read_crypto_from_db(con_string=con_string)
        # print(df.head())
        # print(df.shape)
        
        # update_one_pair('BCH/USDT', con_string=con_string)