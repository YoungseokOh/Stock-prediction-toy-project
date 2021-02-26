import matplotlib.pyplot as plt

def plot_technical_indicators(dataset, last_days):
    plt.figure(figsize=(16, 10), dpi=100)
    shape_0 = dataset.shape[0]
    xmacd_ = shape_0 - last_days

    dataset = dataset.iloc[-last_days:, :]
    x_ = range(3, dataset.shape[0])
    x_ = list(dataset.index)

    # Plot first subplot
    plt.subplot(2, 1, 1)
    plt.plot(dataset['ma7'], label='MA 7', color='g', linestyle='--')
    plt.plot(dataset['price'], label='Closing Price', color='b')
    plt.plot(dataset['ma21'], label='MA 21', color='r', linestyle='--')
    plt.plot(dataset['upper_band'], label='Upper Band', color='c')
    plt.plot(dataset['lower_band'], label='Lower Band', color='c')
    plt.fill_between(x_, dataset['lower_band'], dataset['upper_band'], alpha=0.35)
    plt.title('Technical indicators for Goldman Sachs - last {} days.'.format(last_days))
    plt.ylabel('USD')
    plt.legend()

    # Plot second subplot
    plt.subplot(2, 1, 2)
    plt.title('MACD')
    plt.plot(dataset['MACD'], label='MACD', linestyle='-.')
    plt.hlines(15, xmacd_, shape_0, colors='g', linestyles='--')
    plt.hlines(-15, xmacd_, shape_0, colors='g', linestyles='--')
    plt.plot(dataset['log_momentum'], label='Momentum', color='b', linestyle='-')

    plt.legend()
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