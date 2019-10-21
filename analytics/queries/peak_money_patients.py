## Technical Setup

import pandas as pd

df = pd.read_csv('patient_data_export_20190921.csv')

## Clean Timestamps 
#

df['Timestamp of first call'] = pd.to_datetime(df['Timestamp of first call'], 
                                         errors = 'coerce',
                                         infer_datetime_format=True)
df['Timestamp of last call'] = pd.to_datetime(df['Timestamp of last call'],
                                         errors = 'coerce',
                                         infer_datetime_format=True)
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


start_date =  pd.to_datetime('2017-Jan-01 12:01 am', infer_datetime_format=True)
end_date = pd.to_datetime('2019-Jun-30 11:59 pm', infer_datetime_format = True)

dfPledgeSent = df[df["Pledge sent"] == True]

dfPledgeSentBounded = dfPledgeSent[(dfPledgeSent["Initial Call Date"] >= start_date) & (dfPledgeSent["Initial Call Date"] <= end_date)]

dfPledgeGenBounded = dfPledgeSentBounded.dropna(subset=["Pledge generated time"])


maxCountPledgeSent = (dfPledgeGenBounded.groupby([ pd.Grouper(key="Initial Call Date", freq='W')])["Pledge sent"].transform('sum').max()) 


maxPledgeSentDollars = (dfPledgeGenBounded.groupby([ pd.Grouper(key="Pledge generated time", freq='W')])["Fund pledge"].transform('sum').max()) 


print("most pledges in a week:" + str(maxCountPledgeSent) )


print("most pledge dollars in a week:" + str(maxPledgeSentDollars) )
