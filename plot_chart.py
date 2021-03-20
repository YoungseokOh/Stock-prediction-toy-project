import matplotlib.pyplot as plt
import mplfinance as fplt
from krx_wr_script import pykrx_read_csv
import pandas as pd
import matplotlib.ticker as mticker
import matplotlib.dates as mdates
from mplfinance.original_flavor import candlestick2_ohlc

def plot_technical_indicators(name, dataset, last_days):
    plt.rc('font', family='NanumGothic')
    dataset = dataset.iloc[-last_days:, :]

    # dataset = dataset.reset_index()
    dataset = dataset.set_index(dataset['date'])
    ax = plt.subplot2grid((6,4), (0,0), rowspan=4, colspan=4)
    ax.xaxis.set_major_locator(mticker.MaxNLocator(10))
    #ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))

    #ax.spines['bottom'].set_color("#5998ff")
    #ax.spines['top'].set_color("#5998ff")
    #ax.spines['left'].set_color("#5998ff")
    #ax.spines['right'].set_color("#5998ff")
    ax.yaxis.label.set_color("k")
    ax.tick_params(axis='y', colors='k')
    plt.gca().yaxis.set_major_locator(mticker.MaxNLocator(prune='upper'))
    ax.tick_params(axis='x', colors='w')
    x_ = list(dataset.index)
    x_range = []
    col_name = []
    for col_list in dataset.columns:
        if "ema" in col_list:
            col_name.append(col_list)
    for i in range(0, int(len(x_))):
        x_range.append(dataset['date'].iloc[i])
        #print(x_range)
    # Plot first subplot
    candlestick2_ohlc(ax, dataset['open'], dataset['high'], dataset['low'], dataset['close'], width=0.5, colorup='r', colordown='b')
    ax.plot(dataset['{}'.format(col_name[0])], label='{}'.format(col_name[0].upper()), color='g', linestyle='-.', linewidth=0.8)
    ax.plot(dataset['{}'.format(col_name[1])], label='{}'.format(col_name[1].upper()), color='r', linestyle='-.', linewidth=0.8)
    ax.plot(dataset['{}'.format(col_name[2])], label='{}'.format(col_name[2].upper()), color='b', linestyle='-.', linewidth=0.8)
    if 'upper_band' in dataset.columns:
        ax.plot(dataset['upper_band'], label='Upper Band', color='c', linewidth=0.5)
        ax.plot(dataset['lower_band'], label='Lower Band', color='c', linewidth=0.5)
        ax.fill_between(x_, dataset['lower_band'], dataset['upper_band'], alpha=0.25)
    plt.title('Technical indicators for {} - last {} days.'.format(name, last_days))
    plt.ylabel('KRW')
    #axv.ylabel('Volume')
    # plt.xticks(x_[::30], x_range[::30])
    # xlabels = ax.get_xticklabels()
    # ax.set_xticklabels(xlabels, rotation=45, fontsize=7)

    axv = plt.subplot2grid((6, 4), (4, 0), sharex=ax, rowspan=1, colspan=4)

    axv.xaxis.set_major_locator(mticker.MaxNLocator(10))
    #axv.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    #axv.plot(dataset['volume'], color='c', linewidth=0.5)
    axv.bar(range(len(dataset['volume'])), dataset['volume'], color='m', linewidth=0.5)

    plt.gca().yaxis.set_major_locator(mticker.MaxNLocator(prune='upper'))
    #axv.spines['bottom'].set_color("#5998ff")
    #axv.spines['top'].set_color("#5998ff")
    #axv.spines['left'].set_color("#5998ff")
    #axv.spines['right'].set_color("#5998ff")
    axv.tick_params(axis='x', colors='w')
    axv.tick_params(axis='y', colors='k')

    plt.ylabel('volume')
    axv.yaxis.set_major_locator(mticker.MaxNLocator(nbins=5, prune='upper'))

    axv1 = plt.subplot2grid((6, 4), (5, 0), sharex=ax, rowspan=1, colspan=4)
    axv1.xaxis.set_major_locator(mticker.MaxNLocator(10))
    #axv1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    axv1.plot(dataset['rsi'], color='c', linewidth=0.5)
    axv1.set_yticks([30, 50, 70])
    plt.ylabel('rsi')

    '''
    for label in axv.xaxis.get_ticklabels():
        label.set_rotation(45)
    plt.setp(ax.get_xticklabels(), visible=False)
    '''
    #plt.setp(axv.get_xticklabels(), visible=False)
    #axv = ax.twinx()
    #print(dataset['volume'])
    #
    plt.subplots_adjust(left=.09, bottom=.14, right=.94, top=.95, wspace=.20, hspace=0)
    plt.legend()
    plt.grid(True)
    # plt.show() # Figure test
    fig_save = plt.gcf()
    return fig_save

# plotting by prediction model
# def plot_prediction_model()
#     date_ori = pd.to_datetime(df_korea.iloc[:, 0]).tolist()
#     for i in range(test_size):
#         date_ori.append(date_ori[-1] + timedelta(days=1))
#     date_ori = pd.Series(date_ori).dt.strftime(date_format='%Y-%m-%d').tolist()
#     date_ori[-5:]
#
#     accepted_results = []
#     for r in results:
#         if (np.array(r[-test_size:]) < np.min(df_korea['종가'])).sum() == 0 and \
#                 (np.array(r[-test_size:]) > np.max(df_korea['종가']) * 2).sum() == 0:
#             accepted_results.append(r)
#     print(len(accepted_results))
#
#     accuracies = [calculate_accuracy(df_korea['종가'].values, r[:-test_size]) for r in accepted_results]
#
#     plt.figure(figsize=(12, 3))
#     plt.rcParams["font.family"] = 'NanumBarunGothic'
#     for no, r in enumerate(accepted_results):
#         plt.plot(r, label='forecast %d' % (no + 1), linewidth=0.5, alpha=0.5)
#     avg_list = list()
#     median_list = list()
#     for i in range(len(accepted_results[no])):
#         sum = 0
#         median_results = list()
#         for k in range(len(accepted_results)):
#             median_results.append(accepted_results[k][i])
#             sum = sum + accepted_results[k][i]
#         avg_list.append(sum / len(accepted_results))
#         median_list.append(statistics.median(median_results))
#
#     plt.plot(avg_list, label='Avg forecast', c='red', linewidth=1.2)
#     plt.plot(median_list, label='Avg forecast', c='blue', linewidth=1.2)
#     plt.plot(df_korea['종가'], label='true trend', c='black', linewidth=1.8)
#     x_range_future = np.arange(len(results[0]))
#     plt.xticks(x_range_future[::60], date_ori[::60], fontsize=7)
#     plt.yticks(fontsize=7)
#     plt.legend(fontsize=7)
#     plt.title('Stock name : %s   Average accuracy: %.4f' % (stock_input, np.mean(accuracies)), fontsize=10)
#     plt.show()