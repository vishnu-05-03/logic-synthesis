# Sat Apr 10 15:30:00 2021
# Program to find the prime implicants of a function given Fon and Fdc all in string format

"""
File: BLOCKING_MATRIX_EXPAND.py
Author: M N Vishnu (211EC229)
Description: Program to find the prime implicants of a function given Fon and Fdc all in string format

Input format is SoP and COMPLIMENTED literal is represented BY UPPER CASE and UNCOMPLEMENTED literal is represented BY LOWER CASE.
Example: A'B'C + A'BC + AB'C + ABC
Note: The input should be in the STRING format only.
Example:
    Enter Fon: 'WXZ+xz+XyZ+WxyZ+WYZ'
    Enter Fdc: ''
    Prime Implicants: 
    WxZ+XyZ+WYZ+Xz
"""

import numpy as np

def AND(f1, f2):

    f1 = f1.split("+")
    f1 = [list(i) for i in f1]

    f2 = f2.split("+")
    f2 = [list(i) for i in f2]

    F = []

    for i in f1:
        for j in f2:
            F.append(i+j)
    
    # for removing duplicate literals in a cube
    for i in range(len(F)):
        F[i] = [x for x in set(F[i])]

    # for removing duplicate cubes
    F = [list(x) for x in set(map(tuple, F))]

    # replace and of a literal and its compliment with 0
    for i in range(len(F)):
        if any(j.isupper() and j.lower() in F[i] for j in F[i]):
            F[i] = ['0']

    for i in F[:]:
        rem = False

        # remove term if it is 0
        for j in i:
            if j == '0':
                rem = True
                break
        if rem:
            F.remove(i)
            if len(F) == 0:
                F.append("0")

        # remove multiple 1's
        for j in i:
            if j == '1':
                i.remove(j)
                if len(i) == 0:
                    i.append("1")
    
    for i in F:
        if i == ['1']:
            F = i

    f = ""
    for i in F:
        f += "".join(i)
        f += "+"
    f = f.rstrip("+")

    return f

def simplify(string):
    string = string.split('+')
    string = [list(i) for i in string]
    sets = []

    for i in string:
        sets.append(set(i))

    # print(sets)

    # for i in sets:
    #     if i == {'X','z'}:
    #         print(i)

    for i in range(len(sets)):
        for j in sets:
            if j.issubset(sets[i]) and sets[i] != j:
                sets[i] = sets[i].union('0')

    for i in range(len(sets)):
        sets[i] = list(sets[i])

    for i in sets[:]:
        sets.remove(i) if any(k == '0' for k in i) else None

    for i in sets:
        i = i.sort()

    # remove duplicates
    sets = [list(x) for x in set(map(tuple, sets))]

    f = ""
    for i in sets:
        f += "".join(i)
        f += "+"
    f = f.rstrip("+")
    
    return f

def NOT(f):
    # seperating the string for further processing
    f = f.split("+")
    f = [list(i) for i in f]

    # print(f)

    for i in range(len(f)):
        for j in range(len(f[i])):
            c = f[i][j]
            f[i][j] = c.upper() if c.islower() else c.lower()

    # print(f)
    for i in range(len(f)):
        str = []
        for j in range(len(f[i])):
            str += f[i][j] + ("+" if j != len(f[i])-1 else "") 
        f[i] = str

    # print(f)
    str1 = ""
    for j in range(len(f[0])):
        str1+=f[0][j]
    F = str1
    
    for i in range(1,len(f)):
        str2 = ""
        for j in range(len(f[i])):
            str2+=f[i][j]

        # print(str1+'\n')
        # print(str2+'\n')
        
        F = AND(F, str2)
        # f[i] = AND(str1, str2)
    
    if F == '0':
        return '1'
    elif F == '1':
        return '0'

    f = F.split("+")
    f = [list(i) for i in f]

    # for removing duplicate literals in a cube
    for i in range(len(f)):
        f[i] = [x for x in set(f[i])]

    # for removing duplicate cubes
    f = [list(x) for x in set(map(tuple, f))]

    # replace and of a literal and its compliment with 0
    for i in range(len(f)):
        if any(j.isupper() and j.lower() in f[i] for j in f[i]):
            f[i] = ['0']

    F = ""
    for i in f:
        F += "".join(i)
        F += "+"
    F = F.rstrip("+")

    return simplify(F)

def find_min_rows(matrix):
    rows, cols = matrix.shape
    selected_rows = []
    min_rows = float('inf')

    def backtrack(row_idx, covered_cols):
        nonlocal selected_rows, min_rows

        if row_idx == rows:
            if len(covered_cols) == cols and len(selected_rows) <= min_rows:
                min_rows = len(selected_rows)
                yield list(selected_rows)
            return

        # Include the current row in the selection
        selected_rows.append(row_idx)
        new_covered_cols = covered_cols.union(np.nonzero(matrix[row_idx])[0])

        yield from backtrack(row_idx + 1, new_covered_cols)

        # Exclude the current row from the selection
        selected_rows.pop()
        yield from backtrack(row_idx + 1, covered_cols)

    result = list(backtrack(0, set()))

    return result

# function to find the groups of rows that cover all columns with 1's
# input: matrix with 1's and 0's. example: np.array([[1, 0, 1], [0, 1, 0], [1, 0, 0]])
# output: list of lists of rows that cover all columns with 1's (example: [[0, 1], [1, 2]])
def selected_rows(matrix):

    results = find_min_rows(matrix)
    # print("All possible combinations of minimum rows:")

    results = [set(i) for i in results]


    for i in range(len(results)):
        for j in results:
            if j.issubset(results[i]) and results[i] != j:
                results[i] = results[i].union('0')

    for i in range(len(results)):
        results[i] = list(results[i])

    for i in results[:]:
        results.remove(i) if any(k == '0' for k in i) else None

    for i in results:
        i = i.sort()

    # remove duplicates
    results = [list(x) for x in set(map(tuple, results))]

    return results

# function to find the literals in an expression
# input: expression in SOP form. example: 'WXZ+xz+XyZ+WxyZ+WYZ'
# output: list of literals in the expression. example: ['W', 'X', 'Z', 'x', 'y', 'z']
def literals_list(exp):
    exp_list = exp.split('+')
    exp_list = [list(i) for i in exp_list]

    literals = []
    for i in exp_list:
        for j in i:
            literals.append(j) if j not in literals else None

    return literals

# function to find the blocking matrix for given Foff and cube
def blocking_matrix(Foff, expand_cube):

    # finding the literals in expand_cube
    literals = literals_list(expand_cube)
    # print(literals)

    # finding the cubes in Foff
    cubes = Foff.split('+')
    cubes = [list(i) for i in cubes]
    # print(cubes)
    
    # defining a matrix of size len(literals) x len(cubes)
    matrix = np.zeros((len(literals), len(cubes)))

    # filling the matrix with 1's where the complement of literal is present in the cube 0 otherwise
    for i in range(len(literals)):
        for j in range(len(cubes)):
            matrix[i][j] = 1 if (literals[i].lower() if literals[i].isupper() else literals[i].upper()) in cubes[j] else 0

    # print(matrix)
    return matrix.astype(int)

# function to find the prime implicants of a function given Fon, Fdc and Foff all in string format
# input: Fon and Fdc in string format. example: 'WXZ+xz+XyZ+WxyZ+WYZ', ''
def Prime_implicants(Fon,Fdc):
    if Fdc != '':
        Foff = NOT(Fon + '+' + Fdc)
    else:
        Foff = NOT(Fon)

    Fon_cubelist = Fon.split('+')

    Prime_implicants = []

    for i in Fon_cubelist:
        BlockingMatrix = blocking_matrix(Foff, i)
        Rows = selected_rows(BlockingMatrix)
        Literals = literals_list(i)
        ExpandCubes = [[Literals[i] for i in j] for j in Rows]
        ExpandCubes = ["".join(i) for i in ExpandCubes]
        Prime_implicants.append(ExpandCubes)


    for i in Prime_implicants:
        if len(i) > 1:
            for j in i:
                Prime_implicants.append([j])
            Prime_implicants.remove(i)


    Prime_implicants = [list(x) for x in set(map(tuple, Prime_implicants))]

    Prime_implicants_list = Prime_implicants
    Prime_implicants = ""

    for i in Prime_implicants_list:
        Prime_implicants += "".join(i)
        Prime_implicants += ", "

    Prime_implicants = Prime_implicants.rstrip(', ')
    Prime_implicants = '{' + Prime_implicants + '}'

    return Prime_implicants

# Main function
if __name__ == "__main__":
    Fon = input("Enter Fon: ")
    Fdc = input("Enter Fdc: ")
    print("Prime Cover: ")
    print(Prime_implicants(Fon, Fdc))