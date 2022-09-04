import tkinter.font as font
import requests
import json
import get_features
import pandas as pd
from ml import *
from tkinter import *
from sklearn.model_selection import train_test_split
from sklearn import preprocessing
from sklearn.neighbors import KNeighborsClassifier

class Root(Tk):

    def __init__(self):
        #Initialize window
        super(Root,self).__init__()
        self.title("Botnet detection using DNS Queries")
        self.minsize(640,400)
        canvas = Canvas(self)   
        self.setwidget()
        self.test_dataset()
        myFont = font.Font(size=10)
        
        #Create button
        w = Button (self, text="Train Model", width=10, height=3, command=standard_dataset)
        w['font'] = myFont
        w.place(x=90, y=150)
        canvas.create_line(200, 10, 200, 400, dash=(4, 2))
        canvas.pack(fill=Y,expand=1)

    def setwidget(self):
        #Window design elements
        label=Label(self,text="Botnet Detection using DNS Queries")
        label2=Label(self,text="--------------------------------------------------------------------------------------------------------------------------------")
        header = Label(self,text="Standard Dataset")
        header.config(font=("Comic Sans",22))
        header1 = Label(self,text="Generated Dataset")
        header1.config(font=("Comic Sans",22))
        label.config(font=("Comic Sans", 25))
        header.place(x = 30, y =70)
        header1.place(x = 350, y =70)
        label.place(x=30, y=10)
        label2.place(x=0, y=50)

    def test_dataset(self):
        #Testing dataset model
        self.label7=Label(self,text="Enter URL:",borderwidth=2)
        self.label7.place(x=350, y=230) 
        global player_name
        player_name = Entry(self)
        player_name.place(x=410,y=230)
        myFont = font.Font(size=10)
        w1 = Button ( self,text="Test Model", width=10,height=3,command=self.store_val)
        w1['font'] = myFont
        w1.place(x=410, y=150)

    def store_val(self):
        #Store domain
        global pname
        pname = player_name.get()
        self.dns_request()

    def dns_request(self):
        #Generate response via API
        domain = pname
        api_url = 'https://api.api-ninjas.com/v1/dnslookup?domain={}'.format(domain)
        response = requests.get(api_url, headers={'X-Api-Key': 'OwyJf4r9DwYbFqhvkPxQUw==MSk7U6NfQas9Jx6F'})
        if response.status_code == requests.codes.ok:
            pass
        else:
            print("No response")
            exit(0)
        if len(response.text) <= 2:
            self.label7=Label(self,text="Domain does not exist                                                                ",borderwidth=2)
            self.label7.place(x=350, y=280) 
            
        #convert to JSON
        res = json.loads(response.text)

        #Check if mname and rname exist in response
        flag1, flag2 = False, False
        y = {}
        for x in res:
            if 'mname' in x:
                flag1 = True
                y = x
                y['hasMX'] = 0
                y['hasTXT'] = 0
        for x in res:
            if x['record_type'] == 'MX':
                y['hasMX'] = 1
            if x['record_type'] == 'TXT':
                y['hasTXT'] = 1
            if x['record_type'] == 'A':
                flag2 = True
                y['ip'] = x['value']

        #Extract more features
        if flag1 and flag2:
            y['vowelRatio'] = get_features.vowelConsonantRatio(domain)[0]
            y['consonantRatio'] = get_features.vowelConsonantRatio(domain)[1]
            y['specialCharsRatio'] = get_features.specNumRatio(domain)[1]
            y['numericCharsRatio'] = get_features.specNumRatio(domain)[0]
            y['vowelSequence'] = get_features.longestVowel(domain)
            y['consonantSequence'] = get_features.longestConsonant(domain)
            y['numericSequence'] = get_features.longestNum(domain)
            y['specialSequence'] = get_features.longestSpec(domain)
            y['strangeCharacters'] = get_features.getStrangeCharacters(domain)
            y['domainInAlexaDB'] = get_features.existsInAlexaDb(domain)
            y['ipReputation'] = get_features.getIpReputation(y['ip'])
            y['domainReputation'] = get_features.getDomainReputation(domain)
            y['entropy'] = get_features.entropyCalc(domain)
            y['domain'] = domain
            y['domainLength'] = len(domain)

            #Store response in JSON
            json_object = json.dumps(y, indent = 4)
            with open('Output\\user_test_response.json', 'w') as outfile:
                outfile.write(json_object)
                outfile.seek(0)

            #Read response file
            with open('Output\\user_test_response.json', 'r') as file:
                json_obj = json.load(file)
                global sample

                #Create sample array
                sample = []
                req = ['ttl', 'hasMX', 'hasTXT','vowelRatio','consonantRatio','specialCharsRatio','numericCharsRatio','vowelSequence','consonantSequence','numericSequence','specialSequence','strangeCharacters','domainInAlexaDB','ipReputation','domainReputation','entropy','domainLength']
                for x in req:
                    sample.append(json_obj[x])

        self.test_model()


    def test_model(self):
        #Read data from CSV
        df = pd.read_csv('Output\\data_file.csv')
        df = df[['ttl', 'hasMX', 'hasTXT','vowelRatio','consonantRatio','specialCharsRatio','numericCharsRatio','vowelSequence','consonantSequence','numericSequence','specialSequence','strangeCharacters','domainInAlexaDB','ipReputation','domainReputation','entropy','domainLength','class']]
        df["hasMX"] = df["hasMX"].astype(int)
        df["hasTXT"] = df["hasTXT"].astype(int)
        df["domainReputation"] = df["domainReputation"].astype(int)
        df["ipReputation"] = df["ipReputation"].astype(int)

        #Split test and train data
        X = df.drop('class', axis=1)
        y = df['class']
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.20, random_state = 0)
        X_train = preprocessing.normalize(X_train)
        X_test = preprocessing.normalize(X_test)

        #Create classifier model
        classifier = KNeighborsClassifier()
        classifier.fit(X_train, y_train)
        x = pname + " is a botnet                                             "
        y = pname + " is not a botnet                                         "

        #Predict value for given domain
        if classifier.predict([sample]) > 0.5:
             self.label6=Label(self,text=x,borderwidth=2)
             self.label6.place(x=350, y=280) 
        else:
             self.label6=Label(self,text=y,borderwidth=2)
             self.label6.place(x=350, y=280) 

root = Root()
root.mainloop()
