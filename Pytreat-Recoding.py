import scipy.io as sio
import numpy as np
import pandas as pd
import csv
import re
import sys

ukb8252=pd.read_csv('UKBrodeo/parsed_ukb8252.tsv','\t')
ukb9268=pd.read_csv('UKBrodeo/parsed_ukb9268.tsv','\t')

CodingMD = pd.read_excel('UKBrodeo/DataCodingMetaData.xlsx')

workspace = sio.matlab.loadmat('../workspace7d.mat')
#'varsVARS' has the UDI for every variable in 'Vars' （1-to-1 correspondence)
varsVARS=pd.DataFrame(workspace['varsVARS'])
varsHeader=pd.DataFrame(workspace['varsHeader'])
Vars=pd.DataFrame(workspace['vars'])  #replace this with the raw data

NameCode=ukb8252[['VarName','DataCoding']].copy()

# Combine two parsed html files
ukb9268.columns = ukb8252.columns
ukb = pd.concat([ukb8252,ukb9268])
ukb = ukb.reset_index(drop=True)

# Generate a UDI to DataCoding table
NameCode = ukb[['VarName','DataCoding']].copy()
NameCode = NameCode.loc[NameCode['VarName'] != NameCode['VarName'].shift()]

# Map every variable in Vars to their data Coding
v = pd.DataFrame(varsVARS.apply(lambda x: int(x[0][0].split('-')[0])))
v.columns = ['VarName']
merged = pd.merge(v, NameCode, on='VarName',how='left')

# Recode old coding like -3, -1 to NA (this bit is slow; need to be improved)
CodingMD_sub = CodingMD[CodingMD.NAvalues.notnull()]
NA = CodingMD_sub.NAvalues.str.split(',')

for i in range(CodingMD.shape[0]):

    mask=merged.DataCoding==str(CodingMD_sub.data_coding.iloc[i])
    var_subset=Vars.T[mask].T

    mask1=var_subset.isin(list(map(int, NA[1])))
    var_subset[mask1]='NaN'
    Vars.update(var_subset)

# Recode bizarre coding like -7, -11, 555 to normal coding
# Please make sure its a 1-to-1 recoding
Vars.columns = merged['DataCoding']
CodingMD_sub = CodingMD[['RawLevels','NewLevels', 'data_coding']].dropna()
CodingMD_sub = CodingMD_sub.astype(str)

mappings = {}
for row in CodingMD_sub.T:
    rawLevel = CodingMD_sub['RawLevels'][row]
    newLevel = CodingMD_sub['NewLevels'][row]
    coding   = CodingMD_sub['data_coding'][row]

    mappings[coding] = {float(rlev) : float(nlev)
                        for rlev, nlev
                        in zip(rawLevel.split(','), newLevel.split(','))}

mappings['100318'] = {3.0 : 333.0, 7.0 : 777.0}
mappings

Vars.replace(mappings)
