from flask import Flask, render_template
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from bs4 import BeautifulSoup 
import requests
import datetime as dt
import numpy as np
import warnings
import re
warnings.filterwarnings("ignore")
from pandas.tseries.offsets import Day



#don't change this
matplotlib.use('Agg')
app = Flask(__name__) #do not change this


#initiating a tuple
temp = [] 

## using for statement for looping to get data from 1 to 15 pages in kalibrr
for page in range(1, 15):
    i=0
    # requesting data from kalibrr
    url_get = requests.get('https://www.kalibrr.id/id-ID/job-board/te/data/'+str(page))
    soup = BeautifulSoup(url_get.content,"html.parser")
    table = soup.find('div', attrs={'class':'k-border-b k-border-t k-border-tertiary-ghost-color md:k-border md:k-overflow-hidden md:k-rounded-lg'})
    
    # find length total data
    row = table.find_all('a', attrs={'class':'k-text-primary-color'})
    row_length = len(row)
    
	#Looping scraping data from row_lenght
    for i in range(0, row_length):
    
        #Get Job_title
        job_title=table.find_all('a', attrs={'class':'k-text-primary-color'})[i].text
        job_title = job_title.strip() #remove blank space
        
        #get Location
        location= table.find_all('a', attrs={'class':'k-text-subdued k-block'})[i].text
        location = location.strip() #remove blank space
        
        #get Company
        Company = table.find_all('span', attrs={'class':'k-inline-flex k-items-center k-mb-1'})[i].text 
        Company = Company.strip() #remove blank space      
        
        #Period
        Period =table.find_all('span', attrs={'class':'k-block k-mb-1'})[i].text 
        Period = Period.strip() #remove blank space
        
    	#insert the scrapping process here
        temp.append((Company,job_title,location,Period)) 

temp = temp[::-1]

#change into dataframe
df = pd.DataFrame(temp,columns=('Company','Job Title','location','period'))

#insert data wrangling here


# seperate string ",indonesia"
df['location'] = df['location'].str.split(',').str[0]

# City standardization
df['location General'] = df['location']

df['location General'] = df['location General'].str.replace('Kota Jakarta Barat','Jakarta')
df['location General'] = df['location General'].str.replace('Jakarta Selatan','Jakarta')
df['location General'] = df['location General'].str.replace('Tangerang Selatan','Tangerang')
df['location General'] = df['location General'].str.replace('Jakarta Pusat','Jakarta')
df['location General'] = df['location General'].str.replace('Central Jakarta City','Jakarta')
df['location General'] = df['location General'].str.replace('Jakarta Utara','Jakarta')
df['location General'] = df['location General'].str.replace('Jakarta Barat','Jakarta')
df['location General'] = df['location General'].str.replace('Kota Jakarta Pusat','Jakarta')
df['location General'] = df['location General'].str.replace('Bandung Kota','Bandung')
df['location General'] = df['location General'].str.replace('Bandung Kabupaten','Bandung')
df['location General'] = df['location General'].str.replace('Jakarta Timur','Jakarta')
df['location General'] = df['location General'].str.replace('Kota Jakarta Selatan','Jakarta')
df['location General'] = df['location General'].str.replace('Tangerang Selatan','Tangerang')
df['location General'] = df['location General'].str.replace('Tangerang Kota','Tangerang')
df['location General'] = df['location General'].str.replace('Kota Central Jakarta','Jakarta')
df['location General'] = df['location General'].str.replace('Kota South Jakarta','Jakarta')
df['location General'] = df['location General'].str.replace('South Tangerang','Tangerang')
df['location General'] = df['location General'].str.replace('West Jakarta','Jakarta')
df['location General'] = df['location General'].str.replace('Central Jakarta','Jakarta')
df['location General'] = df['location General'].str.replace('North Jakarta','Jakarta')
df['location General'] = df['location General'].str.replace('South Jakarta','Jakarta')
df['location General'] = df['location General'].str.replace('East Jakarta','Jakarta')
df['location General'] = df['location General'].str.replace('Kota Jakarta','Jakarta')

# Jakarta City standardization
df['location'] = df['location'].str.replace('Kota Jakarta Barat','Jakarta Barat')
df['location'] = df['location'].str.replace('Jakarta Selatan','Jakarta Selatan')
df['location'] = df['location'].str.replace('Tangerang Selatan','Tangerang Selatan')
df['location'] = df['location'].str.replace('Jakarta Pusat','Jakarta Pusat')
df['location'] = df['location'].str.replace('Central Jakarta City','Jakarta Pusat')
df['location'] = df['location'].str.replace('Jakarta Utara','Jakarta Utara')
df['location'] = df['location'].str.replace('Jakarta Barat','Jakarta Barat')
df['location'] = df['location'].str.replace('Kota Jakarta Pusat','Jakarta Pusat')
df['location'] = df['location'].str.replace('Bandung Kota','Bandung')
df['location'] = df['location'].str.replace('Bandung Kabupaten','Bandung')
df['location'] = df['location'].str.replace('Jakarta Timur','Jakarta Timur')
df['location'] = df['location'].str.replace('Kota Jakarta Selatan','Jakarta Selatan')
df['location'] = df['location'].str.replace('Tangerang Selatan','Tangerang')
df['location'] = df['location'].str.replace('Tangerang Kota','Tangerang')
df['location'] = df['location'].str.replace('Kota Central Jakarta','Jakarta Pusat')
df['location'] = df['location'].str.replace('Kota South Jakarta','Jakarta Selatan')
df['location'] = df['location'].str.replace('South Tangerang','Tangerang')
df['location'] = df['location'].str.replace('West Jakarta','Jakarta Barat')
df['location'] = df['location'].str.replace('Central Jakarta','Jakarta Pusat')
df['location'] = df['location'].str.replace('North Jakarta','Jakarta Utara')
df['location'] = df['location'].str.replace('South Jakarta','Jakarta Selatan')
df['location'] = df['location'].str.replace('East Jakarta','Jakarta Timur')
df['location'] = df['location'].str.replace('Kota Jakarta','Jakarta Pusat')

#Replace word Jakarta to Jakarta Pusat in columns Location
df.loc[df['location']=='Jakarta','location']='Jakarta Pusat'

# Separate data between Date Post job and date deadline Apply Job
df['period_posted'] = df['period'].str.split('•').str[0]
df['period'] = df['period'].str.split('•').str[1]

# Take only number from columns PostedDay
df['PostedDay']=df['period_posted'].str.extract('(\d+)')

#Create new columns value_is_NaN to see data NAN base on PostDay Columns
df.loc[df['PostedDay'].isnull(),'value_is_NaN'] = 'Yes'

#Create new 2 datafame to separate value_is_NaN

df1 = df[df['value_is_NaN']!='Yes']
df2 = df[df['value_is_NaN']=='Yes']

#change type of PostedDay to INT in df1
df1['PostedDay'] = df1['PostedDay'].astype('int')

#convert month to days in df1
df1.loc[df['period_posted'].str.contains("months"),'PostedDay']=df1['PostedDay']*30

#converts days to date in df1
df1['PostedDate']=pd.to_datetime(dt.datetime.today().strftime('%Y-%m-%d'))
df1['PostedDate'] = df1['PostedDate'] - pd.to_timedelta(df1['PostedDay'], unit='D')


#convert PostedDate to datetime in df2
df2['PostedDate']=pd.to_datetime(dt.datetime.today().strftime('%Y-%m-%d'))

#fill na with 30 days (NA data is a month data) in df2
df2['PostedDay'].fillna(value=30, inplace=True)
df2['PostedDate'] = df2['PostedDate'] - pd.to_timedelta(df2['PostedDay'], unit='D')

#merge dataframe from df1 and df2
df_merged = pd.concat([df1, df2], ignore_index=True, sort=False)

#Create New DataFrame Test for Period (deadline submit application) and do the replace string to get date data
test = pd.DataFrame(df['period'].str.replace('Apply before','')+' 2023')

#remove blank space in columns Test.Period
test = test['period'].str.strip()

#create new columns in dataframe df_merge after format to datetime in columns Test.Period
df_merged['period apply before']=pd.to_datetime(test,dayfirst=True,format='mixed')

#change type dataframe
df_merged['location'] = df_merged['location'].astype('category')
df_merged['location General'] = df_merged['location General'].astype('category')

#save data to csv
df_merged.to_csv('capstone_olah_data.csv',index=False)

#Summarize data from General location

Job_pivot_table=df_merged.pivot_table(
    index = 'location General',
    values='Job Title',
    aggfunc='count'
).sort_values(by='Job Title',ascending=True)

#end of data wranggling 

@app.route("/")
def index(): 
	
	card_data = f'{Job_pivot_table["Job Title"].mean().round(2)}' #be careful with the " and ' 

	# generate plot
	ax = Job_pivot_table.plot(kind='bar',
                    rot=0,
                                 figsize=(16, 14),
                                 ylabel='Count Job Request',
                                 xlabel='Location');
	ax.legend(["Count"])
	ax.bar_label(ax.containers[0])
	
	# Rendering plot
	# Do not change this
	figfile = BytesIO()
	plt.savefig(figfile, format='png', transparent=True)
	figfile.seek(0)
	figdata_png = base64.b64encode(figfile.getvalue())
	plot_result = str(figdata_png)[2:-1]

	# render to html
	return render_template('index.html',
		card_data = card_data, 
		plot_result=plot_result
		)


if __name__ == "__main__": 
    app.run(debug=True)