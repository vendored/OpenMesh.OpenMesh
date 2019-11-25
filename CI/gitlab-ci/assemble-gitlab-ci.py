#!/usr/bin/python3

import sys, os, re

# Script for automated gitlab-ci creation
# Assembles the gitlab ci from master template file:
master_file = 'ci-master.yml'
# Lines in the master file are copied to the resulting
# assemblied gitlab ci file
target_file = '../../.gitlab-ci.yml'
# Lines containing the String {xxx} are interpreted
# as import statement. Therefore the file xxx is imported
# into that line.
error_on_path_redirection = True
# Notice that xxx can not contain path redirections
# like .. and /


# Prefix to prepend to master file
autogenerated_notice = """#############################################################
#                                                           #
# This is an auto generated file. Do not make               #
# changes to this file. They possible will be overriden.    #
#                                                           #
# To make persistent changes changes files in               #
# ./CI/gitlab-ci/ ...                                       #
# and regenerate this file with the configuration tool      #
#                                                           #
#############################################################

"""


# Checks if an import filename is valid - free of path redirections
def isValidImportFilename(filenameToImport):
    if not error_on_path_redirection:
        return True
    else:
        filterRegex = r"(\/|\\|\.\.+)"
        filtered = re.sub(filterRegex, '', filenameToImport)
        return filenameToImport == filtered

# Returns the directory to work on
def findCIAssemblyDirectory():
    pathname = os.path.dirname(sys.argv[0])      
    return os.path.abspath(pathname)

# Returns file content as string
def readFile(filename):
    file = open(filename, "r")
    content = file.read()
    file.close()
    return content

# Assembles the file in memory and returns file content as string
def assembleTarget(master, depth=3):
    if depth < 0:
        raise "Max depth reached. Possible circular import?"

    master_content = readFile(master)
    regex_import_stmt = r"^\ *\{([^\}\n]+)\}\ *$"
    regex_import_comp = re.compile(regex_import_stmt)
    master_content_list = master_content.splitlines()

    # Walk through file looking for import statements
    cur_index = 0
    while cur_index < len(master_content_list):
        cur_line = master_content_list[cur_index]
        match = regex_import_comp.match(cur_line)

        if match:
            importFile = match.groups()[0]
            if importFile:
                # Found import statement
                print("Importing file: "+importFile)

                if not isValidImportFilename(importFile):
                    raise "Invalid filename "+importFile+ ". Do not include path redirections"

                import_content = assembleTarget(importFile, depth=depth-1)
                import_content_list = import_content.splitlines()
                master_content_list.pop(cur_index)
                for new_line in reversed(import_content_list):
                    master_content_list.insert(cur_index, new_line)

        cur_index += 1

    # Assemble result
    master_content = ''.join(str(e)+'\n' for e in master_content_list)
    return master_content

# Main function
def main():
    print("Starting config assembly")
    os.chdir(findCIAssemblyDirectory())
    target_content = autogenerated_notice
    target_content += assembleTarget(master_file)
    print("Writing config to file "+target_file)

    target_file_handle = open(target_file, "w")
    target_file_handle.write(target_content)
    target_file_handle.write("\n")
    target_file_handle.flush()
    target_file_handle.close()

    print("Finished.")


# Execute main function
if __name__ == '__main__':
    main()