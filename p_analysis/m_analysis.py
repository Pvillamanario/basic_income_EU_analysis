import pandas as pd
import numpy as np


# analysis functions

def analyze_ch1(country):
    # Deactivating SettingWithCopyWarning.
    #A value is trying to be set on a copy of a slice from a DataFrame.

    pd.set_option('mode.chained_assignment', None)

    print(f'The chosen country is: {country}')
    print('Starting country analysis.')
    df_poll = pd.read_json('./data/processed/df_processed.json')

    df_ch1 = df_poll[['country', 'job_title', 'gender', 'uuid']]
    df_ch1 = df_ch1.groupby(['country', 'job_title', 'gender'])['uuid'].count().reset_index()
    df_ch1.rename(columns={'country': 'Country',
                           'job_title': 'Job title',
                           'gender': 'Gender',
                           'uuid': 'Quantity'},
                  inplace=True)

    country_filter = df_ch1['Country'] == country.capitalize()
    df_country = df_ch1.loc[country_filter]
    df_country['Country percentage ‰'] = df_country['Quantity'] / df_country['Quantity'].sum() * 1000

    df_country.to_csv('./data/results/country_analysis.csv')
    print('Country analysis saved to .csv\n')

def analysis_ch2():

    print('Starting vote intention analysis.')

    df_poll = pd.read_json('./data/processed/df_processed.json')
    df_opinion = df_poll[['basic_income_vote',
                          'basic_income_arguments_for',
                          'basic_income_arguments_against', 'uuid']]

    df_opinion['number_pro_args'] = df_opinion['basic_income_arguments_for']\
        .apply(lambda x: len(x.split('|')))
    df_opinion['number_con_args'] = df_opinion['basic_income_arguments_against']\
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

def analysis_ch3():

    print('Starting top jobs/education level analysis.')

    df_poll = pd.read_json('./data/processed/df_processed.json')

    df_edu = df_poll[['full_time_job', 'education_level', 'job_title', 'uuid']]
    working_filter = df_edu['full_time_job'] == 'yes'

    x = df_edu[working_filter].groupby(['education_level', 'job_title']).agg(total=('uuid', 'count'))
    x.reset_index

    df_high = x.loc['high', :].nlargest(3, 'total')
    df_medium = x.loc['medium', :].nlargest(3, 'total')
    df_low = x.loc['low', :].nlargest(3, 'total')
    df_noedu = x.loc['no', :].nlargest(3, 'total')

    df_high['Education_level'] = 'High'
    df_medium['Education_level'] = 'Medium'
    df_low['Education_level'] = 'Low'
    df_noedu['Education_level'] = 'No'

    df_high.reset_index().set_index('Education_level', inplace=True)
    df_medium.reset_index().set_index('Education_level', inplace=True)
    df_low.reset_index().set_index('Education_level', inplace=True)
    df_noedu.reset_index().set_index('Education_level', inplace=True)

    df_edu = pd.concat([df_high, df_medium, df_low, df_noedu]).reset_index()
    df_edu.rename(columns={'job_title': 'Job_title',
                           'total': 'Total'},
                  inplace=True)

    df_edu.to_csv('./data/results/edu_level_analysis.csv')
    print('Top jobs/education analysis saved to .csv\n')
