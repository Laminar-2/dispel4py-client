# Laminar CLI

import cmd
import sys

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
from client import d4pClient

client = d4pClient()

class LaminarCLI(cmd.Cmd):
    def __init__(self):
        super().__init__()
        self.prompt = "(laminar) "
        self.intro  = """Welcome to the Laminar CLI"""

    def do_search(self, arg):
        args = parseArgs(arg)
        if (len(args) != 1):
            print("Invalid arguments\nUsage: search [string]")
            return
        feedback = client.search_Registry(args[0], "both", "text")
        #print(feedback)

    def help_search(self):
        print("Searches the registry for workflows and processing elements matching the search term")
        print("Usage: search [string]")

    def do_run(self, arg):
        args = parseArgs(arg)
        kwargs = {
            "input": int(args[1]) if len(args) > 1 else None
        }
        if (len(args) < 1):
            print("Invalid arguments\nUsage: run [id] [input?]")
            return
        try:
            id = int(args[0])
            feedback = client.run(id, **kwargs)
            if (feedback):
                print(feedback)
            else:
                print(f"No workflow is registered with ID {args[0]}")
        except:
            feedback = client.run(args[0], **kwargs)
            if (feedback):
                print(feedback)
            else:
                print(f"No workflow is registered with name {args[0]}")
    
    def help_run(self):
        print("Runs a workflow in the registry based on the provided name or ID")

    def do_quit(self, arg):
        sys.exit(0)

    def help_quit(self):
        print("Exits the Laminar CLI")

def parseArgs(arg:str):
    return arg.split()


# Start
cli = LaminarCLI()
cli.cmdloop()