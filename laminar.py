# Laminar CLI

import cmd
import sys
import argparse
import shlex
import ast
from typing import IO
import pwinput

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
from client import d4pClient

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
        parser.add_argument("-i", "--input", dest="input", required=False)
        try:
            args = vars(parser.parse_args(shlex.split(arg)))
            try:
                id = int(args["identifier"])
                inputVal = args["input"] if args["rawinput"] or args["input"] is None else ast.literal_eval(args["input"])
                feedback = client.run(id, input=inputVal)
                if (feedback):
                    print(feedback)
                else:
                    print(f"No workflow is registered with ID {args[0]}")
            except:
                inputVal = args["input"] if args["rawinput"] or args["input"] is None else ast.literal_eval(args["input"])
                feedback = client.run(args["identifier"], input=inputVal)
                if (feedback):
                    print(feedback)
                else:
                    print(f"No workflow is registered with name {args[0]}")
        except argparse.ArgumentError as e:
            print(e.message.replace("laminar.py", "run"))
        
    
    def help_run(self):
        print("Runs a workflow in the registry based on the provided name or ID")

    def do_quit(self, arg):
        sys.exit(0)

    def help_quit(self):
        print("Exits the Laminar CLI")

def parseArgs(arg:str):
    return arg.split()


# Start
if client.get_login() is not None:
    print(f"Logged in as {client.get_login()}")
else:
    username = input("Username: ")
    password = pwinput.pwinput("Password: ")
    client.login(username, password)

cli = LaminarCLI()
cli.cmdloop()