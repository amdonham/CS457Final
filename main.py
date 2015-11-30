def printAllFields(filePointer):
    for line in filePointer:
        print(line)

def getConditions(conditions):
    returnConditions = list()
    if conditions.find("and") != -1:
        conditions = conditions.split("and")
        returnConditions.append("and")
    elif conditions.find("or") != -1:
        conditions = conditions.split("or")
        returnConditions.append("or")
    else:
        returnConditions.append("none")
    for condition in conditions:
        condition = condition.split(" ")
        pieces = list()
        for piece in condition:
            if piece != "":
                pieces.append(piece)
        returnConditions.append(pieces)
    return returnConditions
def getFields(fields):
    returnFields = list()
    fields = fields.split(" ")
    while(len(fields)  > 0):
        field0 = fields[0]
        field1 = fields[1]
        returnFields.append([field0.strip(":"), field1.strip("\n")])
        fields.remove(field0)
        fields.remove(field1)
    return returnFields

def processConditions(conditions,filePointer):
    remainingFields = list()
    for condition in conditions:
        if condition[1] == "=":
            successfulConditions = list()
            for line in filePointer:
                fields = getFields(line)
                isTrue = False
                for field in fields:
                    if field[0] == condition[0] and field[1] == condition[2]:
                        isTrue = True
                if(isTrue):
                    remainingFields.append(fields)

        # elif condition[1] == "<":
        # elif condition[1] == ">":
        # elif condition[1] == "<=":
        # elif condition[1] == ">=":
    return remainingFields

def main():
    print("NoSQL Interpreter")
    #query = input("Enter a query: ")
    query = "db.CS457.query(Age > 15 and Manager = 555)"
    query = query.split(".")
    with open (query[1]+'.txt', 'r') as collection:
        command = query[2].split("(")[0]
        if command == "query":
            parameters = query[2].split("(")[1].strip(")")
            if parameters == '':
                printAllFields(collection)
            else:
                parameters = parameters.split(",")
                conditions = getConditions(parameters[0])
                fields = processConditions(conditions, collection)
                print(fields)
                #fields = getFields(parameters[1])
                for parameter in parameters:
                    for doc in collection:
                        for field in doc:
                            if field.find(parameter) != -1:
                                print(field)


main()

