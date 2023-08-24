import sys
import argparse
import json
import inspect
import traceback
import sqlalchemy as sa
import optilogic as ol
from cosmicfrog import FrogModel, Params
from .suppress_stdio import Suppress_stdio
from .frog_platform import OptilogicClient


# Handles launch code for utilities (so you don't have to!)

def __parse_args():

    parser = argparse.ArgumentParser(description='This is a Cosmic Frog utility. Visit www.cosmicfrog.com.')
    
    parser.add_argument('--function', choices=['description', 'parameters', 'run'], required=True, help='The utility function name to call.')
    parser.add_argument('--model_connection_string', type=str, help='Frog model connection string.', default=None)
    parser.add_argument('json_data', type=str, nargs='?', default=None, help='The JSON data payload passed to the function.')
    
    return parser.parse_args()

def __call_function_by_name(connection_string, func_name, data, main_globals):
    """
    Calls the given function by its name with the provided data if it expects exactly one argument.
    """
    print("__call_function_by_name")

    func_name = func_name.strip().lower()

    if func_name not in ['parameters', 'run']:
        raise ValueError(f"Function {func_name} not supported.")

    func = main_globals.get(func_name)
    if not func:
        raise ValueError(f"Function {func_name} not found.")
    
    function_params = inspect.signature(func).parameters



    num_params = len(function_params) 

    if func_name == 'run':

        if num_params != 2:
            raise ValueError(f"Expecting 2 arguments for run function, found {num_params}.")

        params = Params(data)

        print(f"Connecting to : {params.model_name}")

        # If no connection string supplied on command line, assume running in Andromeda
        # and need to pick up connection 
        if connection_string is None:

            oc = OptilogicClient()

            success, connection_string = oc.get_connection_string(params.model_name)

            if not success:
                raise ValueError(f"Cannot get connection string for frog model: {params.model_name}")
            
        engine = sa.create_engine(connection_string)

        # Initialise Frog model (quietly, no console output)
        with Suppress_stdio():
            model = FrogModel(engine=engine)

        func(model, params)

        print("[Utility end]")

        return


    if func_name == 'parameters':

        if num_params != 0:
            raise ValueError(f"Expecting 0 arguments for parameters function, found {num_params}.")
        
        func()

        return
    

def start_utility(main_globals):
    """
    Passes off control to the requested function in the utility
    """
    try:
        print("[Utility start]")

        args = __parse_args()
        data = json.loads(args.json_data) if args.json_data else None

        assert isinstance(data, list), "The data is not a list of parameter values"

        __call_function_by_name(args.model_connection_string, args.function, data, main_globals)

    except Exception as e:
        # Handle the exception as needed. For now, just print the error message.
        print(f"An error occurred: {e}")
        traceback.print_exc()
