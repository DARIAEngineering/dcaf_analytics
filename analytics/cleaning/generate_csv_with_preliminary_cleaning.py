##Generate Initial CSV
# This is the script @mdworken uses to generate the data analysis csv that we distribute to volunteers.
# Sensitive fields are cleaned/edited here before distribution.

##Import Packages
import pandas as pd
import numpy as np
import re

## For google
#Set Up OAUTH
!pip install -U -q PyDrive #'!' is how you run shell commands in google colab

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from google.colab import auth
from google.colab import files
from oauth2client.client import GoogleCredentials

auth.authenticate_user()
gauth = GoogleAuth()
gauth.credentials = GoogleCredentials.get_application_default()
drive = GoogleDrive(gauth)

file1 = drive.CreateFile({'id': '1I859qNrfnyE5_EN5kk81vBbCyVX41GfT'})
file1.GetContentFile('patients.csv')

df = pd.read_csv('patients.csv')

## Clean times
df['Timestamp of first call'] = pd.to_datetime(df['Timestamp of first call'], format = '%Y-%m-%d %H:%M:%S')
df['Timestamp of last call'] = pd.to_datetime(df['Timestamp of last call'], format = '%Y-%m-%d %H:%M:%S')
df['Initial Call Date']=pd.to_datetime(\
                                       df['Initial Call Date'],
                                      errors = 'coerce',
                                      infer_datetime_format=True
                                     )
df['procedure_dt'] = pd.to_datetime(\
                                      df['Procedure date'],
                                         errors = 'coerce',
                                         infer_datetime_format=True)
df['Pledge generated time'] = pd.to_datetime(\
                                      df['Pledge generated time'],
                                         errors = 'coerce',
                                         infer_datetime_format=True)
df['Procedure date'] = pd.to_datetime(\
                                     df['Procedure date'],
                                     errors = 'coerce',
                                      infer_datetime_format=True
                                     )

## Info for first call

def to_just_a_month(datetime):
  return datetime.month
def to_just_a_year(datetime):
  return datetime.year
def true_to_1(boolean):
  if boolean:
    return 1
  else:
    return 0

df['Month of first call'] = df['Timestamp of first call'].apply(to_just_a_month)
df['Year of first call'] = df['Timestamp of first call'].apply(to_just_a_year)


## Durations since initial call

df['Days to first call'] = df['Timestamp of first call'] - df['Initial Call Date']
df['Days to last call'] = df['Timestamp of last call'] - df['Initial Call Date']
df['Days to procedure'] = df['Procedure date'] - df['Initial Call Date']
df['Days to pledge'] = df['Pledge generated time'] - df['Initial Call Date']


def to_days_rounded(timedelta):
  if timedelta.seconds//3600 % 24 >= 12:
    return timedelta.days + 1
  else:
    return timedelta.days
  
df['Days to last call'] = df['Days to last call'].apply(to_days_rounded)
df['Days to first call'] = df['Days to first call'].apply(to_days_rounded)
df['Days to procedure'] = df['Days to procedure'].apply(to_days_rounded)
df['Days to pledge'] = df['Days to pledge'].apply(to_days_rounded)

def clean_states_dcaf(state):
  state=str(state)
  state=state.upper()
  state=state.strip()
  if state == "MARYLAND":
    state = "MD"
  elif state == "DISTRICT OF COLUMBIA":
    state = "DC"
  elif state == "D.C.":
    state = "DC"
  elif state == "VIRGINIA":
    state = "VA"
  elif state == "GEORGIA":
    state = "GA"
  elif state == "M":
    state = "MD"
  elif state == "BEACH":
    state = "VA"
  elif state == "NORTH CAROLINA":
    state = "NC"
  elif state == "TENNESSEE":
    state = "TN"
  elif state == "MDMD":
    state = "MD"
  elif state == "DELAWARE":
    state = "DE"
  elif state == "V":
    state = "VA"
  elif state == "20010":
    state = "DC"
  elif state == "WDC" or state == "DDC":
    state = "DC"
  elif state == "22031":
    state = "DC"
  elif state == "20002":
    state = "DC"
  elif state == "ARKANSAS":
    state = "AR"
  elif state == "IOWA":
    state = "IA"
  return state      

df['State'] = df['State'].apply(clean_states_dcaf)


## Specify weekday/weekend

def to_weekday_weekend(datetime):
  if datetime.weekday() < 5:
    return 'weekday'
  elif datetime.weekday() >= 5: 
    return 'weekend'
  
df['Initial Call Weekday vs Weekend'] = df['Initial Call Date'].apply(to_weekday_weekend)
df['First Call Weekday vs Weekend'] = df['Timestamp of first call'].apply(to_weekday_weekend)
df['Procedure Weekday vs Weekend'] = df['Procedure date'].apply(to_weekday_weekend)

## Cap LMP/Gestation, procedure cost, household size

def cap_at_20(weeks):
  return min(weeks,20)

def cap_at_5000(cost):
  return min(cost,5000)

def cap_at_8(family_size):
  return min(family_size,8)

df['Gestation at procedure in weeks'] = df['Gestation at procedure in weeks'].apply(cap_at_20)
df['LMP at intake (weeks)'] = df['LMP at intake (weeks)'].apply(cap_at_20)
df['Procedure cost'] = df['Procedure cost'].apply(cap_at_5000)
df['Household Size'] = df['Minors in Household'] + df['Adults in Household']
df['Household Size'] = df['Household Size'].apply(cap_at_8)
df2=df[['Has Alt Contact?', 'Voicemail Preference', #whitelist currently desired fields
                'Line', 'Language', 'Age', 'State', 'Race or Ethnicity', 
                'Employment Status', 'Insurance', 'Income', 'Referred By',
                'Referred to clinic by fund', 'LMP at intake (weeks)', 
                'Patient contribution', 'NAF pledge', 'Fund pledge', 'Pledge sent', 
                'Resolved without fund assistance', 
                'Call count', 'Reached Patient call count', 'Fulfilled', 'Gestation at procedure in weeks',
                'Procedure cost', 'Month of first call', 'Year of first call',
                'Days to procedure', 'Days to pledge', 'Days to first call',
                'Days to last call', 'Initial Call Weekday vs Weekend', 'First Call Weekday vs Weekend', 'Procedure Weekday vs Weekend','Household Size']]
df2.columns

## Export the file
from googleapiclient.discovery import build
drive_service = build('drive', 'v3')
from googleapiclient.http import MediaFileUpload

df2.to_csv('dcaf_data_jam.csv')

file_metadata = {
  'name': 'DCAF csv 5-13-18',
  'mimeType': 'text/csv'
}
media = MediaFileUpload('dcaf_data_jam.csv', 
                        mimetype='text/csv',
                        resumable=True)
created = drive_service.files().create(body=file_metadata,
                                       media_body=media,
                                       fields='id').execute()
print('File ID: {}'.format(created.get('id')))
