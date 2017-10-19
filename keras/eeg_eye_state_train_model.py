import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D
from keras import backend as k

# TODO: Load EEG dataset

batch_size = 128
num_classes = 2
epochs = 12

# TODO: Define input data variable
# x_train = load data from dataset
# same for output

# TODO: Define types of input data
# var.astype( ... )

# creating model
model = Sequential()
# TODO: Add appropriate model layers here! (model.add)

# TODO: Compile model (model.compile)

# TODO: Train model (model.fit)

# TODO: Evaluate model (model.evaluate)

model.save('models/keras_eeg_eye.h5')
