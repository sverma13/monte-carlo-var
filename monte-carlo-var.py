# Data analysis libraries
import pandas as pd
import numpy as np

# Data visualization library
import matplotlib.pyplot as plt


# Function: Compute a stock's VaR, CVar, and Monte Carlo VaR
def stock_analysis(ticker):

    # Load data in pandas dataframe
    ticker_file = ticker + '.csv'
    data = pd.read_csv(ticker_file, parse_dates=['Date'])
    data = data.sort_values(by='Date')
    data.set_index('Date', inplace=True)

    data['Returns'] = data['Adj Close'].pct_change()  # Create daily returns column
    returns = data['Returns'].dropna()  # Remove values of N/A

    # Compute statistical data
    avg_daily_return = np.mean(returns)
    std_dev = np.std(returns)

    # Calculate VaR 95 and CVaR 95
    var95 = np.percentile(returns, 5)
    print('var:', var95)
    cvar95 = returns[returns <= var95].mean()
    print('cvar:', cvar95)
    
    # Calculate drawdown and plot figures
    cum_rets_dollars = data['Adj Close']
    print('cum_rets:')
    print(cum_rets_dollars)

    running_max = cum_rets_dollars.cummax()
    print('running_max:')
    print(running_max)

    drawdown = (cum_rets_dollars) / running_max - 1
    print('drawdown:')
    print(drawdown)

    plt.figure(figsize=(8, 7))
    plt.subplot(2,1,1)
    plt.plot(cum_rets_dollars)
    plt.title('Cumulative Returns')
    plt.subplot(2,1,2)
    plt.plot(running_max)
    plt.title('Running Max')
    plt.show()
    
    plt.figure()
    plt.plot(drawdown)
    plt.title('Drawdown')
    plt.show()

    T = 252  # Time period
    S0 = 1  # Starting stock price
    #S0 = cum_rets_dollars.iloc[-1]  # use this line to have the Monte Carlo simulation start at the most recent stock price
    NUM_SIM = 1000  # Number of Monte Carlo simulations
    for i in range(NUM_SIM):
        rand_rets = np.random.normal(avg_daily_return, std_dev, T)  # Generate a random daily stock return using the stock's historical statistical data

        # Create cumulative returns data
        cum_rets = rand_rets + 1
        forecast = S0 * (cum_rets.cumprod())

        # Plot the Monte Carlo simulations over time
        plt.plot(forecast)
        plt.title('Monte Carlo Simulation - Stock Price Over Time')
        plt.xlabel('Time (Days)')
        plt.ylabel('Stock Price (Percent of initial stock price)')

    # Calculate Monte Carlo VaR from the simulations
    var = np.percentile(rand_rets, 5)
    print('Monte Carlo var:', var)
    plt.show()
    
    # Create a histogram of daily stock returns
    plt.hist(returns, bins=25)
    plt.title('Daily Returns Frequency Over %d Days' % T)
    plt.xlabel('Daily Returns (Percent)')
    plt.ylabel('Frequency')
    plt.axvline(x=var95, color='green')  # plot the historical VaR on the histogram
    plt.axvline(x=cvar95, color='red')  # plot the historical CVar on the histogram
    plt.axvline(x=var, color='black', linewidth=2)  # plot the Monte Carlo VaR on the histogram
    plt.show()

    return var  # return the Monte Carlo Var


monte_carlo_var = stock_analysis('TSLA')
