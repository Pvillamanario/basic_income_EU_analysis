import pandas as pd

# Gmail key
import configparser

# Graphical libs
import matplotlib.pyplot as plt
import seaborn as sns

# Reading images libs
from PIL import Image

# Twitter API
import tweepy

# Email libs
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders


def graph_reporting(country):
    print('Loading data...')

    df_country = pd.read_csv('./data/results/country_analysis.csv')
    df_opinion = pd.read_csv('./data/results/opinion_analysis.csv')
    df_edu = pd.read_csv('./data/results/edu_level_analysis.csv')

    # Titles setting:
    if country == '':
        tit1 = 'European gender distribution'
        tit2 = 'European vote intention'
        tit3 = 'European top jobs / education level'
    else:
        tit1 = f'Gender distribution for {country}'
        tit2 = f'Vote intention for {country}'
        tit3 = f'Top jobs/education level in {country}'

    print('Creating gender distribution chart.')
    g = df_country[['Gender', 'Quantity']].set_index('Gender').groupby('Gender').sum().reset_index()
    ax = g.set_index('Gender').plot.pie(y='Quantity', x='Gender', figsize=(8, 8), title=tit1)
    fig = ax.get_figure()
    fig.savefig('./data/reporting/gender_distribution.jpeg')

    print('Creating vote intention chart.')
    h = df_opinion[['Vote_intention', 'Number_of_votes']].reset_index()
    bx = sns.catplot(x='Vote_intention', y='Number_of_votes',
                     kind='bar',
                     aspect=4,
                     palette="ch:.25",
                     data=h,
                     margin_titles=tit2
                     )
    bx.fig.suptitle(tit2)
    bx.savefig('./data/reporting/vote_intention.jpeg')

    print('Creating top jobs/education level chart.\n')
    plt.figure(figsize=(20, 8))
    cx = sns.scatterplot(x="Education_level", y="Total",
                         hue="Job_title", size= "Total",
                         sizes=(100, 500), legend='brief',
                         data=df_edu,
                         )
    cx.legend(loc='lower left', ncol=2)
    cx.set_title(tit3)

    cx.figure.savefig('./data/reporting/top_education_jobs.jpeg')


def pdf_reporting():
    print('Extracting chart images.')
    img1 = Image.open('./data/reporting/gender_distribution.jpeg')
    img2 = Image.open('./data/reporting/vote_intention.jpeg')
    img3 = Image.open('./data/reporting/top_education_jobs.jpeg')

    img1.save(r'./data/reporting/reporting.pdf', save_all=True, append_images=[img2, img3])
    print('PDF reporting generated.\n')


def email_reporting(email):

    # Gmail app key retrieving
    cfg = configparser.RawConfigParser()
    cfg.read('config.ini')

    # Sender / Receiver
    fromaddr = "p.villamanario@gmail.com"
    toaddr = email

    # instance of MIMEMultipart
    msg = MIMEMultipart()

    # storing the senders email address
    msg['From'] = fromaddr

    # storing the receivers email address
    msg['To'] = toaddr

    # storing the subject
    msg['Subject'] = "Data Project I: Poll analysis."

    # string to store the body of the mail
    body = '''Hello, 
    This is the poll analysis about European Basic Income!
    Thanks ;)'''

    # attach the body with the msg instance
    msg.attach(MIMEText(body, 'plain'))

    # open the file to be sent
    filename = "reporting.pdf"
    attachment = open("./data/reporting/reporting.pdf", "rb")  # <--------------------------------------  Attachements
    filename2 = 'country_analysis.csv'
    attachment2 = open("./data/results/country_analysis.csv", "rb")

    # instance of MIMEBase and named as p
    p = MIMEBase('application', 'octet-stream')
    r = MIMEBase('application', 'octet-stream')
    # To change the payload into encoded form
    p.set_payload(attachment.read())
    r.set_payload(attachment2.read())

    # encode into base64
    encoders.encode_base64(p)
    encoders.encode_base64(r)

    p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
    r.add_header('Content-Disposition', "attachment; filename= %s" % filename2)

    # attach the instance 'p' to instance 'msg'
    msg.attach(p)
    msg.attach(r)

    # creates SMTP session
    s = smtplib.SMTP('smtp.gmail.com', 587)

    # start TLS for security
    s.starttls()

    # Authentication
    s.login(fromaddr, cfg['mail']['app_key'])  # <----------------------------------------  Contraseña de aplicación

    # Converts the Multipart msg into a string
    text = msg.as_string()

    # sending the mail
    s.sendmail(fromaddr, toaddr, text)

    # terminating the session
    s.quit()

    print(f'Reporting sent to {email}.\n')


def tweets():

    CONSUMER_KEY = 'kMjAJ03t0W9Z53zDy5jlyUkBj'
    CONSUMER_SECRET = 'FWYQRVEUR2QVte6kYUAIZXmEntjXNRP461VkJFjAB8eQlZqZYF'
    ACCESS_TOKEN = '1273324310204166158-ZtNvphpB6U0QhTRj3bvSXpaGGjuMZI'
    ACCESS_SECRET = 'eEf15oUhVCgEpiA1Sr9iSgyZuVVTYPIqDuK0u2C1gOxbS'

    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

    api = tweepy.API(auth)

    tt = api.search(q='#basicincome OR #rentabasica OR #revenuuniversel', include_entities=False)

    print('\n\n __LAST TWEETS ABOUT BASIC INCOME__\n')
    for i in tt:
        print(i.text, '|', i.created_at, '|', i.place.name if i.place else "Undefined place")