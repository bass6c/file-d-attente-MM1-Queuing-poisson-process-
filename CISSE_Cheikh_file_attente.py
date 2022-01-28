import numpy as np
import matplotlib.pyplot as plt
import numpy.random as rd
import matplotlib.pyplot as plt
from math import *

#file d'attente M/M/1

def file_attente(Lambda,beta,Tmax):
    """"Retourne le nombre de client dans la file
    Z et l'intervalle de temps T """
    Z = [0,]
    T = [0,]
    t = 0
    while t < Tmax:
        if Z[-1] == 0 :
          t +=rd.exponential(1/Lambda)
          T.append(t)
          Z.append(1)
        else :
          t+=rd.exponential(1/(Lambda+beta))
          T.append(t)
          y  = rd.uniform()
          if y < Lambda/(Lambda+beta) : 
            Z.append(Z[-1]+1)
          else :
            Z.append(Z[-1] - 1)
    return Z,T
def extraire_temps(Lambda,beta,Tmax):
    t = 0
    Tarr = [] #temps d'arrivee
    Tsor = []   # temps de sortie
    Z = [0]
    while t < Tmax :
      if Z[-1] == 0:
        t+=rd.exponential(1/Lambda)
        Tarr.append(t)
        Z.append(1)
      else :
          y = rd.uniform()
          t +=rd.exponential(1/(Lambda+beta))
          if y <= Lambda/(Lambda+beta):
            Tarr.append(t)
            Z.append(Z[-1]+1)
          else:
            Tsor.append(t)
            Z.append(Z[-1] - 1)
    return Tarr,Tsor

#File d'attente M/M/2

def file_attente2(Lambda,beta,Tmax):
    Z = [0]
    T = [0]
    t = 0
    while t < Tmax:
        if Z[-1] == 0 :
            t+=rd.exponential(1/(2*Lambda))
            T.append(t)
            Z.append(1)
        if Z[-1] == 1 :
            t+=rd.exponential(1/(2*Lambda+beta))
            T.append(t)
            y = rd.uniform()
            if y < (2*Lambda)/(2*Lambda+beta):
                Z.append(Z[-1]+1)
            else :
                Z.append(Z[-1]-1)
        else :
            t+=rd.exponential(1/(2*Lambda + 2*beta))
            T.append(t)
            y = rd.uniform()
            if y < (2*Lambda)/(2*Lambda+2*beta):
                Z.append(Z[-1]+1)
            else :
                Z.append(Z[-1]-1)
        
    return Z,T

def extraire_temps2(Lambda,beta,Tmax):
    Z = [0]
    Tarr = []
    Tsor = []
    t = 0
    while t < Tmax:
        if Z[-1] == 0 :
            t+=rd.exponential(1/(2*Lambda))
            Tarr.append(t)
            Z.append(1)
        if Z[-1] == 1 :
            t+=rd.exponential(1/(2*Lambda+beta))
            y = rd.uniform()
            if y < (2*Lambda)/(2*Lambda+beta):
                Tarr.append(t)
                Z.append(Z[-1]+1)
            else :
                Tsor.append(t)
                Z.append(Z[-1]-1)
        else :
            t+=rd.exponential(1/(2*Lambda + 2*beta))
            y = rd.uniform()
            if y < (2*Lambda)/(2*Lambda+2*beta):
                Tarr.append(t)
                Z.append(Z[-1]+1)
            else :
                Tsor.append(t)
                Z.append(Z[-1]-1)
        
    return Tarr,Tsor
  

print("=" * 100)
s = " " *35
print(s + "File D'attente M/M/1")
print("=" * 100)
print("\n")
print("a. Representation du nombre de client present pour les deux files .")
Lambda = 3
beta = 9
Tmax = 10
Z1,T1 = file_attente(Lambda, beta,Tmax)
Z2,T2 = file_attente(Lambda, beta, Tmax)
plt.figure(figsize=(8,8))
plt.title("Le nombre de client Z en fonction des temps d'arrives T: M/M/1")
plt.step(T1,Z1, where ="post", label = "Z1")
plt.step(T2,Z2, where = "post", label = "Z2")
plt.legend(loc = "upper right")
plt.show()
print("\n")

print("b. Une estimation theorique du nombre totale de client en attente\n")
Lambda = 3
beta = 9
Tmax = 1000
Z,T = file_attente(Lambda, beta, Tmax)
Z = np.asarray(Z)
a = 2*Lambda/(beta - Lambda)
print("En regime stationaire le nombre tolal de client en attente est ",Z.mean())
print("sensiblement egal a la valeur theorique ", a)
print("\n")

print("c. Le temps passé par les n premiers clients dans la file \n")
Lambda = 3
beta = 9
Tmax = 10000
T1, T2 = extraire_temps(Lambda, beta, Tmax)
T1, T2 = np.asarray(T1), np.asarray(T2)
n = min(len(T1),len(T2))
T = T2[:n] - T1[:n]
"""Le temps moyen passé par un clent dans la file en regime stationaire 
      suit une exponentielle de parametre (beta - lambda)"""

plt.figure(figsize=(8,8))
plt.title("Loi du temps passé par les clients dans la file: M/M/1")
plt.hist(T, bins = 25, density=True, label = "E(beta - lambda)")
plt.legend(loc = "upper right")
plt.show()
print("Le temps passé par les n premiers clients dans la file est \n", T.sum())

print("d. Estimation du temps moyen passé par un client dans la file\n")
Tsejour = T.sum()/len(T)
print("Temps moyen passé par un client dans la file est", Tsejour)
aa = 1/(beta - Lambda)
"""la valeur theorique du temps moyen passe par un client dans la file
est la moyenne d'une exponentielle E(beta - Lambda)"""
print("la valeur theorique : 1/(beta - lambda) est ",aa)
print("\n")

print("=" * 100)
s = " " *35
print(s + "File D'attente M/M/2")
print("=" * 100)
print("\n")

"""
Transition du systeme: 
Nous avons maintenant une file d'attente M/M/2 ou les temps d'arrives sont des E(2lambda) 
et les temps de services E(beta).  
3 situations se presentent devans nous:
- L'arrivee du personne dans le cas ou la file est vide (t = E(2lambda), Proba = 1)
- L'arrivee d'une personne dans le cas ou la file contient
une seule personne au guichet (t = E(2lambda + beta), Proba = Bernoulli(2lamba/(2lambda + beta)) )
- L'arrivee d'une personne dans le cas ou le guichet contient n >= 2 personnes
(t = E(2lamda+2beta), Proba = Bernoulli(2lamba/(2lambda + 2beta)) 

"""
print("b. Le nombre de client present dans la file. ")
Lambda = 3
beta = 9
Tmax = 10
Z,T = file_attente2(Lambda, beta, Tmax)
plt.figure(figsize=(8,8))
plt.title("Le nombre de client Z en fonction des temps d'arrives T: M/M/2")
plt.step(T,Z, where ="post", label = "Z")
plt.legend(loc = "upper right")
plt.show()
print("\n")

print("c. Une estimation Monte carlo du nombre de client en attente au regime stationnaire\n")
Lambda = 3
beta = 9
Tmax = 1000
Z,T = file_attente2(Lambda, beta, Tmax)
Z = np.asarray(Z)
print("En regime stationaire le nombre tolal de client en attente est ",Z.mean())
print("Il ya em moyenne plus de client dans la file, le fonctionnement du point de vue du nombre de client  n'a pas ete ameliore")
print("\n")
print("d. Voir code line 80\n")
print("e. Une estimation Monte Carlo du temps moyen de service\n")
Lambda = 3
beta = 9
Tmax = 10000
T1, T2 = extraire_temps2(Lambda, beta, Tmax)
T1, T2 = np.asarray(T1), np.asarray(T2)
n = min(len(T2), len(T1))
T = T2[:n] - T1[:n]
print("Le temps moyen de service est ",T.mean())
print("Le fonctionnement a ete amelioré du point de vue des temps de service ")
print("\n")


