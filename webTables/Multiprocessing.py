import sys
sys.path.insert(0, '/home/vibhav/bar/webTables')

import os,glob
import datetime as dt
from multiprocessing import Pool
import time
import multiprocessing 
import Hybrid_Limaye
import concurrent.futures
from functools import partial
import logging

logging.basicConfig(filename='/home/vibhav/bar/log/foo.log',level=logging.DEBUG)

no_of_cores = 10

def helper(args):
    return Hybrid_Limaye.RunHybrid(*args)

def run_detection(info_data):
    logging.debug("INSIDE MULT: "+ str(info_data['domain']))
    starttime = time.time()
    TableList = get_tables(info_data['domain'])

    # Hybrid_Limaye.RunHybrid(info_data, TableList)
    
    # job_args = [(info_data ,tables) for tables in TableList]

    # with concurrent.futures.ProcessPoolExecutor() as executor:
    #     executor.map(helper, job_args)

    # pool = multiprocessing.Pool()
    # pool.map(partial(Hybrid_Limaye.RunHybrid, info_data=info_data), TableList)
    # pool.close()

    processes = []
    for i in range(0,no_of_cores):
        p = multiprocessing.Process(
            target=Hybrid_Limaye.RunHybrid, 
            args=(info_data,TableList[i]))
        processes.append(p)
        p.start()
        
    for process in processes:
        process.join()

    logging.debug('That took {} seconds'.format(time.time() - starttime))

def get_tables(domain):
    # TableList = [['file227142_1_cols1_rows7.pdf0.csv']]
    
    # TableList = [['file389632_0_cols1_rows31.pdf0.csv', 'file592476_0_cols1_rows8.pdf1.csv', 'file258799_0_cols1_rows40.pdf0.csv', 'file227142_1_cols1_rows7.pdf0.csv', 'file383362_0_cols1_rows21.pdf0.csv', 'file145480_2_cols1_rows52.pdf0.csv'],[ 'file40567_0_cols1_rows6.pdf0.csv', 'file451761_0_cols1_rows19.pdf0.csv', 'file568285_0_cols1_rows15.pdf0.csv', 'file386878_0_cols1_rows23.pdf0.csv', 'file544895_0_cols1_rows10.pdf0.csv']]

    # all_csv = glob.glob('/home/yasamin/Codes/WebTableAnnotation/data/Limaye/tables_instance/*.csv')
    all_csv = glob.glob('data_csv/' + domain + '/*.csv')
    all_csv = [a.split('/')[-1] for a in all_csv]
    size = int(len(all_csv)/no_of_cores)

    TableList = []
    for loop in range(2):
        if loop==0:
            for i in range(no_of_cores):
                TableList.append(all_csv[i*size:(i+1)*size])
        else:
            for index,i in enumerate(range(no_of_cores*size,len(all_csv))):
                TableList[index].append(all_csv[i])

    return TableList

# if __name__ == "__main__":
#     info_data = {
#             'domain': '04bd5aef.ngrok.io',
#             # 'Levenshtein_Limaye': Levenshtein_Limaye.get(),
#             # 'model': model.get(),
#             # 'search': search.get()    
#         }
#     run_detection(info_data)
