
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


df['Days to first call'] = df['Timestamp of first call'] - df['Initial Call Date']
df['Days to last call'] = df['Timestamp of last call'] - df['Initial Call Date']
df['Days to procedure'] = df['Procedure date'] - df['Initial Call Date']
df['Days to pledge'] = df['Pledge generated time'] - df['Initial Call Date']

  
df['Days to last call'] = df['Days to last call']
df['Days to first call'] = df['Days to first call']
df['Days to procedure'] = df['Days to procedure']
df['Days to pledge'] = df['Days to pledge']



df["Time from intake to Appointment"] = df["Appointment Date"] - df["Initial Call Date"]

df["Time from intake to Appointment in days"] = df["Time from intake to Appointment"]


df["LMP at intake (weeks)"] = pd.Timedelta("7 days") * df["LMP at intake (weeks)"] 
df["LMP at Appointment in approximate days"] = df["Time from intake to Appointment in days"] + df["LMP at intake (weeks)"]

df["LMP at Appointment in weeks"] = (df["LMP at Appointment in approximate days"]/7)


df["LMP at Appointment in weeks"] = df["LMP at Appointment in weeks"].astype('timedelta64[W]')



## Fulfillment rate from July 2017 through Sept 2017
dfPledgeSent = df[df["Pledge sent"] == True]
start_date =  pd.to_datetime('2018-July-01 12:01 am', infer_datetime_format=True)
end_date = pd.to_datetime('2019-Jun-30 11:59 pm', infer_datetime_format = True)


dfPledgeSentBounded = dfPledgeSent[(dfPledgeSent["Timestamp of first call"] >= start_date) & (dfPledgeSent["Timestamp of first call"] <= end_date)]

dfBounded = dfPledgeSent[(df["Timestamp of first call"] >= start_date) & (df["Timestamp of first call"] <= end_date)]


## All pledges
total_pledges_fulfilled = dfPledgeSentBounded[dfPledgeSentBounded["Fulfilled"] == True].count()["BSON ID"]
total_pledges = dfPledgeSentBounded.count()["BSON ID"]


print("Fullfilled Pledges: ", total_pledges_fulfilled)
print("Pledges: ", total_pledges)
print("Fulfillment rate for all pledges:    %", total_pledges_fulfilled/total_pledges * 100, "\n \n")

## Annual report


dfBoundedDemo = df[(df["Initial Call Date"] >= start_date) & (df["Initial Call Date"] <= end_date)]


dfBoundedDemoPS = dfBoundedDemo[dfBoundedDemo["Pledge sent"] == True]

dfBoundedDemo['Race or Ethnicity'] = dfBoundedDemo['Race or Ethnicity'].astype(str)
# will have to repeat this logic for ND, VA, DC with 
def linestats(dfLine):
  dfLine.fillna("Unspecified", inplace = True)
  print(dfLine['Race or Ethnicity'].value_counts())
  print(dfLine['Income'].value_counts())
  print(dfLine['Employment Status'].value_counts())#.plot().pie
  print(dfLine['Age'].value_counts())
  print("\n\n\n\n")
print('=== MD Stats ===')
linestats(dfBoundedDemo[dfBoundedDemo['Line'] == 'MD'])

print('=== VA Stats ===')
linestats(dfBoundedDemo[dfBoundedDemo['Line'] == 'VA'])

print('=== DC Stats ===')
linestats(dfBoundedDemo[dfBoundedDemo['Line'] == 'DC'])

print('=== All Lines ===')
linestats(dfBoundedDemo)


print("\n\n\n=== DEMO For Pledge Sent ===")
linestats(dfBoundedDemoPS)

dfBoundedDemo = df[(df["Initial Call Date"] >= start_date) & (df["Initial Call Date"] <= end_date)]
dfBoundedDemo['Fund pledge'].fillna('0', inplace=True)

dfBoundedDemo['Fund pledge'] = dfBoundedDemo['Fund pledge'].apply(lambda x : int(x))

print("Pledged")
print(dfBoundedDemo.groupby(['Line', 'Age'])['Fund pledge'].sum())



dfBoundedfulfilled = dfBoundedDemo[dfBoundedDemo['Fulfilled'] == True]


print("==== Fulfilled ====")
print(dfBoundedfulfilled.groupby(['Line', 'Age'])['Fund pledge'].sum())




print("Pledged Count")
print(dfBoundedDemo.groupby(['Line', 'Age'])['Pledge sent'].count())



dfBoundedfulfilled = dfBoundedDemo[dfBoundedDemo['Fulfilled'] == True]


print("==== Fulfilled Count ====")
print(dfBoundedfulfilled.groupby(['Line', 'Age'])['Fulfilled'].count())



#Special considerations graph
lmpPS=lmp[lmp['Pledge sent'] == True]
lmpPS['Fulfilled'].value_counts()

## BRAAF considerations

#extract BRAAF Pledged
df1 = dfBounded.replace(np.nan, '', regex=True)
def braaf_from_raw(text):
  text=str(text)
  if "BRAAF" in text:
    return True
  else:
    return False

df1['BRAAF Pledged'] = df1['All External Pledges'].apply(braaf_from_raw)

df2=df1[(df1['Line']== "VA") & (df1['Pledge sent']== True)]
df2['Fund pledge'] = df2['Fund pledge'].apply(lambda x: int(x))

df_braaf = df2[(df2['BRAAF Pledged']  == True )]
df_not = df2[df2['BRAAF Pledged']  != True ]



print("BRAAF")
print(df_braaf['Fund pledge'].describe())



print("\nnot BRAAF")
print(df_not['Fund pledge'].describe())



dfBounded.groupby('Line')['Call count'].mean()
dfBounded['Call count'].mean()

dfBounded.groupby('Line').count()

dfBounded.groupby('Line')['Call count'].count()

dfBounded['Call count'].mean()

dfPledgeSentBounded.groupby('Line')['Time from intake to Appointment in days', 'Days to last call', 'Call count'].mean()
dfPledgeSentBounded[['Time from intake to Appointment in days', 'Days to last call', 'Call count']].mean()

dfPledgeSentBounded.groupby('Line')['Time from intake to Appointment in days', 'Days to last call', 'Call count'].count()

dfPledgeSentBounded['Time from intake to Appointment in days'].mean()

dfPledgeSentBounded['Days to last call'].mean()

dfPledgeSentBounded['Call count'].mean()
