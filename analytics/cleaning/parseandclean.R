library(tidyverse)

data_file <- "DCAFCSV5_8.csv"

theme_set(theme_bw())


## Importing Data File

## The following variables are factors but are going to be treated as characters for post-processsing
  # state 
  # income

## The following variables are integers but are going to be treated as numbers until post-processing
  # LMP_at_intake_weeks
  # gestation_at_procedure_in_weeks
  # days_to_first_call
  # days_to_last_call
  # household_size
  # days_to_pledge
  # days_to_procedure
## The following variables are treated as characters but are going to be dates later
  # year_of_first_call
  # month_of_first_call

dcaf <- read_csv(data_file, 
                 skip = 1,
                 na = c("", "not_specified", "Don't know", "bad_value"),
                 col_names = c("id", "has_alt_contact", "voicemail_preference", "line",
                               "language", "age", "state", "race_or_ethnicity",
                               "employment_status", "insurance", "income", "referred_by",
                               "referred_to_clinic_by_fund", "LMP_at_intake_weeks", "patient_contribution",
                               "NAF_pledge", "fund_pledge", "pledge_sent", "resolved_without_fund_assistance",
                               "call_count", "reached_patient_call_count", "fulfilled", "gestation_at_procedure_in_weeks",
                               "procedure_cost", "month_of_first_call", "year_of_first_call", "days_to_procedure",
                               "days_to_pledge", "days_to_first_call", "days_to_last_call", "initial_call_weekday_vs_weekend",
                               "first_call_weekday_vs_weekend", "procedure_weekday_vs_weekend", "household_size"), 
                 col_types = cols(
                   id = col_skip(),
                   has_alt_contact = col_logical(),
                   voicemail_preference = col_factor(levels = NULL),
                   line = col_factor(levels = NULL),
                   language = col_factor(levels = NULL),
                   age = col_factor(levels = NULL),
                   state = col_character(),
                   race_or_ethnicity = col_factor(levels = NULL),
                   employment_status = col_factor(levels = NULL),
                   insurance = col_factor(levels = NULL),
                   income = col_character(),
                   referred_by = col_factor(levels = NULL),
                   referred_to_clinic_by_fund = col_logical(),
                   LMP_at_intake_weeks = col_number(),
                   patient_contribution = col_double(),
                   NAF_pledge = col_double(),
                   fund_pledge = col_double(),
                   pledge_sent = col_logical(),
                   resolved_without_fund_assistance = col_logical(),
                   call_count = col_integer(),
                   reached_patient_call_count = col_integer(),
                   fulfilled = col_logical(),
                   gestation_at_procedure_in_weeks = col_number(),
                   procedure_cost = col_double(),
                   # Parse out month and year date later
                   month_of_first_call = col_character(),
                   year_of_first_call = col_character(),
                   # Investigate negative numbers
                   days_to_procedure = col_number(),
                   days_to_pledge = col_number(),
                   days_to_first_call = col_number(),
                   days_to_last_call = col_number(),
                   initial_call_weekday_vs_weekend = col_factor(levels = NULL),
                   first_call_weekday_vs_weekend = col_factor(levels = NULL),
                   procedure_weekday_vs_weekend = col_factor(levels = NULL),
                   household_size = col_number()
                 ))

dcaf %>% head(10)

## Convert Voicemail Preference to Logical
dcaf = dcaf %>% 
  mutate(voicemail_preference = str_replace_all(voicemail_preference, c("yes" = "TRUE", "no" = "FALSE"))) %>%
  mutate(voicemail_preference = as.logical(voicemail_preference))



## Order age variables
dcaf = dcaf %>%
  mutate(age = factor(age, levels = c("under_18", "age25_34", "age35_44", "age45_54"), ordered = TRUE))

## Fix state variables
#20002 and 20010 are zip codes in DC
#22031 is the zip code of Fairfax, VA
#V, M, CD, VZ, BEACH, VM are not states [Going to mark as NA]
#DDC and WDC is assumed to be a typo for DC
#MDMD is assumed to be a typo for MD


dcaf = dcaf %>%
  mutate(state = toupper(state)) %>%
  mutate(state = trimws(state)) %>%
  mutate(state = str_replace_all(state, c("20002" = "DC", "20010" = "DC", "22031" = "VA",
                                          "ARKANSAS" = "AR", "D\\.C" = "DC", "DDC" = "DC",
                                          "DC\\." = "DC", "DELAWARE" = "DE", "DISTRICT OF COLUMBIA" = "DC",
                                          "GEORGIA" = "GA", "IOWA" = "IA", "MARYLAND" = "MD",
                                          "MDMD" = "MD", "NORTH CAROLINA" = "NC", "TENNESSEE" = "TN",
                                          "VIRGINIA" = "VA", "WDC" = "DC"))) %>%
  mutate(state = parse_factor(state, levels = NULL, na = c("V", "M", "CD", "VZ", "BEACH", "VM")))

## Coerce Integers
# Coerce certain variables to be integers. This is done since we don't keep precision such as 1.5 weeks

dcaf = dcaf %>% 
mutate(LMP_at_intake_weeks = as.integer(LMP_at_intake_weeks)) %>%
mutate(gestation_at_procedure_in_weeks = as.integer(gestation_at_procedure_in_weeks)) %>%
mutate(days_to_first_call = as.integer(days_to_first_call)) %>%
mutate(days_to_last_call = as.integer(days_to_last_call)) %>%
mutate(days_to_pledge = as.integer(days_to_pledge)) %>%
mutate(days_to_procedure = as.integer(days_to_procedure)) %>%
mutate(household_size = as.integer(household_size))

## Fixing Income

# For the income column, I put any smaller ranges that belong into the bigger range in it. I also took out the per week numbers and extra $s.

dcaf = dcaf %>%
  mutate(income = trimws(income)) %>%
  mutate(income = ifelse(income == "Under $9,999 (less than $192/week)", "Under $9,999", income)) %>%
  mutate(income = ifelse(income == "$10,000-$14,999", "$10,000-14,999", income)) %>%
  mutate(income = ifelse(income == "$30,000-34,999 ($577-672/week)", "$30,000-34,999", income)) %>%
  mutate(income = ifelse(income == "$35,000-39,000 ($673-768/week)", "$35,000-39,999", income)) %>% 
  mutate(income = ifelse(income == "$35,000-39,000", "$35,000-39,999", income)) %>% 
  mutate(income = ifelse(income == "$50,000-$59,999", "$50,000-59,999", income)) %>% 
  mutate(income = ifelse(income == "$60,000-$74,999", "$60,000-74,999", income)) %>% 
  mutate(income = ifelse(income == "$75,000 or more/year", "$75,000 or more" , income)) %>%
  mutate(income = factor(income, ordered = TRUE,
    levels = c("Under $9,999", "$10,000-14,999", "$15,000-19,999",
      "$20,000-24,999", "$25,000-29,999", "$30,000-34,999",
      "$35,000-39,999", "$40,000-44,999", "$45,000-49,999",
      "$50,000-59,999", "$60,000-74,999", "$75,000 or more")))

## Date of First Call

# I'm going to create a date of first call which will combine the month and year of the first call

dcaf = dcaf %>% 
  mutate(year_of_first_call = str_replace_all(year_of_first_call, c("\\.0" = ""))) %>%
  mutate(month_of_first_call = str_replace_all(month_of_first_call, c("\\.0" = ""))) %>%
  mutate(month_of_first_call = str_pad(month_of_first_call, width = 2, side = "left", pad = "0")) %>%
  mutate(date_of_first_call = parse_date(paste(year_of_first_call, month_of_first_call , sep = "/"), format = "%Y/%m", na = "NA/NA")) %>%
  select(-month_of_first_call, -year_of_first_call)


## Combining insurance
  # There are two groups for other state medicaid
  # - Other state Medicaid
  # - Other State Medicaid
  # I'm going to combine it to the former one.

dcaf = dcaf %>%
  mutate(insurance = as.character(insurance)) %>%
  mutate(insurance = ifelse(insurance == "Other State Medicaid", "Other state Medicaid", insurance)) %>%
  mutate(insurance = parse_factor(insurance, levels = NULL))


write.csv(dcaf, "dcaf_clean.csv")

