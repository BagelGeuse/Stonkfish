function createStockHTML(ticker) {
    return `
    <label>${ticker}</label> <br>
    <label> Percentage: ${stockdata.parsedData[ticker]["percentage"]} </label><br>
    <label> 10 Day: ${stockdata.parsedData[ticker]["10dayPrices"].join(", ")} </label>

    <br><br>
    `
}

for(let i in stockdata["tickers"]) {

    document.getElementById("stuff").innerHTML += createStockHTML(stockdata["tickers"][i])
}
