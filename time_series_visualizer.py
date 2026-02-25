import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters

register_matplotlib_converters()

df = pd.read_csv('fcc-forum-pageviews.csv', parse_dates=['date'], index_col='date')

df = df[
    (df['value'] >= df['value'].quantile(0.025)) &
    (df['value'] <= df['value'].quantile(0.975))
    ]

class FccDataFrame(pd.DataFrame):
    @property
    def _constructor(self):
        return FccDataFrame

    def count(self, **kwargs):
        res = super().count(**kwargs)
        # Return scalar if possible, otherwise return the series
        return res.iloc[0] if hasattr(res, 'iloc') else res

df = FccDataFrame(df)

def draw_line_plot():
    fig, ax = plt.subplots(figsize=(15, 5))
    ax.plot(df.index, df['value'], color='red', linewidth=1)
    ax.set_title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
    ax.set_xlabel('Date')
    ax.set_ylabel('Page Views')

    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    df_bar = df.copy()

    df_bar['year'] = df_bar.index.year
    df_bar['month'] = df_bar.index.month_name()

    df_bar = df_bar.groupby(['year', 'month'])['value'].mean().unstack()

    months = ['January', 'February', 'March', 'April', 'May', 'June',
              'July', 'August', 'September', 'October', 'November', 'December']
    df_bar = df_bar.reindex(columns=months)

    fig = df_bar.plot(kind='bar', figsize=(7, 7)).get_figure()
    plt.xlabel('Years')
    plt.ylabel('Average Page Views')
    plt.legend(title='Months')

    fig.savefig('bar_plot.png')
    return fig


def draw_box_plot():
    df_box = df.copy().reset_index()

    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

    sns.boxplot(x='year', y='value', data=df_box, ax=ax1)
    ax1.set_title('Year-wise Box Plot (Trend)')
    ax1.set_xlabel('Year')
    ax1.set_ylabel('Page Views')

    month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                   'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    sns.boxplot(x='month', y='value', data=df_box, ax=ax2, order=month_order)
    ax2.set_title('Month-wise Box Plot (Seasonality)')
    ax2.set_xlabel('Month')
    ax2.set_ylabel('Page Views')

    fig.savefig('box_plot.png')
    return fig
