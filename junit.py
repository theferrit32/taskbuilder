import subprocess
import os.path

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
###
def execute(args):
    rootdirs = []
    classes = []
    for arg in args:
        if ("rootdir" not in arg 
                or "fullyqualifiedclassname" not in arg
                or "compileroot" not in arg):
            print("argument missing from junit module execution: " + str(arg))
            return
        if not os.path.isdir(arg["rootdir"]):
            print("Directory not found: " + arg["rootdir"])
            return
        rootdirs.append(arg["rootdir"])
        classes.append(arg["fullyqualifiedclassname"])
    
    
    # run files with same compileroot together
    while len(args) != 0:
        obj = args[0]
        compileroot = obj["compileroot"]
        # extract all destinations matching this one
        rootdirs = []
        classes = []
        for arg in args:
            if arg["compileroot"] == compileroot:
                rootdirs.append(arg["rootdir"])
                classes.append(arg["fullyqualifiedclassname"])
        
        # delete the args entries with filename in files (list comprehension)
        newargs = [arg for arg in args if not arg["fullyqualifiedclassname"] in classes]
        args = newargs
        
        # convert/combine the root dir and the classname to a real path
        files = []
        for i in range(len(classes)):
            c = classes[i]
            r = rootdirs[i]
            realpath = os.path.join(r, c.replace(".", "/")) + ".java"
            if not os.path.isfile(realpath):
                print("File not found: " + realpath)
                return False
            files.append(realpath)
        
        # do the compilation
        procargs = ["javac", "-cp", (compileroot+":lib/*"), "-d", compileroot]
        procargs.extend(files)
        
        proc = subprocess.Popen(procargs, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        (stdout, stderr) = proc.communicate()
        if iserror(stderr):
            return False
        
        # do the JUnit
        # create the build file for this junit run
        try: os.remove("build.xml")
        except OSError: pass
        
        import xml.etree.ElementTree as ElementTree
        project_elem = ElementTree.parse("junit-build.xml").getroot()
        target_elem = project_elem[0]
        junit_elem = target_elem[0]
        
        # add the project'as compile root to the ant junit classpath element
        classpath_elem = junit_elem[0]
        ElementTree.SubElement(classpath_elem, "pathelement", path=compileroot)
        
        # add test elements to the junit element
        for c in classes:
            ElementTree.SubElement(junit_elem, "test", name=c)
        
        # add failure condition
        fail_elem = ElementTree.SubElement(target_elem, "fail")
        condition_elem = ElementTree.SubElement(fail_elem, "condition")
        isset_elem = ElementTree.SubElement(condition_elem, "isset", property="hasfail")
        
        # write out to the build.xml file
        ElementTree.ElementTree(project_elem).write("build.xml")
        
        
        procargs = ["ant", "junit"]
        proc = subprocess.Popen(procargs, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        (stdout, stderr) = proc.communicate()
        
        # wipe the build file for safety
        #try: os.remove("build.xml")
        #except OSError: pass
        
        
        if iserror(stderr):
            return False
        
    # done with all compilations
    print("JUnit finished")
    return True


def iserror(stderr):
    if len(stderr.strip()) != 0:
        err = stderr.splitlines()
        for errline in err:
            print(str(errline, "UTF-8"))
        return True
