code = input("waiting for input: ")
code += " "
newcode = ""
lenght =len(code)
idcounter = 1
skip = 0
reserved = ["if","else","while","for","return","class","import","from","break","continue","in","not","and","or","is","None","True","False","print"]

allowed_chars = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789=+-*/^%()_. ")

for i in range(lenght):
    if skip > 0:
        skip -= 1
        continue

    if code[i] not in allowed_chars:
        raise ValueError(f"Invalid character '{code[i]}' at position {i}")
    
    if code[i].isalpha():   #"a"<= code[index] and code[index] <= "z" or "A"<= code[index] and code[index] <= "Z":
        flag = True
        sindex = i # start index
        eindex = i # endd index
        index= i
        while flag :
            index+=1
            if code[index].isalpha() or code[index].isdigit() or code[index]=="_":
                eindex = index
            else:
                flag = False
        #res wordcode

        word = code[sindex:eindex+1]

        if word in reserved:
            newcode += word
        else:
            newcode += "id" + str(idcounter) + " "
            idcounter += 1

        skip = eindex - sindex
    if code[i] == "=":
        newcode += "= "
    if code[i] == "+":
        newcode += "+ "
    if code[i] == "-":
        newcode += "- "
    if code[i] == "":
        newcode += ""
    if code[i] == "/":
        newcode += "/ "
    if code[i] == "^":
        newcode += "^"
    if code[i] == "%":
        newcode += " % "
    if code[i] == "(":
        newcode += "("
    if code[i] == ")":
        newcode += ")"
    if code[i] == ".":
        newcode += "."
    if code[i].isdigit():
        newcode += code[i]

print(newcode)