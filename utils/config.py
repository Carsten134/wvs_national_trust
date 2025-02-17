WAVE_YEAR = {
    "DEU": 2018,
    "CAN": 2020,
    "AUS": 2018,
    "NLD": 2022,
    "USA": 2017
}

TIME_SERIES_TRUST_ENC = ["E069_12", "E069_10", "E069_04", "E069_02", "E069_05", "E069_06", "E069_07", "E069_08", "E069_11", "E069_17"]
# Regression config
REF_POL = 5
REF_HAPPINESS = 2
COUNTRIES_ISO = ['AUS','CAN','DEU','NLD','USA']
REGRESSORS = [# corruption
              "group_corruption",
              
              # migration
              "is_immigrant",
              "mother_immigrant",
              "father_immigrant",
              "migration_positive",
              "migration_negative",
              
              # political preference
              *[f"pol_value_{i}" for i in range(1,11) if i != REF_POL],

              # happiness dummies
              *[f"happ__{i}" for i in range(1,5) if i != REF_HAPPINESS],

              # hardships and security
              "hardships_questions",
              "security_neighborhood",
              "security_financial",
              "security_war",
              
              # demographics (including happiness)
              "age_std",
              "age_std^2",
              "gender",
              "above_avg_inc"]
