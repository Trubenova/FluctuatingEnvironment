
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
    GenFitness=2**(l-sum(ThreatBlock))
    GenFitness=1-GenFitness/(2.0**l)
    Fraction=sum(ThreatBlock)*1.0/l
    
    return GenFitness, Fraction

def OneIteration(genotype, Threat, l, p, N, B):   
    beta=B;
    #generates new mutants, calculates fitness of both according to the given thread,  
    #returns one of them. p- prob. of acceptance of the better one
    NewGenotype=Mutate(genotype)
    [GenFitness, GenFraction]=Fitness(genotype, Threat, l)
    [NewFitness, NewFraction]=Fitness(NewGenotype, Threat, l)
    Delta = NewFitness-GenFitness
    if Delta==0: 
        a=random.random()
        #print 'zero'
        if a<1/float(N):
            #print N
            genotype=NewGenotype   #accet neutral mutation
            GenFitness=NewFitness
            GenFraction=NewFraction
            #print 'zero accepted'
    elif Delta>0:   #add variable prob of fixation. 
        d=random.random()
        p=(1.0-np.exp(-beta*Delta))/(1.0-np.exp(-beta*N*Delta))   #toto je prob. 
        #print Delta
        
        #print 'this is d', d
        if d<p:
            genotype=NewGenotype
            GenFitness=NewFitness
            GenFraction=NewFraction
            #print 'this is p', p
            #print 'YES'
    return genotype, GenFitness, GenFraction
    





def EvolutionOneParamSet(k,l,N,p,tau, t, B):  #this runs simulations with variable environment, for tau
    #ACTUALLY LOOKS AT POPULATION, KEEPS ITS FITNESS, AND NUMBER OF ONES IN A FEW BLOCKS
    import numpy as np
    import random
    
    n=l*k
    FitnessArray=[];
    FractionArray=[];
    
    Onemax=[];
    Enviro=GenerateEnviro(t,k,tau)
    genome=InitPop(n,1)
    B1=[]
    B2=[]
    B3=[]
    print 'Initialisation done'
    for i in Enviro:  # RUNS through the whole time defined by generated environement
        [genome, GenFitness, GenFraction]=OneIteration(genome,i,l, p, N, B)  #possible mutation
        Block1=Fitness(genome,1,l)  #captures first 3 blocks
        Block2=Fitness(genome,2,l)
        Block3=Fitness(genome,3,l)
        B1.append(Block1)
        #B2.append(Block2)
        #B3.append(Block3)
        Onemax.append(sum(genome))
        FitnessArray.append(GenFitness)  #captures evolving fitness
        FractionArray.append(GenFraction)  #Captures evolvinf fraction
    #FitnessArray=np.array(FitnessArray)
    End2=len(FitnessArray)
    End1=End2-3*tau*k   #this will find a point before the end which is 
                        #5*timeperiod*all possible time period away frm the end
   
    FileName=('M1F2EvolutionWithK'+str(k)+'.txt') 
    #CHANGE THIS TO INVESTIGATE RUNTIME OF VARIOUS PARAMETERS. 
    ouf = open(FileName, "w")
    ouf.write("p n k l tau t")
    ouf.write('\n')
    ouf.write(str(p)) 
    ouf.write('\n')
    ouf.write(         str(n)) 
    ouf.write('\n')
    ouf.write(          str(k)) 
    ouf.write('\n')
    ouf.write(          str(l)) 
    ouf.write('\n')
    ouf.write(          str(tau)) 
    ouf.write('\n')
    ouf.write(          str(t))
    ouf.write('\n')
    ouf.write("Fraction")
    ouf.write('\n')
    ouf.write(str(FractionArray))
    ouf.write('\n')
    ouf.write("FITNESS")
    ouf.write('\n')
    ouf.write(str(FitnessArray))
    ouf.write('\n')
    ouf.write("Enviro")
    ouf.write('\n')
    ouf.write(str(Enviro))
    
    
    ouf.write('\n')
    ouf.write("Block1")
    ouf.write('\n')
    ouf.write(str(B1))

        
    #ouf.write('\n')
    #ouf.write("Block2")
    #ouf.write('\n')
    #ouf.write(str(B2))

        
    #ouf.write('\n')
    #ouf.write("Block3")
    #ouf.write('\n')
    #ouf.write(str(B3))

    ouf.close()

    
    
def MainRun():   #this runs evolution of one population for various parameters
    tau=1
    t=10000
    k=10
    N=100
    p=0.5
    It=10
    B=5000
    lrange=range(10,50,10)
    krange=[90,100]
    l=20
    prange=range(2,10,1)
    taurange=[3000,4000]
    #p=(1.0-np.exp(-beta*Delta))/(1.0-np.exp(-beta*N*Delta))
    
    for i in krange:  #CHANGE THIS TO INVESTIGATE RUNTIME OF VARIOUS PARAMETERS. 
        print i
        k=i #CHANGE THIS TO INVESTIGATE RUNTIME OF VARIOUS PARAMETERS. 
        EvolutionOneParamSet(k,l,N,p,tau, t, B)
    print 'All done!!!'

import numpy as np
import random


MainRun()








