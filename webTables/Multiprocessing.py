import sys
sys.path.insert(0, '/home/vibhav/bar/webTables')

import os,glob
import datetime as dt
from multiprocessing import Pool
import time
import multiprocessing 
import Hybrid_Limaye
import logging

logging.basicConfig(filename='/home/vibhav/bar/log/foo.log',level=logging.DEBUG)

def helper(args):
    return Hybrid_Limaye.RunHybrid(*args)

def run_detection(domain, model, search, Levenshtein_Limaye):
    # logging.debug(a+" "+b)

    starttime = time.time()

    TableList = get_tables(domain)
    job_args = [(domain, model, search, Levenshtein_Limaye ,i) for i in TableList]
    pool = multiprocessing.Pool()
    pool.map(helper, job_args)
    pool.close()
    print('That took {} seconds'.format(time.time() - starttime))

def get_tables(domain):
    TableList = [['file812_0_cols1_rows20.pdf0.csv']]

    # no_of_cores = 15
    # # all_csv = glob.glob('/home/yasamin/Codes/WebTableAnnotation/data/Limaye/tables_instance/*.csv')
    # all_csv = glob.glob('data_csv/' + domain + '/*.csv')
    # all_csv = [a.split('/')[-1] for a in all_csv]
    # size = int(len(all_csv)/no_of_cores)

    # TableList = []
    # for loop in range(2):
    #     if loop==0:
    #         for i in range(no_of_cores):
    #             TableList.append(all_csv[i*size:(i+1)*size])
    #     else:
    #         for index,i in enumerate(range(no_of_cores*size,len(all_csv))):
    #             TableList[index].append(all_csv[i])
    
    return TableList

# if __name__ == "__main__":
#     run_detection({
#         'domain':'53838f60.ngrok.io',
#         'model':1
#         })
