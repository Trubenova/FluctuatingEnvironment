def InitPop(n,Which):  #generates a random bitstring 50:50, ot all zeros if specified
    if Which==1:
        genome=n*[0]
    else:
        genome=sum(np.random.randint(2, size=(1,n)))  #for random init, cca 50:50\n"
    
    
    return genome

def Mutate(genome):     #Takes and returns genome with random bit mutated. 
    NewGenome=list(genome)
    i=random.randint(0,len(genome)-1)
    NewGenome[i]=(NewGenome[i]-1)**2
    return NewGenome

def GenerateEnviro(t, k, tau):   #generates string of 1 to k values, tau repeats, total length t*tau
    Enviro=[]
    threats=range(1,k+1,1)
    random.shuffle(threats)
    for j in range(0,t,1):
        for i in threats:
            new=tau*[i]
            Enviro=Enviro+new
    return Enviro

def Fitness(genome, Threat,l):   #calculates fitness as a sum of all ones in a kth block (threat)
    ThreatBlock=genome[(Threat-1)*l:Threat*l]
    GenFitness=sum(ThreatBlock)
    return GenFitness

def OneIteration(genotype, Threat, l, p, N):   
    #generates new mutants, calculates fitness of both according to the given thread,  
    #returns one of them. p- prob. of acceptance of the better one
    NewGenotype=Mutate(genotype)
    GenFitness=Fitness(genotype, Threat, l)
    NewFitness=Fitness(NewGenotype, Threat, l)
    if NewFitness==GenFitness: 
        a=random.random()
        if a<1/float(N):
            genotype=NewGenotype   #accet neutral mutation
            GenFitness=NewFitness
    elif NewFitness>GenFitness:   #add variable prob of fixation. 
        d=random.random()
        if d<p:
            genotype=NewGenotype
            GenFitness=NewFitness
    return genotype, GenFitness
    

def AdaptationTime(k, l, N, p):  #optimises one population IN ONE ENVIRO!!, returns time neccessary
    
    
    n=k*l   # total length of the genome, k traits of length l
    FitnessArray=[];
    Onemax=[];
    
    genome=InitPop(n,2)
    Fnow=l/2  #random init of fitness. 
    while Fnow <l:   # to find the adaptation time, do until optimized
        [genome, GenFitness]=OneIteration(genome,3,l, p, N)
        #Onemax.append(sum(genome))
        FitnessArray.append(GenFitness)
        Fnow=GenFitness
    Topt=len(FitnessArray)
    #print Topt
    #plt.plot(Onemax)
    #plt.plot(FitnessArray)
    #print FitnessArray[-1]
    #print FitnessArray[Topt-1]
    return Topt

def OneParamSet(k,l,N,p, it):   #for a given parameter set, finds average of opt. times and variance
    OptTimes=[]
    for i in range(it):
        Topt=AdaptationTime(k, l, N,p)
        OptTimes.append(Topt)
    MeanOT= np.mean(OptTimes)
    STDOT= np.std(OptTimes)
    return MeanOT, STDOT


import numpy as np
import random


k=10
N=100
p=0.9
It=100
l=50
n=k*l
lrange=range(5,105,5)
krange=range(5,105,5)
prange=range(1,11, 1)
Nrange=range(10,10000,300)
Priemery =[]
Deviacie=[]
Tanalytical=[]


for i in prange:   #this       CHANGE THIS TO INVESTIGATE RUNTIME OF VARIOUS PARAMETERS. 
    p=i/10.0   #this   CHANGE THIS TO INVESTIGATE RUNTIME OF VARIOUS PARAMETERS. 
    #k=i
    [MeanOT, STDOT]=OneParamSet(k,l,N,p,It)
    TAN=k*l*(np.log(l)-np.log(2)+1)/p
    Priemery.append(MeanOT)
    Deviacie.append(STDOT)
    Tanalytical.append(TAN)

#Priemery=np.array(Priemery)
#Deviacie=np.array(Deviacie)
#Tanalytical=np.array(Tanalytical)


MyX=prange         #this  CHANGE THIS TO INVESTIGATE RUNTIME OF VARIOUS PARAMETERS. 
print MyX
print Priemery
print Deviacie
print Tanalytical


FileName=('M1OptTimeP.txt') #this  CHANGE THIS TO INVESTIGATE RUNTIME OF VARIOUS PARAMETERS. 
ouf = open(FileName, "w")
ouf.write("p n k l it")
ouf.write('\n')
ouf.write(str(p)) 
ouf.write('\n')
ouf.write(         str(n)) 
ouf.write('\n')
ouf.write(          str(k)) 
ouf.write('\n')
ouf.write(          str(l)) 
ouf.write('\n')
ouf.write(          str(It))

ouf.write('\n')
ouf.write("My X axis")
ouf.write('\n')
ouf.write(str(MyX))

ouf.write('\n')
ouf.write("Priemery")
ouf.write('\n')
ouf.write(str(Priemery))

ouf.write('\n')
ouf.write("Deviacie")
ouf.write('\n')
ouf.write(str(Deviacie))

ouf.write('\n')
ouf.write("Tanalytical")
ouf.write('\n')
ouf.write(str(Tanalytical))
ouf.close()

print len(MyX)
print len(Priemery)
print len(Deviacie)
