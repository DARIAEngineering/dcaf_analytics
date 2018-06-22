## NOTE: This script is based off of the much more sensitive/less redacted data, and will not run with the DKDC data.

## Technical Setup

#Import Packages
import pandas as pd
import numpy as np
import re
import seaborn as sns

## For google
#Set Up OAUTH and import dataframe
!pip install -U -q PyDrive

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from google.colab import auth
from google.colab import files
from oauth2client.client import GoogleCredentials

auth.authenticate_user()
gauth = GoogleAuth()
gauth.credentials = GoogleCredentials.get_application_default()
drive = GoogleDrive(gauth)

file1 = drive.CreateFile({'id': 'REDACTED_FOR_SECURITY_PURPOSES'})
file1.GetContentFile('patient_data_export_20180621.csv')
df = pd.read_csv('patient_data_export_20180621.csv')
df.columns



# Clean Timestamps
df['Timestamp of first call'] = pd.to_datetime(df['Timestamp of first call'], format = '%Y-%m-%d %H:%M:%S')
df['Timestamp of last call'] = pd.to_datetime(df['Timestamp of last call'], format = '%Y-%m-%d %H:%M:%S')
df['Appointment Date'] = pd.to_datetime(\
                                      df['Appointment Date'],
                                         errors = 'coerce',
                                         infer_datetime_format=True)

#

## Q: Spent on pre-7 weeks procedures since July, average cost?

# By *estimated* LMP at appointment time 


df["Time from intake to Appointment"] = df["Appointment Date"] - df["Timestamp of first call"]
def to_days_rounded(timedelta):
  if timedelta.seconds//3600 % 24 >= 12:
    return timedelta.days + 1
  else:
    return timedelta.days

df["Time from intake to Appointment in days"] = df["Time from intake to Appointment"].apply(to_days_rounded)


df["LMP at Appointment"] = df["Time from intake to Appointment in days"]/7+df["LMP at intake (weeks)"]


july_2017_as_datetime = pd.to_datetime('2017-July-01', infer_datetime_format=True)
jan_1_2018_as_datetime = pd.to_datetime('2018-Jan-01', infer_datetime_format=True)

spent_on_pre_7_weeks = df[(df["LMP at Appointment"] <= 7) 
                          & (df["Timestamp of first call"] > july_2017_as_datetime) 
                          & (df["Timestamp of first call"] < jan_1_2018_as_datetime)
                          & (df["Fulfilled"]) == True].sum()["Procedure cost"]
average_spent_on_pre_7_weeks = df[(df["LMP at Appointment"] <= 7) 
                          & (df["Timestamp of first call"] > july_2017_as_datetime) 
                          & (df["Timestamp of first call"] < jan_1_2018_as_datetime)
                          & (df["Fulfilled"]) == True].mean()["Procedure cost"]

print("Amount spent on appointments pre 7 weeks (from July 2017 through December 2018): $", spent_on_pre_7_weeks)
print("Average spent on appointments before 7 weeks is (from July 2017 through December 2018): $", average_spent_on_pre_7_weeks)

##Q: Fulfillment rate from year 2017
dfPledgeSent = df[df["Pledge sent"] == True]#TEMP CHANGE
jan_1_2017_as_datetime =  pd.to_datetime('2017-Jan-01', infer_datetime_format=True)
dfPledgeSent2017 = dfPledgeSent[(dfPledgeSent["Timestamp of first call"] > jan_1_2017_as_datetime) 
                                & (dfPledgeSent["Timestamp of first call"] < jan_1_2018_as_datetime)]


## All pledges
total_pledges_fulfilled = dfPledgeSent2017[dfPledgeSent2017["Fulfilled"] == True].count()["BSON ID"]
total_pledges = dfPledgeSent2017.count()["BSON ID"]


print("Fullfilled Pledges: ", total_pledges_fulfilled)
print("Pledges: ", total_pledges)
print("Fulfillment rate for all pledges:    %", total_pledges_fulfilled/total_pledges * 100, "\n \n")


## < 7 weeks

pledges_fulfilled_7_weeks = dfPledgeSent2017[(dfPledgeSent2017["LMP at Appointment"] <= 7)
                                                   & (dfPledgeSent2017["Fulfilled"] == True)].count()["BSON ID"]                                                  
pledges_7_weeks = dfPledgeSent2017[dfPledgeSent2017["LMP at Appointment"] <= 7].count()["BSON ID"]


print("Fullfilled Pledge 7 weeks: ", pledges_fulfilled_7_weeks)
print("Pledges 7 weeks: ", pledges_7_weeks)
print("Fulfillment rate 7 week pledges:    %", pledges_fulfilled_7_weeks/pledges_7_weeks * 100, "\n \n")



## 8+ weeks
pledges_fulfilled_8_weeks = dfPledgeSent2017[(dfPledgeSent2017["LMP at Appointment"] > 7)
                                                   & (dfPledgeSent2017["Fulfilled"] == True)].count()["BSON ID"]                                                  
pledges_8_weeks = dfPledgeSent2017[dfPledgeSent2017["LMP at Appointment"] > 7].count()["BSON ID"]

print("Fullfilled Pledge 8+ weeks: ", pledges_fulfilled_8_weeks)
print("Pledges 8+ weeks: ", pledges_8_weeks)
print("Fulfillment rate 8+ week pledges:    %", pledges_fulfilled_8_weeks/pledges_8_weeks * 100, "\n \n")

## Fulfillment rate from July 2017 through Sept 2017
dfPledgeSent = df[df["Pledge sent"] == True]
july_1_2017_as_datetime =  pd.to_datetime('2017-July-01', infer_datetime_format=True)
oct_1_2017_as_datetime = pd.to_datetime('2017-October-01', infer_datetime_format = True)



dfPledgeSentJulySept2017 = dfPledgeSent[(dfPledgeSent["Timestamp of first call"] > july_1_2017_as_datetime) 
                                & (dfPledgeSent["Timestamp of first call"] < oct_1_2017_as_datetime)]


## All pledges
total_pledges_fulfilled = dfPledgeSentJulySept2017[dfPledgeSent2017["Fulfilled"] == True].count()["BSON ID"]
total_pledges = dfPledgeSentJulySept2017.count()["BSON ID"]


print("Fullfilled Pledges: ", total_pledges_fulfilled)
print("Pledges: ", total_pledges)
print("Fulfillment rate for all pledges:    %", total_pledges_fulfilled/total_pledges * 100, "\n \n")


## < 7 weeks

pledges_fulfilled_7_weeks = dfPledgeSentJulySept2017[(dfPledgeSent2017["LMP at Appointment"] <= 7)
                                                   & (dfPledgeSent2017["Fulfilled"] == True)].count()["BSON ID"]                                                  
pledges_7_weeks = dfPledgeSentJulySept2017[dfPledgeSentJulySept2017["LMP at Appointment"] <= 7].count()["BSON ID"]


print("Fullfilled Pledge 7 weeks: ", pledges_fulfilled_7_weeks)
print("Pledges 7 weeks: ", pledges_7_weeks)
print("Fulfillment rate 7 week pledges:    %", pledges_fulfilled_7_weeks/pledges_7_weeks * 100, "\n \n")



## 8+ weeks
pledges_fulfilled_8_weeks = dfPledgeSentJulySept2017[(dfPledgeSentJulySept2017["LMP at Appointment"] > 7)
                                                   & (dfPledgeSentJulySept2017["Fulfilled"] == True)].count()["BSON ID"]                                                  
pledges_8_weeks = dfPledgeSentJulySept2017[dfPledgeSentJulySept2017["LMP at Appointment"] > 7].count()["BSON ID"]

print("Fullfilled Pledge 8+ weeks: ", pledges_fulfilled_8_weeks)
print("Pledges 8+ weeks: ", pledges_8_weeks)
print("Fulfillment rate 8+ week pledges:    %", pledges_fulfilled_8_weeks/pledges_8_weeks * 100, "\n \n")

### FISCAL YEAR 2017
## Q: For non-NAF patients: 2nd tri patients funded over x dollars? 3rd tri patients funded over y?

x = 300
y = 600

above_cap_2nd_tri_5_num_sum = dfPledgeSent2017[(dfPledgeSent2017["Gestation at procedure in weeks"] >=13) 
                                     & (dfPledgeSent2017["Gestation at procedure in weeks"]<=24)
                                     & (dfPledgeSent2017["Procedure cost"] > x)
                                     & (dfPledgeSent2017["NAF pledge"] > 0)].describe()["Procedure cost"]
above_cap_3rd_tri_5_num_sum = dfPledgeSent2017[(dfPledgeSent2017["Gestation at procedure in weeks"] >=25) 
                                              & (dfPledgeSent2017["Procedure cost"] > y)
                                              & (dfPledgeSent2017["NAF pledge"] > 0)].describe()["Procedure cost"]

print("5 Number Summary for 'above cap 2nd trimester with a postive NAF pledge' \n", above_cap_2nd_tri_5_num_sum, "\n \n")

print("5 Number Summary 'above cap 3rd trimester with a positive NAF pledge' \n", above_cap_3rd_tri_5_num_sum)

## Q: Pledge amounts/total number of pledges over 25 weeks
dfPledgeSent2017["Gestation at procedure in weeks"].value_counts()
average_third_tri_pledge = dfPledgeSent2017[dfPledgeSent2017["Gestation at procedure in weeks"] >= 25].mean()["Procedure cost"]
number_of_third_tri_pledge = dfPledgeSent2017[dfPledgeSent2017["Gestation at procedure in weeks"] >= 25].count()["BSON ID"]
five_number_summary = dfPledgeSent2017[dfPledgeSent2017["Gestation at procedure in weeks"] >= 25].describe()["Procedure cost"]

print("Average third trimester pledge:  $", average_third_tri_pledge)
print("Number of third trimester pledges:  ", number_of_third_tri_pledge)
print("Five Number Summary of ALL Third Tri Pledges: \n", five_number_summary)

## Q: Fulfillment rate from FISCAL YEAR 2017
dfPledgeSent = df[df["Pledge sent"] == True]
july_1_2016_as_datetime =  pd.to_datetime('2016-July-01', infer_datetime_format=True)
jun_1_2017_as_datetime = pd.to_datetime('2017-Jun-01', infer_datetime_format=True)
dfPledgeSentFY2017 = dfPledgeSent[(dfPledgeSent["Timestamp of last call"] > july_1_2016_as_datetime) & (dfPledgeSent["Timestamp of last call"] < jun_1_2017_as_datetime)]





## All pledges
total_pledges_fulfilled = dfPledgeSentFY2017[dfPledgeSentFY2017["Fulfilled"] == True].count()["BSON ID"]
total_pledges = dfPledgeSentFY2017.count()["BSON ID"]


print("Fullfilled Pledges: ", total_pledges_fulfilled)
print("Pledges: ", total_pledges)
print("Fulfillment rate for all pledges:    %", total_pledges_fulfilled/total_pledges * 100, "\n \n")


## < 7 weeks

pledges_fulfilled_7_weeks = dfPledgeSentFY2017[(dfPledgeSentFY2017["LMP at Appointment"] <= 7)
                                                   & (dfPledgeSentFY2017["Fulfilled"] == True)].count()["BSON ID"]                                                  
pledges_7_weeks = dfPledgeSentFY2017[dfPledgeSentFY2017["LMP at Appointment"] <= 7].count()["BSON ID"]


print("Fullfilled Pledge 7 weeks: ", pledges_fulfilled_7_weeks)
print("Pledges 7 weeks: ", pledges_7_weeks)
print("Fulfillment rate 7 week pledges:    %", pledges_fulfilled_7_weeks/pledges_7_weeks * 100, "\n \n")



## 8+ weeks
pledges_fulfilled_8_weeks = dfPledgeSentFY2017[(dfPledgeSentFY2017["LMP at Appointment"] > 7)
                                                   & (dfPledgeSentFY2017["Fulfilled"] == True)].count()["BSON ID"]                                                  
pledges_8_weeks = dfPledgeSentFY2017[dfPledgeSentFY2017["LMP at Appointment"] > 7].count()["BSON ID"]

print("Fullfilled Pledge 8+ weeks: ", pledges_fulfilled_8_weeks)
print("Pledges 8+ weeks: ", pledges_8_weeks)
print("Fulfillment rate 8+ week pledges:    %", pledges_fulfilled_8_weeks/pledges_8_weeks * 100, "\n \n")

### FISCAL YEAR 2017
## Q: Pledge amounts
dfPledgeSentFY2017["Gestation at procedure in weeks"].value_counts()
average_third_tri_pledge = dfPledgeSentFY2017[dfPledgeSentFY2017["Gestation at procedure in weeks"] >= 25].mean()["Procedure cost"]
number_of_third_tri_pledge = dfPledgeSentFY2017[dfPledgeSentFY2017["Gestation at procedure in weeks"] >= 25].count()["BSON ID"]
five_number_summary = dfPledgeSentFY2017[dfPledgeSentFY2017["Gestation at procedure in weeks"] >= 25].describe()["Procedure cost"]

print("Average third trimester pledge:  $", average_third_tri_pledge)
print("Number of third trimester pledges:  ", number_of_third_tri_pledge)
print("Five Number Summary of ALL Third Tri Pledges: \n", five_number_summary)

### FISCAL YEAR 2017
## Q: For non-NAF patients: 2nd tri patients funded over x dollars? 3rd tri patients funded over y dollars?

x = 300
y = 600

above_cap_2nd_tri_5_num_sum = dfPledgeSentFY2017[(dfPledgeSentFY2017["Gestation at procedure in weeks"] >=13) 
                                     & (dfPledgeSentFY2017["Gestation at procedure in weeks"]<=24)
                                     & (dfPledgeSentFY2017["Procedure cost"] > x)
                                     & (dfPledgeSentFY2017["NAF pledge"] > 0)].describe()["Procedure cost"]
above_cap_3rd_tri_5_num_sum = dfPledgeSentFY2017[(dfPledgeSentFY2017["Gestation at procedure in weeks"] >=25) 
                                              & (dfPledgeSentFY2017["Procedure cost"] > y)
                                              & (dfPledgeSentFY2017["NAF pledge"] > 0)].describe()["Procedure cost"]

print("5 Number Summary for 'above cap 2nd trimester with a postive NAF pledge' \n", above_cap_2nd_tri_5_num_sum, "\n \n")

print("5 Number Summary 'above cap 3rd trimester with a positive NAF pledge' \n", above_cap_3rd_tri_5_num_sum)

#

dfPledgeSent["PSBU"] = dfPledgeSent["Fulfilled"] != True
dfPledgeSent["Ful"] = dfPledgeSent["Fulfilled"] == True
#dfPledgeSent2017on = dfPledgeSent[dfPledgeSent["Timestamp of first call"] >= jan_1_2017_as_datetime ]
dfPledgeSent.groupby(pd.Grouper(key='Timestamp of first call', freq='W')).sum().plot(y='PSBU')
dfPledgeSent.groupby(pd.Grouper(key='Timestamp of first call', freq='W')).sum().plot(y='Ful')

dfPledgeSent.groupby(pd.Grouper(key='Timestamp of first call', freq='W')).mean().plot(y='PSBU')
