from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .forms import ReportForm
from .models import Report

# Create your views here.
personal_details = []
symptoms = []
final_output = []

def home(request):
    drop_down = ["itching", "skin_rash" ,"nodal_skin_eruptions" ,"continuous_sneezing" ,
                 "shivering" ,"chills" ,"joint_pain" ,"stomach_pain" ,"acidity" ,
                 "ulcers_on_tongue" ,"muscle_wasting" ,"vomiting" ,"burning_micturition",
                 "spotting_ urination", "fatigue" ,"weight_gain", "anxiety",
                 "cold_hands_and_feets", "mood_swings", "weight_loss", "restlessness",
                 "lethargy", "patches_in_throat", "irregular_sugar_level",
                 "cough", "high_fever", "sunken_eyes", "breathlessness", "sweating",
                 "dehydration", "indigestion", "headache", "yellowish_skin", "dark_urine",
                 "nausea", "loss_of_appetite", "pain_behind_the_eyes", "back_pain",
                 "constipation", "abdominal_pain", "diarrhoea", "mild_fever", "yellow_urine",
                 "yellowing_of_eyes", "acute_liver_failure", "swelling_of_stomach",
                 "swelled_lymph_nodes", "malaise", "blurred_and_distorted_vision", "phlegm",
                 "throat_irritation", "redness_of_eyes", "sinus_pressure", "runny_nose",
                 "congestion", "chest_pain", "weakness_in_limbs", "fast_heart_rate",
                 "pain_during_bowel_movements", "pain_in_anal_region", "bloody_stool",
                 "irritation_in_anus", "neck_pain", "dizziness", "cramps", "bruising",
                 "obesity", "swollen_legs", "swollen_blood_vessels", "puffy_face_and_eyes",
                 "enlarged_thyroid", "brittle_nails", "swollen_extremeties", "excessive_hunger",
                 "extra_marital_contacts", "drying_and_tingling_lips", "slurred_speech",
                "knee_pain", "hip_joint_pain", "muscle_weakness", "stiff_neck",
                "swelling_joints", "movement_stiffness", "spinning_movements", "loss_of_balance",
                "unsteadiness", "weakness_of_one_body_side", "loss_of_smell",
                "bladder_discomfort", "foul_smell_of urine", "continuous_feel_of_urine",
                "passage_of_gases", "internal_itching", "toxic_look_(typhos)",
                "depression", "irritability", "muscle_pain", "altered_sensorium",
                "red_spots_over_body", "belly_pain", "abnormal_menstruation",
                "dischromic _patches", "watering_from_eyes", "increased_appetite", "polyuria",
                "family_history", "mucoid_sputum", "rusty_sputum", "lack_of_concentration",
                "visual_disturbances", "receiving_blood_transfusion",
                "receiving_unsterile_injections", "coma", "stomach_bleeding",
                "distention_of_abdomen", "history_of_alcohol_consumption", "fluid_overload",
                "blood_in_sputum", "prominent_veins_on_calf", "palpitations",
                "painful_walking", "pus_filled_pimples", "blackheads", "scurring",
                "skin_peeling", "silver_like_dusting", "small_dents_in_nails",
                "inflammatory_nails", "blister", "red_sore_around_nose", "yellow_crust_ooze"]
    return render(request, "predict/home.html", {"drop_down":drop_down})

def report(request):
    return render(request, "predict/report.html", {"details":personal_details, "symptoms":symptoms, "outputs": final_output})

def myReports(request):
    return render(request, "predict/myReports.html")


def index(request):
    import requests
    url = "https://goquotes-api.herokuapp.com/api/v1/random/1?type=tag&val=medical"
    response = requests.request("GET", url)
    quote_list = response.text.split('"')
    quote = quote_list[13]
    author = quote_list[17]
    return render(request, "predict/index.html", {"quote": quote, "author": author})

def signupuser(request):
    if request.method =='GET':
        return render(request, 'predict/signupuser.html', {'form':UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('index')
            except IntegrityError:
                return render(request, 'predict/signupuser.html', {'form': UserCreationForm(), 'error': 'Username already taken.'})
            else:
                return render(request, 'predict/signupuser.html', {'form': UserCreationForm(), 'error': 'Password did not match!'})

def loginuser(request):
    if request.method == 'GET':
        return render(request, 'predict/loginuser.html', {'form': AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'predict/loginuser.html', {'form': AuthenticationForm(), 'error':'Username and Password did not match'})
        else:
            login(request, user)
            return redirect('index')


def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('index')

def prediction(request):
    import numpy as np
    import pandas as pd
    from sklearn import tree
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.naive_bayes import GaussianNB
    from sklearn.metrics import accuracy_score

    # Training data
    path_train = "C:/Users/Mayan/Desktop/new/disease_prediction-project/predict/templates/predict/Training.csv"
    data_training = pd.read_csv(path_train)
    path_test = "C:/Users/Mayan/Desktop/new/disease_prediction-project/predict/templates/predict/Testing.csv"
    data_testing = pd.read_csv(path_test)

    x_train = data_training.values[:, 0:131]
    y_train = data_training.values[:, 131:132]

    x_test = data_testing.values[:, 0:131]
    y_test = data_testing.values[:, 131:132]

    clf3 = tree.DecisionTreeClassifier()
    clf4 = RandomForestClassifier()
    gnb = GaussianNB()

    clf3.fit(x_train, y_train)
    clf4.fit(x_train, np.ravel(y_train))
    gnb = gnb.fit(x_train, np.ravel(y_train))

    y_pred_tree = clf3.predict(x_test)
    y_pred_random = clf4.predict(x_test)
    y_pred_naive = gnb.predict(x_test)

    accuracy_score_tree = accuracy_score(y_test, y_pred_tree)
    accuracy_score_random = accuracy_score(y_test, y_pred_naive)
    accuracy_score_naive = accuracy_score(y_test, y_pred_random)

    disease = {"itching": 0, "skin_rash": 0, "nodal_skin_eruptions": 0, "continuous_sneezing": 0,
               "shivering": 0, "chills": 0, "joint_pain": 0, "stomach_pain": 0, "acidity": 0,
               "ulcers_on_tongue": 0, "muscle_wasting": 0, "vomiting": 0, "burning_micturition": 0,
               "spotting_ urination": 0, "fatigue": 0, "weight_gain": 0, "anxiety": 0,
               "cold_hands_and_feets": 0, "mood_swings": 0, "weight_loss": 0, "restlessness": 0,
               "lethargy": 0, "patches_in_throat": 0, "irregular_sugar_level": 0, "cough": 0,
               "high_fever": 0, "sunken_eyes": 0, "breathlessness": 0, "sweating": 0,
               "dehydration": 0, "indigestion": 0, "headache": 0, "yellowish_skin": 0, "dark_urine": 0,
               "nausea": 0, "loss_of_appetite": 0, "pain_behind_the_eyes": 0, "back_pain": 0,
               "constipation": 0, "abdominal_pain": 0, "diarrhoea": 0, "mild_fever": 0, "yellow_urine": 0,
               "yellowing_of_eyes": 0, "acute_liver_failure": 0,
               "swelling_of_stomach": 0, "swelled_lymph_nodes": 0, "malaise": 0,
               "blurred_and_distorted_vision": 0, "phlegm": 0, "throat_irritation": 0,
               "redness_of_eyes": 0, "sinus_pressure": 0, "runny_nose": 0, "congestion": 0, "chest_pain": 0,
               "weakness_in_limbs": 0, "fast_heart_rate": 0, "pain_during_bowel_movements": 0,
               "pain_in_anal_region": 0, "bloody_stool": 0, "irritation_in_anus": 0, "neck_pain": 0,
               "dizziness": 0, "cramps": 0, "bruising": 0, "obesity": 0, "swollen_legs": 0,
               "swollen_blood_vessels": 0, "puffy_face_and_eyes": 0, "enlarged_thyroid": 0,
               "brittle_nails": 0, "swollen_extremeties": 0, "excessive_hunger": 0,
               "extra_marital_contacts": 0, "drying_and_tingling_lips": 0, "slurred_speech": 0,
               "knee_pain": 0, "hip_joint_pain": 0, "muscle_weakness": 0, "stiff_neck": 0,
               "swelling_joints": 0, "movement_stiffness": 0, "spinning_movements": 0, "loss_of_balance": 0,
               "unsteadiness": 0, "weakness_of_one_body_side": 0, "loss_of_smell": 0,
               "bladder_discomfort": 0, "foul_smell_of urine": 0, "continuous_feel_of_urine": 0,
               "passage_of_gases": 0, "internal_itching": 0, "toxic_look_(typhos)": 0,
               "depression": 0, "irritability": 0, "muscle_pain": 0, "altered_sensorium": 0,
               "red_spots_over_body": 0, "belly_pain": 0, "abnormal_menstruation": 0,
               "dischromic _patches": 0, "watering_from_eyes": 0, "increased_appetite": 0, "polyuria": 0,
               "family_history": 0, "mucoid_sputum": 0, "rusty_sputum": 0, "lack_of_concentration": 0,
               "visual_disturbances": 0, "receiving_blood_transfusion": 0,
               "receiving_unsterile_injections": 0, "coma": 0, "stomach_bleeding": 0,
               "distention_of_abdomen": 0, "history_of_alcohol_consumption": 0, "fluid_overload": 0,
               "blood_in_sputum": 0, "prominent_veins_on_calf": 0, "palpitations": 0,
               "painful_walking": 0, "pus_filled_pimples": 0, "blackheads": 0, "scurring": 0,
               "skin_peeling": 0, "silver_like_dusting": 0, "small_dents_in_nails": 0,
               "inflammatory_nails": 0, "blister": 0, "red_sore_around_nose": 0, "yellow_crust_ooze": 0,
               }
    # print(len(disease))
    name = request.GET.get("name")
    age = request.GET.get("age")
    gender = request.GET.get("gender")
    height = request.GET.get("height")
    weight = request.GET.get("weight")

    symptom1 = request.GET.get("symptom1")
    symptom2 = request.GET.get("symptom2")
    symptom3 = request.GET.get("symptom3")
    symptom4 = request.GET.get("symptom4")
    symptom5 = request.GET.get("symptom5")

    if symptom1 in disease:
        disease[symptom1] = 1
    if symptom2 in disease:
        disease[symptom2] = 1
    if symptom3 in disease:
        disease[symptom3] = 1
    if symptom4 in disease:
        disease[symptom4] = 1
    if symptom5 in disease:
        disease[symptom5] = 1

    lis = []
    # print(lis)
    for elem in disease.values():
        lis.append(elem)

    list_symptoms = [lis]
    # print(len(list_symptoms))
    output_decision = clf3.predict(list_symptoms)
    output_random = clf4.predict(list_symptoms)
    output_navie = gnb.predict(list_symptoms)

    # consult_doctor codes----------

    #   doctor_specialization = ["Rheumatologist","Cardiologist","ENT specialist","Orthopedist","Neurologist",
    #                             "Allergist/Immunologist","Urologist","Dermatologist","Gastroenterologist"]
    predicted_disease = output_navie[0]

    Rheumatologist = ['Osteoarthristis', 'Arthritis']

    Cardiologist = ['Heart attack', 'Bronchial Asthma', 'Hypertension ']

    ENT_specialist = ['(vertigo) Paroymsal  Positional Vertigo', 'Hypothyroidism']

    Orthopedist = []

    Neurologist = ['Varicose veins', 'Paralysis (brain hemorrhage)', 'Migraine', 'Cervical spondylosis']

    Allergist_Immunologist = ['Allergy', 'Pneumonia',
                              'AIDS', 'Common Cold', 'Tuberculosis', 'Malaria', 'Dengue', 'Typhoid']

    Urologist = ['Urinary tract infection',
                 'Dimorphic hemmorhoids(piles)']

    Dermatologist = ['Acne', 'Chicken pox', 'Fungal infection', 'Psoriasis', 'Impetigo']

    Gastroenterologist = ['Peptic ulcer diseae', 'GERD', 'Chronic cholestasis', 'Drug Reaction', 'Gastroenteritis',
                          'Hepatitis E',
                          'Alcoholic hepatitis', 'Jaundice', 'hepatitis A',
                          'Hepatitis B', 'Hepatitis C', 'Hepatitis D', 'Diabetes ', 'Hypoglycemia']

    if predicted_disease in Rheumatologist:
        consultdoctor = "Rheumatologist"

    if predicted_disease in Cardiologist:
        consultdoctor = "Cardiologist"


    elif predicted_disease in ENT_specialist:
        consultdoctor = "ENT specialist"

    elif predicted_disease in Orthopedist:
        consultdoctor = "Orthopedist"

    elif predicted_disease in Neurologist:
        consultdoctor = "Neurologist"

    elif predicted_disease in Allergist_Immunologist:
        consultdoctor = "Allergist/Immunologist"

    elif predicted_disease in Urologist:
        consultdoctor = "Urologist"

    elif predicted_disease in Dermatologist:
        consultdoctor = "Dermatologist"

    elif predicted_disease in Gastroenterologist:
        consultdoctor = "Gastroenterologist"

    else:
        consultdoctor = "other"

    personal_details.clear()
    symptoms.clear()
    final_output.clear()

    personal_details.append("Name: " + name)
    personal_details.append("Age: " + age)
    personal_details.append("Gender: " + gender)
    personal_details.append("Height: " + height)
    personal_details.append("Weight: " + weight)

    symptoms.append("Symptom1: " + symptom1)
    symptoms.append("Symptom2: " + symptom2)
    symptoms.append("Symptom3: " + symptom3)
    symptoms.append("Symptom4: " + symptom4)
    symptoms.append("Symptom5: " + symptom5)

    final_output.append("Predicted disease: " + predicted_disease)
    final_output.append("Consult to a: " + consultdoctor)

    return render(request, "predict/prediction.html",
                  {'decision':output_decision, 'random':output_random,
                   'navie':predicted_disease, 'acc_tree':accuracy_score_tree,
                   'acc_random':accuracy_score_random, 'acc_naive':accuracy_score_naive})
