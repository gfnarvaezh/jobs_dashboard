import json
from scrappers_runtime import run_scrappers

def lambda_handler(event, context):
   run_scrappers(test = False)