import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import linregress

def draw_plot():
    df = pd.read_csv('epa-sea-level.csv')

    plt.figure(figsize=(10, 6))
    plt.scatter(df['Year'], df['CSIRO Adjusted Sea Level'], label='Original Data', alpha=0.5)

    reg1 = linregress(df['Year'], df['CSIRO Adjusted Sea Level'])

    x1 = pd.Series([i for i in range(1880, 2051)])
    y1 = reg1.slope * x1 + reg1.intercept
    plt.plot(x1, y1, 'r', label='Best Fit Line 1 (1880-2050)')

    df_recent = df[df['Year'] >= 2000]
    reg2 = linregress(df_recent['Year'], df_recent['CSIRO Adjusted Sea Level'])

    x2 = pd.Series([i for i in range(2000, 2051)])
    y2 = reg2.slope * x2 + reg2.intercept
    plt.plot(x2, y2, 'green', label='Best Fit Line 2 (2000-2050)')

    plt.xlabel('Year')
    plt.ylabel('Sea Level (inches)')
    plt.title('Rise in Sea Level')
    plt.legend()

    plt.savefig('sea_level_plot.png')
    return plt.gca()
