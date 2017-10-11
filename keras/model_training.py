import keras
from keras.datasets import mnist
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D
from keras import backend as k

batch_size = 128    # how many samples to evaluate in one cycle
num_classes = 10    # how many possible outputs are there (digits)
epochs = 12         # how many times model will train itself
# dimension of images
img_wid, img_hei = 28, 28
# loading training and testing data from mnist
(x_train, y_train), (x_test, y_test) = mnist.load_data()

if k.image_data_format() == 'channels_first':
    x_train = x_train.reshape(x_train.shape[0], 1, img_wid, img_hei)
    x_test = x_test.reshape(x_test.shape[0], 1, img_wid, img_hei)
    input_shape = (1, img_wid, img_hei)
else:
    x_train = x_train.reshape(x_train.shape[0], img_wid, img_hei, 1)
    x_test = x_test.reshape(x_test.shape[0], img_wid, img_hei, 1)
    input_shape = (img_wid, img_hei, 1)

x_train = x_train.astype('float32')
x_test = x_test.astype('float32')

x_train /= 255
x_test /= 255

print('x_train shape: {0}'.format(x_train))
print('{0} - train samples'.format(x_train.shape[0]))
print('{0} - test samples'.format(x_test.shape[0]))
# creating output variables
y_train = keras.utils.to_categorical(y_train, num_classes)
y_test = keras.utils.to_categorical(y_test, num_classes)
# creating model
model = Sequential()
model.add(Conv2D(32, kernel_size=(3, 3),
                 activation='relu',
                 input_shape=input_shape))
model.add(Conv2D(64, (3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))
model.add(Flatten())
model.add(Dense(128, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(num_classes, activation='softmax'))

model.compile(loss=keras.losses.categorical_crossentropy,
              optimizer=keras.optimizers.Adadelta(),
              metrics=['accuracy'])

model.fit(x_train, y_train,
          batch_size=batch_size,
          epochs=epochs,
          verbose=1,
          validation_data=(x_test, y_test))

score = model.evaluate(x_test, y_test, verbose=0)
print('Test loss: {0}'.format(score[0]))
print('Test accuracy: {0}%'.format(score[1] * 100))

model.save('models/keras_cnn.h5')
