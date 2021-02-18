import sys
import warnings
if not sys.warnoptions:
   warnings.simplefilter('ignore')
from finta import TA
from pykrx import stock
import pandas as pd
import numpy as np
import statistics
import tensorflow as tf
import warnings
import matplotlib.pyplot as plt
import seaborn as sns
import GPUtil
import time
from sklearn.preprocessing import MinMaxScaler
from datetime import timedelta
from tqdm import tqdm
from datetime import datetime
from tensorflow.python.client import device_lib
from threading import Thread

tf.test.is_gpu_available()
print(device_lib.list_local_devices())
config = tf.ConfigProto()
config.gpu_options.per_process_gpu_memory_fraction = 1
sns.set()
tf.compat.v1.random.set_random_seed(1234)
warnings.filterwarnings("ignore")

simulation_size = 10
num_layers = 2
size_layer = 256
timestamp = 10
epoch = 500
dropout_rate = 0.8
test_size = 30
learning_rate = 0.0001

date_Start = '20200101'
stock_input = "코리아센터"
date_End = datetime.today().strftime("%Y%m%d")

print("Daily candle dates {} - {}".format(date_Start, date_End))
for ticker in stock.get_market_ticker_list(market="ALL"):
   stock_name = stock.get_market_ticker_name(ticker)
   if stock_name == stock_input:
       print('Found : {}, ticker : {}'.format(stock_input, ticker))
       korea_center_ticker = ticker
       korea_center_name = stock_input

df_korea = stock.get_market_ohlcv_by_date(date_Start, date_End, korea_center_ticker)
df_korea = df_korea.reset_index()
print(len(df_korea))
df_korea.insert(5, '종가2', df_korea['종가'])
#df = pd.read_csv('../dataset/GOOG-year.csv')
#df_korea.rename(columns=df.columns)
#print(df_korea.head())
#print(df.head())
print(df_korea.iloc[:, 4:5].tail())
minmax = MinMaxScaler().fit(df_korea.iloc[:, 4:5].astype('float32')) # Close index
df_log = minmax.transform(df_korea.iloc[:, 4:5].astype('float32')) # Close index
df_log = pd.DataFrame(df_log)
df_log.head()
df_train = df_log
df_korea.shape, df_train.shape

class Monitor(Thread):
    def __init__(self, delay):
        super(Monitor, self).__init__()
        self.stopped = False
        self.delay = delay  # Time between calls to GPUtil
        self.start()

    def run(self):
        while not self.stopped:
            GPUtil.showUtilization()
            time.sleep(self.delay)

    def stop(self):
        self.stopped = True

monitor = Monitor(10)
monitor.stop()
class Model:
   def __init__(
           self,
           learning_rate,
           num_layers,
           size,
           size_layer,
           output_size,
           forget_bias=0.1,
   ):
       def lstm_cell(size_layer):
           return tf.nn.rnn_cell.LSTMCell(size_layer, state_is_tuple=False)

       rnn_cells = tf.nn.rnn_cell.MultiRNNCell(
           [lstm_cell(size_layer) for _ in range(num_layers)],
           state_is_tuple=False,
       )
       self.X = tf.placeholder(tf.float32, (None, None, size))
       self.Y = tf.placeholder(tf.float32, (None, output_size))
       drop = tf.contrib.rnn.DropoutWrapper(
           rnn_cells, output_keep_prob=forget_bias
       )
       self.hidden_layer = tf.placeholder(
           tf.float32, (None, num_layers * 2 * size_layer)
       )
       self.outputs, self.last_state = tf.nn.dynamic_rnn(
           drop, self.X, initial_state=self.hidden_layer, dtype=tf.float32
       )
       self.logits = tf.layers.dense(self.outputs[-1], output_size)
       self.cost = tf.reduce_mean(tf.square(self.Y - self.logits))
       self.optimizer = tf.train.AdamOptimizer(learning_rate).minimize(
           self.cost
       )

def calculate_accuracy(real, predict):
   real = np.array(real) + 1
   predict = np.array(predict) + 1
   percentage = 1 - np.sqrt(np.mean(np.square((real - predict) / real)))
   return percentage * 100

def anchor(signal, weight):
   buffer = []
   last = signal[0]
   for i in signal:
       smoothed_val = last * weight + (1 - weight) * i
       buffer.append(smoothed_val)
       last = smoothed_val
   return buffer

def forecast():
   tf.reset_default_graph()
   modelnn = Model(
       learning_rate, num_layers, df_log.shape[1], size_layer, df_log.shape[1], dropout_rate
   )
   # Original code
   #sess = tf.InteractiveSession()
   sess = tf.Session(config=config)
   sess.run(tf.global_variables_initializer())
   date_ori = pd.to_datetime(df_korea.iloc[:, 0]).tolist()

   pbar = tqdm(range(epoch), desc='train loop')
   for i in pbar:
       init_value = np.zeros((1, num_layers * 2 * size_layer))
       total_loss, total_acc = [], []
       for k in range(0, df_train.shape[0] - 1, timestamp):
           index = min(k + timestamp, df_train.shape[0] - 1)
           batch_x = np.expand_dims(
               df_train.iloc[k: index, :].values, axis=0
           )
           batch_y = df_train.iloc[k + 1: index + 1, :].values
           logits, last_state, _, loss = sess.run(
               [modelnn.logits, modelnn.last_state, modelnn.optimizer, modelnn.cost],
               feed_dict={
                   modelnn.X: batch_x,
                   modelnn.Y: batch_y,
                   modelnn.hidden_layer: init_value,
               },
           )
           init_value = last_state
           total_loss.append(loss)
           total_acc.append(calculate_accuracy(batch_y[:, 0], logits[:, 0]))
       pbar.set_postfix(cost=np.mean(total_loss), acc=np.mean(total_acc))

   future_day = test_size

   output_predict = np.zeros((df_train.shape[0] + future_day, df_train.shape[1]))
   output_predict[0] = df_train.iloc[0]
   upper_b = (df_train.shape[0] // timestamp) * timestamp
   init_value = np.zeros((1, num_layers * 2 * size_layer))

   for k in range(0, (df_train.shape[0] // timestamp) * timestamp, timestamp):
       out_logits, last_state = sess.run(
           [modelnn.logits, modelnn.last_state],
           feed_dict={
               modelnn.X: np.expand_dims(
                   df_train.iloc[k: k + timestamp], axis=0
               ),
               modelnn.hidden_layer: init_value,
           },
       )
       init_value = last_state
       output_predict[k + 1: k + timestamp + 1] = out_logits

   if upper_b != df_train.shape[0]:
       out_logits, last_state = sess.run(
           [modelnn.logits, modelnn.last_state],
           feed_dict={
               modelnn.X: np.expand_dims(df_train.iloc[upper_b:], axis=0),
               modelnn.hidden_layer: init_value,
           },
       )
       output_predict[upper_b + 1: df_train.shape[0] + 1] = out_logits
       future_day -= 1
       date_ori.append(date_ori[-1] + timedelta(days=1))

   init_value = last_state

   for i in range(future_day):
       o = output_predict[-future_day - timestamp + i:-future_day + i]
       out_logits, last_state = sess.run(
           [modelnn.logits, modelnn.last_state],
           feed_dict={
               modelnn.X: np.expand_dims(o, axis=0),
               modelnn.hidden_layer: init_value,
           },
       )
       init_value = last_state
       output_predict[-future_day + i] = out_logits[-1]
       date_ori.append(date_ori[-1] + timedelta(days=1))

   output_predict = minmax.inverse_transform(output_predict)
   deep_future = anchor(output_predict[:, 0], 0.4)

   return deep_future

results = []
for i in range(simulation_size):
   print('simulation %d'%(i + 1))
   results.append(forecast())

date_ori = pd.to_datetime(df_korea.iloc[:, 0]).tolist()
for i in range(test_size):
   date_ori.append(date_ori[-1] + timedelta(days = 1))
date_ori = pd.Series(date_ori).dt.strftime(date_format = '%Y-%m-%d').tolist()
date_ori[-5:]

accepted_results = []
for r in results:
   if (np.array(r[-test_size:]) < np.min(df_korea['종가'])).sum() == 0 and \
   (np.array(r[-test_size:]) > np.max(df_korea['종가']) * 2).sum() == 0:
       accepted_results.append(r)
print(len(accepted_results))

accuracies = [calculate_accuracy(df_korea['종가'].values, r[:-test_size]) for r in accepted_results]

plt.figure(figsize = (12, 3))
plt.rcParams["font.family"] = 'NanumBarunGothic'
for no, r in enumerate(accepted_results):
   plt.plot(r, label = 'forecast %d'%(no + 1), linewidth=0.5, alpha=0.5)
avg_list = list()
median_list = list()
for i in range(len(accepted_results[no])):
   sum = 0
   median_results = list()
   for k in range(len(accepted_results)):
       median_results.append(accepted_results[k][i])
       sum = sum + accepted_results[k][i]
   avg_list.append(sum / len(accepted_results))
   median_list.append(statistics.median(median_results))
plt.plot(avg_list, label='Avg forecast', c='red', linewidth=1.2)
plt.plot(median_list, label='Avg forecast', c='blue', linewidth=1.2)
plt.plot(df_korea['종가'], label='true trend', c='black', linewidth=1.8)
x_range_future = np.arange(len(results[0]))
plt.xticks(x_range_future[::60], date_ori[::60], fontsize= 7)
plt.yticks(fontsize=7)
plt.legend(fontsize=7)
plt.title('Stock name : %s   Average accuracy: %.4f' %(stock_input, np.mean(accuracies)), fontsize=10)
plt.show()
