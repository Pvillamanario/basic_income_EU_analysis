import pandas as pd
import re

# wrangling functions

def wrangle():

    print('Raw data retrieved.')
    df_personal_info =  pd.read_parquet('./data/raw/personal_info.parquet')
    df_country_info =   pd.read_parquet('./data/raw/country_info.parquet')
    df_norm_job_codes = pd.read_parquet('./data/raw/norm_job_codes-names.parquet')
    df_career_info =    pd.read_parquet('./data/raw/career_info.parquet')
    df_country_codes =  pd.read_parquet('./data/raw/webscraping_country_code-name.parquet')
    df_poll_info =      pd.read_parquet('./data/raw/poll_info.parquet')

    # Personal info wrangling:
    df_personal_info['age'] = df_personal_info['age'].apply(lambda x: re.sub(r'\D', '', x)).astype(int)
    df_personal_info['gender'] = df_personal_info['gender'].apply(lambda x: x.lower().capitalize())
    df_personal_info["gender"].replace("Fem", "Female", inplace=True)
    df_personal_info['dem_has_children'] = df_personal_info['dem_has_children'].apply(lambda x: x.lower())
    print('--> df_personal_info normalized.')

    # Personal info wrangling:
    df_country_info.replace('GB', 'UK', inplace=True)  # normalize GB-UK
    df_country_info.replace('GR', 'EL', inplace=True)  # normalize GR-EL

    try:
        df_country_codes.set_index('code', inplace=True)
    except:
        pass

    df_country_info['country'] = df_country_info['country_code'].apply(lambda x: df_country_codes.loc[x])
    df_country_info['rural'] = df_country_info['rural'].apply(lambda x: x.lower())
    df_country_info = df_country_info[['uuid', 'country_code', 'country', 'rural']]

    # Career info wrangling:
    df_career_info['dem_education_level'].fillna('no', inplace=True)
    df_career_info['normalized_job_code'].replace('None', 'none', inplace=True)
    df_norm_job_codes.fillna('none', inplace=True)

    df_career_info = df_career_info.merge(df_norm_job_codes, on='normalized_job_code', how='left')
    df_career_info.rename(
        columns={'dem_education_level': 'education_level',
                 'dem_full_time_job': 'full_time_job',
                 'title': 'job_title'},
        inplace=True)

    print('--> df_career_info normalized.')

    # Poll info wrangling:
    df_poll_info.rename(columns={'question_bbi_2016wave4_basicincome_awareness': 'basic_income_awareness',
                                 'question_bbi_2016wave4_basicincome_vote': 'basic_income_vote',
                                 'question_bbi_2016wave4_basicincome_effect': 'basic_income_effect',
                                 'question_bbi_2016wave4_basicincome_argumentsfor': 'basic_income_arguments_for',
                                 'question_bbi_2016wave4_basicincome_argumentsagainst': 'basic_income_arguments_against'},
                        inplace=True)

    df_poll_info['basic_income_effect'] = df_poll_info['basic_income_effect']\
        .apply(lambda x: re.sub('‰Û_', "I would", x))

    print('--> df_career_info normalized.')

    # Merging DataFrames:
    print('Merging data frames.')
    df_processed = df_personal_info.merge(df_country_info, on='uuid', how='left') \
        .merge(df_career_info, on='uuid', how='left') \
        .merge(df_poll_info, on='uuid', how='left')

    df_processed.to_csv('./data/processed/df_processed.csv')
    print('Processed data saved.\n')