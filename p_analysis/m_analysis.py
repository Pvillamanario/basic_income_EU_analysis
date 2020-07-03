import pandas as pd
import numpy as np


# analysis functions

def analysis_settings(country):
    # Deactivating SettingWithCopyWarning.
    # A value is trying to be set on a copy of a slice from a DataFrame.
    pd.set_option('mode.chained_assignment', None)

    # Selecting country slice from dataset to be analysed

    df_poll = pd.read_csv('./data/processed/df_processed.csv')
    df_poll.replace(' United Kingdom', 'United Kingdom', inplace=True)
    country_filter = df_poll['country'] == country

    if country == '':
        print('---Whole dataset selected:---')
        df_poll = df_poll
    else:
        print(f'\n---The chosen country is: {country.upper()} ---\n')
        df_poll = df_poll[country_filter]

    return df_poll


def analyze_ch1(df_poll):
    print('Starting analysis.')
    df_ch1 = df_poll[['country', 'job_title', 'gender', 'uuid']]
    df_ch1 = df_ch1.groupby(['country', 'job_title', 'gender'])['uuid'].count().reset_index()
    df_ch1.rename(columns={'country': 'Country',
                           'job_title': 'Job title',
                           'gender': 'Gender',
                           'uuid': 'Quantity'},
                  inplace=True)
    df_ch1['Country percentage ‰'] = df_ch1['Quantity'] / df_ch1['Quantity'].sum() * 1000

    df_ch1.to_csv('./data/results/country_analysis.csv')
    print('Country analysis saved to .csv\n')


def analysis_ch2(df_poll):
    print('Starting vote intention analysis.')
    df_opinion = df_poll[['basic_income_vote',
                          'basic_income_arguments_for',
                          'basic_income_arguments_against', 'uuid']]

    df_opinion['number_pro_args'] = df_opinion['basic_income_arguments_for'] \
        .apply(lambda x: len(x.split('|')))
    df_opinion['number_con_args'] = df_opinion['basic_income_arguments_against'] \
        .apply(lambda x: len(x.split('|')))

    df_opinion = df_opinion.groupby('basic_income_vote').agg(number_pro_args=('number_pro_args', 'sum'),
                                                             number_con_args=('number_con_args', 'sum'),
                                                             number_votes=('uuid', 'count')
                                                             )
    df_opinion = df_opinion[['number_votes', 'number_pro_args', 'number_con_args']]
    df_opinion.reset_index(inplace=True)
    df_opinion.rename(columns={'basic_income_vote': 'Vote_intention', 'number_votes': 'Number_of_votes',
                               'number_pro_args': 'Number_pro_arguments', 'number_con_args': 'Number_con_arguments'},
                      inplace=True)
    df_opinion.set_index('Vote_intention')

    df_opinion.to_csv('./data/results/opinion_analysis.csv')
    print('Vote intention analysis saved to .csv\n')


def analysis_ch3(df_poll):
    print('Starting top jobs/education level analysis.')

    df_edu = df_poll[['full_time_job', 'education_level', 'job_title', 'uuid']]
    df_edu = df_edu.groupby(['education_level', 'job_title']).agg(total=('uuid', 'count'))
    df_edu = df_edu.reset_index()
    df_edu = df_edu.groupby('education_level').apply(lambda x: x.nlargest(3, 'total')).reset_index(drop=True)
    df_edu.rename(columns={'education_level': 'Education_level', 'job_title': 'Job_title', 'total': 'Total'},
                  inplace=True)
    df_edu.set_index('Education_level', inplace=True)
    df_edu.to_csv('./data/results/edu_level_analysis.csv')
    print('Top jobs/education level analysis saved to .csv\n')

