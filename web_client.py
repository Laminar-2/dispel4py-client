
from dispel4py.workflow_graph import WorkflowGraph 
from typing import Union
from globals import *
import requests as req
import cloudpickle as pickle 
import codecs
import json 
import logging
from enum import Enum

logger = logging.getLogger(__name__)
logging.basicConfig(format='%(message)s', level=logging.INFO) 

def get_payload(code: any):

    pickled = codecs.encode(pickle.dumps(code), "base64").decode()

    return pickled

def get_objects(results):

    objectList = []

    #todo:check if list is empty 
    for index, result in enumerate(results,start=1):

        if 'workflowName' in result.keys():
            workflow = "Result " + str(index) + ": " + "ID: " + str(result['workflowId']) + "\n" + + "Description: " + result['description'] + "\n"
            obj = pickle.loads(codecs.decode(result['workflowCode'].encode(), "base64")) 
            print(workflow)
        else:
            pe_name = result['peName']
            pe = "Result " + str(index) + ": " + "ID: " + str(result['peId']) + "\n" + "PE Name: " +pe_name + "\n" + "Description: " + result['description'] +"\n"
            obj = pickle.loads(codecs.decode(result['peCode'].encode(), "base64"))
            print(pe)

        objectList.append(obj)
    
    return objectList

class Process(Enum):
    SIMPLE = 1
    MULTI = 2
    DYNAMIC = 3

class PERegistrationData:
    
    #todo: Handle PE exceptions
    #  
    def __init__(
        self,
        *,
        pe: type, 
        pe_name: str = None,
        pe_code: any = None,
        description: str = None
    ):

        if pe is not None: 
            pe_name = pe.__class__.__name__
            pe_code = get_payload(pe)

        self.pe_name = pe_name 
        self.pe_code = pe_code 
        self.description = description


    def to_dict(self):
        return {
            "peName": self.pe_name,
            "peCode": self.pe_code,
            "description": self.description,
        }

    def __str__(self):
        return "PERegistrationData(" + json.dumps(self.to_dict(), indent=4) + ")"

class WorkflowRegistrationData:

    def __init__(
        self,
        *,
        workflow: any, #todo change?
        workflow_name: str = None,
        workflow_code: str = None,
        workflow_pes = None, #todo give type 
        entry_point: str = None,
        description: str = None
    ):

        if workflow is not None: 
            workflow_name = workflow.__class__.__name__
            workflow_code = get_payload(workflow)
            

        #todo: Handle PE exceptions 

        workflow_pes = workflow.getContainedObjects() 
       
        self.workflow_name = workflow_name 
        self.workflow_code = workflow_code 
        self.entry_point = entry_point
        self.description = description
        self.workflow_pes = workflow_pes

        #todo:remove
        #print(json.dumps(self.workflow_code))
        #exit()

    def to_dict(self):
        return {
            "workflowName": self.workflow_name,
            "workflowCode": self.workflow_code,
            "entryPoint": self.entry_point,
            "description": self.description,
        }

    def __str__(self):
        return "WorkflowRegistrationData(" + json.dumps(self.to_dict(), indent=4) + ")"

class ExecutionData:

    def __init__(
        self,
        *,
        workflow_id: int,
        workflow_name: str,
        workflow_code: WorkflowGraph, 
        input: any,
        process: Process,
        args: any
    ):

        self.workflow_id = workflow_id 
        self.workflow_name = workflow_name 
        self.input = get_payload(input)
        self.workflow_code = get_payload(workflow_code)
        self.args = get_payload(args)
        self.process = process.value
     
    def to_dict(self):
        return {
            "workflowId": self.workflow_id,
            "workflowName": self.workflow_name,
            "workflowCode": self.workflow_code,
            "inputCode": self.input,
            "process": self.process,
            "args": self.args
        }

    def __str__(self):
        return "ExecutionData(" + json.dumps(self.to_dict(), indent=4) + ")"

class SearchData:

    def __init__(
        self,
        *,
        search: str, 
        search_type: bool,
       
    ):
        self.search = search 
        self.search_type = search_type 
 
    def to_dict(self):
        return {
            "search": self.search,
            "searchType": self.search_type,
        }

    def __str__(self):
        return "SearchData(" + json.dumps(self.to_dict(), indent=4) + ")"

class WebClient:

    def __init__(): 
        None 
        #todo: implement 
    
    def register_PE(self, pe_payload: PERegistrationData):

        data = json.dumps(pe_payload.to_dict())
        response = req.post(URL_REGISTER_PE, data=data,headers=headers)
        response = json.loads(response.text)

        if 'ApiError' in response.keys():
            logger.error(response['ApiError']['message'])
            return None 
        else: 
            logger.info("Successfully registered PE: " + response["peName"] + " ID:" + str(response["peId"]))
            return int(response["peId"])
       
    def register_Workflow(self, workflow_payload: WorkflowRegistrationData):

        workflow_dict = workflow_payload.to_dict()
        
        data = json.dumps(workflow_dict)
        response = req.post(URL_REGISTER_WORKFLOW, data=data,headers=headers) #add workflow resources 
        response = json.loads(response.text)

        if 'ApiError' in response.keys():
            logger.error(response['ApiError']['message'])
            return None 
        else: 

            workflow_id = response['workflowId']

            #Link PEs to Workflow 
            for pe_obj in workflow_payload.workflow_pes:
     
                get_pe_url = URL_GET_PE_NAME + pe_obj.name 
                pe_res = req.get(url=get_pe_url)
                pe_res = json.loads(pe_res.text)

                #Check if exists 
                if 'ApiError' in pe_res.keys():
                    #register PE
                    data = PERegistrationData(pe=pe_obj)
                    pe_id = WebClient.register_PE(self,data)
                    #Link PE
                    req.put(url=URL_LINK_PE_TO_WORKFLOW.format(workflow_id,pe_id))
                else:
                    req.put(url=URL_LINK_PE_TO_WORKFLOW.format(workflow_id,pe_res["peId"]))
                    #Link PE to Workflow 
                    
            logger.info("Successfully registered Workflow: " + response["workflowName"] + " ID:" + str(response["workflowId"]))
            return response["workflowId"]

    def run(self, execution_payload: ExecutionData):

        data = json.dumps(execution_payload.to_dict())

        response = req.post(url=URL_EXECUTE,data=data,headers=headers)

        response = json.loads(response.text)

        if 'ApiError' in response.keys():
            logger.error(response['ApiError']['message'])
            return None 
        else:   
            logger.info("Successfully executed workflow: ") #todo should print if successful 
            return response["result"] 

    def get_PE(self, pe: Union[int,str]):

        if isinstance(pe, str):
            
            url = URL_GET_PE_NAME + pe
            
        elif isinstance(pe, int):

            url = URL_GET_PE_ID + str(pe)
        else:
            assert 'invalid type'

        response = req.get(url=url)
        response = json.loads(response.text)

        if 'ApiError' in response.keys():
            logger.error(response['ApiError']['message'])
            return None 

        else: 

            peCode = response["peCode"]
            unpickled_result = pickle.loads(codecs.decode(peCode.encode(), "base64"))
            return unpickled_result

    def get_Workflow(self, workflow: Union[int,str]):

        if isinstance(workflow, str):
            
            url = URL_GET_WORKFLOW_NAME + workflow
            
        if isinstance(workflow, int):

            url = URL_GET_WORKFLOW_ID + str(workflow)

        response = req.get(url=url)
        response = json.loads(response.text)

        if 'ApiError' in response.keys():
            logger.error(response['ApiError']['message'])
            return None 

        else: 

            workflowCode = response["workflowCode"]
            unpickled_result: WorkflowGraph = pickle.loads(codecs.decode(workflowCode.encode(), "base64"))
            return unpickled_result

    def get_PEs_By_Workflow(self, workflow: Union[int,str]):

        if isinstance(workflow, str):
            
            url = URL_GET_PE_BY_WORKFLOW_NAME + workflow
            
        if isinstance(workflow, int):

            url = URL_GET_PE_BY_WORKFLOW_ID + str(workflow)

        response = req.get(url=url)
        response = json.loads(response.text)

        objectList = []

        for index, response in enumerate(response,start=1):
            pe_name = response['peName']
            pe = "Result " + str(index) + ": " + "ID: " + str(response['peId']) + "\n" + "PE Name: " +pe_name + "\n" + "Description: " + response['description'] +"\n"
            obj = pickle.loads(codecs.decode(response['peCode'].encode(), "base64"))
            print(pe)

            objectList.append(obj)
        
        return objectList

    def remove_PE(self,pe: Union[int,str]):

        if isinstance(pe, str):
            
            url = URL_REMOVE_PE_NAME + pe
            
        if isinstance(pe, int):

            url = URL_REMOVE_PE_ID + str(pe)
        
        response = req.delete(url=url)
        response = json.loads(response.text)

        if response == 1:
            logger.info("Sucessfully removed PE: " + str(pe))
        else:
            if isinstance(pe,str):
                logger.error("Could not find PE '"+ pe +"' to remove")
            else:
                logger.error("Could not find PE with ID "+ str(pe) +" to remove")

    def remove_Workflow(self,workflow:Union[int,str]):

        if isinstance(workflow, str):
            
            url = URL_REMOVE_WORKFLOW_NAME + workflow
            
        if isinstance(workflow, int):

            url = URL_REMOVE_WORKFLOW_ID + str(workflow)
        
        response = req.delete(url=url)
        response = json.loads(response.text)

        if response == 1:
            logger.info("Sucessfully removed Workflow: " + str(workflow))
        else:
            if isinstance(workflow,str):
                logger.error("Could not find Workflow '"+ workflow +"' to remove")
            else:
                logger.error("Could not find Workflow with ID "+ str(workflow) +" to remove")

    def search(self,search_payload: SearchData):

        search_dict = search_payload.to_dict()

        url = URL_SEARCH.format(search_dict['search'],search_dict['searchType'])

        response = req.get(url=url)
        response = json.loads(response.text)

        return get_objects(response)

    def get_Registry(self):
        
        url = URL_REGISTRY_ALL

        response = req.get(url=url)
        response = json.loads(response.text)

        return get_objects(response)


