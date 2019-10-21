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




## Fulfillment rate from July 2017 through Sept 2017
dfPledgeSent = df[df["Pledge sent"] == True]
start_date =  pd.to_datetime('2018-July-01 12:01 am', infer_datetime_format=True)
end_date = pd.to_datetime('2019-Jun-30 11:59 pm', infer_datetime_format = True)


dfPledgeSentBounded = dfPledgeSent[(dfPledgeSent["Initial Call Date"] >= start_date) & (dfPledgeSent["Initial Call Date"] <= end_date)]

dfBounded = df[(df["Initial Call Date"] >= start_date) & (df["Initial Call Date"] <= end_date)]

print(dfPledgeSentBounded.groupby(['Clinic'])["Pledge sent"].count().nlargest(50))
