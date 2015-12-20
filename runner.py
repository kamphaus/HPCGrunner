#!/usr/bin/env python

#import dircache
import sys
#import yaml
import argparse

import Cklib.Workflow as Workflow

def main(argv):
    #if len(argv) > 1:
    #    read_yaml_files(argv[1:])
    #else:
    #    read_yaml_files(dircache.listdir("."))
    parser = argparse.ArgumentParser()
    if sys.argv[1:]:
        parser.add_argument('action', nargs = '*', choices = ['run', 'clean', 'viz'])
    else:
        parser.add_argument('--action', default = ['run'])
    arguments = parser.parse_args()
    Workflow.execute(arguments)
    
    return 0

if "__main__" == __name__:
    sys.exit(main(sys.argv))