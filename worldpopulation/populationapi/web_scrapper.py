import requests
from bs4 import BeautifulSoup
import re
"""
Three endpoints: data by year(historical), forecast data(based on year), data by city
sample_data - 
    data by year(historical) -

    {'Population of India (2020 and historical)': [{'year':'2020','':''},{'2019':'','':''}]

"""
#import pdb;pdb.set_trace()
base_url='https://www.worldometers.info/world-population/'

#table_headings = ('','','','')

def get_url(endpoint):
    endpoint = '{}-population'.format(endpoint.lower())
    url = base_url + endpoint + '/'
    return url

def get_data(table_number, requested_country):
    """
    Example data returned: [{'Year': '2020', 'Population': '1,380,004,385', 'Yearly %  Change': '0.99 %', 'Yearly Change': '13,586,631', 'Migrants (net)': '-532,687', 'Median Age': '28.4', 'Fertility Rate': '2.24', 'Density (P/Km²)': '464', 'Urban Pop %': '35.0 %', 'Urban Population': '483,098,640', "Country's Share of World Pop": '17.70 %', 'World Population': '7,794,798,739', 'IndiaGlobal Rank': '2'}, 
    {'Year': '2019', 'Population': '1,366,417,754', 'Yearly %  Change': '1.02 %', 'Yearly Change': '13,775,474', 'Migrants (net)': '-532,687', 'Median Age': '27.1', 'Fertility Rate': '2.36', 'Density (P/Km²)': '460', 'Urban Pop %': '34.5 %', 'Urban Population': '471,828,295', "Country's Share of World Pop": '17.71 %', 'World Population': '7,713,468,100', 'IndiaGlobal Rank': '2'}]
    """

    url = get_url(requested_country)
    #import pdb;pdb.set_trace()

    response = requests.get(url)
    soup=BeautifulSoup(re.sub("<!--|-->","", response.text), 'html.parser')

    tables_in_page = [table for table in soup.find_all("table")]

    required_table = tables_in_page[table_number]

    #table_headings = [ heading.get_text() for heading in soup.find_all('h2')]

    headers = [header.get_text() for header in required_table.find('thead').find_all('th')]

    data_list = []    
    for row in required_table.find('tbody').find_all('tr'):
        data = [data.get_text() for data in row.find_all('td')]
        #print(data)
        data_dict = dict(zip(headers,data))
        data_list.append(data_dict)

    return data_list   



#print(get_data(3,'india'))