import json
import logging
import optilogic
import time

# Functions to facilitate interactions with Optilogic platform - Use 'optilogic' library

#TODO: rename database=model, storage_name=model_name etc for cf library
#TODO: use optilogic library where possible

class OptilogicClient():
    """
    wrapper for optilogic module for consumption in cosmic frog services
    """
    def __init__(self, username, appkey, logger = logging.getLogger()):
        self.api = optilogic.pioneer.Api(auth_legacy=False, appkey=appkey, un=username)
        self.logger = logger

    def model_exists(self, model_name):
        """
        returns True if a given model exists, False otherwise
        """
        try:
            return self.api.storagename_database_exists(model_name)
        except Exception:
            return False

    def get_connection_string(self, model_name):
        try:
            status = "error"
            rv = {"message" : "error getting connection string"}
            if self.api.storagename_database_exists(model_name):
                connections = self.api.sql_connection_info(model_name)
                rv = connections
                status = "success"
            else:
                rv = {"message" : f"model {model_name} does not exist"}
                
            return status, rv
        except Exception as e:
            return "exception", e
    
    def create_model_synchronous(self, model_name, model_template):
        try:
            new_model = self.api.database_create(name=model_name, template=model_template)

            status = "success"
            rv = {}
            if "crash" in new_model:
                status = "error"
                rv['message'] = json.loads( new_model['response_body'])['message']
                rv['httpStatus'] = new_model['resp'].status_code
            else:
                while not self.api.storagename_database_exists(model_name):
                    self.logger.info(f"creating {model_name}")
                    time.sleep(10.0)
                connections = self.api.sql_connection_info(model_name)
                rv['model'] = new_model
                rv['connection'] = connections

            return status, rv
        
        except Exception as e:
            return "exception", e

