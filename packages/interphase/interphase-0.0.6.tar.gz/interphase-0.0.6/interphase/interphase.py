__all__ = ['typewriter']
import os
from .addons import link, printError, printWarning, printInfo, iF
from .module import typeHead, typeBody, returner
# import traceback

class typewriter:
    def __init__(self, base_directiory:str, d_ts:bool = True) -> None:
        if base_directiory == "":
            printWarning("Warning: Base Directory is Empty String")

        self.directiory = base_directiory
        self.d_ts = d_ts

    def __str__(self):
        return f"<class 'Typewriter', base directory: {link(self.directiory)}/[*].{iF(self.d_ts, 'd.ts', 'ts')}>"
    
    def write(self, file_name:str, typeName:str, data:any, export:bool=True, interface:bool=False) -> None: # interface is not supported yet
        if typeName == "":
            printError("Error: Type Name is Empty String")
            return
        
        if file_name == "":
            printError("Error: File Name is Empty String")
            return
        
        header = typeHead(typeName, export, interface) # interface is not supported yet (False)
        text = typeBody(data, 1)

        # traace_stack = traceback.extract_stack()
        # traace_frame = traace_stack[-2]
        # traace_file = traace_frame.filename
        # traace_directory = os.path.dirname(traace_file)

        # new_path = os.path.join(traace_directory, self.directiory, file_name + iF(self.d_ts, '.d.ts', '.ts'))

        new_path = os.path.join(self.directiory, file_name + iF(file_name.find(".") == -1, iF(self.d_ts, '.d.ts', '.ts') ,""))

        try:
            file = open(new_path, "a")
            file.write(returner(header, text, "\n\n"))
            file.close()
        except Exception as e:
            printError("Error: " + str(e))
            return
        
        printInfo("Type Generated at " + link(new_path))
        return typeName