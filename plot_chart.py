import matplotlib.pyplot as plt
import mplfinance as fplt
from krx_wr_script import pykrx_read_csv
import pandas as pd
from mplfinance.original_flavor import candlestick2_ohlc

def plot_technical_indicators(name, dataset, last_days):
    dataset = dataset.iloc[-last_days:, :]
    dataset = dataset.reset_index()
    ax = plt.subplot()
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
    plt.plot(dataset['{}'.format(col_name[0])], label='{}'.format(col_name[0].upper()), color='g', linestyle='-.', linewidth=0.8)
    plt.plot(dataset['{}'.format(col_name[1])], label='{}'.format(col_name[1].upper()), color='r', linestyle='-.', linewidth=0.8)
    plt.plot(dataset['{}'.format(col_name[2])], label='{}'.format(col_name[2].upper()), color='b', linestyle='-.', linewidth=0.8)
    if 'upper_band' in dataset.columns:
        plt.plot(dataset['upper_band'], label='Upper Band', color='c', linewidth=0.5)
        plt.plot(dataset['lower_band'], label='Lower Band', color='c', linewidth=0.5)
        plt.fill_between(x_, dataset['lower_band'], dataset['upper_band'], alpha=0.25)
    plt.title('Technical indicators for {} - last {} days.'.format(name, last_days))
    plt.rcParams["font.family"] = 'DejaVu Sans'
    plt.ylabel('KRW')
    plt.xticks(x_[::30], x_range[::30])
    xlabels = ax.get_xticklabels()
    ax.set_xticklabels(xlabels, rotation=45, fontsize=7)
    plt.legend()
    plt.grid(True)
    plt.show()
    plt.draw()
    fig_save = plt.gcf()
    return fig_save
    # plt.show()
    # plt.draw()
    # fig_save.savefig('results/{}.png'.format(name))

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