import yaml
import os
import shutil

def read_yaml_file(filename, default=None, ignoreNonExistantFile=False, fixCorruption=False):
    if filename[-5:] == ".yaml" or filename[-4:] == ".yml":
        if ignoreNonExistantFile:
            try:
                file = open(filename)
                result = yaml.safe_load(fixCorruptedYaml(file.read(), fixCorruption))
                file.close()
            except IOError:
                return default
        else:
            file = open(filename)
            result = yaml.safe_load(fixCorruptedYaml(file.read(), fixCorruption))
            file.close()
        return result
    else:
        raise ValueError('Filename must have .yaml ending')

def fixCorruptedYaml(content, fixCorruption=False):
    """Fixes indentation errors"""
    if not fixCorruption:
        return content
    else:
        lines = content.splitlines()
        indent = 0
        opensNewBlock = False
        for index,l in enumerate(lines):
            lIndent = len(l) - len(l.lstrip(' '))
            if opensNewBlock:
                indent = lIndent
                opensNewBlock = False
            elif lIndent > indent:
                l = (' '*indent)+l.lstrip(' ')
                lines[index] = l
            if l.rstrip()[-1]==':':
                opensNewBlock = True
        return '\n'.join(lines)

def save_yaml_file(filename, data):
    if filename[-5:] == ".yaml" or filename[-4:] == ".yml":
        file = open(filename, "w")
        yaml.dump(data, file)
        file.close()
    else:
        raise ValueError('Filename must have .yaml ending')


def moveFilesOfType(sourceDir, targetDir, types=()):
    if len(types)>0:
        lengths = set(len(x) for x in types)
        ext = {i:list(x for x in types if len(x)==i) for i in lengths}
        source = os.listdir(sourceDir)
        for file in source:
            if any(file[-i:] in ext[i] for i in lengths):
                shutil.move(os.path.join(sourceDir, file), os.path.join(targetDir, file))


def findFileOfType(sourceDir, types=()):
    if len(types)>0:
        lengths = set(len(x) for x in types)
        ext = {i:list(x for x in types if len(x)==i) for i in lengths}
        source = os.listdir(sourceDir)
        for file in source:
            if any(file[-i:] in ext[i] for i in lengths):
                return file
    return None


def archiveFile(file):
    if os.path.exists(file):
        filename, file_extension = os.path.splitext(file)
        counter = 1
        while os.path.exists(filename + "." + str(counter) + file_extension):
            counter += 1
        shutil.move(file, filename + "." + str(counter) + file_extension)
    else:
        print "File '"+file+"' does not exist."