# Imports 
from dispel4py.base import ProducerPE, IterativePE, ConsumerPE
from dispel4py.workflow_graph import WorkflowGraph
import random
from easydict import EasyDict as edict
from client import d4pClient,Process
import inspect 
from util import *

class NumberProducer(ProducerPE):
    def __init__(self):
        ProducerPE.__init__(self)
        
    def _process(self, inputs):
        # this PE produces one input
        result= random.randint(1, 1000)
        return result

class IsPrime(IterativePE):
    def __init__(self):
        IterativePE.__init__(self)
    def _process(self, num):
        # this PE consumes one input and produces one output
        print("before checking data - %s - is prime or not" % num)
        if all(num % i != 0 for i in range(2, num)):
            return num

class PrintPrime(ConsumerPE):
    def __init__(self):
        ConsumerPE.__init__(self)
    def _process(self, num):
        # this PE consumes one input
        print("the num %s is prime" % num)

producer = NumberProducer()
isprime = IsPrime()
printprime = PrintPrime()

graph = WorkflowGraph()
graph.connect(producer, 'output', isprime, 'input')
graph.connect(isprime, 'output', printprime, 'input')

#Create Client Instance
print(underline("\n Create Client Instance\n"))
client = d4pClient()

#Create User and Login 
print(underline("\n Create User and Login \n"))
client.register("root","root")
client.login("root","root")

print(underline("\n Register Graph \n"))
client.register_Workflow(graph,"graph1")

print(underline("\n Text to Code Search \n"))
client.search_Registry("prime","pe","text")

print(underline("\n Code to Text Search \n"))
client.search_Registry("random.randint(1, 1000)","pe","code")

print(underline("\nExecute Workflow with Simple\n"))
client.run(graph,input=5)

print(underline("\n Execute Workflow with Multi\n"))
client.run(graph,input=5,process=Process.MULTI,args={'num':5,'simple': False})




