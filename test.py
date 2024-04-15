from DAO import DAO
from EmployeeDAO import EmployeeDAO
from FingerprintImageDAO import FingerprintImageDAO
from ModelDAO import ModelDAO
from DAO import DAO
from Model import Model
import os
import cv2
import random
import itertools
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import tensorflow as tk
from tensorflow import keras
from keras.models import Sequential, load_model
from keras.utils import to_categorical, plot_model
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from keras import layers, regularizers, optimizers, callbacks
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
import random
from datetime import datetime

# fingerprint_images = FingerprintImageDAO().getAllFingerprintImage()
# model = ModelDAO().trainNewModel(fingerprint_images)
#
# ModelDAO().saveModel(model)

# model = load_model("sID.keras")
# img_predict = cv2.imread(r"D:\TAI_LIEU_HOC\Ki2Nam4\PTTKPM\SOCOFing\Altered\Altered-Easy\15__F_Right_thumb_finger_Obl.BMP", cv2.IMREAD_GRAYSCALE)
# img_resize = cv2.resize(img_predict, (96, 96))
#
# data_predict = np.array(img_resize, dtype="object").reshape(-1, 96, 96, 1)
# data_predict = data_predict / 255.0
#
# y_predict = model.predict(data_predict.astype(np.float32))
# print(data_predict.shape)
# print(np.argmax(y_predict))

dao = DAO()
modelDAO = ModelDAO()
print(dao.connection is modelDAO.connection)


