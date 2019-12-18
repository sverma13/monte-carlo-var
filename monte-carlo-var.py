# Data analysis libraries
import pandas as pd
import numpy as np

# Data visualization library
import matplotlib.pyplot as plt

# Function: Compute a stock's VaR, CVar, and Monte Carlo VaR
def stockAnalysis(ticker):

    # Load data in pandas dataframe
    tickerFile = ticker + '.csv'
    data = pd.read_csv(tickerFile, parse_dates=['Date'])
    data = data.sort_values(by='Date')
    data.set_index('Date', inplace=True)

    data['Returns'] = data['Adj Close'].pct_change() # Create daily returns column
    returns = data['Returns'].dropna() # Remove values of N/A

    # Compute statistical data
    avgDailyReturn = np.mean(returns)
    stdDev = np.std(returns)

    # Calculate VaR 95 and CVaR 95
    var95 = np.percentile(returns, 5)
    print('var:', var95)
    cvar95 = returns[returns <= var95].mean()
    print('cvar:', cvar95)

    T = 252 # Time period
    S0 = 1 # Starting stock price
    numSim = 1000 # Number of Monte Carlo simulations
    for i in range(numSim):
        randRets = np.random.normal(avgDailyReturn, stdDev, T) # Generate a random daily stock return using the stock's historical statistical data
        
        # Create cumulative returns data
        cumRets = randRets + 1
        forecast = S0 * (cumRets.cumprod())

        # Plot the Monte Carlo simulations over time
        plt.plot(forecast)
        plt.title('Monte Carlo Simulation - Stock Price Over Time')
        plt.xlabel('Time (Days)')
        plt.ylabel('Stock Price (Percent of initial stock price)')

    # Calculate Monte Carlo VaR from the simulations
    var = np.percentile(randRets, 5)
    print('Monte Carlo var:', var)
    plt.show()
    
    # Create a histogram of daily stock returns
    plt.hist(returns, bins=25)
    plt.title('Daily Returns Frequency Over %d Days' % T)
    plt.xlabel('Daily Returns (Percent)')
    plt.ylabel('Frequency')
    plt.axvline(x=var95, color='green') # plot the historical VaR on the histogram
    plt.axvline(x=cvar95, color='red') # plot the historical CVar on the histogram
    plt.axvline(x=var, color='black', linewidth=2) # plot the Monte Carlo VaR on the histogram
    plt.show()

    return var # return the Monte Carlo Var

monteCarloVar = stockAnalysis('AMZN')