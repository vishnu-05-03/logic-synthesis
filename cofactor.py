# Program to find the cofactor of a boolean expression with respect to a term

"""
Input format is SoP and COMPLIMENTED literal is represented BY UPPER CASE and UNCOMPLEMENTED literal is represented BY LOWER CASE.
Example: A'B'C + A'BC + AB'C + ABC
Enter the expression: ABc+Abc+aBc+abc
Enter the term with respect to which you want to find the cofactor: a
Output: Bc+bc
"""

# Input SoP expression
f = 'ABc+Abc+aBc+abc' #input("Enter the expression: ")

# Input the term with respect to which you want to find the cofactor. It can be term with more than one literals
cwt = 'a' #input("Enter the term with respect to which you want to find the cofactor: ")

# seperating the string for further processing
f = f.split("+")
f = [list(i) for i in f]

# Function for finding the cofactor of a boolean SoP expression with respect to a single literal
def cofactor(f, cwt):

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
    f = cofactor(f, i)

# Combining the reduced expression to a single string
reduced_exp = ""
for i in f:
    reduced_exp += "".join(i)
    reduced_exp += "+"
reduced_exp = reduced_exp.rstrip("+")


# Printing the reduced expression
print(reduced_exp)
