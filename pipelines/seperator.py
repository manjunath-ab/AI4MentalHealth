import pandas as pd

result=pd.read_csv('blurt_illness2.csv')
result.dropna(how='all',inplace=True)
result.to_csv('blurt_illness2_5.csv',index=False,sep='$')
