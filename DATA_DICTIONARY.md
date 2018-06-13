# Data Fields for Datakind
This is a basic dictionary of the data provided to volunteers.

Field | Description
------------ | -------------
Has Alt Contact?| Whether the patient has specified an alternate contact.
Voicemail Preference| The patient's prefered voicemail policy when DCAF returns their calls.
Line| The line the patient was serviced on.
Language| Preferred language of the patient.
Age| Age range the patient falls in.
State| The state from which the patient is travelling.
Race or Ethnicity| Patient's race or ethnicity.
Employment Status| Patient's current employment status.
Insurance| Patient's current insurance coverage, if any. This includes public and private options. [Note: If a patient reports a managed care organization, it is up to either the patient or case manager to determine and report as public insurance rather than private.]
Income| Patient's income, as reported in ranges.
Referred By| How the patient discovered or was referred to the fund.
Referred to clinic by fund| TODO
LMP at intake (weeks)| Last Menstrual Period at intake. Note that this is truncated after 20 weeks for the current dataset.
Patient contribution| The amount of money contributed by the patient. This amount may change at the actual appointment, but is used during case management to record how much a patient can possibly contribute.
NAF pledge| The amount contributed by the National Abortion Federation, a large, national abortion funding organization. This amount may change at the actual appointment, but is used during case management to record how much NAf can contribute.
Fund pledge| The amount the Fund is contributing to the patient's procedure in the form of a pledge sent to the clinic.
Pledge sent| This indicates if a pledge was generated through the DARIA system for a patient.
Resolved without fund assistance| The patient has resolved their case without the aid of the Fund. This could be a patient chooses to continue the pregnancy, has found other sources of funding, or any other circumstances the Fund should not continue contacting the patient.
Call count| Total calls
Reached Patient call count| Total calls where the patient and case manager reached each other succesfully
Fulfilled| Whether pledge was fulfilled.
Gestation at procedure in weeks| Gestation at the scheduled time of procedure.
Procedure cost| The amount actually paid by DCAF to the fund, truncated at 5000.
Month of first call| The month of initial contact by the patient.
Year of first call| The year of initial contact by the patient.
Days to procedure| Days elapsed between the patient initially calling the hotline and the patient's procedure date, if reported.
Days to pledge| Days elapsed between the patient initially calling the hotline and patient receiving a pledge from DCAF.
Days to first call| Days elapsed between the patient initially calling the hotline and a case manager returning their call.
Days to last call| Days elapsed between the patient initially calling the hotline and their final call with a case manager.
Initial Call Weekday vs Weekend| Whether the initial call was on a weekday or a weekend
First Call Weekday vs Weekend| Whether the first call was on a weekday or a weekend
Procedure Weekday vs Weekend| Whether the procedure was on a weekday or a weekend
Household Size| The size of the patient's household, truncated at 8.
