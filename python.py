import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


base_path = '/Users/freddiekiessling/Desktop/Data_Science/PSTAT_277B/ZM1_ZL1_ZS1'

def load_and_process_soybean_data(base_path):

    # File paths for each commodity and frequency
    oil_day_path = f'{base_path}/CBOT_DL_ZL1!, 1D.csv'
    oil_min_path = f'{base_path}/CBOT_DL_ZL1!, 1.csv'
    oil_sec_path = f'{base_path}/CBOT_DL_ZL1!, 1S.csv'

    meal_day_path = f'{base_path}/CBOT_DL_ZM1!, 1D.csv'
    meal_min_path = f'{base_path}/CBOT_DL_ZM1!, 1.csv'
    meal_sec_path = f'{base_path}/CBOT_DL_ZM1!, 1S.csv'

    soybeans_day_path = f'{base_path}/CBOT_DL_ZS1!, 1D.csv'
    soybeans_min_path = f'{base_path}/CBOT_DL_ZS1!, 1.csv'
    soybeans_sec_path = f'{base_path}/CBOT_DL_ZS1!, 1S.csv'

    # Soybean Oil
    soy_oil_day = pd.read_csv(oil_day_path)
    soy_oil_min = pd.read_csv(oil_min_path)
    soy_oil_sec = pd.read_csv(oil_sec_path)

    # Soybean Meal
    soy_meal_day = pd.read_csv(meal_day_path)
    soy_meal_min = pd.read_csv(meal_min_path)
    soy_meal_sec = pd.read_csv(meal_sec_path)

    # Soybeans
    soy_beans_day = pd.read_csv(soybeans_day_path)
    soy_beans_min = pd.read_csv(soybeans_min_path)
    soy_beans_sec = pd.read_csv(soybeans_sec_path)

    for df in [soy_oil_day, soy_oil_min, soy_oil_sec, soy_meal_day, soy_meal_min, soy_meal_sec, soy_beans_day, soy_beans_min, soy_beans_sec]:
        df['time'] = pd.to_datetime(df['time'], unit='s')

    return soy_oil_day, soy_oil_min, soy_oil_sec, soy_meal_day, soy_meal_min, soy_meal_sec, soy_beans_day, soy_beans_min, soy_beans_sec



def crush_spread_calculations_per_data_time(soy_beans_day, soy_meal_day, soy_oil_day,
                                          soy_beans_min, soy_meal_min, soy_oil_min,
                                          soy_beans_sec, soy_meal_sec, soy_oil_sec):
    """
    Calculate crush spreads for daily, minute, and second data.
    
    Returns:
    tuple: (crush_spread_day, crush_spread_min, crush_spread_sec)
    """
    # For daily data
    crush_spread_day = pd.DataFrame({
        'time': soy_beans_day['time'],
        'crush_spread': calculate_crush_spread(
            soy_meal_day['close'],
            soy_oil_day['close'],
            soy_beans_day['close']
        )
    })

    # For minute data
    crush_spread_min = pd.DataFrame({
        'time': soy_beans_min['time'],
        'crush_spread': calculate_crush_spread(
            soy_meal_min['close'],
            soy_oil_min['close'],
            soy_beans_min['close']
        )
    })

    # For second data
    crush_spread_sec = pd.DataFrame({
        'time': soy_beans_sec['time'],
        'crush_spread': calculate_crush_spread(
            soy_meal_sec['close'],
            soy_oil_sec['close'],
            soy_beans_sec['close']
        )
    })

    # Set time as index for easier time series analysis
    crush_spread_day.set_index('time', inplace=True)
    crush_spread_min.set_index('time', inplace=True)
    crush_spread_sec.set_index('time', inplace=True)
    
    return crush_spread_day, crush_spread_min, crush_spread_sec






def plot_commodity_timeseries(data_dict, commodity_name):
    fig, axes = plt.subplots(1, 3, figsize=(20, 5))
    fig.suptitle(f'{commodity_name} Price Time Series', fontsize=16)
    timeframes = ['sec', 'min', 'day']
    titles = ['Second Data', 'Minute Data', 'Daily Data']
    for ax, timeframe, title in zip(axes, timeframes, titles):
        data_dict[timeframe].plot(y='close', ax=ax)
        ax.set_title(title)
        ax.set_xlabel('Time')
        ax.set_ylabel('Price')
        ax.tick_params(axis='x', rotation=45)
    plt.tight_layout()
    plt.show()



def plot_crush_spreads(crush_spreads):
    fig, axes = plt.subplots(1, 3, figsize=(20, 5))
    fig.suptitle('Soybean Crush Spread Time Series', fontsize=16)
    timeframes = ['sec', 'min', 'day']
    titles = ['Second Data', 'Minute Data', 'Daily Data']
    
    for ax, timeframe, title in zip(axes, timeframes, titles):
        crush_spreads[timeframe]['crush_spread'].plot(ax=ax)
        ax.set_title(title)
        ax.set_xlabel('Time')
        ax.set_ylabel('Crush Spread')
        ax.tick_params(axis='x', rotation=45)
    
    plt.tight_layout()
    plt.show()






def plot_all_commodities(soy_oil_sec, soy_oil_min, soy_oil_day,
                        soy_meal_sec, soy_meal_min, soy_meal_day,
                        soy_beans_sec, soy_beans_min, soy_beans_day):
    """
    Plot time series for all commodities
    """
    # Plot individual commodities
    data = {
        'sec': soy_oil_sec,
        'min': soy_oil_min,
        'day': soy_oil_day
    }
    plot_commodity_timeseries(data, 'Soybean Oil')

    data = {
        'sec': soy_meal_sec,
        'min': soy_meal_min,
        'day': soy_meal_day
    }
    plot_commodity_timeseries(data, 'Soybean Meal')

    data = {
        'sec': soy_beans_sec,
        'min': soy_beans_min,
        'day': soy_beans_day
    }
    plot_commodity_timeseries(data, 'Soybeans')

    

def plot_all_crush_spreads(crush_spread_sec, crush_spread_min, crush_spread_day):
    """
    Plot all crush spreads
    """
    # Plot crush spreads
    crush_data = {
        'sec': crush_spread_sec,
        'min': crush_spread_min,
        'day': crush_spread_day
    }
    plot_crush_spreads(crush_data)























