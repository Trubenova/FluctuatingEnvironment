


def InitPop(n,Which,k):  #generates a random bitstring 50:50, ot all zeros if specified
    if Which==1:
        genome=n*[0]
        genome=np.array(genome)
    if Which==3:
        genome0=sum(np.random.randint(k, size=(1,n)))
        genome=[x+1 for x in genome0]
    else:
        genome=sum(np.random.randint(2, size=(1,n)))  #for random init, cca 50:50\n"
    
    return genome

def Mutate(genome, k):     #Takes and returns genome with random bit mutated. 
    NewGenome=list(genome)
    i=random.randint(0,len(genome)-1)
    O=NewGenome[i]
    Pl=random.randint(1,k-1)
    j= (O-1-Pl)%k+1
    NewGenome[i]=j
    NewGenome=np.array(NewGenome)
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

def Fitness(genome, Threat,l=1):   
    k=len(genome)/l
    AllBlocks=genome
    Ran=range(0,l)
    #print Ran
    GenFitness=0
    Frac=0
    for i in range(0,k):
        ThisBlock=AllBlocks[0:l]
        ff=sum(i  == Threat for i in ThisBlock)
        F1=2**(l-ff)
        F2=1-F1/(2.0**l)
        Frac=Frac+ff
        GenFitness=GenFitness+F2
        AllBlocks=np.delete(AllBlocks, Ran)
    GenFitness=GenFitness/float(k)
    Frac=Frac/float(len(genome))
    return GenFitness, Frac




def OneIteration(genotype, Threat, l, p, N, B):   
    #generates new mutants, calculates fitness of both according to the given thread,  
    #returns one of them. p- prob. of acceptance of the better one
    k=len(genotype)/l
    #print k
    NewGenotype=Mutate(genotype, k)
    beta=B
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
    


# In[71]:

def AdaptationTime(k, l, N, p):  #optimises one population IN ONE ENVIRO!!, returns time neccessary
    
 
    
    n=k*l   # total length of the genome, k traits of length l
    FitnessArray=[];
    Onemax=[];
    
    genome=InitPop(n,3,k)
    Fnow=0  #random init of fitness. 
    while Fnow <1:   # to find the adaptation time, do until optimized
        [genome, GenFitness]=OneIteration(genome,3,l, p, N)
        #Onemax.append(sum(genome))
        FitnessArray.append(GenFitness)
        Fnow=GenFitness
        
       
    Topt=len(FitnessArray)
    
    return Topt

def OneParamSet(k,l,N,p, it):   #for a given parameter set, finds average of opt. times and variance
    OptTimes=[]
    for i in range(it):
        print i
        Topt=AdaptationTime(k, l, N,p)
        OptTimes.append(Topt)
    MeanOT= np.mean(OptTimes)
    STDOT= np.std(OptTimes)
    return MeanOT, STDOT


# In[72]:

def EvolutionOneParamSet(k,l,N,p,tau, t, B):  #this runs simulations with variable environment, for tau
    #ACTUALLY LOOKS AT POPULATION, KEEPS ITS FITNESS, AND NUMBER OF ONES IN A FEW BLOCKS
    import numpy as np
    import random
    
    n=l*k
    FitnessArray=[];
    Onemax=[];
    Enviro=GenerateEnviro(t,k,tau)
    genome=InitPop(n,3,k)
    B1=[]
    B2=[]
    B3=[]

    for i in Enviro:  # RUNS through the whole time defined by generated environement
        [genome, GenFitness, GenFrac]=OneIteration(genome,i,l, p, N, B)  #possible mutation
 
        Block1=Fitness(genome,1,l)  #captures first 3 blocks
        Block2=Fitness(genome,2,l)
        Block3=Fitness(genome,3,l)
        B1.append(Block1)
        B2.append(Block2)
        B3.append(Block3)
        Onemax.append(GenFrac)
        FitnessArray.append(GenFitness)  #captures evolving fitness
    #FitnessArray=np.array(FitnessArray)
    End2=len(FitnessArray)
    End1=End2-3*tau*k   #this will find a point before the end which is 
                        #5*timeperiod*all possible time period away frm the en 
   

    FileName=('M3F2EvolutionWithK'+str(k)+'.txt') 
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
    ouf.write("onemax")
    ouf.write('\n')
    ouf.write(str(Onemax))
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

        
    ouf.write('\n')
    ouf.write("Block2")
    ouf.write('\n')
    ouf.write(str(B2))

        
    ouf.write('\n')
    ouf.write("Block3")
    ouf.write('\n')
    ouf.write(str(B3))

    ouf.close()
    print 'One tau done'

 


    
def MainRun():   #this runs evolution of one population for various parameters
    tau=1
    t=1000
    k=5
    N=100
    p=0.9
    lrange=range(10,50,10)
    krange=range(75,105,5)
    l=10
    B=5000
    prange=range(2,10,1)
    taurange=[800]
    for i in krange:  #CHANGE THIS TO INVESTIGATE RUNTIME OF VARIOUS PARAMETERS. 
        print i
        k=i #CHANGE THIS TO INVESTIGATE RUNTIME OF VARIOUS PARAMETERS. 
        EvolutionOneParamSet(k,l,N,p,tau, t, B)
    print 'All done!!!'

import numpy as np
import random
MainRun()



