import subprocess
import os.path

"""
>> modules.conf:
[compile]
filename

>> taskbuilder.conf:
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
###
def execute(args):
    files = []
    for arg in args:
        if "filename" not in arg:
            print("filename missing from checkstyle module execution arguments: " + str(arg))
            return False
        if not os.path.isfile(arg["filename"]):
            print("File not found: " + filename)
            return False
        files.append(arg["filename"])

    procargs = [
        "java", "-jar", "bin/checkstyle-7.2-all.jar", 
        "-c", "./csc_checkstyle.xml"
    ]
    procargs.extend(files)
    
    proc = subprocess.Popen(procargs, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    (stdout, stderr) = proc.communicate()
    
    # check stdout for [blah] tags, these are notifications 
    stdout = str(stdout, "UTF-8")
    outlines = stdout.splitlines()
    
    # checkstyle asticks a line "Starting audit..." at the top and "Audit done." 
    # at the bottom, so by default, output will have two lines
    if "Starting audit..." in outlines:
        outlines.remove("Starting audit...")
    if "Audit done." in outlines:
        outlines.remove("Audit done.")
    
    if len(outlines) == 0:
        print("Checkstyle finished")
        return True
    else:
        for line in outlines:
            print(line)
        return False
    
