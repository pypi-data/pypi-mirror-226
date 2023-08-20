import argparse
import json
import inspect
import traceback
from cosmicfrog import Params

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
    func = main_globals.get(func_name)
    if not func:
        raise ValueError(f"Function {func_name} not found!")
    
    function_params = inspect.signature(func).parameters

    num_params = len(function_params) 

    if num_params not in (0, 1):
        raise ValueError(f"Function {func_name} expects {len(num_params)} parameters, but only 1 or 0 are supported.")

    params = Params(data)
    
    if num_params == 1:
        return func(params)
    else:
        return func()

def start_utility(main_globals):
    """
    Passes off control to the requested function in the utility
    """
    try:
        args = __parse_args()
        data = json.loads(args.json_data) if args.json_data else None

        assert isinstance(data, list), "The data is not a list of parameter values"

        result = __call_function_by_name(args.function, data, main_globals)

        # Dump output to stdout
        # TODO: More sophisticated method to return result to CF, realtime updates
        print(result)

    except Exception as e:
        # Handle the exception as needed. For now, just print the error message.
        print(f"An error occurred: {e}")
        traceback.print_exc()
