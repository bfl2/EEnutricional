import crossOver as cross
import mutation as mut
import random
import numpy as np
from operator import itemgetter
from nutrientesDataset import nutDataset
from nutrientesDataset import target





def fooIndiv():
    indiv = createIndiv()
    addProduto(indiv, getProduto(1), 3)
    addProduto(indiv, getProduto(2), 2)
    addProduto(indiv, getProduto(3), 1)
    addProduto(indiv, getProduto(4), 1)
    addProduto(indiv, getProduto(6), 1)
    addProduto(indiv, getProduto(6), 1)
    return indiv



def createIndiv():
    fit = "-1"
    cesta = []
    indiv ={"fitness":fit, "cesta":cesta}

    return indiv
def addProduto(indiv,produto,quantidade):
    done = False
    for prod in indiv["cesta"]:
        if(produto["_id"]==prod["_id"]):#checka se produto ja esta na lista
            prod["quantidade"] = prod["quantidade"] + quantidade
            done = True
            break
    if(not done):
        prod = dict(produto)#copia o dicionario de referencia do produto
        prod["quantidade"] = quantidade
        indiv["cesta"].append(prod)

    return indiv
def getProduto(id):
    produtoCopy = dict(nutDataset[id])
    return produtoCopy


def sumNutrientes(indiv):
    totalNutrientes = {'proteina': 0, 'lipideos': 0, 'colesterol': 0, 'carboidrato': 0, 'fibra_alimentar': 0,
                       'calcio': 0, 'magnesio': 0, 'manganes': 0, 'fosforo': 0,
                       'ferro': 0, 'sodio': 0, 'potassio': 0, 'cobre': 0, 'zinco': 0, 'vitamina_c': 0, 'kcal': 0}

    for alimento in indiv["cesta"]:  # Somando os nutrientes
        for nutriente in totalNutrientes:
            totalNutrientes[nutriente] = totalNutrientes[nutriente] + alimento[nutriente]*alimento["quantidade"]

    return totalNutrientes

def fitness(indiv): #o individuo eh uma cesta de alimentos
    fit = 0
    totalNutrientes = sumNutrientes(indiv)
    pesosNutrientes = [3,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2]
    difPercentual = []
    for key in totalNutrientes:
        difPercentual.append(abs(totalNutrientes[key]-target[key])/target[key]) # diferenca absoluta percentual do
    print(difPercentual)
    difPercentualWeighted = [a * b for a, b in zip(difPercentual, pesosNutrientes)]
    print(difPercentualWeighted, len(difPercentual))
    print(totalNutrientes)
    fit = sum(difPercentualWeighted)

    return fit


### do EEAckley
#gera os individuos para o caso do vetor de sigmas
def generateIndiv2():
    n = 30
    sigma = [round(random.uniform(-15, 15), 5) for x in range(30)]
    chromossome= []

    while (len( chromossome) < n):
        chromossome.append(round(random.uniform(-15, 15), 5))
    fit = fitness(chromossome)
    indiv = [chromossome, fit, sigma]

    return indiv


def generatePop(size):
    pop = []
    while (len(pop)< size):
        pop.append(generateIndiv2())
    pop = sorted(pop, key=itemgetter(1))
    return pop


def get2RandomParents(allParents):
    lenParents = len(allParents)
    i1 =0
    i2 =0
    while(i1==i2):
        i1 = random.randint(0,lenParents-1)
        i2 = random.randint(0,lenParents-1)
    parents = [allParents[i1],allParents[i2]]
    return parents


def generateChildren(allParents,childrenCount):
    sigma = 0.2
    children = []
    childrenList = []
    while (len(children)<childrenCount):
        parents = get2RandomParents(allParents)
        child = cross.recombination_2fixed_parents(parents[0], parents[1])
        #child = cross.recombination_all_random(allParents)
        #child = cross.recombination_all_parents(allParents)
        #child[2] = sigma
        child = mut.mutation_case2(child)
        children.append(child)
    childrenList = sorted(children, key=itemgetter(1))


    return childrenList


def getAvgFit(pop):
    sum = 0
    for c in pop:
        sum+=c[1]
    return sum/len(pop)


def EENutricional():

    childrenCount = 200
    parentCount = 30
    generationCount = 0
    condSaida = False
    parents = generatePop(parentCount) # Populacao inicial
    minFit = parents[0][1]

    ##Listas de saida
    minFitList =[]
    avgFitList =[]


    while(condSaida == False):
        print(generationCount)
        children = generateChildren(parents,childrenCount)
        parents = children[:parentCount]
        minFit = parents[0][1]
        avgFit = getAvgFit(parents)

        print("Geracao:{} Tamanho da populacao de pais:{} Avg Fitness:{} / Min Fitness:{}".format(generationCount,len(parents), round(avgFit,5),round(minFit,5)))
        minFitList.append(minFit)
        avgFitList.append(avgFit)

        #if(generationCount%10 == 0):
        #    print("population sigma values")
        #    print([i[2] for i in parents])

        generationCount += 1
        if(generationCount>200):
            condSaida=True


    bestIndiv = parents[0][0]
    dataset = {"avgFitList":avgFitList, "minFitList":minFitList,"generationCount":generationCount,"minFit":minFit, "avgFit":avgFit,"bestIndiv":bestIndiv}
    print("Best solution n={}//Fitness={} {}".format(len (parents[0][0]),parents[0][1],parents[0][0]))
    return dataset


if __name__ == "__main__":
    EENutricional()
