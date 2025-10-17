
import cProfile
import pstats
import os
import pandas as pd
import time
import statistics
from app.main_docker import predict, model
from app.model import CustomerData

# =========================================
# Configuration du profiling
# =========================================
OUTPUT_DIR = "cProfile"
os.makedirs(OUTPUT_DIR, exist_ok=True)

PROFILE_PATH = os.path.join(OUTPUT_DIR, "profiling_results_optimized.prof")
SUMMARY_PATH = os.path.join(OUTPUT_DIR, "profiling_summary_optimized.txt")

# =========================================
# Exemple de payload (comme une requête API)
# =========================================
sample_data = {
  "EXT_SOURCE_2": 0.268645,
  "EXT_SOURCE_3": 0.769735,
  "NAME_EDUCATION_TYPE": 3,
  "CODE_GENDER_0_0": 0,
  "FLAG_DOCUMENT_3": 1,
  "NAME_CONTRACT_STATUS_most_use_Refused": 0,
  "NAME_INCOME_TYPE": 2,
  "CNT_DRAWINGS_ATM_CURRENT_mean": 0,
  "EXT_SOURCE_1": 0.176564,
  "FLAG_OWN_CAR_0_0": 1,
  "PAYMENT_RATIO_mean": 1,
  "MONTHS_BALANCE_std": 18.976630,
  "CNT_PAYMENT_max": 50,
  "BALANCE_LIMIT_RATIO_max": 0,
  "DAYS_BIRTH": -19932,
  "SK_ID_PREV_nunique": 4.0,
  "NAME_FAMILY_STATUS_Married": 0,
  "CNT_DRAWINGS_CURRENT_mean": 0.0,
  "AMT_DOWN_PAYMENT_max": 6787.5,
  "FLAG_DOCUMENT_6": 0,
  "NAME_YIELD_GROUP_most_use": 3,
  "REGION_RATING_CLIENT": 2,
  "DEF_30_CNT_SOCIAL_CIRCLE": 0.0,
  "WALLSMATERIAL_MODE_Panel": 0,
  "DAYS_LATE_max": -3.0,
  "REG_CITY_NOT_LIVE_CITY": 0,
  "DAYS_EMPLOYED": -7635,
  "SK_DPD_DEF_max": 0.0,
  "NAME_CONTRACT_TYPE_most_use_Cash_loans": 0,
  "AMT_INSTALMENT_sum": 546870.780,
  "CODE_REJECT_REASON_most_use_HC": 0,
  "NAME_GOODS_CATEGORY_most_use_Clothing_and_Accessories": 0,
  "OCCUPATION_TYPE_Core_staff": 1,
  "ORGANIZATION_TYPE_Transport_type_3": 0,
  "AMT_CREDIT": 235000,
  "OWN_CAR_AGE": 5,
  "CODE_REJECT_REASON_most_use_SCOFR": 0,
  "NAME_CONTRACT_TYPE_Cash_loans": 1,
  "CNT_INSTALMENT_FUTURE_max": 5.0,
  "NAME_GOODS_CATEGORY_most_use_Furniture": 0,
  "DRAWINGS_LIMIT_RATIO_mean": 0,
  "AMT_ANNUITY": 3458.0,
  "DAYS_LAST_DUE_1ST_VERSION_max": 587.0,
  "DAYS_DECISION_min": -543.0,
  "AMT_DIFF_mean": 0.000000,
  "AMT_DRAWINGS_ATM_CURRENT_mean": 0,
  "NUM_INSTALMENT_NUMBER_max": 14.0,
  "FLOORSMAX_AVG": 0.2345,
  "NAME_TYPE_SUITE_most_use_Other_A": 0,
  "PRODUCT_COMBINATION_most_use_Card_Street": 0,
  "ORGANIZATION_TYPE_Self_employed": 0,
  "AMT_REQ_CREDIT_BUREAU_QRT": 0.0,
  "SK_DPD_min": 0.0,
  "MONTHS_BALANCE_max": -25.0,
  "EMERGENCYSTATE_MODE_0_0": 0,
  "AMT_BALANCE_max": 0.0,
  "DAYS_ID_PUBLISH": -1992,
  "DAYS_FIRST_DUE_min": -890,
  "ORGANIZATION_TYPE_Postal": 0,
  "FLAG_DOCUMENT_18": 0,
  "DAYS_LAST_DUE_mean": -4506,
  "DAYS_DECISION_mean": -525,
  "NAME_SELLER_INDUSTRY_most_use_Industry": 0,
  "OCCUPATION_TYPE_Laborers": 1,
  "NAME_CLIENT_TYPE_most_use_Repeater": 0,
  "NAME_CLIENT_TYPE_most_use_Refreshed": 1,
  "ORGANIZATION_TYPE_Industry_type_3": 0,
  "NAME_TYPE_SUITE_Unaccompanied": 1,
  "ORGANIZATION_TYPE_Construction": 0,
  "ORGANIZATION_TYPE_Other": 0,
  "CHANNEL_TYPE_most_use_AP_Cash_loan": 0,
  "CHANNEL_TYPE_most_use_Channel_of_corporate_sales": 0,
  "PRODUCT_COMBINATION_most_use_POS_mobile_with_interest": 0,
  "OCCUPATION_TYPE_Drivers": 0,
  "AMT_ANNUITY_min": 1756.505,
  "RATE_DOWN_PAYMENT_max": 0.096732,
  "HOUSETYPE_MODE_specific_housing": 0,
  "AMT_REQ_CREDIT_BUREAU_MON": 0.0,
  "LIVE_REGION_NOT_WORK_REGION": 0,
  "SK_DPD_max": 0.0,
  "AMT_REQ_CREDIT_BUREAU_WEEK": 0.0,
  "AMT_CREDIT_LIMIT_ACTUAL_max": 0,
  "ORGANIZATION_TYPE_Industry_type_9": 0,
  "FLAG_DOCUMENT_16": 0,
  "NAME_FAMILY_STATUS_Single_not_married": 1,
  "CHANNEL_TYPE_most_use_Country_wide": 0,
  "CNT_INSTALMENT_FUTURE_min": 0.0,
  "OCCUPATION_TYPE_Low_skill_Laborers": 0,
  "FLAG_WORK_PHONE": 1,
  "DAYS_LAST_DUE_max": -354,
  "DAYS_LAST_PHONE_CHANGE": -275,
  "ORGANIZATION_TYPE_Government": 0,
  "NAME_TYPE_SUITE_Other_B": 0,
  "ORGANIZATION_TYPE_Military": 0,
  "PRODUCT_COMBINATION_most_use_Cash_Street_low": 0,
  "YEARS_BEGINEXPLUATATION_AVG": 0.9678,
  "CNT_PAYMENT_min": 5.0,
  "SELLERPLACE_AREA_max": 750.0,
  "AMT_DIFF_max": 0,
  "NAME_SELLER_INDUSTRY_most_use_Construction": 0,
  "DAYS_FIRST_DRAWING_mean": 365243.0,
  "HOUR_APPR_PROCESS_START_max": 15.0,
  "LIVE_CITY_NOT_WORK_CITY": 1,
  "NAME_HOUSING_TYPE_Rented_apartment": 0,
  "PRODUCT_COMBINATION_most_use_Cash_Street_high": 0,
  "ORGANIZATION_TYPE_Business_Entity_Type_3": 1,
  "NAME_CONTRACT_TYPE_most_use_Revolving_loans": 0,
  "ORGANIZATION_TYPE_School": 0,
  "ORGANIZATION_TYPE_Kindergarten": 0,
  "DAYS_LAST_DUE_min": -25.0,
  "CNT_DRAWINGS_CURRENT_sum": 0.0,
  "OCCUPATION_TYPE_Accountants": 0,
  "BASEMENTAREA_AVG": 0.0634,
  "NAME_HOUSING_TYPE_Municipal_apartment": 0,
  "OCCUPATION_TYPE_Security_staff": 0,
  "CHANNEL_TYPE_most_use_Contact_center": 0,
  "AMT_INSTALMENT_mean": 56098.0,
  "ORGANIZATION_TYPE_Trade_type_2": 0,
  "AMT_PAYMENT_CURRENT_max": 0,
  "EMERGENCYSTATE_MODE_1_0": 0,
  "ORGANIZATION_TYPE_Transport_type_2": 0,
  "AMT_REQ_CREDIT_BUREAU_YEAR": 1.0,
  "PRODUCT_COMBINATION_most_use_POS_industry_with_interest": 0,
  "FLAG_DOCUMENT_11": 0,
  "AMT_REQ_CREDIT_BUREAU_DAY": 0,
  "AMT_DIFF_min": 0.000,
  "AMT_DRAWINGS_POS_CURRENT_mean": 0,
  "SK_ID_PREV_count": 4.0,
  "NAME_CONTRACT_STATUS_most_use_Active": 1,
  "AMT_DRAWINGS_ATM_CURRENT_sum": 0.0,
  "ENTRANCES_AVG": 0.0687,
  "DAYS_REGISTRATION": -4311.0,
  "NAME_PRODUCT_TYPE_most_use_x_sell": 0,
  "NAME_FAMILY_STATUS_Civil_marriage": 0,
  "ORGANIZATION_TYPE_Security_Ministries": 0,
  "DAYS_LATE_mean": -7.298880,
  "ORGANIZATION_TYPE_Bank": 0,
  "ORGANIZATION_TYPE_Business_Entity_Type_2": 0,
  "SELLERPLACE_AREA_mean": 150.000000,
  "NONLIVINGAREA_AVG": 0.0098,
  "CNT_DRAWINGS_ATM_CURRENT_sum": 0.0,
  "NAME_HOUSING_TYPE_House_apartment": 1,
  "PRODUCT_COMBINATION_most_use_Cash_X_Sell_middle": 0,
  "AMT_INCOME_TOTAL": 203390.0,
  "NAME_FAMILY_STATUS_Separated": 0,
  "ORGANIZATION_TYPE_Legal_Services": 0,
  "ORGANIZATION_TYPE_Realtor": 0,
  "REGION_POPULATION_RELATIVE": 0.00589,
  "NAME_TYPE_SUITE_Spouse_partner": 0,
  "ORGANIZATION_TYPE_Industry_type_11": 0,
  "ORGANIZATION_TYPE_Trade_type_6": 0,
  "ORGANIZATION_TYPE_Trade_type_7": 0,
  "ORGANIZATION_TYPE_Restaurant": 0,
  "WALLSMATERIAL_MODE_Block": 1,
  "AMT_GOODS_PRICE_min": 19526.00,
  "PRODUCT_COMBINATION_most_use_Card_X_Sell": 0,
  "DAYS_DECISION_max": -230,
  "FLAG_DOCUMENT_13": 0,
  "FLOORSMIN_AVG": 0.3082,
  "ORGANIZATION_TYPE_Industry_type_12": 0,
  "NAME_HOUSING_TYPE_With_parents": 0,
  "PRODUCT_COMBINATION_most_use_POS_industry_without_interest": 0,
  "AMT_DRAWINGS_CURRENT_sum": 0,
  "AMT_ANNUITY_max": 32559.0,
  "NONLIVINGAPARTMENTS_AVG": 0.0026,
  "NAME_CONTRACT_STATUS_most_use_Signed": 0,
  "APARTMENTS_AVG": 0.0355,
  "HOUR_APPR_PROCESS_START_std": 2.786500,
  "AMT_APPLICATION_mean": 2760840.000,
  "CNT_CHILDREN": 0,
  "NAME_CASH_LOAN_PURPOSE_most_use_Buying_a_holiday_home_land": 0,
  "DAYS_LATE_min": -28,
  "OCCUPATION_TYPE_High_skill_tech_staff": 0,
  "OCCUPATION_TYPE_Cleaning_staff": 0,
  "OBS_30_CNT_SOCIAL_CIRCLE": 2.0,
  "NAME_PORTFOLIO_most_use_Cash": 0,
  "NAME_HOUSING_TYPE_Office_apartment": 0,
  "NAME_SELLER_INDUSTRY_most_use_Auto_technology": 1,
  "HOUR_APPR_PROCESS_START": 15,
  "CHANNEL_TYPE_most_use_Stone": 0,
  "NAME_TYPE_SUITE_most_use_Unaccompanied": 1,
  "CHANNEL_TYPE_most_use_Credit_and_cash_offices": 1,
  "COMMONAREA_AVG": 0.0302,
  "WALLSMATERIAL_MODE_Stone_brick": 1,
  "DAYS_FIRST_DRAWING_max": 365243.0,
  "ORGANIZATION_TYPE_Trade_type_3": 0,
  "AMT_DRAWINGS_CURRENT_mean": 0
}

# Création de l’objet CustomerData (simulation d’une requête FastAPI)
customer = CustomerData(**sample_data)

# =========================================
# Fonction à profiler
# =========================================
def test_prediction():
    """Effectue plusieurs appels directs à la fonction FastAPI predict()"""
    latencies = []
    for i in range(10):
        start = time.perf_counter()
        response = predict(customer)
        latency = (time.perf_counter() - start) * 1000  # en ms
        latencies.append(latency)
        print(f"✅ Prédiction {i+1} - {latency:.2f} ms - Label : {response.get('label', 'N/A')}")
    print("\n=== 📊 Statistiques globales ===")
    print(f"Moyenne latence : {statistics.mean(latencies):.2f} ms")
    print(f"Latence min : {min(latencies):.2f} ms")
    print(f"Latence max : {max(latencies):.2f} ms")

# =========================================
# Exécution du profiling
# =========================================
with cProfile.Profile() as pr:
    test_prediction()

# =========================================
# Résumé du profilage
# =========================================
stats = pstats.Stats(pr)
stats.sort_stats(pstats.SortKey.TIME)

print("\n=== 🔍 Fonctions les plus coûteuses ===")
stats.print_stats(20)

# Sauvegarde complète pour visualisation (SnakeViz ou pstats)
stats.dump_stats(PROFILE_PATH)

# Sauvegarde résumé dans un fichier texte
with open(SUMMARY_PATH, "w") as f:
    f.write("=== Résumé du Profiling (Top 20) ===\n")
    ps = pstats.Stats(pr, stream=f)
    ps.sort_stats(pstats.SortKey.TIME)
    ps.print_stats(20)

print(f"\n📁 Résultats enregistrés dans :\n - {PROFILE_PATH}\n - {SUMMARY_PATH}")
