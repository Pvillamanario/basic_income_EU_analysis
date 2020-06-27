# Graphical libs
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Email libs
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

# Reading images lib
from PIL import Image


def graph_reporting():
    print('Loading data...')

    df_country = pd.read_json('./data/results/country_analysis.json')
    df_opinion = pd.read_json('./data/results/opinion_analysis.json')
    df_edu = pd.read_json('./data/results/edu_level_analysis.json')


    print('Creating gender distribution chart.')
    g = df_country[['Gender', 'Quantity']].set_index('Gender').groupby('Gender').sum().reset_index()
    ax = g.set_index('Gender').plot.pie(y='Quantity', x='Gender', figsize=(8, 8))
    fig = ax.get_figure()
    fig.savefig('./data/reporting/gender_distribution.jpeg')


    print('Creating vote intention chart.')
    h = df_opinion[['Vote_intention', 'Number_of_votes']].reset_index()
    bx = sns.catplot(x='Vote_intention', y='Number_of_votes', kind='bar', aspect=4, palette="ch:.25", data=h);
    bx.savefig('./data/reporting/vote_intention.jpeg')


    print('Creating top jobs/education level chart.\n')
    plt.figure(figsize=(20, 8))
    cx = sns.scatterplot(x="Education_level", y="Total",
                         hue="Job_title", size="Total",
                         sizes=(100, 500), legend='brief',
                         data=df_edu)
    lgn = cx.legend(loc='lower left', ncol=2)

    cx.figure.savefig('./data/reporting/top_education_jobs.jpeg')


def pdf_reporting():
    print('Adding images.')
    img1 = Image.open('./data/reporting/gender_distribution.jpeg')
    img2 = Image.open('./data/reporting/vote_intention.jpeg')
    img3 = Image.open('./data/reporting/top_education_jobs.jpeg')

    img1.save(r'./data/reporting/reporting.pdf', save_all=True, append_images=[img2, img3])
    print('PDF reporting generated.\n')


def email_reporting(email):


    fromaddr = "p.villamanario@gmail.com"  # <--------------------------------------  Cuenta envío
    toaddr = email  # <----------------------------------------  Email receptor

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

    # instance of MIMEBase and named as p
    p = MIMEBase('application', 'octet-stream')

    # To change the payload into encoded form
    p.set_payload((attachment).read())

    # encode into base64
    encoders.encode_base64(p)

    p.add_header('Content-Disposition', "attachment; filename= %s" % filename)

    # attach the instance 'p' to instance 'msg'
    msg.attach(p)

    # creates SMTP session
    s = smtplib.SMTP('smtp.gmail.com', 587)

    # start TLS for security
    s.starttls()

    # Authentication
    s.login(fromaddr, "______")  # <----------------------------------------  Contraseña de aplicación

    # Converts the Multipart msg into a string
    text = msg.as_string()

    # sending the mail
    s.sendmail(fromaddr, toaddr, text)

    # terminating the session
    s.quit()

    print(f'Reporting sent to {email}')