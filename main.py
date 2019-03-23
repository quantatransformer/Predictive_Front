"""
Note: 

This is the main file of the index-prediction project.
The parameters are loaded from command line.
All the related files will be saved into output.

Author: Yadong Zhang
E-mail: ydup@foxmail.com

"""
from library.lstm import LSTMmodule
from library.prepare import *
import pandas as pd
from tqdm import tqdm
import numpy as np
import matplotlib.pyplot as plt
from keras.models import Sequential
from keras.layers import Dense, Activation, LSTM
from pandas import Series
import time

# Get the time
timenow = int(time.time())

class Config(object):
	'''
	Default parameters
	'''
	look_back = 100
	epoch = 10
	learning_rate = 0.1
	trainPercentage = 0.95

config = Config()

# Read paramters from config
config = readCommandArg(config)

# Module parameters
look_back = config.look_back  # look back window
look_forward = 1  # look forward length
percent = config.trainPercentage  # training percentage 
epoch = config.epoch  # epoch for training
learning_rate = config.learning_rate  # learning rate
outputPath = 'output/'

# Download data with fred
allData = pd.read_csv('data/data.csv', index_col=0)  # read all data from filedir
allData = allData[~allData['Adj Close'].isnull()]
featureName = ['Adj Close']  # input: adjusted closed value
targetName = 'Adj Close'  # output: adjusted closed value
# Scaler the data into (0, 1)
scaleredData, maper = scalerModelData(allData, columns=featureName)

# Create the dataset for keras model
X, Y, dateY = create_dataset(scaleredData, look_back, look_forward, featureName, targetName)

# Divide the data into train and test
AllLen = X.shape[0]

trainX = X[0: int(AllLen*percent)]
trainY = Y[0: int(AllLen*percent)]
trainDate = dateY[0: int(AllLen*percent)]

testX = X[int(AllLen*percent): ]
testY = Y[int(AllLen*percent): ]
testDate = dateY[int(AllLen*percent): ]

trainLen = len(trainY)
testLen = len(testY)
print '# Data Processing Finished!'

# Initialize the LSTM model
lstm = LSTMmodule(look_back, look_forward, featureName)
# lstm = LSTMmodule(look_back, look_forward, featureName, targetName)
# train the model
lstm.train(trainX, trainY, nb_epoch=epoch)

evalList = []
# Predict the model with the trainX
predictTrainY = lstm.predict(trainX)
outputTrain = pd.DataFrame(np.concatenate([trainY, predictTrainY], axis=1), index=np.squeeze(trainDate), columns=['origin', 'predict'])
outputTrain.loc[:, 'origin'] = invscaler(outputTrain['origin'].values, maper['Adj Close'][0], maper['Adj Close'][1])
outputTrain.loc[:, 'predict'] = invscaler(outputTrain['predict'].values, maper['Adj Close'][0], maper['Adj Close'][1])
outputTrain.to_csv(outputPath+'/outputTrain.csv')

# Predict the mdoel with the testX
predictTestY = lstm.predict(testX)
outputTest = pd.DataFrame(np.concatenate([testY, predictTestY], axis=1), index=np.squeeze(testDate), columns=['origin', 'predict'])
outputTest.loc[:, 'origin'] = invscaler(outputTest['origin'].values, maper['Adj Close'][0], maper['Adj Close'][1])
outputTest.loc[:, 'predict'] = invscaler(outputTest['predict'].values, maper['Adj Close'][0], maper['Adj Close'][1])
outputTest.to_csv(outputPath+'/outputTest.csv')

# Re-train the model with the new data
PredictTrainList = []
for i in tqdm(range(testX.shape[0]), desc='Predict'):
    predictValue = lstm.predict([testX[i:i+1]])
    lstm.train(testX[i:i+1], testY[i:i+1], nb_epoch=epoch, batch_size=1, verbose=0)
    PredictTrainList.append(np.squeeze(predictValue))

outputTrainTest = pd.DataFrame(np.concatenate([testY, np.reshape(np.squeeze(PredictTrainList), (testLen, 1))], axis=1), index=np.squeeze(testDate), columns=['origin', 'predict'])
outputTrainTest.loc[:, 'origin'] = invscaler(outputTrainTest['origin'].values, maper['Adj Close'][0], maper['Adj Close'][1])
outputTrainTest.loc[:, 'predict'] = invscaler(outputTrainTest['predict'].values, maper['Adj Close'][0], maper['Adj Close'][1])
outputTrainTest.to_csv(outputPath+'/outputTrainTest.csv')





