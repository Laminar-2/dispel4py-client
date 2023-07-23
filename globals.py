from dispel4py.base import *

CLIENT_AUTH_ID: str = "None"

BASE_URL_REGISTER: str = "http://localhost:8080/registry/{}"

URL_REGISTRY_ALL: str = BASE_URL_REGISTER + "/all"

URL_REGISTER_PE: str = BASE_URL_REGISTER + "/pe/add"

URL_GET_PE_NAME: str = BASE_URL_REGISTER  + "/pe/name/"

URL_GET_PE_ID: str = BASE_URL_REGISTER + "/pe/id/"

URL_REMOVE_PE_NAME: str = BASE_URL_REGISTER + "/pe/remove/name/"

URL_REMOVE_PE_ID: str = BASE_URL_REGISTER + "/pe/remove/id/"

URL_PE_ALL: str = BASE_URL_REGISTER + "/pe/all"

URL_REGISTER_WORKFLOW: str = BASE_URL_REGISTER + "/workflow/add"

URL_GET_WORKFLOW_NAME: str = BASE_URL_REGISTER + "/workflow/name/"

URL_GET_WORKFLOW_ID: str = BASE_URL_REGISTER + "/workflow/id/"

URL_GET_PE_BY_WORKFLOW_NAME: str = BASE_URL_REGISTER + "/workflow/pes/name/"

URL_GET_PE_BY_WORKFLOW_ID: str = BASE_URL_REGISTER + "/workflow/pes/id/"

URL_REMOVE_WORKFLOW_NAME: str = BASE_URL_REGISTER + "/workflow/remove/name/"

URL_REMOVE_WORKFLOW_ID: str = BASE_URL_REGISTER + "/workflow/remove/id/"

URL_LINK_PE_TO_WORKFLOW: str = BASE_URL_REGISTER + "/workflow/{}/pe/{}"

URL_EXECUTE: str = "http://localhost:8080/execution/{}/run"

URL_REGISTER_USER: str = "http://localhost:8080/auth/register"

URL_LOGIN_USER: str =  "http://localhost:8080/auth/login"

URL_SEARCH: str = BASE_URL_REGISTER + "/search/{}/type/{}"

PE_TYPES = (BasePE,IterativePE,ProducerPE,ConsumerPE,SimpleFunctionPE,CompositePE,GenericPE)

headers = { 
            'Content-type':'application/json', 
            'Accept':'application/json'
          }

