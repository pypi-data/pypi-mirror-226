import sys
import argparse
import json
import inspect
import traceback
import sqlalchemy as sa
from cosmicfrog import FrogModel, Params
from .suppress_stdio import Suppress_stdio


# Handles launch code for utilities (so you don't have to!)

def __parse_args():

    parser = argparse.ArgumentParser(description='This is a Cosmic Frog utility. Visit www.cosmicfrog.com.')
    
    parser.add_argument('--function', choices=['description', 'parameters', 'run'], required=True, help='The utility function name to call.')
    parser.add_argument('json_data', type=str, nargs='?', default=None, help='The JSON data payload passed to the function.')
    
    return parser.parse_args()

def __call_function_by_name(func_name, data, main_globals):
    """
    Calls the given function by its name with the provided data if it expects exactly one argument.
    """
    func_name = func_name.strip().lower()

    if func_name not in ['parameters', 'run']:
        raise ValueError(f"Function {func_name} not supported.")

    func = main_globals.get(func_name)
    if not func:
        raise ValueError(f"Function {func_name} not found.")
    
    function_params = inspect.signature(func).parameters

    print("[Utility start]")

    num_params = len(function_params) 

    if func_name == 'run':

        if num_params != 2:
            raise ValueError(f"Expecting 2 arguments for run function, found {num_params}.")

        params = Params(data)
        engine = sa.create_engine(params.connection_string)

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
        args = __parse_args()
        data = json.loads(args.json_data) if args.json_data else None

        assert isinstance(data, list), "The data is not a list of parameter values"

        __call_function_by_name(args.function, data, main_globals)

    except Exception as e:
        # Handle the exception as needed. For now, just print the error message.
        print(f"An error occurred: {e}")
        traceback.print_exc()
