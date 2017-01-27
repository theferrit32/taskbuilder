import sys, os, re
import importlib

FAIL_VAL = 1
loaded_modules = []
pymods = {}
module_tag_re = re.compile(r"\[([a-zA-Z]+)\][\s]*$")
comment_re = re.compile(r"^#")

###
# Reads the lines of a file ignoring the empty lines
###
def read_lines(filename):
    retarr = []
    with open(filename, "r") as f:
        arr = f.read().splitlines()
        for line in arr:
            if len(line) != 0:
                retarr.append(line)
    return retarr


###
# Checks to see if a module name exists in the loaded modules
# Return True if it does, False otherwise
###
def module_exists(module_name):
    return get_module_definition_by_name(module_name) != None

###
#
###
def get_module_definition_by_name(module_name):
    for m in loaded_modules:
        if m["name"] == module_name:
            return m
    return None

###
# Read in the module configuration
# file is in the format:
# 
# [modulename]
# term1 term2 term3 ...
#
#
###
def load_modules():
    filename = "modules.conf"
    lines = read_lines(filename)
    modules = []
    module = None
    for line in lines:
        # check if line for mat is a config headers
        m = module_tag_re.match(line)
        if m is not None:
            name = m.group(1)
            if module_exists(name):
                print("Duplicate module found")
                continue
            else:
                module = name
                loaded_modules.append({"name": module, "fields": []})
        else:
            # is a content line
            if module is not None:
                mdef = get_module_definition_by_name(module)
                #print("modifying module: " + mdef["name"])
                terms = line.split()
                #print("adding terms: " + str(terms))
                for t in terms:
                    mdef["fields"].append(t)
                # only accept one line of terms right now
                module = None
                

###
# Loads a config file, by default "taskbuilder.conf"
# This file defines the execution of the tashbuilder program
# It contains a sequence of config file sections with given
# names and contents. The config header maps onto a loaded module 
# and each line in the section under the header is executed in order
# according to the definition of that module within the program
###
def get_config():
    filename = "taskbuilder.conf"
    lines = read_lines(filename)
    config = []
    current_config_index = -1
    dictionary = {}
    module = None
    for line in lines:
        # check if line format is a config header
        header_matcher = module_tag_re.match(line)
        comment_matcher = comment_re.match(line)
        
        if comment_matcher is not None:
            # is a comment, skip
            continue
        elif header_matcher is not None:
            # see if the module is known
            name = header_matcher.group(1)
            if module_exists:
                module = name
                dictionary = {"task": module, "item": []}
                config.append({"task": module, "items": []})
                current_config_index += 1
            else:
                print("Unknown task name: " + name)
                return
        else:
            # is is a line within a module
            if module is not None:
                mod_fields = get_module_definition_by_name(module)["fields"]
                
                task_fields = line.split()
                
                if len(mod_fields) != len(task_fields):
                    print("Task config had different number of terms than module config in: " + module)
                    return
                
                items = config[current_config_index]["items"]
                
                item = {}
                for i in range(len(mod_fields)):
                    fieldname = mod_fields[i]
                    fieldvalue = task_fields[i]
                    item[fieldname] = fieldvalue
                items.append(item)
                
            else:
                # line preceeded module name
                print("Config file contained line outside a defined task")
    # done with lines
    return config


def main(argv):
    load_modules()
    #print("Loaded modules: " + str(loaded_modules))
    #print()
    config = get_config()
    if config is None:
        print("Exiting")
        return
    #print("Taskbuilder config: " + str(config))
    #print()
    
    # check for module existence
    for module in loaded_modules:
        # this inserts the python module into sys.modules
        modulename = module["name"]
        try:
            importlib.import_module(modulename)
            pymods[modulename] = sys.modules[modulename]
            # set the blocking to false if it isn't already defined
            if not hasattr(pymods[modulename], "blocking"):
                pymods[modulename].blocking = False
        except Exception as e:
            print(str(e))
            return
    print("Imported all python modules: " + str(list(pymods.keys())))
    
    
    # execute tasks in the config
    for task in config:
        tmod = pymods[task["task"]]
        retval = tmod.execute(task["items"])
        if retval is False and tmod.blocking is True:
            print("\n\nEnding execution due to failed execution of task: " + tmod.__name__)
            return FAIL_VAL
    
    print("\nAll tasks completed successfully\n")


if __name__ == "__main__":
    main(sys.argv)
