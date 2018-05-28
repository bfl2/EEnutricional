from numpy.random import normal as N
from math import exp, sqrt
import numpy as np


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

#essa funcao implementa a segunda versao da estrategia evolutica considerando sigmas independentes
def mutation_case2(indiv):
    chromosome = indiv[0]
    sigma = indiv[-1]
    mutationed = chromosome[:]
    n = len(chromosome) 

    epson_0 = 0.0001 
    learning_rate = 1/sqrt(2*n)
    learning_rate_line = 1/sqrt(2*sqrt(n))
    
    var_fix = N(0,1)
    sigma_line = []
    
    for i in range(0,n): ###sigma nao eh o ultimo elemento da lista de cromossomo e sim do individuo
        var_aleat = N(0,1)
        
        sigma_line.append(sigma[i]*exp((learning_rate_line * var_fix) + (learning_rate * var_aleat)))
        
        if sigma_line[i] < epson_0:
            sigma_line[i] = epson_0
            
        mutationed[i] = (chromosome[i] + sigma_line[i] * var_aleat)
        aux = fitness(mutationed)
        if(aux > indiv[1]):
            mutationed[i] = chromosome[i]


    ### Mutacao tem que retornar individuo no formato: [cromossomo, fitness, sigma]
    mutationedF = [mutationed, fitness(mutationed), sigma_line]

    return mutationedF


if __name__ == '__main__':

    print(mutation_case1(list(range(31))))
    print(fitness([float[i] for i in range[30]]))
