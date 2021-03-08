import matplotlib.pyplot as plt

def plot_technical_indicators(name, dataset, last_days):
    plt.figure(figsize=(10, 2), dpi=100)
    dataset = dataset.iloc[-last_days:, :]
    x_ = list(dataset.index)
    x_range = []
    for i in range(0, int(len(x_))):
        x_range.append(dataset['date'].iloc[i])
        #print(x_range)
    # Plot first subplot
    ax = plt.subplot(1, 1, 1)
    plt.plot(dataset['ema7'], label='EMA 7', color='g', linestyle='-.', linewidth=0.8)
    plt.plot(dataset['ema25'], label='EMA 25', color='r', linestyle='-.', linewidth=0.8)
    plt.plot(dataset['ema99'], label='EMA 99', color='b', linestyle='-.', linewidth=0.8)
    plt.plot(dataset['close'], label='Closing Price', color='black', linestyle='-', linewidth=1.2, dash_capstyle= 'round')
    plt.plot(dataset['upper_band'], label='Upper Band', color='c', linewidth=0.5)
    plt.plot(dataset['lower_band'], label='Lower Band', color='c', linewidth=0.5)
    plt.fill_between(x_, dataset['lower_band'], dataset['upper_band'], alpha=0.25)
    plt.title('Technical indicators for {} - last {} days.'.format(name, last_days))
    plt.rcParams["font.family"] = 'AppleGothic'
    plt.ylabel('KRW')
    plt.xticks(x_[::30], x_range[::30])
    xlabels = ax.get_xticklabels()
    ax.set_xticklabels(xlabels, rotation=45, fontsize=7)
    plt.legend()
    plt.grid(True)
    plt.show()

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