from numpy.random import normal as N
from math import exp, sqrt
import numpy as np
from random import randint


def fitness(chromossome): ### Entrada eh uma lista com 30 floats
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
    return round(fit,10)

def mutation_case1(indiv):###entrada eh uma lista da forma [cromossomo,fitness, sigma] Onde cromossomo eh uma lista e fitness e sigma sao floats
    chromosome = indiv[0]
    sigma = indiv[-1]
    mutationed = []
    n = len(chromosome)

    epson_0 = 0.2
    learning_rate = 1 / sqrt(n)
    sigma_line = sigma * exp(learning_rate * N(0, 1))

    if abs(sigma_line) < epson_0:
        sigma_line = epson_0

    for xi in chromosome: ###sigma nao eh o ultimo elemento da lista de cromossomo e sim do individuo
        mutationed.append(xi + sigma_line * N(0, 1))

    ### Mutacao tem que retornar individuo no formato: [cromossomo, fitness, sigma]
    mutationedF = [mutationed, fitness(mutationed), sigma_line]

    return mutationedF

#mutacao basica: troca aleatoriamente posicao de dois elementos, alterando a composicao da cesta
def mutation_case2(indiv):
    chromosome = indiv["alimentos_quantidade"]
    n = len(chromosome)
    pos_aleat1 = randint(0,n-1)
    pos_aleat2 = randint(0,n-1)
    aux = 0
    aux = chromosome[pos_aleat1]
    chromosome[pos_aleat1] = chromosome[pos_aleat2]
    chromosome[pos_aleat2] = aux


    return indiv


if __name__ == '__main__':

    print(mutation_case1(list(range(31))))
    print(fitness([float[i] for i in range[30]]))
