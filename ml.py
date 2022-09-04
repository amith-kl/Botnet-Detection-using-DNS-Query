import pandas as pd
import tensorflow as tf
from tkinter import *
from matplotlib import pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay

def standard_dataset():
    botlabel = Label()
    botlabel.config(font=("Comic Sans", 10))
    botlabel.place(x=30,y=260)
    
    #Setting data
    data = pd.read_csv('Output\\CleanedData.csv')
    data = data.loc[:, ~data.columns.str.contains('^Unnamed')]
    X = data.drop(['Domain', 'Class'], axis=1)
    y = data.Class
    X_train,X_test,Y_train,Y_test = train_test_split(X, y, test_size=0.33, random_state=42)
    
    #Creating and training model
    ann = tf.keras.models.Sequential()
    ann.add(tf.keras.layers.Dense(units=35,activation="relu"))
    ann.add(tf.keras.layers.Dense(units=35,activation="relu"))
    ann.add(tf.keras.layers.Dense(units=1,activation="sigmoid"))
    ann.compile(optimizer="adam",loss="binary_crossentropy",metrics=['accuracy'])
    history = ann.fit(X_train, Y_train, validation_split = 0.1, epochs=20, batch_size=32)
    
    #Plotting accuracy of testing and validation
    print(history.history.keys())
    plt.plot(history.history['accuracy'])
    plt.plot(history.history['val_accuracy'])
    plt.title('model accuracy')
    plt.ylabel('accuracy')
    plt.xlabel('epoch')
    plt.legend(['train', 'val'], loc='upper left')
    plt.show()
    
    #Plotting loss of testing and validation
    plt.plot(history.history['loss'])
    plt.plot(history.history['val_loss'])
    plt.title('model loss')
    plt.ylabel('loss')
    plt.xlabel('epoch')
    plt.legend(['train', 'val'], loc='upper left')
    plt.show()
    
    #Model prediciton
    predictions = ann.predict(X_test)
    Y_pred = (predictions > 0.5)
    y_true = Y_test.astype(int).tolist()
    y_pred = Y_pred.astype(int).tolist()

    #Plotting confusion matrix
    matrix = confusion_matrix(y_true, y_pred)
    labels = ['Botnet', 'Not Botnet']
    disp = ConfusionMatrixDisplay(confusion_matrix=matrix, display_labels=labels)
    disp.plot(cmap=plt.cm.Blues)
    plt.show()
    
    #Printing accuracy
    accuracy = ann.evaluate(X_test, Y_test)
    botlabel2 = Label(text="Accuracy :")
    botlabel2.config(font=("Comic Sans", 11))
    botlabel2.place(x=30,y=280)
    test = accuracy[1]*100
    test1 = '{:.2f}'.format(test)
    
    botlabel1 = Label(text=test1)
    botlabel1.place(x=100,y=280)
