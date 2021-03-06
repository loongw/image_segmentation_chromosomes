import matplotlib.pyplot as plt
import numpy as np
import utilities
import os
from OverlapSegmentationNet import OverlapSegmentationNet

import tensorflow as tf

# Load data
xdata = np.load('xdata_88x88.npy')
labels = np.load('ydata_88x88_0123_onehot.npy')
train_test_boundary_index = round(13434*.8)

model = OverlapSegmentationNet(input_shape=(88,88,1))

# Choose loss
model.compile(loss='mean_squared_error', optimizer='adam')

# Specify the number of epochs to run
num_epoch = 5
for i in range(num_epoch):
    
    # Fit
    model.fit(x=xdata, y=labels, epochs=1, validation_split=0.2) 
    os.makedirs('models', exist_ok=True)
    filename = 'models/savedmodel_' + str(i) + 'epoch'
    model.save(filename)
    
    # Predict and plot images
    predictions = model.predict(xdata[0:4,...])
    utilities.plotSamplesOneHots(predictions[0:4,...].round())
   
    # Calculate mIOU
    y_pred_train = model.predict(xdata[0:train_test_boundary_index,...]).round()
    trainIOU = utilities.IOU(y_pred_train, labels[0:train_test_boundary_index,...])
    print('Training IOU: ' + str(trainIOU))
    trainAccuracy = utilities.globalAccuracy(y_pred_train, labels[0:train_test_boundary_index,...])
    print('Training accuracy: ' + str(trainAccuracy))
    del y_pred_train
    
    y_pred_test = model.predict(xdata[train_test_boundary_index:,...]).round()
    testIOU = utilities.IOU(y_pred_test, labels[train_test_boundary_index:,...])
    print('Testing IOU: ' + str(testIOU))
    testAccuracy = utilities.globalAccuracy(y_pred_test, labels[train_test_boundary_index:,...])
    print('Testing accuracy: ' + str(testAccuracy))
    del y_pred_test

