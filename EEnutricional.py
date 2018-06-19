#import crossOver as cross
import mutation as mut
import random
import numpy as np
from operator import itemgetter
import nutrientesDataset as nutdts

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

def buildIndiv(alimentos_quantidade,sigma):
    fit ="-1"

    indiv = {"fitness": fit, "alimentos_quantidade": alimentos_quantidade, "alimentos_id": nutdts.alimentos_id,
             "sigma": sigma}
    fit = fitness(indiv)
    indiv["fitness"]=fit

    return indiv



def displayIndiv(indiv):
    i =0
    nutKeys = ["proteina", "lipideos", "colesterol", "carboidrato", "fibra_alimentar", "calcio", "magnesio",
                "manganes", "fosforo", "ferro", "sodio", "potassio", "cobre", "zinco", "vitamina_c", "kcal"]
    for ali_id in indiv["alimentos_id"]:

        if(indiv["alimentos_quantidade"][i]>0):
            print("{} X {}".format(indiv["alimentos_quantidade"][i], get_alimento(ali_id)["descricao"]))
        i+=1
    sum = sumNutrientes(indiv)
    for nutriente in nutKeys:
        print ("{}: {}/{}".format(nutriente,round(sum[nutriente],3),nutdts.target[nutriente]));

    return

def displayPopFit(pop):
    i = 0
    for indiv in pop:
        print("indiv:{} Fitness:{}".format(i,indiv["fitness"]))
        i+=1




def concatListDict(list1, list2):
    for dict in list2:
        list1.append(dict)
    return list1




def generateIndiv():
    ## alimentos_quantidade e alimentos_id possuem o mesmo tamanho, sendo os valores de cada indice i representantes
    ## de qual alimento do dataset eh este(alimentos_id) e sua quantidade(alimentos_quantidade)
    n = 60
    fit = "-1"
    alimentos_quantidade = []
    sigma = [round(random.uniform(-3, 3), 2) for x in range(n)]

    while (len(alimentos_quantidade) < n):
        alimentos_quantidade.append(round(random.uniform(0, 1),1))

    indiv = {"fitness": fit, "alimentos_quantidade": alimentos_quantidade, "alimentos_id": nutdts.alimentos_id, "sigma":sigma}
    fit = fitness(indiv)
    indiv["fitness"] = fit


    return indiv

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


def generatePop(size):
    pop = []
    while (len(pop)< size):
        pop.append(generateIndiv())
    pop = sorted(pop, key=fitness)
    return pop


def get2RandomParents(allParents):
    lenParents = len(allParents)
    i1 =0
    i2 =0
    while(i1==i2):
        i1 = random.randint(0,lenParents-1)
        i2 = random.randint(0,lenParents-1)
    parents = [dict(allParents[i1]),dict(allParents[i2])]
    return parents


def generateChildren(allParents,childrenCount):
    children = []
    childrenList = []
    while (len(children)<childrenCount):
        parents = get2RandomParents(allParents)
        child = recombination_2fixed_parents(parents[0], parents[1])
        #child = mut.mutation_case2(child)
        #child = generateIndiv()
        children.append(child)



    return children



def getAvgFit(pop):
    sum = 0
    for c in pop:
        sum+=c["fitness"]
    return sum/len(pop)


def EENutricional():

    childrenCount = 200
    parentCount = 30
    generationCount = 0
    condSaida = False
    parents = generatePop(parentCount) # Populacao inicial
    minFit = parents[0]["fitness"]

    ##Listas de saida
    minFitList =[]
    avgFitList =[]


    while(condSaida == False):
        print(generationCount)
        children = generateChildren(parents,childrenCount)
        aux = concatListDict(parents,children)
        aux = sorted(aux, key=fitness)
        aux2 = random.sample(aux, 20)
        parents = concatListDict(aux[:10],aux2)
        parents = sorted(parents, key=fitness)

        minFit = parents[0]["fitness"]
        avgFit = getAvgFit(parents)

        print("Geracao:{} Tamanho da populacao de pais:{} Avg Fitness:{} / Min Fitness:{}".format(generationCount,len(parents), round(avgFit,5),round(minFit,5)))
        minFitList.append(minFit)
        avgFitList.append(avgFit)

        #if(generationCount%10 == 0):
        #    print("population sigma values")
        #    print([i[2] for i in parents])
        ##

        generationCount += 1
        if(generationCount>200):
            condSaida=True


    bestIndiv = dict(parents[0])
    dataset = {"avgFitList":avgFitList, "minFitList":minFitList,"generationCount":generationCount,"minFit":minFit, "avgFit":avgFit,"bestIndiv":bestIndiv}
    print("Best solution n={}//Fitness={} ".format(len (parents),parents[0]['fitness']))
    displayIndiv(parents[0])

    return dataset


if __name__ == "__main__":
    EENutricional()
