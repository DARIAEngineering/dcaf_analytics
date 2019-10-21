
## Technical Setup

#Import Packages
import pandas as pd
import numpy as np
import re
import seaborn as sns

df = pd.read_csv('MatchedDataApril2019.csv')

## Clean Timestamps 
#

df['Timestamp of first call'] = pd.to_datetime(df['Timestamp of first call'], format = '%Y-%m-%d %H:%M:%S')
df['Timestamp of last call'] = pd.to_datetime(df['Timestamp of last call'], format = '%Y-%m-%d %H:%M:%S')
df['Appointment Date'] = pd.to_datetime(\
                                      df['Appointment Date'],
                                         errors = 'coerce',
                                         infer_datetime_format=True)



df['Initial Call Date']=pd.to_datetime(\
                                       df['Initial Call Date'],
                                      errors = 'coerce',
                                      infer_datetime_format=True
                                     )

df['Pledge generated time'] = pd.to_datetime(\
                                      df['Pledge generated time'],
                                         errors = 'coerce',
                                         infer_datetime_format=True)
df['Procedure date'] = pd.to_datetime(\
                                     df['Procedure date'],
                                     errors = 'coerce',
                                      infer_datetime_format=True
                                     )

df["amount"].fillna(value = 0, inplace = True)
df["amount"] = pd.to_numeric(df["amount"], errors = "coerce")


start_date = pd.to_datetime("July 1 - 2017")
end_date = pd.to_datetime("Jun 30 - 2018")


print(df[(df["Pledge sent"] == True)  & (df["Initial Call Date"] > start_date) & (df["Initial Call Date"] < end_date)][["Fund pledge"]].agg(['sum']))


print( df[(df["Fund pledge"]>= 1000) & (df["Pledge sent"] == True) & (df["Initial Call Date"] > start_date) & (df["Initial Call Date"] < end_date) ][["Fund pledge"]].agg(['sum'])  )


print( df[(df["Fund pledge"]>= 1000) & (df["Fulfilled"] == True) & (df["Initial Call Date"] > start_date) & (df["Initial Call Date"] < end_date) ][["Fund pledge"]].agg(['sum'])  )

#df["amount"].fillna(value = 0, inplace = True)
#df["amount"] = pd.to_numeric(df["amount"], errors = "coerce")
#print(df[(df["Pledge sent"] == True)  & (df["Initial Call Date"] > start_date) & (df["Initial Call Date"] < end_date)][["amount"]].agg(['sum']))
