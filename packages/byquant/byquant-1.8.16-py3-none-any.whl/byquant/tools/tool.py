import backtrader as bt
import numpy as np
import pandas as pd
import scipy.stats as stats

def isCross(line1,line2):
    if line1[0] > line2[0] and line1[-1] < line2[-1]:
        return True
    else:
        return False
        
def crossUp(line1,line2):
    return line1[0] > line2[0] and line1[-1] < line2[-1]

def crossDown(line1,line2):
    return line1[0] < line2[0] and line1[-1] > line2[-1]
    
        
def num2date(datetime):
    return bt.num2date(datetime)
    
def regularSTD(data):
    return (data - data.mean()) / data.std()
    
def regularMM(data):
    return (data - data.min()) / (data.max() - data.min())

def scoreatpercentile(data,percent=38.2): #黄金分割 38.2、61.8
    return stats.scoreatpercentile(data,percent=percent)
    
def corr(data1,data2):
    if isinstance(data1, pd.DataFrame):
        arr1 = np.array(data1.close)
    elif isinstance(data1, pd.Series):
        arr1 = np.array(data1)
    elif isinstance(data1, list):
        arr1 = data1
    else:
        arr1 = data1
        
    if isinstance(data2, pd.DataFrame):
        arr2 = np.array(data2.close)
    elif isinstance(data2, pd.Series):
        arr2 = np.array(data2)
    elif isinstance(data2, list):
        arr2 = data2
    else:
        arr2 = data2
        
    return np.corrcoef(arr1,arr2)[0,1]
    
def spearmanr(data1,data2):
    if isinstance(data1, pd.DataFrame):
        arr1 = np.array(data1.close)
    elif isinstance(data1, pd.Series):
        arr1 = np.array(data1)
    elif isinstance(data1, list):
        arr1 = data1
    else:
        arr1 = data1
        
    if isinstance(data2, pd.DataFrame):
        arr2 = np.array(data2.close)
    elif isinstance(data2, pd.Series):
        arr2 = np.array(data2)
    elif isinstance(data2, list):
        arr2 = data2
    else:
        arr2 = data2
        
    spearmanr = stats.spearmanr(arr1,arr2)
    return spearmanr.statistic
