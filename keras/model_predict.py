from keras.models import load_model
import scipy

model = load_model('models/keras_cnn.h5')

img_names = ['one', 'two', 'three', 'four', 'five',
             'six', 'seven', 'eight', 'nine', 'zero']

for i in range(len(img_names)):
    image = scipy.misc.imread('my_images/' + img_names[i] + '.png',
                              flatten=True)
    prediction = model.predict_classes(image.reshape((1, 28, 28, 1)))
    print('{0} \t-> {1}'.format(img_names[i], prediction))
