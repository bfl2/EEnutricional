from numpy.random import normal as N
from math import exp, sqrt
import numpy as np
import random
import nutrientesDataset as nutdts


def getAboveTargetNut(indiv):
    i = 0
    sum = sumNutrientes(indiv)
    for nut in sum:
        if (sum[nut] > nutdts.target[nut]):
            i += 1
    return i


def get_alimento(id):
    produtoCopy = dict(nutdts.nutDataset[id])
    return produtoCopy


def sumNutrientes(indiv):
    totalNutrientes = {'proteina': 0, 'lipideos': 0, 'colesterol': 0, 'carboidrato': 0, 'fibra_alimentar': 0,
                       'calcio': 0, 'magnesio': 0, 'manganes': 0, 'fosforo': 0,
                       'ferro': 0, 'sodio': 0, 'potassio': 0, 'cobre': 0, 'zinco': 0, 'vitamina_c': 0, 'kcal': 0}
    i = 0
    for alimento_id in indiv["alimentos_id"]:  # Somando os nutrientes
        alimento = get_alimento(alimento_id)
        for nutriente in totalNutrientes:
            totalNutrientes[nutriente] = totalNutrientes[nutriente] + alimento[nutriente]*indiv["alimentos_quantidade"][i]
        i+=1

    return totalNutrientes

def fitness(indiv): #o individuo eh uma cesta de alimentos
    fitnessDebugFlag = False
    fit = 0
    totalNutrientes = sumNutrientes(indiv)
    pesosNut1 = [300, 200, 100, 4, 10, 10, 20, 10, 10, 1, 5, 100, 100, 7, 10, 1000]
    pesosNut2 = [300, 200, 100, 10, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2000]
    pesosNutrientes = pesosNut1
    pesosKey = ["proteina","lipideos","colesterol","carboidrato","fibra_alimentar","calcio","magnesio","manganes","fosforo","ferro","sodio","potassio","cobre","zinco","vitamina_c","kcal"]

    difPercentual = []
    for key in totalNutrientes:
        frac = abs(totalNutrientes[key] - nutdts.target[key]) / nutdts.target[key]
        if(totalNutrientes[key] < nutdts.target[key]):
            frac =( nutdts.target[key]/(totalNutrientes[key]+0.1)-1)

        difPercentual.append(frac) # diferenca absoluta percentual do


    difPercentualWeighted = [a * b for a, b in zip(difPercentual, pesosNutrientes)]
    if(fitnessDebugFlag == True):
        print(difPercentual)
        print(difPercentualWeighted, len(difPercentual))
        print(totalNutrientes)
    fit = sum(difPercentualWeighted)
    indiv["fitness"] = fit

    return fit


# mutacao basica: troca aleatoriamente posicao de dois elementos, alterando a composicao da cesta
def mutation_case2(indiv):
    chromosome = indiv["alimentos_quantidade"]
    sigma_values = indiv["sigma"]

    n = len(chromosome)
    prob_target = getAboveTargetNut(indiv) / 16.0  # 16 eh o numero de nutrientes
    rolet = 0
    pos_aleat = random.randint(0, n - 1)
    if(rolet<prob_target):
        sigma_values[pos_aleat] -= 1
    else:
        sigma_values[pos_aleat] += 1

    chromosome[pos_aleat] += sigma_values[pos_aleat]
    chromosome[pos_aleat] = max(chromosome[pos_aleat],0)

    return indiv

def mutation_case1(indiv):
    chromosome = indiv["alimentos_quantidade"]
    n = len(chromosome)
    pos_aleat1 = random.randint(0,n-1)
    pos_aleat2 = random.randint(0,n-1)
    aux = 0
    aux = chromosome[pos_aleat1]
    chromosome[pos_aleat1] = chromosome[pos_aleat2]
    chromosome[pos_aleat2] = aux


    return indiv
