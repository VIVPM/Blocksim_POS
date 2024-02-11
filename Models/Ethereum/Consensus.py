import numpy as np
from InputsConfig import InputsConfig as p
from Models.Ethereum.Node import Node
from Models.Consensus import Consensus as BaseConsensus
import random

#from ImportClasses import Node

class Consensus(BaseConsensus):


    
    def Protocol(miner):
        TOTAL_Stakes = sum([miner.Stakes for miner in p.NODES])
        Stakes = miner.Stakes/TOTAL_Stakes
        return random.expovariate(Stakes * 1/p.Binterval)
        # return 12


    """ 
	This method apply the longest-chain approach to resolve the forks that occur when nodes have multiple differeing copies of the blockchain ledger
    """
    def fork_resolution():
        BaseConsensus.global_chain = [] # reset the global chain before filling it

        a=[]
        for i in p.NODES:
            a+=[i.blockchain_length()]
        x = max(a)

        b=[]
        z=0
        for i in p.NODES:
            if i.blockchain_length() == x:
                b+=[i.id]
                z=i.id

        if len(b) > 1:
            c=[]
            for i in p.NODES:
                if i.blockchain_length() == x:
                    c+=[i.last_block().miner]
            z = np.bincount(c)
            z= np.argmax(z)

        for i in p.NODES:
            if i.blockchain_length() == x and i.last_block().miner == z:
                for bc in range(len(i.blockchain)):
                    BaseConsensus.global_chain.append(i.blockchain[bc])
                break



