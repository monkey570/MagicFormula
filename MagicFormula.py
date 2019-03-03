'''
MIT License

Copyright (c) 2018 Kadri Mufti

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.


'''

import pandas as pd
import datetime
from bs4 import BeautifulSoup
import requests
from tqdm import tqdm
import sys
import argparse
import re
import os

class MagicFormula:

    def __init__(self):
        self.desc = "Class is MagicFormula for stocks data retrieval from the MagicFormula website."

    def get_stocks(self, email, password, minMarketCap=100, stocksNum=50, compression=None):
        ##############################
        #### magicformula website ####
        ##############################

        try:
            # to login into page
            s = requests.Session()
            url1 = "https://www.magicformulainvesting.com/Account/LogOn"
            login_data = {"Email": email, "Password": password, "login": "Login"}
            r1 = s.post(url1, data=login_data, headers={"Referer": "https://www.magicformulainvesting.com/"})
            # Get the stocks data
            url2 = "https://www.magicformulainvesting.com/Screening/StockScreening"
            if stocksNum < 50:
                select30 = "true"
                total = 30
            else:
                select30 = "false"
                total = 50
            payload = {"MinimumMarketCap": minMarketCap, "Select30": select30, "stocks": "Get+Stocks"}
            r2 = s.post(url2, data=payload)
            soup = BeautifulSoup(r2.text, "html.parser")
            try:
                results = soup.find("div", {"id": "report"}).find("tbody").find_all("tr")
                chk = 0
            except:
                print('Email and Password combination failed. Please check both for correctness.')
                chk = 1
                sys.exit(1)
            numrows = len(results)

            # create dataframe with initial data out of magicformula website
            df = pd.DataFrame(index=range(numrows),
                              columns=list(['Company Name',         # 0
                                            'Ticker',               # 1
                                            'Market Cap ($Mlns)',   # 2
                                            'Price From',           # 3
                                            'Most Recent Quarter Data']))  # 4
            j = 0
            t = tqdm(total=total)
            for item in results:
               i = 0
               name = item.find_all("td")
               while i < len(name):
                   df.iloc[[j], [i]] = name[i].text
                   i += 1
               j += 1
               t.update()
            t.close()
            print("No errors encountered.")
        except:
            if chk == 0:
                print("Unknown problem encountered: could be internet or server-side issue. Please try again later.")
            sys.exit(1)

        ##########################################
        ### Saving the dataframe to a csv file ###
        ##########################################

        now = datetime.datetime.now()
        dateversion = now.strftime("%Y-%m-%d")
        if not os.path.exists(str(dateversion)):
            os.mkdir(str(dateversion))
        filename = str(dateversion)+'\MagicFormulaStocks_MarketCap' + str(minMarketCap) + '_' + str(dateversion) + '.csv'
        df.to_csv(path_or_buf=filename, mode='w+', compression=compression)
        print("MagicFormula stocks data retrieval complete.")
        return df, filename


def main():
    parser = argparse.ArgumentParser(description="Stocks data retrieval from the MagicFormula website.")
    parser.add_argument("-mcap", "--minMarketCap", type=int, default=100, help="minimum market capitalization")
    parser.add_argument("-sn", "--stocksNum", type=int, default=50,
                       help="number of stocks to retrieve (either 30 or 50)")
    parser.add_argument("-cm", "--compression", default=None, help="compression type when saving to CSV")
    parser.add_argument("email", help="login email")
    parser.add_argument("password", help="login password")
    args = parser.parse_args()
    # Check for email and password entered
    if re.fullmatch(r'(^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$)', args.email, re.IGNORECASE) == None:
        raise Exception('Email format is invalid.')

    MF = MagicFormula()
    MF.get_stocks(args.email, args.password, args.minMarketCap, args.stocksNum, args.compression)


if __name__ == '__main__':
    print('Running MagicFormula')
    main()