############################################################################################
# IFNepitope2 is developed for predicting, desigining and scanning IFN-γ induding peptides #
# for human and mouse hosts. It is developed by Prof G. P. S. Raghava's group.                   #
# Please cite: https://webs.iiitd.edu.in/raghava/ifnepitope2/                              #
###########################################################################################
import argparse
import warnings
import subprocess
import pkg_resources
import os
import sys
import numpy as np
import pandas as pd
import math
import itertools
from collections import Counter
import pickle
import re
import glob
import time
import uuid
from time import sleep
from tqdm import tqdm
from sklearn.ensemble import ExtraTreesClassifier
import zipfile
import platform
warnings.filterwarnings('ignore')

parser = argparse.ArgumentParser(description='Please provide following arguments') 

BLAST_BINARIES = {
    "Linux": "/../blast_binaries/linux/blastp",
    "Darwin": "/../blast_binaries/mac/blastp",
    "Windows": "/../blast_binaries/windows/blastp.exe",
}

def get_blastp_path(def_file_path):
    operating_system = platform.system()
    blastp_path = def_file_path + BLAST_BINARIES.get(operating_system)
    if not blastp_path:
        print(f"Unsupported operating system: {operating_system}")
        return None

    if not os.path.exists(blastp_path):
        print(f"BLASTP binary not found: {blastp_path}")
        return None

    return blastp_path



## Read Arguments from command
parser.add_argument("-i", "--input", type=str, required=True, help="Input: protein or peptide sequence(s) in FASTA format or single sequence per line in single letter code")
parser.add_argument("-o", "--output",type=str, help="Output: File for saving results by default outfile.csv")
parser.add_argument("-s", "--host",type=int, choices = [1,2], help="Host: 1: Human, 2: Mouse, by default 1")
parser.add_argument("-j", "--job",type=int, choices = [1,2,3], help="Job Type: 1:Predict, 2: Design, 3:Scan, by default 1")
parser.add_argument("-t","--threshold", type=float, help="Threshold: Value between 0 to 1 by default 0.49")
parser.add_argument("-w","--winleng", type=int, choices =range(8, 21), help="Window Length: 8 to 20 (scan mode only), by default 8")
parser.add_argument("-d","--display", type=int, choices = [1,2], help="Display: 1:IFN-γ inducers, 2: All peptides, by default 1")
args = parser.parse_args()

# Function for generating all possible mutants
def mutants(file1,file2):
    std = list("ACDEFGHIKLMNPQRSTVWY")
    cc = []
    dd = []
    ee = []
    df2 = file2
    df2.columns = ['Name']
    df1 = file1
    df1.columns = ['Seq']
    for k in range(len(df1)):
        cc.append(df1['Seq'][k])
        dd.append('Original_'+'Seq'+str(k+1))
        ee.append(df2['Name'][k])
        for i in range(0,len(df1['Seq'][k])):
            for j in std:
                if df1['Seq'][k][i]!=j:
                    dd.append('Mutant_'+df1['Seq'][k][i]+str(i+1)+j+'_Seq'+str(k+1))
                    cc.append(df1['Seq'][k][:i] + j + df1['Seq'][k][i + 1:])
                    ee.append(df2['Name'][k])
    xx = pd.concat([pd.DataFrame(ee),pd.DataFrame(dd),pd.DataFrame(cc)],axis=1)
    xx.columns = ['Seq_ID','Mutant_ID','Seq']
    return xx
# Function for generating pattern of a given length
def seq_pattern(file1,file2,num):
    df1 = file1
    df1.columns = ['Seq']
    df2 = file2
    df2.columns = ['Name']
    cc = []
    dd = []
    ee = []
    for i in range(len(df1)):
        for j in range(len(df1['Seq'][i])):
            xx = df1['Seq'][i][j:j+num]
            if len(xx) == num:
                cc.append(df2['Name'][i])
                dd.append('Pattern_'+str(j+1)+'_Seq'+str(i+1))
                ee.append(xx)
    df3 = pd.concat([pd.DataFrame(cc),pd.DataFrame(dd),pd.DataFrame(ee)],axis=1)
    df3.columns= ['Seq_ID','Pattern_ID','Seq']
    return df3
# Function to check the seqeunce
def readseq(file):
    with open(file) as f:
        records = f.read()
    records = records.split('>')[1:]
    seqid = []
    seq = []
    for fasta in records:
        array = fasta.split('\n')
        name, sequence = array[0].split()[0], re.sub('[^ACDEFGHIKLMNPQRSTVWY-]', '', ''.join(array[1:]).upper())
        seqid.append('>'+name)
        seq.append(sequence)
    if len(seqid) == 0:
        f=open(file,"r")
        data1 = f.readlines()
        for each in data1:
            seq.append(each.replace('\n',''))
        for i in range (1,len(seq)+1):
            seqid.append(">Seq_"+str(i))
    df1 = pd.DataFrame(seqid)
    df2 = pd.DataFrame(seq)
    return df1,df2
# Function to check the length of seqeunces
def lenchk(file1):
    cc = []
    df1 = file1
    df1.columns = ['seq']
    for i in range(len(df1)):
        if len(df1['seq'][i])>20:
            cc.append(df1['seq'][i][0:20])
        else:
            cc.append(df1['seq'][i])
    df2 = pd.DataFrame(cc)
    df2.columns = ['Seq']
    return df2
# Function to generate the features out of seqeunces
def feature_gen(file,q=1):
    std = list("ACDEFGHIKLMNPQRSTVWY")
    df1 = file
    df1.columns = ['Seq']
    zz = df1.Seq
    dd = []
    for i in range(0,len(zz)):
        cc = []
        for j in std:
            for k in std:
                count = 0
                temp = j+k
                for m3 in range(0,len(zz[i])-q):
                    b = zz[i][m3:m3+q+1:q]
                    b.upper()
                    if b == temp:
                        count += 1
                    composition = (count/(len(zz[i])-(q)))*100
                cc.append(composition)
        dd.append(cc)
    df2 = pd.DataFrame(dd)
    head = []
    for s in std:
        for u in std:
            head.append("DPC"+str(q)+"_"+s+u)
    df2.columns = head
    return df2
# Function to process the blast output
def BLAST_processor(blast_result,name1,ml_results,thresh):
    if os.stat(blast_result).st_size != 0:
        df1 = pd.read_csv(blast_result, sep="\t", names=['name','hit','identity','r1','r2','r3','r4','r5','r6','r7','r8','r9'])
        df__2 = name1
        df2 = pd.DataFrame()
        df2 = df2.append(df__2.values.tolist())
        df3 = ml_results
        cc = []
        for i in df2[0]:
            kk = i.replace('>','')
            if len(df1.loc[df1.name==kk])>0:
                df4 = df1[['name','hit']].loc[df1['name']==kk].reset_index(drop=True)
                if df4['hit'][0].split('_')[0]=='P':
                    cc.append(0.5)
                if df4['hit'][0].split('_')[0]=='N':
                    cc.append(-0.5)
            else:
                cc.append(0)
        df6 = pd.DataFrame()
        df6['Seq_ID'] = [i.replace('>','') for i in df2[0]]
        df6['ML_Score'] = df3['ML_score']
        df6['BLAST_Score'] = cc
        df6['Total_Score'] = df6['ML_Score']+df6['BLAST_Score']
        df6['Prediction'] = ['IFN-γ inducer' if df6['Total_Score'][i]>thresh else 'Non-inducer' for i in range(0,len(df6))]
    else:
        df__2 = name1
        df3 = ml_results
        df2 = pd.DataFrame()
        df2 = df2.append(df__2.values.tolist())
        ss = []
        vv = []
        for j in df2[0]:
            ss.append(j.replace('>',''))
            vv.append(0)
        df6 = pd.DataFrame()
        df6['Seq_ID'] = ss
        df6['ML_Score'] = df3['ML_score']
        df6['BLAST_Score'] = vv
        df6['Total_Score'] = df6['ML_Score']+df6['BLAST_Score']
        df6['Prediction'] = ['IFN-γ inducer' if df6['Total_Score'][i]>thresh else 'Non-inducer' for i in range(0,len(df6))]
    return df6
# Function to read and implement the model
def model_run(file1,file2):
    a = []
    data_test = file1
    clf = pickle.load(open(file2,'rb'))
    y_p_score1=clf.predict_proba(data_test)
    y_p_s1=y_p_score1.tolist()
    a.extend(y_p_s1)
    df = pd.DataFrame(a)
    df1 = df.iloc[:,-1].round(2)
    df2 = pd.DataFrame(df1)
    df2.columns = ['ML_score']
    return df2
def main():  
    ('###############################################################################################')
    print('# This program IFNepitope2 is developed for predicting, desigining and scanning          #')
    print('# IFN-γ inducing peptides, developed by Prof G. P. S. Raghava group.                     #')
    print('# Please cite: IFNepitope2; available at https://webs.iiitd.edu.in/raghava/ifnepitope2/  #')
    print('##########################################################################################')

    # Parameter initialization or assigning variable for command level arguments

    Sequence= args.input        # Input variable 
    
    # Output file 
    
    if args.output == None:
        result_filename= "outfile.csv" 
    else:
        result_filename = args.output
            
    # Threshold 
    if args.threshold == None:
            Threshold = 0.49
    else:
            Threshold= float(args.threshold)
    # Job Type 
    if args.job == None:
            Job = int(1)
    else:
            Job = int(args.job)
    # Window Length 
    if args.winleng == None:
            Win_len = int(9)
    else:
            Win_len = int(args.winleng)

    # Display
    if args.display == None:
            dplay = int(1)
    else:
            dplay = int(args.display)
    # Host
    if args.host == None:
            hst = int(1)
    else:
            hst = int(args.host)

    #####################################BLAST Path############################################
    nf_path = os.path.dirname(__file__)
    blastp = get_blastp_path(nf_path)
    blastdb1 = nf_path + "/../blast_db/human_db"
    blastdb2 = nf_path + "/../blast_db/mouse_db"

    ###########################################################################################

    if Job==3:
        print("\n");
        print('##############################################################################')
        print('Summary of Parameters:')
        print('Input File: ',Sequence,'; Threshold: ', Threshold,'; Job Type: ',Job)
        print('Output File: ',result_filename,'; Window Length: ',Win_len,'; Display: ',dplay)
        print('##############################################################################')
    else:
        print("\n");
        print('##############################################################################')
        print('Summary of Parameters:')
        print('Input File: ',Sequence,'; Threshold: ', Threshold,'; Job Type: ',Job)
        print('Output File: ',result_filename,'; Display: ',dplay)
        print('# ############################################################################')
    #======================= Prediction Module start from here =====================
    if Job == 1:
        print('\n======= Thanks for using Predict module of IFNepitope2. Your results will be stored in file :',result_filename,' =====\n')
        df_2,dfseq = readseq(Sequence)
        df1 = lenchk(dfseq)
        X = feature_gen(df1)
        if hst == 1:
            mlres = model_run(X, nf_path + '/../model/human_et.pkl')
        else:
            mlres = model_run(X,nf_path + '/../model/mouse_et.pkl')
        filename = str(uuid.uuid4())
        df11 = pd.concat([df_2,df1],axis=1)
        df11.to_csv(filename,index=None,header=False,sep="\n")
        mlres = mlres.round(3)
        if hst == 1:    
            os.system(blastp + " -task blastp-short -db " + blastdb1 + "-query " + filename  + " -out RES_1_6_6.out -outfmt 6 -evalue 0.001")
        else:
            os.system(blastp + " -task blastp-short -db " + blastdb2 + "-query " + filename  + " -out RES_1_6_6.out -outfmt 6 -evalue 0.001")
        df44 = BLAST_processor('RES_1_6_6.out',df_2,mlres,Threshold)
        df44['Sequence'] = df1.Seq
        df44 = df44[['Seq_ID','Sequence','ML_Score','BLAST_Score','Total_Score','Prediction']]
        if dplay == 1:
            df44 = df44.loc[df44.Prediction=="IFN-γ inducer"]
        else:
            df44 = df44
        df44 = round(df44,3)
        df44.to_csv(result_filename, index=None)
        os.remove('RES_1_6_6.out')
        os.remove(filename)
        print("\n=========Process Completed. Have an awesome day ahead.=============\n")    
    #===================== Design Model Start from Here ======================
    elif Job == 2:
        print('\n======= Thanks for using Design module of IFNepitope2. Your results will be stored in file :',result_filename,' =====\n')
        print('==== Designing Peptides: Processing sequences please wait ...')
        df_2,dfseq = readseq(Sequence)
        df1 = lenchk(dfseq)
        df_1 = mutants(df1,df_2)
        dfseq = df_1[['Seq']]
        X = feature_gen(dfseq)
        if hst == 1:
            mlres = model_run(X, nf_path + '/../model/human_et.pkl')
        else:
            mlres = model_run(X, nf_path + '/../model/mouse_et.pkl')
        filename = str(uuid.uuid4())
        df_1['Mutant'] = ['>'+df_1['Mutant_ID'][i] for i in range(len(df_1))]
        df11 = df_1[['Mutant','Seq']] 
        df11.to_csv(filename,index=None,header=False,sep="\n")
        mlres = mlres.round(3)
        if hst == 1:
            os.system(blastp + " -task blastp-short -db " + blastdb1 + "/human_db -query " + filename  + " -out RES_1_6_6.out -outfmt 6 -evalue 0.001")
        else:
            os.system(blastp + " -task blastp-short -db " + blastdb2 + "/mouse_db -query " + filename  + " -out RES_1_6_6.out -outfmt 6 -evalue 0.001")
        df44 = BLAST_processor('RES_1_6_6.out',df11[['Mutant']],mlres,Threshold)
        df44['Mutant_ID'] = ['_'.join(df44['Seq_ID'][i].split('_')[:-1]) for i in range(len(df44))]
        df44.drop(columns=['Seq_ID'],inplace=True)
        df44['Seq_ID'] = [i.replace('>','') for i in df_1['Seq_ID']]
        df44['Sequence'] = df_1.Seq
        df44 = df44[['Seq_ID','Mutant_ID','Sequence','ML_Score','BLAST_Score','Total_Score','Prediction']]
        if dplay == 1:
            df44 = df44.loc[df44.Prediction=="IFN-γ inducer"]
        else:
            df44 = df44
        df44 = round(df44,3)
        df44.to_csv(result_filename, index=None)
        os.remove('RES_1_6_6.out')
        os.remove(filename)
        print("\n=========Process Completed. Have an awesome day ahead.=============\n")
    #=============== Scan Model start from here ==================
    elif Job==3:
        print('\n======= Thanks for using Scan module of IFNepitope2. Your results will be stored in file :',result_filename,' =====\n')
        print('==== Scanning Peptides: Processing sequences please wait ...')
        df_2,dfseq = readseq(Sequence)
        df_1 = seq_pattern(dfseq,df_2,Win_len)
        dfseq = df_1[['Seq']]
        X = feature_gen(dfseq)
        if hst == 1:
            mlres = model_run(X, nf_path + '/../model/human_et.pkl')
        else:
            mlres = model_run(X, nf_path + '/../model/mouse_et.pkl')
        filename = str(uuid.uuid4())
        df_1['Pattern'] = ['>'+df_1['Pattern_ID'][i] for i in range(len(df_1))]
        df11 = df_1[['Pattern','Seq']]
        df11.to_csv(filename,index=None,header=False,sep="\n")
        mlres = mlres.round(3)
        if hst == 1:
            os.system(blastp + " -task blastp-short -db " + blastdb1 + "/human_db -query " + filename  + " -out RES_1_6_6.out -outfmt 6 -evalue 0.001")
        else:
            os.system(blastp + " -task blastp-short -db " + blastdb2 + "/mouse_db -query " + filename  + " -out RES_1_6_6.out -outfmt 6 -evalue 0.001")
        df44 = BLAST_processor('RES_1_6_6.out',df11[['Pattern']],mlres,Threshold)
        df44['Pattern_ID'] = ['_'.join(df44['Seq_ID'][i].split('_')[:-1]) for i in range(len(df44))]
        df44.drop(columns=['Seq_ID'],inplace=True)
        df44['Seq_ID'] = [i.replace('>','') for i in df_1['Seq_ID']]
        df44['Sequence'] = df_1.Seq
        df44 = df44[['Seq_ID','Pattern_ID','Sequence','ML_Score','BLAST_Score','Total_Score','Prediction']]
        if dplay == 1:
            df44 = df44.loc[df44.Prediction=="IFN-γ inducer"]
        else:
            df44 = df44
        df44 = round(df44,3)
        df44.to_csv(result_filename, index=None)
        os.remove('RES_1_6_6.out')
        os.remove(filename)
        print("\n=========Process Completed. Have an awesome day ahead.=============\n")
    print('\n======= Thanks for using IFNepitope2. Your results are stored in file :',result_filename,' =====\n\n')
if __name__ == "__main__":
    main()