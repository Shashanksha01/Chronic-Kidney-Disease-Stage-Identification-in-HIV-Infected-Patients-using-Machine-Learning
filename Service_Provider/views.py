
from django.db.models import  Count, Avg
from django.shortcuts import render, redirect
from django.db.models import Count
from django.db.models import Q
import datetime
import xlwt
from django.http import HttpResponse
# Importing the libraries
import pandas as pd
import numpy as np
import re
from sklearn.ensemble import VotingClassifier
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.metrics import accuracy_score
from sklearn.metrics import f1_score

from sklearn.tree import DecisionTreeClassifier

# Create your views here.
from Remote_User.models import ClientRegister_Model,kidney_model,kidney_disease_model,detection_ratio_model,detection_accuracy_model


def serviceproviderlogin(request):
    if request.method  == "POST":
        admin = request.POST.get('username')
        password = request.POST.get('password')
        if admin == "Admin" and password =="Admin":
            detection_accuracy_model.objects.all().delete()
            return redirect('View_Remote_Users')

    return render(request,'SProvider/serviceproviderlogin.html')

def Find_Kidney_Disease_Ratio(request):
    detection_ratio_model.objects.all().delete()
    ratio = ""
    kword = 'Positive Stage'
    print(kword)
    obj = kidney_disease_model.objects.all().filter(Q(prediction=kword))
    obj1 = kidney_disease_model.objects.all()
    count = obj.count();
    count1 = obj1.count();
    ratio = (count / count1) * 100
    if ratio != 0:
        detection_ratio_model.objects.create(names=kword, ratio=ratio)

    ratio1 = ""
    kword1 = 'Negative Stage'
    print(kword1)
    obj1 = kidney_disease_model.objects.all().filter(Q(prediction=kword1))
    obj11 = kidney_disease_model.objects.all()
    count1 = obj1.count();
    count11 = obj11.count();
    ratio1 = (count1 / count11) * 100
    if ratio1 != 0:
        detection_ratio_model.objects.create(names=kword1, ratio=ratio1)


    obj = detection_ratio_model.objects.all()
    return render(request, 'SProvider/Find_Kidney_Disease_Ratio.html', {'objs': obj})

def View_Kidney_Disease_Positive_Details(request):

    keyword="Positive Stage"

    obj = kidney_disease_model.objects.all().filter(prediction=keyword)
    return render(request, 'SProvider/View_Kidney_Disease_Positive_Details.html', {'objs': obj})

def View_Remote_Users(request):
    obj=ClientRegister_Model.objects.all()
    return render(request,'SProvider/View_Remote_Users.html',{'objects':obj})

def ViewTrendings(request):
    topic = kidney_disease_model.objects.values('topics').annotate(dcount=Count('topics')).order_by('-dcount')
    return  render(request,'SProvider/ViewTrendings.html',{'objects':topic})


def charts(request,chart_type):
    chart1 = detection_ratio_model.objects.values('names').annotate(dcount=Avg('ratio'))
    return render(request,"SProvider/charts.html", {'form':chart1, 'chart_type':chart_type})

def charts1(request,chart_type):
    chart1 = detection_accuracy_model.objects.values('names').annotate(dcount=Avg('ratio'))
    return render(request,"SProvider/charts1.html", {'form':chart1, 'chart_type':chart_type})

def Find_Kidney_Disease_Status(request):

    obj =kidney_disease_model.objects.all()
    return render(request, 'SProvider/Find_Kidney_Disease_Status.html', {'list_objects': obj})

def likeschart(request,like_chart):
    charts =detection_accuracy_model.objects.values('names').annotate(dcount=Avg('ratio'))
    return render(request,"SProvider/likeschart.html", {'form':charts, 'like_chart':like_chart})


def Download_Trained_DataSets(request):

    response = HttpResponse(content_type='application/ms-excel')
    # decide file name
    response['Content-Disposition'] = 'attachment; filename="TrainedData.xls"'
    # creating workbook
    wb = xlwt.Workbook(encoding='utf-8')
    # adding sheet
    ws = wb.add_sheet("sheet1")
    # Sheet header, first row
    row_num = 0
    font_style = xlwt.XFStyle()
    # headers are bold
    font_style.font.bold = True
    # writer = csv.writer(response)
    obj = kidney_disease_model.objects.all()
    data = obj  # dummy method to fetch data.
    for my_row in data:
        row_num = row_num + 1

        ws.write(row_num, 0, my_row.id1, font_style)
        ws.write(row_num, 1, my_row.age, font_style)
        ws.write(row_num, 2, my_row.bp, font_style)
        ws.write(row_num, 3, my_row.sg, font_style)
        ws.write(row_num, 4, my_row.al, font_style)
        ws.write(row_num, 5, my_row.su, font_style)
        ws.write(row_num, 6, my_row.rbc, font_style)
        ws.write(row_num, 7, my_row.pc, font_style)
        ws.write(row_num, 8, my_row.pcc, font_style)
        ws.write(row_num, 9, my_row.ba, font_style)
        ws.write(row_num, 10, my_row.bgr, font_style)
        ws.write(row_num, 11, my_row.bu, font_style)
        ws.write(row_num, 12, my_row.sc, font_style)
        ws.write(row_num, 13, my_row.sod, font_style)
        ws.write(row_num, 14, my_row.pot, font_style)
        ws.write(row_num, 15, my_row.hemo, font_style)
        ws.write(row_num, 16, my_row.pcv, font_style)
        ws.write(row_num, 17, my_row.wc, font_style)
        ws.write(row_num, 18, my_row.rc, font_style)
        ws.write(row_num, 19, my_row.htn, font_style)
        ws.write(row_num, 20, my_row.dm, font_style)
        ws.write(row_num, 21, my_row.cad, font_style)
        ws.write(row_num, 22, my_row.appet, font_style)
        ws.write(row_num, 23, my_row.pe, font_style)
        ws.write(row_num, 24, my_row.ane, font_style)
        ws.write(row_num, 25, my_row.prediction, font_style)

    wb.save(response)
    return response


def train_model(request):
    detection_accuracy_model.objects.all().delete()
    df = pd.read_csv('kidney_disease.csv',encoding='latin-1')
    df
    df.columns

    def apply_measure(pottacium):
        if pottacium >= 3.6 and pottacium <= 5.2:
                   return 0  #status = "Negative"
        elif pottacium >= 5.2 or pottacium <= 3.6:
                   return 1 #status = "Positive"

    df['results'] = df['pot'].apply(apply_measure)

    cv = CountVectorizer(lowercase=False, strip_accents='unicode', ngram_range=(1, 1))
    X = df['id']
    y = df['results']

    X = cv.fit_transform(df['id'].apply(lambda X: np.str_(X)))

    models = []
    from sklearn.model_selection import train_test_split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20)
    X_train.shape, X_test.shape, y_train.shape

    #Naive Bayes
    print("Naive Bayes")
    from sklearn.naive_bayes import MultinomialNB
    NB = MultinomialNB()
    NB.fit(X_train, y_train)
    predict_nb = NB.predict(X_test)
    naivebayes = accuracy_score(y_test, predict_nb) * 100
    print(naivebayes)
    print(confusion_matrix(y_test, predict_nb))
    print(classification_report(y_test, predict_nb))
    models.append(('naive_bayes', NB))

    detection_accuracy_model.objects.create(names="Naive Bayes", ratio=naivebayes)

    # SVM Model
    print("SVM")
    from sklearn import svm
    lin_clf = svm.LinearSVC()
    lin_clf.fit(X_train, y_train)
    predict_svm = lin_clf.predict(X_test)
    svm_acc = accuracy_score(y_test, predict_svm) * 100
    print(svm_acc)
    print("CLASSIFICATION REPORT")
    print(classification_report(y_test, predict_svm))
    print("CONFUSION MATRIX")
    print(confusion_matrix(y_test, predict_svm))
    models.append(('svm', lin_clf))

    detection_accuracy_model.objects.create(names="SVM", ratio=svm_acc)

    # Logistic Regression
    print("Logistic Regression")

    from sklearn.linear_model import LogisticRegression
    reg = LogisticRegression(random_state=0, solver='lbfgs').fit(X_train, y_train)
    y_pred = reg.predict(X_test)
    print("ACCURACY")
    print(accuracy_score(y_test, y_pred) * 100)
    print("CLASSIFICATION REPORT")
    print(classification_report(y_test, y_pred))
    print("CONFUSION MATRIX")
    print(confusion_matrix(y_test, y_pred))
    models.append(('logistic', reg))

    detection_accuracy_model.objects.create(names="Logistic Regression", ratio=accuracy_score(y_test, y_pred) * 100)
    #Decision Tree Classifier
    print("Decision Tree Classifier")
    dtc = DecisionTreeClassifier()
    dtc.fit(X_train, y_train)
    dtcpredict = dtc.predict(X_test)
    print("ACCURACY")
    print(accuracy_score(y_test, dtcpredict) * 100)
    print("CLASSIFICATION REPORT")
    print(classification_report(y_test, dtcpredict))
    print("CONFUSION MATRIX")
    print(confusion_matrix(y_test, dtcpredict))
    models.append(('DecisionTreeClassifier', dtc))
    detection_accuracy_model.objects.create(names="Decision Tree Classifier", ratio=accuracy_score(y_test, dtcpredict) * 100)
    
    #SGD Classifier
    print("SGD Classifier")
    from sklearn.linear_model import SGDClassifier
    sgd_clf = SGDClassifier(loss='hinge', penalty='l2', random_state=0)
    sgd_clf.fit(X_train, y_train)
    sgdpredict = sgd_clf.predict(X_test)
    print("ACCURACY")
    print(accuracy_score(y_test, sgdpredict) * 100)
    print("CLASSIFICATION REPORT")
    print(classification_report(y_test, sgdpredict))
    print("CONFUSION MATRIX")
    print(confusion_matrix(y_test, sgdpredict))
    models.append(('SGDClassifier', sgd_clf))
    detection_accuracy_model.objects.create(names="SGD Classifier", ratio=accuracy_score(y_test, sgdpredict) * 100)

    #KNeighborsClassifier
    print("KNeighborsClassifier")
    from sklearn.neighbors import KNeighborsClassifier
    kn = KNeighborsClassifier()
    kn.fit(X_train, y_train)
    knpredict = kn.predict(X_test)
    print("ACCURACY")
    print(accuracy_score(y_test, knpredict) * 100)
    print("CLASSIFICATION REPORT")
    print(classification_report(y_test, knpredict))
    print("CONFUSION MATRIX")
    print(confusion_matrix(y_test, knpredict))
    models.append(('KNeighborsClassifier', kn))
    detection_accuracy_model.objects.create(names="KNeighborsClassifier", ratio=accuracy_score(y_test, knpredict) * 100)

    classifier = VotingClassifier(models)
    classifier.fit(X_train, y_train)
    y_pred = classifier.predict(X_test)

    ldata = 'Labeled_Data.csv'
    df.to_csv(ldata, index=False)
    df.to_markdown

    status = ''
    type = ''
    obj1 = kidney_model.objects.values('id1',
    'age',
    'bp',
    'sg',
    'al',
    'su',
    'rbc',
    'pc',
    'pcc',
    'ba',
    'bgr',
    'bu',
    'sc',
    'sod',
    'pot',
    'hemo',
    'pcv',
    'wc',
    'rc',
    'htn',
    'dm',
    'cad',
    'appet',
    'pe',
    'ane'
    )

    kidney_disease_model.objects.all().delete()
    for t in obj1:

        id1= t['id1']
        age= t['age']
        bp= t['bp']
        sg= t['sg']
        al= t['al']
        su= t['su']
        rbc= t['rbc']
        pc= t['pc']
        pcc= t['pcc']
        ba= t['ba']
        bgr= t['bgr']
        bu= t['bu']
        sc= t['sc']
        sod= t['sod']
        pot= t['pot']
        hemo= t['hemo']
        pcv= t['pcv']
        wc= t['wc']
        rc= t['rc']
        htn= t['htn']
        dm= t['dm']
        cad= t['cad']
        appet= t['appet']
        pe= t['pe']
        ane= t['ane']

        print(id1)

        review_data = [id1]
        vector1 = cv.transform(review_data).toarray()
        predict_text = classifier.predict(vector1)

        pred = str(predict_text).replace("[", "")
        pred1 = pred.replace("]", "")

        prediction = int(pred1)
        print(prediction)
        if (prediction == 0):
            val = 'Negative Stage'
        elif (prediction == 1):
            val = 'Positive Stage'

        print(val)


        kidney_disease_model.objects.create(id1=id1,
        age=age,
        bp=bp,
        sg=sg,
        al=al,
        su=su,
        rbc=rbc,
        pc=pc,
        pcc=pcc,
        ba=ba,
        bgr=bgr,
        bu=bu,
        sc=sc,
        sod=sod,
        pot=pot,
        hemo=hemo,
        pcv=pcv,
        wc=wc,
        rc=rc,
        htn=htn,
        dm=dm,
        cad=cad,
        appet=appet,
        pe=pe,
        ane=ane,
        prediction=val
        )

    obj = detection_accuracy_model.objects.all()
    return render(request,'SProvider/train_model.html', {'objs': obj})














