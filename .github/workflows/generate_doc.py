import ast
import json
import sys

files = sys.argv[1:]
result = {}

if len(files) == 0:
    print("No file in argument...")
    exit(1)

def extract_infos(file):
    with open(file, "r") as f:
        node = ast.parse(f.read())

    classes = [ c for c in node.body if isinstance(c, ast.ClassDef) ]
    vars = [ v for v in node.body if isinstance(v, ast.Assign) ]

    #  modules's variables
    res_vars = []
    for cts in vars:
        for t in cts.targets:
            res_vars.append(t.id)
            #print("    {}".format( t.id ))

    # module's class
    res_class = {}
    for c in classes:
        res_class[c.name] = []
        functions = [ f for f in c.body if isinstance(f, ast.FunctionDef) ]
        for f in functions:
            res_class[c.name].append( f.name )

    return { "variables": res_vars, "classes": res_class }

for file in files:
    result[file] = extract_infos(file)

print( json.dumps(result) )


