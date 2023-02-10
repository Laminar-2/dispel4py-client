from dispel4py.base import ProducerPE, IterativePE, ConsumerPE
from dispel4py.workflow_graph import WorkflowGraph
import random
from easydict import EasyDict as edict
from easydict import EasyDict as edict
from client import d4pClient,Process
from dispel4py.new.dynamic_redis import process as dyn_process
from dispel4py.new.simple_process import process as simple_process
from dispel4py.new.multi_process import process as multi_process

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
        print("before checking data - %s - is prime or not“" % num)
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

client = d4pClient()

#SIMPLE 
#simple_process(graph, {producer: 5})
#client.run(graph,input=5)

#MULTI 
#multi_process(graph, {producer: 5}, edict({'num':5, 'iter': 5,'simple': False}))
#client.run(graph,input=5,process=Process.MULTI,args=edict({'num':5, 'iter': 5,'simple': False}))

#REDIS 
#producer.name='producer'
#dyn_process(graph,{'producer': 5}, edict({'num':5,'iter':5, 'simple':False, 'redis_ip':'localhost', 'redis_port':'6379'}))
client.run(graph,input=5,process=Process.DYNAMIC,args= edict({'num':5,'iter':5, 'simple':False, 'redis_ip':'localhost', 'redis_port':'6379'}))

