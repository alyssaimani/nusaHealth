from distutils.log import debug
from fileinput import filename
from urllib import request
from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import pandas as pd
from sklearn import tree
from sklearn.metrics import accuracy_score
import numpy as np
import pickle 


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///nusahealth.db'
db = SQLAlchemy(app)

data_test = open("data/Testing.csv")
test_symptoms = pd.read_csv(data_test)
test_symptoms = pd.DataFrame(test_symptoms)

data_medicine = open("data/disease_medicine.csv")
df_medicine = pd.read_csv(data_medicine)
df_medicine = pd.DataFrame(df_medicine)

data_precaution = open("data/disease_precaution.csv")
df_precaution = pd.read_csv(data_precaution)
df_precaution = pd.DataFrame(df_precaution)

data_rFactors = open("data/disease_riskFactors.csv")
df_rFactors = pd.read_csv(data_rFactors)
df_rFactors = pd.DataFrame(df_rFactors)

test_data = test_symptoms.drop(["prognosis"], axis=1)
test_target = test_symptoms["prognosis"]

                  

label = ["Itching","Skin rash","Nodal skin eruptions","Continuous sneezing","Shivering","Chills","Joint pain","Stomach pain","Acidity","Ulcers on tongue","Muscle wasting","Vomiting","Burning micturition","Spotting urination","Fatigue","Weight gain","Anxiety","Cold hands and feets","Mood swings","Weight loss","Restlessness","Lethargy","Patches in throat","Irregular sugar level","Cough","High fever","Sunken eyes","Breathlessness","Sweating","Dehydration","Indigestion","Headache","Yellowish skin","Dark urine","Nausea","Loss of appetite","Pain behind the eyes","Back pain","Constipation","Abdominal pain","Diarrhoea","Mild fever","Yellow urine","Yellowing of eyes","Acute liver failure","Fluid overload","Swelling of stomach","Swelled lymph nodes","Malaise","Blurred and distorted vision","Phlegm","Throat irritation","Redness of eyes","Sinus pressure","Runny nose","Congestion","Chest pain","Weakness in limbs","Fast heart rate","Pain during bowel movements","Pain in anal region","Bloody stool","Irritation in anus","Neck_pain","Dizziness","Cramps","Bruising","Obesity","Swollen legs","Swollen blood vessels","Puffy face and eyes","Enlarged thyroid","Brittle nails","Swollen extremeties","Excessive hunger","Extra marital contacts","Drying and tingling lips","Slurred speech","Knee pain","Hip joint pain","Muscle weakness","Stiff neck","Swelling joints","Movement stiffness","Spinning movements","Loss of balance","Unsteadiness","Weakness of one body side","Loss of smell","Bladder discomfort","Foul smell of urine","Continuous feel of urine","Passage of gases","Internal itching","Toxic look (typhos)","Depression","Irritability","Muscle pain","Altered sensorium","Red spots over body","Belly pain","abnormal menstruation","Dischromic patches","Watering from eyes","Increased appetite","Polyuria","Family history","Mucoid sputum","Rusty sputum","Lack of concentration","Visual disturbances","Receiving blood transfusion","Receiving unsterile injections","Coma","Stomach bleeding","Distention of abdomen","History of alcohol consumption","Fluid overload","Blood in sputum","Prominent veins on calf","Palpitations","Painful walking","Pus filled pimples","Blackheads","Scurring","Skin peeling","Silver like dusting","Small dents in nails","Inflammatory nails","Blister","Red sore around nose","Yellow crust ooze"]


    
@app.route('/')
def index():
   return render_template('index.html')

@app.route('/diagnosa/', methods=['POST', 'GET'])
def diagnosa():
   if request.method == 'POST':
     
      user_name = request.form['nm']
      user_bdate = request.form['tgl']
      user_symptoms = {}
      index = []
      for key in list(request.form.keys())[2:]:
         user_symptoms[key] = request.form[key]
         index.append(label.index(key))
      
      input = np.zeros(132)
      
      for x in range(len(index)):
         input[index[x]] = 1



      filename = 'data/diagnose_model.sav'
      loaded_model = pickle.load(open(filename, 'rb'))
      result = loaded_model.predict([input])
      accuracy = loaded_model.score(test_data, test_target)
      lower = result[0].lower()


      if((df_rFactors["LDNAME"]==lower).any()):
         idx = df_rFactors[df_rFactors["LDNAME"]==lower].index.values

         did = df_rFactors.loc[idx[0]].values[0]

         idx = df_medicine[df_medicine["Disease_ID"]==did].index.values 
         med_desc = df_medicine.loc[idx[0]].values[4]
         med_comp = df_medicine.loc[idx[0]].values[3]
         medicine= df_medicine.loc[idx[0]].values[1]
         
      return render_template('hasil_diagnosa.html', user_name=user_name, user_bdate=user_bdate, user_symptoms = user_symptoms , result=result, accuracy=accuracy, medicine=medicine,med_desc=med_desc, med_comp=med_comp)
      
   else:
      return render_template('diagnosa.html')

@app.route('/rekapmedis/')
def rekap_medis():
   return render_template('rekap_medis.html')

@app.route('/riwayatdiagnosa/')
def riwayat_diagnosa():
   return render_template('riwayat_diagnosa.html')

@app.route('/hasil_diagnosa/')
@app.route('/hasil_diagonosa/<user_name>/<user_bdate>/<user_symptoms>/<result>/<accuracy>/<medicine>/<med_desc>/<med_comp>/')
def hasil_diagnosa(user_name=None, user_bdate=None, user_symptoms=None, result=None, accuracy=None, medicine=None, med_desc=None, med_comp=None):
   return render_template("hasil_diagnosa.html", user_name=user_name, user_bdate=user_bdate, user_symptoms=user_symptoms, result=result,   accuracy=accuracy, medicine=medicine, med_desc=med_desc, med_comp = med_comp)


if __name__ == "__main__":
   app.run(debug=True)