import requests
import sys
import json
import os

import stockRequests as sr

def getTickerID(ticker):

    with open("./stockData.json", "r") as f:
        stockData = json.loads(f.read())
        return stockData["tickers"].index(ticker)

def getTickerFromID(id):
    with open("./stockData.json") as f:
        parsedData = json.loads(f.read())
        return parsedData["tickers"][id]

def getStockData(ticker):
    #Open the stockdata file
    with open("./stockData.json", "r") as f:
        stockData = json.loads(f.read())
        
        #lookup the ticker symbol in the json file and get the stock data for that ticker symbol
        newData = sr.requestHistory(ticker) 

        #slice off the first 490 elements and store it in the file
        stockData["apiData"][ticker] = newData[490:]

    #write the new data to the file
    with open("./stockData.json", "w") as f:
        f.truncate()
        f.write(json.dumps(stockData))

def compileForRScript(ticker):
    #All of the closing prices
    prices = []

    #Open and read the stocks closing prices
    with open("./stockData.json", "r") as f:
        stockData = json.loads(f.read())
        prices = stockData["apiData"][ticker]

    #turn it into a list of just the closing prices
    closingPrices = [report["close"] for report in prices]
    #reverse it, the R script likes the 0th index as 0 days ago
    closingPrices.reverse()
    #stringify it
    closingPrices = json.dumps(closingPrices)[1:-1].split(" ")
    #remove spaces
    closingPrices = "".join(closingPrices)+","

    #write it to the input file for the R script
    with open("R.test.txt", "w+") as f:
        f.truncate()
        f.write(closingPrices)
    
    #Run the r script
    os.system("Rscript Stonkphish_Script.R")

def storeResult(ticker):

    percentage = 0
    stockData = None

    with open("stockData.json", "r") as f:
        stockData = json.loads(f.read())

    with open("result.txt", "r") as f:
        percentage = f.read()

    tenDayPrices = [report["close"] for report in stockData["apiData"][ticker]]

    tenDayPrices.reverse()
    tenDayPrices = tenDayPrices[0:10]

    stockData["parsedData"][ticker] = {
        "percentage": percentage,
        "10dayPrices": tenDayPrices
    }    

    with open("stockData.json", "w+") as f:
        f.truncate
        f.write(json.dumps(stockData))

def displayStock(ticker):
    
    parsedData = None

    with open("stockData.json", "r") as f:
        parsedData = json.loads(f.read())["parsedData"][ticker]
    
    print(parsedData)



#allow for console debugging
if(__name__ == "__main__"):
    if(sys.argv[1] == "getTickerFromID"):
        print(getTickerFromID(int(sys.argv[2])))
    if(sys.argv[1] == "getIDFromTicker"):
        print(getTickerID(sys.argv[2]))
    if(sys.argv[1] == "getStockData"):
        getStockData(sys.argv[2])
    if(sys.argv[1] == "compileR"):
        compileForRScript(sys.argv[2])
    if(sys.argv[1] == "storeResult"):
        storeResult(sys.argv[2])
    if(sys.argv[1] == "displayStock"):
        displayStock(sys.argv[2])
    


# For testing this script:
# Input your api key into .env
# In the terminal, run 'python apilib.py <command> <stock>
# get followed by the index of the stock in the json file gets the latest stock data, compileR readies the stock for processing by the R script