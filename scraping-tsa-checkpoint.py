# Import libraries to be used
import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL of the page that we want to scrape
url = "https://www.tsa.gov/coronavirus/passenger-throughput"

# Send a request to the server to retrieve the page's html
r = requests.get(url)

soup = BeautifulSoup(r.text, 'html.parser')

# Isolate the table containing daily checkpoint travel count
table = soup.find('table')

''' IF USING ORIGINAL TABLE HEADINGS

# Create an empty list to store the column headings
    headings = []

# Loop through the table headings and add each to the list
    for th in table.find_all('th'):
        label = th.text.strip()
        headings.append(label)
'''
# Set desired headings
headings = ['Month', 'Day', '2021', '2020', '2019']

# Create a pandas dataframe with the headings as column labels
df = pd.DataFrame(columns = headings)

# Loop through the table rows
for tr in table.find_all('tr')[1:]:
        # Retrieve the table data
        data = tr.find_all('td')
        cells = [i.text.strip() for i in data]

        # Parse date column to separate month and day
        separated = cells[0].split("/")
        cells.insert(0, separated[0])
        cells[1] = separated[1]
        # Discard year

        # Return number of rows in data frame
        length = len(df)
        # Store the table data in new row in the data frame
        df.loc[length] = cells

# Export dataframe as csv file
df.to_csv('tsa_checkpoint_data.csv')