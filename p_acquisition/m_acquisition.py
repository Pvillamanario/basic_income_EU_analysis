import pandas as pd
from sqlalchemy import create_engine
import requests
from bs4 import BeautifulSoup as bs

# acquisition functions


def acquire_db_data(path):

    # SqlAlchemy Engine
    path = './data/raw/raw_data_project_m1.db'
    engine = create_engine(f'sqlite:///{path}')
    print('DataBase connected.')


    # Table acquisition ----> Saving as .parquet

    df_personal_info = pd.read_sql_table('personal_info', engine)
    df_personal_info.to_parquet('./data/raw/personal_info.parquet')

    df_country_info = pd.read_sql_table('country_info', engine)
    df_country_info.to_parquet('./data/raw/country_info.parquet')

    df_career_info = pd.read_sql_table('career_info', engine)
    df_career_info.to_parquet('./data/raw/career_info.parquet')

    df_poll_info = pd.read_sql_table('poll_info', engine)
    df_poll_info.to_parquet('./data/raw/poll_info.parquet')

    print('DataBase data acquired.')

    # Closing connection to db
    engine.dispose()
    print('DataBase connection closed')


def api_request_job_codes():

    print('Loading job list')

    # Creating list of unique values of job code.
    df_career_info = pd.read_parquet('./data/raw/career_info.parquet')
    norm_job_codes = df_career_info['normalized_job_code'].unique().tolist()
    norm_job_dic = {}

    # API request to retrieve job names.
    print('Connecting to jobs API...')
    for i in norm_job_codes[1:]:  # Let's skip 'none'

        response = requests.get(f'http://api.dataatwork.org/v1/jobs/{i}')
        norm_job_dic[i] = (response.json())['title']

    norm_job_dic['none'] = 'none'  # Let's add none to job dic

    print('Job titles retrieved and saved.')
    pd.DataFrame(norm_job_dic.items(), columns=['normalized_job_code', 'title'])\
        .to_parquet('./data/raw/norm_job_codes-names.parquet')


def country_codes():
    url = 'https://ec.europa.eu/eurostat/statistics-explained/index.php/Glossary:Country_codes'
    html = requests.get(url).content

    soup = bs(html, 'lxml')
    soup = soup.find_all('td')
    lst = []

    for i in soup:
        if str(i) != ' ':
            lst.append(str(i)[4:-6])

    countries = []
    codes = []

    for i in range(0, len(lst[:56])):  # Hasta UK
        if i % 2 == 0:
            countries.append(lst[i])
        else:
            codes.append((lst[i].strip())[1:-1])

    pd.DataFrame(zip(countries, codes), columns=['country', 'code'])\
        .to_parquet('./data/raw/webscraping_country_code-name.parquet')