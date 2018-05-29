import crossOver as cross
import mutation as mut
import random
import numpy as np
from operator import itemgetter
from nutrientesDataset import nutDataset


def removeFit(pop):
    res =[]
    for e in pop:
        res.append(e[0])
    return res


def generateIndivI():
    n = 30
    indiv = []
    while (len(indiv) < n):
        indiv.append(round(random.randint(-15, 15), 5))

    return indiv


def generateIndiv():
    n = 30
    sigma = 1.2
    chromossome= []
    while (len( chromossome) < n):
        chromossome.append(round(random.uniform(-15, 15), 5))
    fit = fitness(chromossome)
    indiv = [chromossome,fit,sigma]

    return indiv


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


def fitness(chromossome):
    c1=20
    c2=0.2
    c3=2*np.pi
    sum1 = 0
    sum2 = 0
    for xi in chromossome:
        sum1+= xi**2
        sum2+= np.cos(c3*xi)
    sum1 = sum1/len(chromossome)
    sum2 = sum2/len(chromossome)
    fit = -c1*np.exp(-c2*np.sqrt(sum1)) - np.exp(sum2) + c1 + np.e
    return round(fit,5)

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
