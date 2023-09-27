
"""
Input format of the function expression is SoP and COMPLIMENTED literal is represented BY UPPER CASE and UNCOMPLEMENTED literal is represented BY LOWER CASE.
Example: A'B'C + A'BC + AB'C + ABC
Enter the expression: ABc+Abc+aBc+abc

Opeartions available:
1. cofactor
2. bool_difference
3. consensus
4. smoothing

Operation codes:
1. cofactor: 1
2. bool_difference: 2
3. consensus: 3
4. smoothing: 4


Example1:
Enter the operation code: 1
Enter the expression: ABc+Abc+aBc+abc
Enter the term with respect to which cofactor has to be found: a
Cofactor of the expression with respect to the term is:  Bc+bc

Example2:
Enter the operation code: 2
Enter the expression: ABc+Abc+aBc+abc
Enter the term with respect to which bool_difference has to be found: a
Bool_difference of the expression with respect to the term is:  0

Example3:
Enter the operation code: 3
Enter the expression: ABc+Abc+aBc+abc
Enter the term with respect to which consensus has to be found: a
Consensus of the expression with respect to the term is:  Bc+bc

Example4:
Enter the operation code: 4
Enter the expression: ABc+Abc+aBc+abc
Enter the term with respect to which smoothing has to be found: a
Smoothing of the expression with respect to the term is:  cB+cb


"""

# Function to find the cofactor of a boolean expression with respect to a term
def cofactor(f,cwt):
    # seperating the string for further processing
    f = f.split("+")
    f = [list(i) for i in f]

    # Function for finding the cofactor of a boolean SoP expression with respect to a single literal
    def cofactor_1(f, cwt):

        for i in range(len(f)):
            if cwt.islower():
                f[i] = [j.replace(cwt.lower(), "1") for j in f[i]]
                f[i] = [j.replace(cwt.upper(), "0") for j in f[i]]
            else:
                f[i] = [j.replace(cwt.lower(), "0") for j in f[i]]
                f[i] = [j.replace(cwt.upper(), "1") for j in f[i]]
            # f[:] is used to make a copy of f
        for i in f[:]:
            rem = False

            for j in i:
                if j == '0':
                    rem = True
                    break
            if rem:
                f.remove(i)

            for j in i:
                if j == '1':
                    i.remove(j)
                    if len(i) == 0:
                        i.append("1")

        for i in f:
            if i == ['1']:
                return i
        return f
    
    # cwt is split to list and iterated over each literal
    cwt = list(cwt)
    for i in cwt:
        f = cofactor_1(f, i)

    # Combining the reduced expression to a single string
    reduced_exp = ""
    for i in f:
        reduced_exp += "".join(i)
        reduced_exp += "+"
    reduced_exp = reduced_exp.rstrip("+")

    return reduced_exp


# Compute OR of two boolean expressions
def OR(f1, f2):
    
    f1 = f1.split("+")
    f1 = [list(i) for i in f1]

    f2 = f2.split("+")
    f2 = [list(i) for i in f2]

    F = []

    F = f1 + f2

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


# Compute AND of two boolean expressions
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


# Compute NOT of a boolean expression
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

    return F


# Compute the bool_difference of a boolean expression with respect to a term
def bool_difference(f,cwt):
    a = AND(cofactor(f,cwt), NOT(cofactor(f,NOT(cwt)))) 
    b = AND(NOT(cofactor(f,cwt)), cofactor(f,NOT(cwt)))

    return OR(a,b)


# Compute Consensus of a boolean expression with respect to a term
def consensus(f,wrt):
    return AND(cofactor(f,wrt), cofactor(f,NOT(wrt)))


# Compute Smoothing of a boolean expression with respect to a term
def smoothing(f,wrt):
    return OR(cofactor(f,wrt), cofactor(f,NOT(wrt)))


# Main function
if __name__ == "__main__":

    op = int(input("Enter the operation code: "))

    match op:
        case 1:
            f = input("Enter the expression: ")
            cwt = input("Enter the term with respect to which cofactor has to be found: ")
            print("Cofactor of the expression with respect to the term is: ", cofactor(f,cwt))
        case 2:
            f = input("Enter the expression: ")
            cwt = input("Enter the term with respect to which bool_difference has to be found: ")
            print("Bool_difference of the expression with respect to the term is: ", bool_difference(f,cwt))
        case 3:
            f = input("Enter the expression: ")
            wrt = input("Enter the term with respect to which consensus has to be found: ")
            print("Consensus of the expression with respect to the term is: ", consensus(f,wrt))
        case 4:
            f = input("Enter the expression: ")
            wrt = input("Enter the term with respect to which smoothing has to be found: ")
            print("Smoothing of the expression with respect to the term is: ", smoothing(f,wrt))
        case _:
            print("Invalid operation code")