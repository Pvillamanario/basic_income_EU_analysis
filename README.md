# EUROPEAN BASIC INCOME
# Vote intention poll
####IRONHACK Data Analysis - Project I

This repository correspond to the pipeline project performed at IRONHACK Data Analysis Bootcamp.

This pipeline completes data acquisition, wrangling, analysis and reporting tasks to process information about the vote 
intention concerning the Basic Income issue on a poll carried out around the European Union. 

This is a MVP and not all data correspond to reality.

![Image](https://www.globalbusinessoutlook.com/wp-content/uploads/2017/06/Universal-Basic-Income-810x456.jpg)

---
#### **Usage**
Pipeline is launched through main_script.py giving as paramenters:
- `-c / --country` - an European country.
- `-p / --path`    - raw database path.
- `-e / --email`   - PDF report receiver via email.
- `-hs / --hashtag` - hashtag about Basic Income based on language - Text, location, date/time) **beta**.

Example:
`python main_script.py -p ./data/raw/raw_data_project_m1.db -e pvillamanario@gmail.com -c United_Kingdom -hs basicincome`


### **Inputs**

- Raw database containing poll data.
- API calls to retrieve job titles according to ID.
- Web scraping to get country names from country codes.

---
### **Processing stages**

#### **Acquisition**

- [Data base](https://github.com/Pvillamanario/basic_income_EU_analysis/blob/master/data/raw/raw_data_project_m1.db) connection throuhg SQLAlchemy.
- Data base data retrieved with pandas.
- Job titles obtained with an [API](http://dataatwork.org/data/) call.
- Country codes info got from [EuroStat](https://ec.europa.eu/eurostat/statistics-explained/index.php/Glossary:Country_codes) with requests and ReGex.

#### **Wrangling**
- Data combined, cleaned and normalized with pandas.
- Clean .csv as output.
  
#### **Analysis**
As requested, given one country or all of them, three .csv output containing:
- Country, gender, job, number of people surveyed and % referred to total.
- Vote intention and number of pro and against arguments.
- Top jobs by quantity according to education level.
  
#### **Reporting**
With the previous analysis performed:
- Charts generated for each of the analysis with seaborn.
- Charts grouped as PDF file using PIL.
- Report sent as attachment to de email address passed as  with SMTP lib.
- \#BasicIncome tweets with text, location and date/time. 

  
---
### **:To be completed...:**
- Passing a selection of countries as arguments.
- Refactor and improve (a lot) file management, titles, country filter...
- ~~Improve~~ Re do the charts so they can be shown to the world...
---

