# MagicFormula
Python function for simply and quickly getting stocks off of the MagicFormulaInvesting website.


### 1) The purpose of the MagicFormula function:

The purpose of the MagicFormula function is to automatically retrieve the list of “magic formula” stocks off of the website: www.magicformulainvesting.com.


### 2) How it works:

The way the function works is by scraping page results after sending a post request (using the login information of a user’s personal account) to the Magic Formula website. It is dependent on the following four packages:
pandas
datetime
BeautifulSoup
requests


### 3)  How it is used:

df, filepath = get_stocks(self, email, password, minMarketCap=100, stocksNum=30)

The function requires a few parameters to begin scraping. It generally works smoothly and very quickly except if there are random internet-related or server-side-related issues that might cause a delay or an exception to be raised. The function returns a pandas dataframe and a path to the dataframe saved as a CSV file.


email: The email you use to log into www.magicformulainvesting.com entered as a string.


password: The website password you use to log into www.magicformulainvesting.com entered as a string.


minMarketCap: The minimum market capitalization of companies to be considered. By default, this value is 100, but any integer value may be used.


stocksNum: The number of output stocks in the dataframe, which is either 30 (the default value), or 50 (if any other number is entered).
