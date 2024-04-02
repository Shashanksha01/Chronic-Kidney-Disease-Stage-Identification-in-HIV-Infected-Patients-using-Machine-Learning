from django.db import models

# Create your models here.
from django.db.models import CASCADE


class ClientRegister_Model(models.Model):
    username = models.CharField(max_length=30)
    email = models.EmailField(max_length=30)
    password = models.CharField(max_length=10)
    phoneno = models.CharField(max_length=10)
    country = models.CharField(max_length=30)
    state = models.CharField(max_length=30)
    city = models.CharField(max_length=30)

class kidney_model(models.Model):


    id1=models.CharField(max_length=300)
    age=models.CharField(max_length=300)
    bp=models.CharField(max_length=300)
    sg=models.CharField(max_length=300)
    al=models.CharField(max_length=300)
    su=models.CharField(max_length=300)
    rbc=models.CharField(max_length=300)
    pc=models.CharField(max_length=300)
    pcc=models.CharField(max_length=300)
    ba=models.CharField(max_length=300)
    bgr=models.CharField(max_length=300)
    bu=models.CharField(max_length=300)
    sc=models.CharField(max_length=300)
    sod=models.CharField(max_length=300)
    pot=models.CharField(max_length=300)
    hemo=models.CharField(max_length=300)
    pcv=models.CharField(max_length=300)
    wc=models.CharField(max_length=300)
    rc=models.CharField(max_length=300)
    htn=models.CharField(max_length=300)
    dm=models.CharField(max_length=300)
    cad=models.CharField(max_length=300)
    appet=models.CharField(max_length=300)
    pe=models.CharField(max_length=300)
    ane=models.CharField(max_length=300)



class kidney_disease_model(models.Model):

    id1 = models.CharField(max_length=300)
    age = models.CharField(max_length=300)
    bp = models.CharField(max_length=300)
    sg = models.CharField(max_length=300)
    al = models.CharField(max_length=300)
    su = models.CharField(max_length=300)
    rbc = models.CharField(max_length=300)
    pc = models.CharField(max_length=300)
    pcc = models.CharField(max_length=300)
    ba = models.CharField(max_length=300)
    bgr = models.CharField(max_length=300)
    bu = models.CharField(max_length=300)
    sc = models.CharField(max_length=300)
    sod = models.CharField(max_length=300)
    pot = models.CharField(max_length=300)
    hemo = models.CharField(max_length=300)
    pcv = models.CharField(max_length=300)
    wc = models.CharField(max_length=300)
    rc = models.CharField(max_length=300)
    htn = models.CharField(max_length=300)
    dm = models.CharField(max_length=300)
    cad = models.CharField(max_length=300)
    appet = models.CharField(max_length=300)
    pe = models.CharField(max_length=300)
    ane = models.CharField(max_length=300)
    prediction=models.CharField(max_length=300)

class detection_accuracy_model(models.Model):

    names = models.CharField(max_length=300)
    ratio = models.CharField(max_length=300)

class detection_ratio_model(models.Model):

    names = models.CharField(max_length=300)
    ratio = models.CharField(max_length=300)



