"""
can I make a function which the ai will happily use??


OK THIS DIDN'T WORK

but i have a good idea
we can give the AI functions for
"pull more data with sql",
or "sollicit feedback""

"""

import seaborn as sns
import matplotlib.pyplot as plt
import pandas_datareader as pdr
from datetime import datetime, timedelta

from datetime import datetime, timedelta


def plot_stock_analysis(ticker: str, days: int = 365):
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)

    # Fetch stock data
    df = pdr.get_data_yahoo(ticker, start=start_date, end=end_date)

    # Create the plot
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10), sharex=True)

    # Plot stock price
    sns.lineplot(data=df, x=df.index, y="Close", ax=ax1)
    ax1.set_title(f"{ticker} Stock Price and Volume Analysis")
    ax1.set_ylabel("Stock Price")

    # Plot volume with color based on price change
    volume_colors = [
        "g" if close > open else "r" for close, open in zip(df["Close"], df["Open"])
    ]
    sns.barplot(x=df.index, y=df["Volume"], palette=volume_colors, ax=ax2)
    ax2.set_ylabel("Volume")

    plt.tight_layout()
    return fig


# plot_stock_analysis("AAPL")
plot_stock_analysis("TSLA")
