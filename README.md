# crypto_handbook_web
Web service built on Flask for getting information on different coins

This website is run locally and is set up using Flask. I wanted to create a more complex web service than the last one, and one that would actually be useful to me. I used the CoinGecko API to get the data for the cryptos. It's free and does not require any authorizations. I'm able to expand the range of supported coins out much more but I chose to only do the five most popular for simplicity. The homepage lets the user select a coin to get information on, and it redirects to the specific page. I wanted to do something cool with a graph, so I set one up for each coin using MatPlotLib, inputting historical data from CoinGecko. It tracks the price over the past 24 hours. 
