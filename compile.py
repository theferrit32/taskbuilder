import subprocess
import os.path
import shutil
"""
modules.conf
[compile]
filename

taskbuilder.conf:
[compile]
file1
anotherfile
lastone
-->

[
    {"filename": "file1"},
    {"filename": "anotherfile"},
    {"filename": "lastone"}
]

"""

# Optional, default is False
# If set to true, and execute returns false, then taskbuilder will halt
blocking = True


###
# Entry point for module
#
# params:  
# args 
#       - an array of objects with key/value pairs mapping taskbuilder.conf values to 
#         correponding keys in modules.conf
# 
# return: True if ran successfully, False otherwise
# 
###
def execute(args):
    files = []
    destinations = []
    # validate inputs
    for arg in args:
        if ("filename" not in arg
                or "destination" not in arg):
            print("argument missing from compile module execution: " + str(arg))
            return
        if not os.path.isfile(arg["filename"]):
            print("File not found: " + filename)
            return
        files.append(arg["filename"])
        destinations.append(arg["destination"])
    
    
    # compile files with same destination together
    while len(args) != 0:
        obj = args[0]
        dest = obj["destination"]
        # extract all destinations matching this one
        files = []
        for arg in args:
            if arg["destination"] == dest:
                files.append(arg["filename"])
        
        # delete the args entries with filename in files (list comprehension)
        newargs = [arg for arg in args if not arg["filename"] in files]
        args = newargs
        
        # do the compilation
        procargs = ["javac", "-cp", (dest+":lib/*"), "-d", dest]
        procargs.extend(files)

        proc = subprocess.Popen(procargs, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        (stdout, stderr) = proc.communicate()
        if len(stderr.strip()) != 0:
            err = stderr.splitlines()
            for errline in err:
                print(str(errline, "UTF-8"))
            return False
    
    # done with all compilations
    print("Compile finished")
    
