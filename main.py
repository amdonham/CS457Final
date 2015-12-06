import operator

def get_operator_fn(op):
    return {
        '=' : operator.eq,
        '>' : operator.gt,
        '<' : operator.lt,
        '>=' : operator.ge,
        '<=' : operator.le
        }[op]

def printAllFields(filePointer):
    for line in filePointer:
        print(line)

def parseConditions(conditions):
    returnConditions = list()
    conditions = conditions.split(" ")
    statement = list()
    for condition in conditions:
        if condition == "and" or condition == "or":
            returnConditions.append(statement)
            returnConditions.append(condition)
            statement = list()
        else:
            statement.append(condition)
    returnConditions.append(statement)
    return returnConditions



def filterFields(parsedFields,fields):
    returnList = list()
    returnRow = ''
    fields = fields.split("+")
    for row in parsedFields:
        row = row.split(" ")
        for field in fields:
            for i in range(0, int(len(row)/2)):
                rowField = row[2*i].strip(":")
                rowValue = row[2*i + 1]
                if rowField == field:
                    returnRow += rowField + ": " + rowValue + " "
        if returnRow != '':
            returnList.append(returnRow)
        returnRow = ''
    return returnList







def clean(db):
    newDB = list()
    for row in db:
        row = row.strip(" \n")
        newDB.append(row)
    return newDB

def filter(conditions,db):
    result = list()
    isAnd = False
    isOr = False
    for condition in conditions:
        if condition != "and" and condition != "or" and not isAnd and not isOr:
            for row in db:
                field = condition[0]
                operator = get_operator_fn(condition[1])
                value = condition[2]
                rowFields = row.split(" ")
                rowAppended = False
                for i in range(0,int(len(rowFields)/2)):
                    if not rowAppended:
                        rowField = rowFields[2*i].strip(":")
                        rowValue = rowFields[2*i + 1]
                        if field == rowField:
                            if operator(rowValue,value):
                                result.append(row)
                                rowAppended = True
        if isAnd:
            tempConditions = list()
            tempConditions.append(condition)
            result = filter(tempConditions, result)
            isAnd = False
        if isOr:
            tempConditions = list()
            tempConditions.append(condition)
            tempResult = filter(tempConditions, db)
            for item in tempResult:
                result.append(item)
            isOr = False
        if condition == "and":
            isAnd = True
        if condition == "or":
            isOr = True

    return result

def main():
    print("NoSQL Interpreter")
    #query = input("Enter a query: ")
    query = "db.CS457.query(Manager = 555, SNum+Dept)"
    query = query.split(".")
    db = ''
    with open (query[1]+'.txt', 'r') as collection:
        db = collection.readlines()
        db = clean(db)
    collection.close()
    #print(db)
    command = query[2].split("(")[0]
    parameters = query[2].split("(")[1].strip(")")
    if command == "query":
        if parameters == '':
            printAllFields(collection)
        else:
            parameters = parameters.split(",")
            conditions = parseConditions(parameters[0])
            parsedFields = filter(conditions, db)
            returnFields = filterFields(parsedFields,parameters[1].strip(" "))
            for row in returnFields:
                print(row)






main()

