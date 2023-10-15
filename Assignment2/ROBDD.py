# Program to find the ROBDD of a given boolean expression and order of variables

"""
Write a long documentation here

Name: ROBDD.py
Author: M N Vishnu (211EC229), Keerthi Bhushan M (211EC226)
Description: Program to find the ROBDD of a given boolean expression and order of variables

Input format is SoP and COMPLIMENTED literal is represented BY UPPER CASE and UNCOMPLEMENTED literal is represented BY LOWER CASE.
Example: A'B'C + A'BC + AB'C + ABC
Note: The input should be in the STRING format only.
Example:
    Enter the expression: 'ABc+Abc+aBc+abc'
    Enter the order of ROBDD implementation: 'a<b<c'
    Output: {'c': ['1', '0'], '0': ['0', '0'], '1': ['1', '1']}

    Here the dictionary represents graph of ROBDD.
    Example:
        key 'c' represents function of a particular node
        the value pair ['1','0'] represents right and left node functions
        '1' represents the right node function '1'
        '0' represents the left node function '0'

"""


class node:

    def __init__(self, funct, right, left):
        self.funct = funct
        self.left = left
        self.right = right

    def __str__(self):
        return f"function: {self.funct},right_function : {self.right} left_function : {self.left}"

# Function for finding the cofactor of boolean SoP expressions


def cofactor(f, cwt):
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
        if len(f) == 0:
            return '0'
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

# Function for finding the AND of two boolean SoP expressions


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

# Function for finding the NOT boolean SoP expressions


def NOT(f):
    if f == '1':
        return '0'
    if f == '0':
        return '1'
    # seperating the string for further processing
    f = f.split("+")
    f = [list(i) for i in f]

    for i in range(len(f)):
        for j in range(len(f[i])):
            c = f[i][j]
            f[i][j] = c.upper() if c.islower() else c.lower()

    for i in range(len(f)):
        str = []
        for j in range(len(f[i])):
            str += f[i][j] + ("+" if j != len(f[i])-1 else "")
        f[i] = str

    str1 = ""
    for j in range(len(f[0])):
        str1 += f[0][j]
    F = str1

    for i in range(1, len(f)):
        str2 = ""
        for j in range(len(f[i])):
            str2 += f[i][j]

        F = AND(F, str2)

    return F

# Function for finding if the two nodes are equal


def is_same(a, b):

    if a.left == b.left and a.right == b.right:
        return True
    return False

# Function to push node to unique table


def to_unique_table(a):
    for i in unique_table:
        if is_same(a, i):
            return a
    unique_table.append(a)
    return a

# Function for building the ROBDD


def build(function, order, i):
    if function == '0':
        return to_unique_table(node('0', '0', '0'))
    elif function == '1':
        return to_unique_table(node('1', '1', '1'))
    else:
        var = order[i]

        right_funct = cofactor(function, var)
        left_funct = cofactor(function, NOT(var))
        i += 1
        right_build = build(right_funct, order, i)
        left_build = build(left_funct, order, i)

        if is_same(right_build, left_build):
            return to_unique_table(right_build)
        else:
            return to_unique_table(node(function, right_funct, left_funct))


if __name__ == "__main__":

    # Unique table initialization
    unique_table = []

    # Input of boolean expression and order of variables
    F = input("Enter the expression: ")
    fun = F.split('+')
    fun = [list(i) for i in fun]
    fun = [item for row in fun[:] for item in row]
    fun = [i.lower() for i in fun]

    order = input("Enter the order of ROBDD implementation: ")
    order = order.split('<')

    if set(order) == set(fun):
        # Function for building the ROBDD of a given boolean expression and order of variables
        build(F, order, 0)

        # Printing the ROBDD
        ROBDD = {unique_table[i].funct: [
            unique_table[i].right, unique_table[i].left] for i in range(len(unique_table))}
        ROBDD = dict(list(ROBDD.items())[::-1])
        print(ROBDD)
    else:
        print("Wrong input format")
