
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
    


# In[5]:

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





def EvolutionOneParamSet(k,l,N,p,tau, t):  #this runs simulations with variable environment, for tau
    #ACTUALLY LOOKS AT POPULATION, KEEPS ITS FITNESS, AND NUMBER OF ONES IN A FEW BLOCKS
    import numpy as np
    import random
    
    n=l*k
    FitnessArray=[];
    Onemax=[];
    Enviro=GenerateEnviro(t,k,tau)
    genome=InitPop(n,1)
    B1=[]
    B2=[]
    B3=[]

    for i in Enviro:  # RUNS through the whole time defined by generated environement
        [genome, GenFitness]=OneIteration(genome,i,l, p, N)  #possible mutation
 
        Block1=Fitness(genome,1,l)  #captures first 3 blocks
        Block2=Fitness(genome,2,l)
        Block3=Fitness(genome,3,l)
        B1.append(Block1)
        B2.append(Block2)
        B3.append(Block3)
        Onemax.append(sum(genome))
        FitnessArray.append(GenFitness)  #captures evolving fitness
    #FitnessArray=np.array(FitnessArray)
    End2=len(FitnessArray)
    End1=End2-3*tau*k   #this will find a point before the end which is 
                        #5*timeperiod*all possible time period away frm the end
     

    FileName=('M1EvolWithTau'+str(tau)+'.txt') 
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
    t=10000
    k=10
    N=100
    p=0.9
    It=10
    lrange=range(10,50,10)
    l=20
    prange=range(2,10,1)
    taurange=[300,400,500,600,800,1000]
    for i in taurange:  #CHANGE THIS TO INVESTIGATE RUNTIME OF VARIOUS PARAMETERS. 
        print i
        tau=i #CHANGE THIS TO INVESTIGATE RUNTIME OF VARIOUS PARAMETERS. 
        EvolutionOneParamSet(k,l,N,p,tau, t)
    print 'All done!!!'

import numpy as np
import random

MainRun()





