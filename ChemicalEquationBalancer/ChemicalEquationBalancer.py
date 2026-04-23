"""
Chemical Equation Balancer by Anshu Aramandla
"""

import re
import math
import numpy as np
from sympy import Matrix

def main():
    print("Chemical Equation Balancer. Use () for subgroups and * for hydrates.")
    left = parse(input("Reactants: "), False)
    right = parse(input("Products: "), False)
    newLeft, newRight = balance(left, right)
    highestCoeff = 0
    for molecule in newLeft:
        if molecule[0] > highestCoeff:
            highestCoeff = molecule[0]
    for molecule in newRight:
        if molecule[0] > highestCoeff:
            highestCoeff = molecule[0]
    spacer = len(str(highestCoeff))
    print("Original equation: " + eqToStr(left, right, spacer))
    print("Balanced equation: " + eqToStr(newLeft, newRight, spacer))

# balance equation as system of equations matrix Ax=b
def balance(left, right):
    # array of elements
    elements = []
    for molecule in left + right:
        for elem, _ in simplify(molecule):
            if elem not in elements:
                elements.append(elem)
    # create matrix (rows = elements, columns = molecules)
    numMolecules = len(left) + len(right)
    matrix = [[0]*numMolecules for _ in elements]
    for col, molecule in enumerate(left):
        for elem, num in simplify(molecule):
            row = elements.index(elem)
            matrix[row][col] += num
    for col, molecule in enumerate(right):
        for elem, num in simplify(molecule):
            row = elements.index(elem)
            matrix[row][len(left)+col] -= num
    nullSpace = Matrix(matrix).nullspace()
    # check if solvable
    if not nullSpace:
        print("Not solvable")
        exit()
    result = nullSpace[0]
    # simplify
    overallLCM = math.lcm(*[v.q for v in result])
    coeffs = [int(v * overallLCM) for v in result]
    overallGCD = math.gcd(*coeffs)
    finalCoeffs = [coeff // overallGCD for coeff in coeffs]
    # answers
    newLeft = [[finalCoeffs[i]] + molecule[1:] for i, molecule in enumerate(left)]
    newRight = [[finalCoeffs[i + len(left)]] + molecule[1:] for i, molecule in enumerate(right)]
    return newLeft, newRight

# return array of (element, num) pairs from molecule
def simplify(molecule, multiplier=1):
    result = []
    for item in molecule[1:]:
        if item[0] == "()" or item[0] == "*":
            subscript = item[1]
            for inner in simplify([0] + item[2], multiplier * subscript):
                result.append(inner)
        else:
            result.append((item[0], item[1] * multiplier))
    return result

# equation to string for printing
def eqToStr(left, right, spacer):
    # molecule to string
    def moleculeToStr(molecule):
        returnString = ""
        coeff = molecule[0]
        if coeff == 1:
            returnString += " "*spacer
        else:
            returnString += " "*(spacer - len(str(coeff))) + str(coeff)
        returnString += groupToStr(molecule[1:])
        return returnString
    # for handling subgroups and hydrates
    def groupToStr(group):
        returnString = ""
        for item in group:
            if item[0] == "()":
                subscript = item[1]
                returnString += "(" + groupToStr(item[2]) + ")"
                if subscript != 1:
                    returnString += toSubscript(str(subscript))
            elif item[0] == "*":
                coeff = item[1]
                returnString += "·"
                if coeff != 1:
                    returnString += str(coeff)
                returnString += groupToStr(item[2])
            else:
                elem, subscript = item
                returnString += elem
                if subscript != 1:
                    returnString += toSubscript(str(subscript))
        return returnString
    leftStr = " + ".join(moleculeToStr(i) for i in left)
    rightStr = " + ".join(moleculeToStr(i) for i in right)
    returnString = leftStr + " → " + rightStr
    return returnString

# parse expression in string form, e.g.
# "4Fe + 3O2" -> [[4, ["Fe", 1]], [3, ["O", 2]]]
# "Al(OH)3" -> [[1, ("Al", 1), ("()", 3, [("O", 1), ("H", 1)])]]
# "CuSO4*5H2O" -> [[1, ("Cu", 1), ("S", 1), ("O", 4), ("*", 5, [("H", 2), ("O", 1)])]]
def parse(s, merge):
    molecules = [c.strip() for c in s.split("+")]
    result = []
    for molecule in molecules:
        result.append(parseMolecule(molecule.strip(), merge))
    return result

# parse one molecule
def parseMolecule(s, merge):
    m = re.match(r'^(\d+)', s)
    if m:
        coefficient = int(m.group(1))
        s = s[m.end():]
    else:
        coefficient = 1
    elements = parseGroup(s, merge)
    return [coefficient] + elements

# parse subgroup in parentheses or hydrate dot
def parseGroup(s, merge, multiplier=1):
    elements = []
    i = 0
    while i < len(s):
        if s[i] == "(":
            depth, j = 1, i + 1
            while j < len(s) and depth:
                if s[j] == "(":
                    depth += 1
                elif s[j] == ")":
                    depth -= 1
                j += 1
            inner = s[i+1:j-1]
            m = re.match(r'(\d+)', s[j:])
            sub = int(m.group(1)) if m else 1
            j += m.end() if m else 0
            innerElements = parseGroup(inner, merge, multiplier=1)
            elements.append(("()", sub, innerElements))
            i = j
        elif s[i] == "*":
            i += 1
            # check coefficient of hydrate group
            m = re.match(r'(\d+)', s[i:])
            sub = int(m.group(1)) if m else 1
            i += m.end() if m else 0
            innerElements = parseGroup(s[i:], merge, multiplier=1)
            elements.append(("*", sub, innerElements))
            break
        elif s[i].isupper():
            m = re.match(r'([A-Z][a-z]*)', s[i:])
            el = m.group(1)
            i += m.end()
            m2 = re.match(r'(\d+)', s[i:])
            sub = int(m2.group(1)) if m2 else 1
            i += m2.end() if m2 else 0
            elements.append((el, sub))
        else:
            i += 1
    return elements

def toSubscript(text):
    n = "0123456789+-=()"
    s = "₀₁₂₃₄₅₆₇₈₉₊₋₌₍₎"
    r = text.maketrans(n, s)
    return text.translate(r)

# execute main function
if __name__ == "__main__":
    main()