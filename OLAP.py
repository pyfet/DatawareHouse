
import pandas as pd
import numpy as np
import random as rd
import os

# Setup the dimension table

data1 = {"key":["CA", "NY", "WA", "ON", "QU"],
        "name":["California", "new York", "Washington", "Ontario", "Quebec"],
        "country":["USA", "USA", "USA", "Canada", "Canada"]}
state_table = pd.DataFrame(data1)


data2 = {"key":range(1,13),
         "desc":["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
         "quarter":["Q1","Q1","Q1","Q2","Q2","Q2","Q3","Q3","Q3","Q4","Q4","Q4"]}
month_table = pd.DataFrame(data2)


data3 = {"key":["Printer", "Tablet", "Laptop"],
         "price":[225, 570, 1120]}
prod_table = pd.DataFrame(data3)


# Function to generate the Sales table
def gen_sales(no_of_recs):
    # Generate transaction data randomly
    loc = rd.choices(state_table.key,weights = [2, 2, 1, 1, 1],k=no_of_recs)
    time_month = rd.choices(month_table.key,k=no_of_recs)
    time_year = rd.choices([2018,2019],k=no_of_recs)
    prod = rd.choices(prod_table.key,k= no_of_recs,weights = [1, 3, 2])
    unit = rd.choices([1,2],k=no_of_recs,weights = [10, 3])
    
    sales = pd.DataFrame({'month':time_month,
                      'year':time_year,
                      'location':loc,
                      'product':prod,
                      'unit':unit
                         }
                      )
    
      # Sort the records by time order
    sales = sales.sort_values(by = ['year','month'])
    return(sales)


sales_fact = gen_sales(500)
sales_fact["value"] = 1
sales_fact['quarter'] = 1
sales_fact['country'] = 1


def amount(cols):
    value = cols[0]
    product = cols[1]
    while value == 1:
        if  product == "Tablet":
            return 570
        elif product == "Printer":
            return 225
        else:
            return 1120
        
def quarter(cols):
    quarter = cols[0]
    month = cols[1]
    while quarter == 1:
        if  month <= 3:
            return 'Q1'
        elif month <= 6:
            return 'Q2'
        elif month <= 9:
            return 'Q3'
        else:
            return 'Q4' 

def country(cols):
    country = cols[0]
    location = cols[1]
    while country == 1:
        if  location == "CA":
            return 'USA'
        elif location == "NY":
            return 'USA'
        elif location == "WA":
            return 'USA'
        elif location == "ON":
            return 'Canada'
        else:
            return 'Canada'        


sales_fact["quarter"] = sales_fact[['quarter','month']].apply(quarter,axis=1)
sales_fact["country"] = sales_fact[['country','location']].apply(country,axis=1)


sales_fact["value"] = sales_fact[['value','product']].apply(amount,axis=1)
sales_fact['amount'] = sales_fact["value"]*sales_fact['unit']


sales_fact.to_csv('sales.csv')
sale = os.path.abspath("sales.csv")
revenue =  pd.read_csv(sale)


revenue.drop(['Unnamed: 0','unit','value'],axis=1,inplace=True)


revenue = revenue[['month', 'quarter','year','location','country','product','amount']]


print("Wecome To Operation of OLAP \n")
print('Data present in the databse\n')
print(revenue)

play = True

while play:
    olap = str(input("Which operation would you like to perform? \n1)rollup\n2)dice\n3)slice\n4)drilldown\n5)pivot\n")).lower()
    if olap in ['dice','rollup','slice','drilldown','pivot']:
        print("Looks like you selected {}.".format(olap))
        
        '''
        "Dice" is about limited each dimension to a certain range of values, 
        while keeping the number of dimensions the same in the resulting cube. 
        For example, we can focus in sales happening in [Jan/ Feb/Mar, Laptop/Tablet, CA/NY].
        '''
        if olap == 'dice':
            dc = revenue[(revenue['year'] ==2018) & (revenue['location'] == 'CA') & 
                    ((revenue['product'] =='Laptop') | (revenue['product']=='Tablet')) &
                    ((revenue['month']==1) | (revenue['month']==2) | (revenue['month']==3))]
            print(dc.groupby(['year','product','month']).sum())

        '''
        "Rollup" is about applying an aggregation function to collapse a number of dimensions.
        For example, we want to focus in the annual revenue for each product and collapse 
        the location dimension (ie: we don't care where we sold our product). 
        '''
        elif olap == 'rollup':
            print(revenue.groupby(['year','product']).sum())

        '''
        "Slice" is about fixing certain dimensions to analyze the remaining dimensions.
        For example, we can focus in the sales happening in "2019", "Feb", 
        or we can focus in the sales happening in "2019", "Jan", "Tablet".
        '''
        elif olap == 'slice':
            print(revenue[(revenue['year'] ==2019) & (revenue['month'] == 2)].head())

        '''
        "Drilldown" is the reverse of "rollup" and applying an aggregation function to a finer level of granularity.
        For example, we want to focus in the annual and monthly revenue for each product 
        and collapse the location dimension (ie: we don't care where we sold our product).
        '''
        elif olap == 'drilldown':
            revenues = revenue[revenue['product'] == 'Laptop']
            print(revenues.groupby(['year','month']).sum())

        '''
        "Pivot" is about analyzing the combination of a pair of selected dimensions.
        For example, we want to analyze the revenue by year and month.
        Or we want to analyze the revenue by product and location.
        '''
        elif olap == 'pivot':
            print(revenue.pivot_table(index='year',columns='month',values='amount'))
        
        flag = str(input("Do you wish to continue [y|N] > "))

        if flag.lower == 'y':
            continue
        else:
            play = False

    else:
        print('Please enter a valid operation')
