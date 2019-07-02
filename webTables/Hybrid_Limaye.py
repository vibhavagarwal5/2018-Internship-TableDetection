import pandas as pd
import time
import os
import glob
import copy

import FullPhase as fp
import LabelColumn as LC
# import MetricsCalcul_Limaye as MCal
# import PrecisionRecallF1 as PRF
import Embedding as emb
# import Embedding_LabelColumn_Looping as emb
# import Embedding_Baseline as emb

def RunHybrid(domain, model, search, Levenshtein_Limaye, TableList):
	print("I am in Hybrid of Limaye")
	print(domain, Levenshtein_Limaye)
	print(TableList)

	#contains prediction results
	mapped_Prediction_Dict = dict()
	RLU_precision = 0 
	RLU_recall = 0 
	RLU_F1 = 0
	RLU_TP_Total = 0 
	RLU_FN_Total = 0 
	RLU_FP_Total = 0
	#---------------
	Emb_precision = 0 
	Emb_recall = 0 
	Emb_F1 = 0 
	Emb_TP_Total = 0
	Emb_FN_Total = 0
	Emb_FP_Total = 0
	#---------------
	HybridI_precision = 0
	HybridI_recall = 0  
	HybridI_F1 = 0
	HybridI_TP_Total = 0 
	HybridI_FN_Total = 0 
	HybridI_FP_Total = 0
	#---------------
	HybridII_precision = 0
	HybridII_recall = 0  
	HybridII_F1 = 0
	HybridII_TP_Total = 0 
	HybridII_FN_Total = 0 
	HybridII_FP_Total = 0
	
	#change the path to  have csv filename without the path inside
	# os.chdir('/home/yasamin/Codes/WebTableAnnotation/data/Limaye/tables_instance/')
	os.chdir('/home/vibhav/bar/data_csv/' + domain + '/')

	entity_dir = '/home/vibhav/bar/data_csv_out/' + domain

	if not os.path.exists(entity_dir):
		oldmask = os.umask(000)
		os.makedirs(entity_dir,0o777)
		os.umask(oldmask)

	#reading all CSV files in path
	# allCsvTableFiles = glob.glob('*.csv')

	start_time = time.time()
	
	for table_csv in TableList:
		
		# if(table_csv in TableList):
			# os.chdir('/home/yasamin/Codes/WebTableAnnotation/data/Limaye/tables_instance/')
			# os.chdir('/home/vibhav/bar/data_csv/www.bag.admin.ch/')
			with open(table_csv, 'r', encoding='utf-8') as csvTableFile:
				print("This is the Table file name : ",table_csv)
				print('')
				T = pd.read_csv(table_csv, header=None)
				#switch path to normal form
				os.chdir('/home/yasamin/Codes/WebTableAnnotation/')
				

				#Remove the row if there is no GT in entity file for it.
				# entity_csv = table_csv
				# os.chdir('/home/yasamin/Codes/WebTableAnnotation/data/Limaye/entities_instance/')
				# with open(entity_csv, 'r', encoding='utf-8') as csvEntityFile:
				# 	print("This is the Entity file name : ",entity_csv)
				# 	E = pd.read_csv(entity_csv, header=None)
				# 	count_row = T.shape[0]
				# 	for i in range(0, count_row):
				# 		if not(i in E[E.columns[-1]].values):
				# 			print("This i does not exists:",i)
				# 			T = T.drop([i])										
						
				# #switch path to normal form
				# os.chdir('/home/yasamin/Codes/WebTableAnnotation/')
			#----------------------------------------------------------------
								#uncomment for Refined Lookup
			#----------------------------------------------------------------
				# RLU_TPrimeIsAnnotated , RLU_TPrimeAnnotation = fp.getFullPhase(T,table_csv, search, Levenshtein_Limaye)
				# print("Refined Lookup result:")
				# print("-"*30)
				# print(RLU_TPrimeAnnotation)
				# print(RLU_TPrimeIsAnnotated)
				
			#----------------------------------------------------------------
								#uncomment for Embedding
			#----------------------------------------------------------------
				Emb_TPrimeIsAnnotated, Emb_TPrimeAnnotation = emb.getEmbedding(T, model, search, Levenshtein_Limaye)

				print('Time1 hybrid Limaye: ' + format(time.time() - start_time))

				print("\nEmbedding result:")
				print("-"*30)
				print(Emb_TPrimeAnnotation)
				print(Emb_TPrimeIsAnnotated)
				T['new_col'] = Emb_TPrimeAnnotation.values()
				print(T)
				T.to_csv(entity_dir + "/" + table_csv,header=False,index=False)

				print('Time2 hybrid Limaye: ' + format(time.time() - start_time))
				
			#----------------------------------------------------------------
								#uncomment for Hybrid I(uncomment also embedding and RLU)
			#----------------------------------------------------------------
			# #Hybrid1

			# 	HybridI_TPrimeIsAnnotated = copy.deepcopy(RLU_TPrimeIsAnnotated)
			# 	HybridI_TPrimeAnnotation = copy.deepcopy(RLU_TPrimeAnnotation)
				
			# 	for k in HybridI_TPrimeIsAnnotated:
			# 		if(HybridI_TPrimeIsAnnotated[k] == True):
			# 			continue
			# 		elif(HybridI_TPrimeIsAnnotated[k] == False):
			# 			try:
			# 				HybridI_TPrimeIsAnnotated[k] = Emb_TPrimeIsAnnotated[k]
			# 				HybridI_TPrimeAnnotation[k] = Emb_TPrimeAnnotation[k]
			# 			except KeyError:
			# 				HybridI_TPrimeIsAnnotated[k] = False
			# 				HybridI_TPrimeAnnotation[k] = ' '
				
			# 	print("Hybrid I result:")
			# 	print("-"*30)
			# 	print(HybridI_TPrimeAnnotation)
			# 	print(HybridI_TPrimeIsAnnotated)
				
			#----------------------------------------------------------------
								#uncomment for Hybrid II(uncomment also embedding and RLU)
			#----------------------------------------------------------------
			# #Hybrid2
			# 	HybridII_TPrimeIsAnnotated = copy.deepcopy(Emb_TPrimeIsAnnotated)
			# 	HybridII_TPrimeAnnotation = copy.deepcopy(Emb_TPrimeAnnotation)

			# 	for k in HybridII_TPrimeIsAnnotated:
			# 		if(HybridII_TPrimeIsAnnotated[k] == True):
			# 			continue
			# 		elif(HybridII_TPrimeIsAnnotated[k] == False):
			# 			try:
			# 				HybridII_TPrimeIsAnnotated[k] = RLU_TPrimeIsAnnotated[k]
			# 				HybridII_TPrimeAnnotation[k] = RLU_TPrimeAnnotation[k]
			# 			except KeyError:
			# 				HybridII_TPrimeIsAnnotated[k] = False
			# 				HybridII_TPrimeAnnotation[k] = ' '
						
			# 	print("Hybrid II result:")
			# 	print("-"*30)
			# 	print(HybridII_TPrimeAnnotation)
			# 	print(HybridII_TPrimeIsAnnotated)



			#----------------------------------------------------------------
			#----------------------------------------------------------------
									#Metrics
			#----------------------------------------------------------------
			#----------------------------------------------------------------


			#----------------------------------------------------------------
								#uncomment for Hybrid I(uncomment also embedding and RLU)
			#----------------------------------------------------------------
				# #metrics:
				# HybridI_TP, HybridI_FN, HybridI_FP =  MCal.MetricsCalcul(T,table_csv,HybridI_TPrimeAnnotation,HybridI_TPrimeIsAnnotated)
				# HybridI_TP_Total = HybridI_TP_Total+HybridI_TP
				# HybridI_FN_Total = HybridI_FN_Total+HybridI_FN
				# HybridI_FP_Total = HybridI_FP_Total+HybridI_FP
				# HybridI_precision, HybridI_recall, HybridI_F1 = PRF.Precision_Recall_F1(HybridI_TP_Total,HybridI_FN_Total,HybridI_FP_Total)
			#----------------------------------------------------------------
								#uncomment for Hybrid II(uncomment also embedding and RLU)
			#----------------------------------------------------------------
				
				# # metrics:
				# HybridII_TP, HybridII_FN, HybridII_FP =  MCal.MetricsCalcul(T,table_csv,HybridII_TPrimeAnnotation,HybridII_TPrimeIsAnnotated)
				# HybridII_TP_Total = HybridII_TP_Total+HybridII_TP
				# HybridII_FN_Total = HybridII_FN_Total+HybridII_FN
				# HybridII_FP_Total = HybridII_FP_Total+HybridII_FP
				# HybridII_precision, HybridII_recall, HybridII_F1 = PRF.Precision_Recall_F1(HybridII_TP_Total,HybridII_FN_Total,HybridII_FP_Total)
			#----------------------------------------------------------------
								#uncomment for Refined Lookup
			#----------------------------------------------------------------
			# #metrics:
			# 	RLU_TP, RLU_FN, RLU_FP =  MCal.MetricsCalcul(T,table_csv,RLU_TPrimeAnnotation,RLU_TPrimeIsAnnotated)
			# 	RLU_TP_Total = RLU_TP_Total+RLU_TP
			# 	RLU_FN_Total = RLU_FN_Total+RLU_FN
			# 	RLU_FP_Total = RLU_FP_Total+RLU_FP
			# 	RLU_precision, RLU_recall, RLU_F1 = PRF.Precision_Recall_F1(RLU_TP_Total,RLU_FN_Total,RLU_FP_Total)		
			
			#----------------------------------------------------------------
								#uncomment for Embedding
			#----------------------------------------------------------------	
			#metrics:
				# Emb_TP, Emb_FN, Emb_FP =  MCal.MetricsCalcul(T,table_csv,Emb_TPrimeAnnotation,Emb_TPrimeIsAnnotated)
				# Emb_TP_Total = Emb_TP_Total+Emb_TP
				# Emb_FN_Total = Emb_FN_Total+Emb_FN
				# Emb_FP_Total = Emb_FP_Total+Emb_FP
				# Emb_precision, Emb_recall, Emb_F1 = PRF.Precision_Recall_F1(Emb_TP_Total,Emb_FN_Total,Emb_FP_Total)
				
				
	#------------------------------------------------------------------------------------------
	# print("Final result of the core partition")
	# print("-"*30) 
	#----------------------------------------------------------------
	# print("Final Refined Lookup:")
	# print("Final RLU Precision : ", RLU_precision )
	# print("Final RLU Recall : ",RLU_recall)
	# print("Final RLU F1 : ",RLU_F1)
	# print("-"*30)
	# print("Final RLU FN ",RLU_FN_Total)
	# print("Final RLU FP ",RLU_FP_Total)
	# print("Final RLU TP ",RLU_TP_Total)
	# print("-"*30)
	#----------------------------------------------------------------
	# print("Embedding:")
	# print("Final Embedding Precision : ", Emb_precision )
	# print("Final Embedding Recall : ",Emb_recall)
	# print("Final Embedding F1 : ",Emb_F1)
	# print("-"*30)
	# print("Final Embedding FN ",Emb_FN_Total)
	# print("Final Embedding FP ",Emb_FP_Total)
	# print("Final Embedding TP ",Emb_TP_Total)
	# print("-"*30)
	#----------------------------------------------------------------
	# print("Hybrid I:")
	# print("Final Hybrid I Precision : ", HybridI_precision )
	# print("Final Hybrid I Recall : ",HybridI_recall)
	# print("Final Hybrid I F1 : ",HybridI_F1)
	# print("-"*30)
	# print("Final Hybrid I FN ",HybridI_FN_Total)
	# print("Final Hybrid I FP ",HybridI_FP_Total)
	# print("Final Hybrid I TP ",HybridI_TP_Total)
	# print("-"*30)	
	#----------------------------------------------------------------
	# print("Hybrid II:")
	# print("Final Hybrid II Precision : ", HybridII_precision )
	# print("Final Hybrid II Recall : ",HybridII_recall)
	# print("Final Hybrid II F1 : ",HybridII_F1)
	# print("-"*30)
	# print("Final Hybrid II FN ",HybridII_FN_Total)
	# print("Final Hybrid II FP ",HybridII_FP_Total)
	# print("Final Hybrid II TP ",HybridII_TP_Total)
	# print("-"*30)	
	print("\n-----------------------------------------------------------------------------------")
	print("Run time for 1 lookup phase and one embedding phase, Local Endpoint ",time.time() - start_time)
	print("-----------------------------------------------------------------------------------\n")
	return
