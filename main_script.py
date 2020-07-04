import argparse
from p_acquisition import m_acquisition as mac
from p_wrangling import m_wrangling as mwr
from p_analysis import m_analysis as man 
from p_reporting import m_reporting as mre 


def argument_parser():
    parser = argparse.ArgumentParser(description = 'Specify database path, country and email address.')
    parser.add_argument("-p", "--path", help="Database path.", type=str, required=True)
    parser.add_argument("-c", "--country", help="Country results.", type=str, required=False, default='')
    parser.add_argument("-e", "--email", help="Email to send reporting.", type=str, required=True)
    parser.add_argument("-hs", "--hashtag", help="Twitter hashtag.", type=str, required=True)
    args = parser.parse_args()
    return args


def main(arguments):

    print('\n\n<< Starting pipeline >>\n')

    # Data acquisition
    mac.acquire_db_data(arguments.path)
    # mac.api_request_job_codes()
    mac.country_codes()

    # Data wrangling
    mwr.wrangle()

    # Data analysis
    df_poll = man.analysis_settings(arguments.country)
    man.analyze_ch1(df_poll)
    man.analysis_ch2(df_poll)
    man.analysis_ch3(df_poll)

    # Data reporting
    mre.graph_reporting(arguments.country)
    mre.pdf_reporting()
    mre.email_reporting(arguments.email)
    mre.tweets(arguments.hashtag)

    print('\n\n========== Pipeline is complete. You may find the results in the folder ./data/results =========')


if __name__ == '__main__':
    arguments = argument_parser()
    main(arguments)
