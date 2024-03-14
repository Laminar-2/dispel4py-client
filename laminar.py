# Laminar CLI

import cmd
import sys
import argparse
import shlex
import ast
from typing import IO
import pwinput
import imp

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' # gets the libraries to write less garbage to the terminal
from client import d4pClient, Process
from dispel4py.base import GenericPE, WorkflowGraph

client = d4pClient()

class CustomArgumentParser(argparse.ArgumentParser):
    def __init__(self, exit_on_error=True):
        super().__init__(exit_on_error=exit_on_error)

    def exit(self, status=0, message=None):
        if self.exit_on_error:
            sys.exit(status)
        else:
            raise argparse.ArgumentError(None, message=message)

class LaminarCLI(cmd.Cmd):
    def __init__(self):
        super().__init__()
        self.prompt = "(laminar) "
        self.intro  = """Welcome to the Laminar CLI"""

    def do_search(self, arg):
        parser = CustomArgumentParser(exit_on_error=False)
        parser.add_argument("search_type", choices=["workflow", "pe", "both"], default="both")
        parser.add_argument("search_term")
        try:
            args = vars(parser.parse_args(shlex.split(arg)))
            feedback = client.search_Registry(args["search_term"], args["search_type"], "text")
        except argparse.ArgumentError as e:
            print(e.message.replace("laminar.py", "search"))

    def help_search(self):
        print("Searches the registry for workflows and processing elements matching the search term")
        print("Usage: search [string]")

    def do_run(self, arg):
        parser = CustomArgumentParser(exit_on_error=False)
        parser.add_argument("identifier")
        parser.add_argument("--rawinput", action="store_true")
        parser.add_argument("-v", "--verbose", action="store_true")
        parser.add_argument("-i", "--input", dest="input", required=False)
        parser.add_argument("-r", "--resource", action="append", required=False)
        parser.add_argument("--multi", action="store_true")
        parser.add_argument("--dynamic", action="store_true")

        try:
            args = vars(parser.parse_args(shlex.split(arg)))
            try:
                id = int(args["identifier"])
                inputVal = args["input"] if args["rawinput"] or args["input"] is None else ast.literal_eval(args["input"])
                runType = Process.SIMPLE
                if args["multi"]:
                    runType = Process.MULTI
                elif args["dynamic"]:
                    runType = Process.DYNAMIC
                feedback = client.run(id, input=inputVal, verbose=args["verbose"], resources=args["resource"], process=runType)
                if (feedback):
                    print(feedback)
                else:
                    print(f"No workflow is registered with ID {id}")
            except:
                inputVal = args["input"] if args["rawinput"] or args["input"] is None else ast.literal_eval(args["input"])
                runType = Process.SIMPLE
                if args["multi"]:
                    runType = Process.MULTI
                elif args["dynamic"]:
                    runType = Process.DYNAMIC
                feedback = client.run(args["identifier"], input=inputVal, verbose=args["verbose"], resources=args["resource"], process=runType)
                if (feedback is not None):
                    print(feedback)
                else:
                    print(f"No workflow is registered with name {args['identifier']}")
        except argparse.ArgumentError as e:
            print(e.message.replace("laminar.py", "run"))
        
    
    def help_run(self):
        print("Runs a workflow in the registry based on the provided name or ID")

    def do_register(self, arg):
        parser = CustomArgumentParser(exit_on_error=False)
        parser.add_argument("filepath")
        try:
            args = vars(parser.parse_args(shlex.split(arg)))
            try: 
                mod = imp.load_source('__main__', args["filepath"])
                pes = {}
                workflows = {}
                for var in dir(mod):
                    attr = getattr(mod, var)
                    if isinstance(attr, GenericPE):
                        pes.update({var: attr})
                    if isinstance(attr, WorkflowGraph):
                        workflows.update({var: attr})
                if len(pes) == 0 and len(workflows) == 0:
                    print("Could not find any PEs or Workflows")
                    return
                if len(pes) > 0:
                    print("Found PEs")
                for key in pes:
                    print(f"• {key} - {type(pes[key]).__name__}", end=" ")
                    docstring = pes[key].__doc__
                    r = client.register_PE(pes[key], docstring)
                    if r is None:
                        print("(Exists)")
                    else:
                        print(f"(ID {r})")
                if len(workflows) > 0:
                    print("Found workflows")
                for key in workflows:
                    print(f"• {key} - {type(workflows[key]).__name__}", end=" ")
                    docstring = workflows[key].__doc__
                    r = client.register_Workflow(workflows[key], key, docstring)
                    if r is None:
                        print("(Exists)")
                    else:
                        print(f"(ID {r})")
                for var in dir(mod):
                    attr = getattr(mod, var)
                    if isinstance(attr, GenericPE):
                        setattr(mod, var, None)
                    if isinstance(attr, WorkflowGraph):
                        setattr(mod, var, None)
                
            except FileNotFoundError:
                print(f"Could not find file at {args['filepath']}")
            except SyntaxError:
                print(f"Target file has invalid python syntax")
        except argparse.ArgumentError as e:
            print(e.message.replace("laminar.py", "register"))

    def help_register(self):
        print("Registers all workflows and PEs instantiated within a given file input")

    def do_quit(self, arg):
        sys.exit(0)

    def help_quit(self):
        print("Exits the Laminar CLI")

def parseArgs(arg:str):
    return arg.split()

def clear_terminal():
    if os.name == "nt":
        os.system('cls')
    else:
        os.system('clear')

clear_terminal()

# Start
if client.get_login() is not None:
    print(f"Logged in as {client.get_login()}")
else:
    while client.get_login() is None:
        username = input("Username: ")
        password = pwinput.pwinput("Password: ")
        client.login(username, password)
        if client.get_login() is None:
            print("Invalid login")

clear_terminal()

cli = LaminarCLI()
cli.cmdloop()