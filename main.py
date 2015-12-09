import operator

def get_operator_fn(op):
    return {
        '=' : operator.eq,
        '>' : operator.gt,
        '<' : operator.lt,
        '>=' : operator.ge,
        '<=' : operator.le
        }[op]

def printAllFields(db):
    for line in db:
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
    id = 1
    for row in db:
        row = row.strip(" \n")
        row = "ID: " + str(id) + " " + row
        newDB.append(row)
        id += 1
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

def sum(field,db):
    returnFields = filterFields(db, field)
    if len(returnFields) == 0:
        return None
    sum = 0
    for item in returnFields:
        if item != None:
            item = item.split(" ")
            sum += int(item[1])
    return sum

def avg(field,db):
    returnFields = filterFields(db, field)
    if len(returnFields) == 0:
     return None
    sum = 0
    count = 0
    for item in returnFields:
        if item != None:
            item = item.split(" ")
            sum += int(item[1])
            count+=1
    avg = sum/count
    return avg

def max(field,db):
    returnFields = filterFields(db, field)
    max = None
    for item in returnFields:
        if item != None:
            item = item.split(" ")
            if max == None or int(item[1]) > max:
                max = int(item[1])
    return max

def cartProds(fields,db):
    fieldVals = list()
    for field in fields:
        fieldVals.append(filterFields(db,field.strip(" ")))
    ret = doCartProd(fieldVals)
    if len(ret) == 0:
        return None
    return ret

def doCartProd(fields):
    retList = list()
    for field in fields[0]:
        for otherField in fields[1]:
            retList.append(field + " " + otherField)
    return retList

def main():
    print("NoSQL Interpreter")
    while(True):
        query = input("Enter a query: ")
        query = query.strip(" ")
        #query = "db.CS457.cartprod(Dept,Age)"
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
                printAllFields(db)
            else:
                parameters = parameters.split(",")
                conditions = parseConditions(parameters[0])
                parsedFields = ''
                if conditions[0][0] != '':
                    parsedFields = filter(conditions, db)
                else:
                    parsedFields = db
                if len(parameters) > 1:
                    returnFields = filterFields(parsedFields, parameters[1].strip(" "))
                    for row in returnFields:
                        print(row)
                else:
                    returnFields = filterFields(parsedFields, '')
                    for row in parsedFields:
                        print(row)

        if command == "sum" :
            field = parameters
            ret = sum(field,db)
            if ret != None:
                print(ret)

        if command == "avg" :
            field = parameters
            ret = avg(field,db)
            if ret != None:
                print(ret)

        if command == "max" :
            field = parameters
            ret = max(field,db)
            if ret != None:
                print(ret)

        if command == "cartprod":
            fields = parameters.split(",")
            ret = cartProds(fields,db)
            if ret != None:
                for item in ret:
                    print(item)



main()

