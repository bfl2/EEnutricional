from random import randint
import numpy as np
import nutrientesDataset as nutdts

def fitness(indiv): #o individuo eh uma cesta de alimentos
    fitnessDebugFlag = False
    fit = 0
    totalNutrientes = sumNutrientes(indiv)
    pesosNutrientes = [3, 1, 1, 4, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 10]  # Ordem:
    pesosKey = ["proteina","lipideos","colesterol","carboidrato","fibra_alimentar","calcio","magnesio","manganes","fosforo","ferro","sodio","potassio","cobre","zinco","vitamina_c","kcal"]

    difPercentual = []
    for key in totalNutrientes:
        difPercentual.append(abs(totalNutrientes[key]-nutdts.target[key])/nutdts.target[key]) # diferenca absoluta percentual do


    difPercentualWeighted = [a * b for a, b in zip(difPercentual, pesosNutrientes)]
    if(fitnessDebugFlag == True):
        print(difPercentual)
        print(difPercentualWeighted, len(difPercentual))
        print(totalNutrientes)
    fit = sum(difPercentualWeighted)
    indiv["fitness"] = fit

    return fit

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


def buildIndiv(alimentos_quantidade,sigma):
    fit ="-1"

    indiv = {"fitness": fit, "alimentos_quantidade": alimentos_quantidade, "alimentos_id": nutdts.alimentos_id,
             "sigma": sigma}
    fit = fitness(indiv)
    indiv["fitness"]=fit

    return indiv


#   Input Format ([Chromosome, Fitness, sigma])
def recombination_2fixed_parents(parent_1, parent_2):

    """Cada gene do filho eh a média de cada gene dos pais"""

    alimentos_qtd_1 = parent_1["alimentos_quantidade"]
    alimentos_qtd_2 = parent_2["alimentos_quantidade"]

    sigma_1 = parent_1["sigma"]
    sigma_2 = parent_2["sigma"]

    zip_alimentos = zip(alimentos_qtd_1, alimentos_qtd_2)
    zip_sigmas = zip(list(sigma_1), list(sigma_2))

    child = [round((x[0] + x[1]), 1) / 2 for x in zip_alimentos]
    sigma_child = [round((s[0] + s[1]), 1) / 2 for s in zip_sigmas]

    return buildIndiv(child, sigma_child)


def recombination_2fixed_random(parent_1, parent_2):

    """Cada gene do filho eh a escolha aleatoria do gene do primeiro ou segundo pai"""
    alimentos_qtd_1 = parent_1["alimentos_quantidade"]
    alimentos_qtd_2 = parent_2["alimentos_quantidade"]

    sigma_1 = parent_1["sigma"]
    sigma_2 = parent_2["sigma"]

    zip_alimentos = zip(alimentos_qtd_1, alimentos_qtd_2)
    zip_sigmas = zip(list(sigma_1), list(sigma_2))

    child = [x[randint(0, 1)] for x in zip_alimentos]
    sigma_child = [s[randint(0, 1)] for s in zip_sigmas]


    return buildIndiv(child, sigma_child)


#   Receive a population of individuals
def recombination_all_parents(all_parents):

    """Cada gene do filho eh a média de cada gene dos pais escolhidos randomicamente"""

    tuple_parents = []
    tuple_sigmas = []
    size = len(all_parents)
    num_gene = len(all_parents[0][0])
    is_float = False

    for i in range(num_gene):
        p1 = all_parents[randint(0, size - 1)]
        p2 = all_parents[randint(0, size - 1)]

        tuple_parents.append((p1[0][i], p2[0][i]))

        if type(p1[2]) is float:
            tuple_sigmas.append((p1[2], p2[2]))
            is_float = True
        else:
            tuple_sigmas.append((p1[2][i], p2[2][i]))

    child = [(x[0] + x[1])/2 for x in tuple_parents]
    sigma_child = [(s[0] + s[1])/2 for s in tuple_sigmas]

    fitness_child = fitness(child)

    if is_float:
        sigma_child = sigma_child[randint(0, num_gene-1)]

    return [child, fitness_child, sigma_child]


def recombination_all_random(all_parents):

    """Cada gene do filho eh a escolha aleatoria do gene do primeiro ou segundo pai
        escolhidos randomicamente"""

    tuple_parents = []
    tuple_sigmas = []
    size = len(all_parents)
    num_gene = len(all_parents[0][0])
    is_float = False

    for i in range(num_gene):
        p1 = all_parents[randint(0, size - 1)]
        p2 = all_parents[randint(0, size - 1)]

        tuple_parents.append((p1[0][i], p2[0][i]))

        if type(p1) is float:
            tuple_sigmas.append((p1[2], p2[2]))
            is_float = True
        else:
            tuple_sigmas.append((p1[2][i], p2[2][i]))

    child = [x[randint(0, 1)] for x in tuple_parents]
    sigma_child = [s[randint(0, 1)] for s in tuple_sigmas]

    fitness_child = fitness(child)

    if is_float:
        sigma_child = sigma_child[randint(0, num_gene-1)]

    return [child, fitness_child, sigma_child]


#   Basic Test
if __name__ == '__main__':

    p1 = [list(range(30)), 12.3, 5.0]
    p2 = [list(range(30)), 52.3, 2.0]

    pop = [p1, p2]
    print(recombination_2fixed_parents(p1, p2))
    print(recombination_all_parents(pop))

    print(recombination_2fixed_parents.__doc__)