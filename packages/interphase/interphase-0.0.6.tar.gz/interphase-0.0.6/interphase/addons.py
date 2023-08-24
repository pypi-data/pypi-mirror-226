
def link(uri, label=None):
    if label is None: 
        label = uri
    parameters = ''
    escape_mask = '\033]8;{};{}\033\\{}\033]8;;\033\\'

    return escape_mask.format(parameters, uri, label)

def printError(text:any):
    print("\033[91m " + str(text) + " \033[0m")

def printWarning(text:any):
    print("\033[93m " + str(text) + " \033[0m")

def printInfo(text:any):
    print("\033[92m " + str(text) + " \033[0m")

def iF(condition:bool, first:any, second:any):
    if condition:
        return first
    else:
        return second
