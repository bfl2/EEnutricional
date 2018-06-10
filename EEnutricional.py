import crossOver as cross
import mutation as mut
import random
import numpy as np
from operator import itemgetter
import nutrientesDataset as nutdts




def displayIndiv(indiv):
    i =0
    for ali_id in indiv["alimentos_id"]:
        print("id:{} alimento:{} quantidade:{}".format(ali_id,get_alimento(ali_id)["descricao"],indiv["alimentos_quantidade"][i]))
        i+=1
    return




def fooIndiv():
    indiv = createIndiv()
    sample = random.sample(nutdts.alimentos_id, 10)
    for id in sample:
        add_alimento(indiv,id,1)
    return indiv



def createIndiv():
    ## alimentos_quantidade e alimentos_id possuem o mesmo tamanho, sendo os valores de cada indice i representantes
    ## de qual alimento do dataset eh este(alimentos_id) e sua quantidade(alimentos_quantidade)
    n = 60
    fit = "-1"
    alimentos_quantidade = []
    sigma = [round(random.uniform(-15, 15), 5) for x in range(n)]

    while (len(alimentos_quantidade) < n):
        alimentos_quantidade.append(round(random.uniform(0, 1)))

    indiv = {"fitness": fit, "alimentos_quantidade": alimentos_quantidade, "alimentos_id": nutdts.alimentos_id, "sigma":sigma}
    fit = fitness(indiv)
    indiv["fitness"] = fit


    return indiv

def add_alimento(indiv, produto_id, quantidade):
    done = False
    arr_index = 0
    if(type(produto_id)==int): #caso o id do produto seja passado, ao inves do dicionario do produto
        produto = get_alimento(produto_id)
        try:
            arr_index = indiv["alimentos_id"].index(produto_id)
            indiv["alimentos_quantidade"][arr_index] = round(max((indiv["alimentos_quantidade"][arr_index] + quantidade), 0)) #quantidade sempre positiva
        except:
            print("Id do produto:{} fora da selecao de ids".format(produto_id))
    else:
        print("add_alimento falhou, produto_id != int")

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
    pesosNutrientes = [3, 1, 1, 4, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 10]  # Ordem: proteina,lipideos,colesterol,carboidrato,fibra_alimentar,calcio,magnesio,
                                                                         # manganes,fosforo,ferro,sodio,potassio,cobre,zinco,vitamina_c,kcal

    difPercentual = []
    for key in totalNutrientes:
        difPercentual.append(abs(totalNutrientes[key]-nutdts.target[key])/nutdts.target[key]) # diferenca absoluta percentual do

    difPercentualWeighted = [a * b for a, b in zip(difPercentual, pesosNutrientes)]
    if(fitnessDebugFlag == True):
        print(difPercentual)
        print(difPercentualWeighted, len(difPercentual))
        print(totalNutrientes)
    fit = sum(difPercentualWeighted)

    return fit

### do EEAckley
#gera os individuos para o caso do vetor de sigmas
def generateIndiv2():
    n = 30
    sigma = [round(random.uniform(-15, 15), 5) for x in range(60)]
    chromossome= []

    while (len( chromossome) < n):
        chromossome.append(round(random.uniform(0,15), 5))
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
