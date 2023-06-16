def parseCreateDatabase(tokens):
    if tokens[0] == "CREATE":
        tokens.pop(0)
        if tokens[0] == "DATABASE":
            tokens.pop(0)
            id = parserId(tokens)
            if id is not None:
                if tokens and tokens[0] == ";":
                    tokens.pop(0)
                    return ("CREATE DATABASE", id)
    return None
    
def parseUse(tokens):
    if tokens[0] == "USE":
        tokens.pop(0)
        id = parserId(tokens)
        if id is not None:
            if tokens and tokens[0] == ";":
                tokens.pop(0)
                return ("USE", id)
    return None

def parserId(tokens):
    return tokens[0].isidentifier()

def parserType(tokens):
    return tokens[0] in ['bit', 'int']

def parser(tokens):
    if tokens[0] == 'CREATE':
        tokens.pop(0)
        if tokens[0] == 'DATABASE':
            tokens.pop(0)
            if parserId(tokens):
                tokens.pop(0)
                if tokens[0] == ';':
                    # É necessário verificar se ainda tem comandos seguintes depois de reconhecer um comando, se sim, chama parser() recursivamente
                    tokens.pop(0) # pop() deve ser feito apenas se ainda tiver comandos
                    print('CREATE DATABASE <id> ;') # pode ser retornado true se tiver acabado os tokens
                    # parser()
        if tokens[0] == 'TABLE':
            tokens.pop(0)
            if parserId(tokens):
                tokens.pop(0)
                if tokens[0] == '(':
                    tokens.pop(0)
                    if parserId(tokens):
                        tokens.pop(0)
                        if parserType(tokens):
                            tokens.pop(0)
                            tokens = someIdType(tokens)
                            if tokens[0] == ')':
                                tokens.pop(0)
                                if tokens[0] == ';':
                                    tokens.pop(0)
                                    print('CREATE TABLE')
    if tokens[0] == 'USE':
        tokens.pop(0)
        if parserId(tokens):
            tokens.pop(0)
            if tokens[0] == ';':
                tokens.pop(0)
                print('USE ID')
                

# tokens = ['CREATE', 'TABLE', 'Persons', '(', 'PersonID', 'int', ',', 'LastName', 'bit', ')', ';']   

def someIdType(tokens):
    if tokens[0] == ',':
        tokens.pop(0)
        if parserId(tokens):
            tokens.pop(0)
            if parserType(tokens):
                tokens.pop(0)
                tokens = someIdType(tokens)
    return tokens

# id (id tipo D)
# D -> ,id tipo D | e

def main():
    # Teste 1: comando válido
    # tokens = ["CREATE", "DATABASE", "mydb", ";"]
    # result = parser(tokens)

    # Teste 2: comando inválido (faltando ";")
    # tokens = ["CREATE", "DATABASE", "mydb"]
    # result = parser(tokens)
    
    # Teste 1: comando válido
    # tokens = ["USE", "mydb", ";"]
    # parser(tokens)

    # Teste 2: comando inválido (faltando ";")
    # tokens = ["USE", "mydb"]
    # parser(tokens)

    tokens = ['CREATE', 'TABLE', 'Persons', '(', 'PersonID', 'int', ',', 'LastName', 'bit', ')', ';']
    parser(tokens)

if __name__ == "__main__":
    main()
