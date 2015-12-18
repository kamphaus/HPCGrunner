#!/usr/bin/env python

#import dircache
import sys
#import yaml

import Cklib.Workflow as Workflow

def main(argv):
    #if len(argv) > 1:
    #    read_yaml_files(argv[1:])
    #else:
    #    read_yaml_files(dircache.listdir("."))
    Workflow.execute()
    
    return 0

if "__main__" == __name__:
    sys.exit(main(sys.argv))