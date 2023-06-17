def parserId(tokens):
    return tokens[0].isidentifier()

def parserType(tokens):
    return tokens[0] in ['bit', 'int']

def parserValue(tokens):
    return True

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
                    print('CREATE DATABASE <id> ;') # pode ser retornado true se tiver acabado os tokens <- melhor retornar depois de tudo no finaly do try except
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
                            tokens = moreThanOneIdType(tokens)
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
                
    if tokens[0] == 'INSERT':
        tokens.pop(0)
        if tokens[0] == 'INTO':
            tokens.pop(0)
            if parserId(tokens):
                tokens.pop(0)
                if tokens[0] == '(':
                    tokens.pop(0)
                    if parserId(tokens):
                        tokens.pop(0)
                        tokens = moreThanOneId(tokens)
                        if tokens[0] == ')':
                            tokens.pop(0)
                            if tokens[0] == 'VALUES':
                                tokens.pop(0)
                                if tokens[0] == '(':
                                    tokens.pop(0)
                                    if parserValue(tokens):
                                        tokens.pop(0)
                                        tokens = moreThanOneValue(tokens)
                                        if tokens[0] == ')':
                                            tokens.pop(0)
                                            tokens = moreThanOneRegister(tokens)
                                            if tokens[0] == ';':
                                                tokens.pop(0)
                                                print('INSERT INTO')
    if tokens[0] == 'SELECT':
        tokens.pop(0)
        if tokens[0] == '*':
            tokens.pop(0)
            if tokens[0] == 'FROM':
                tokens.pop(0)
                if parserId(tokens):
                    tokens.pop(0)
                    if tokens[0] == ';':
                        tokens.pop(0)
                        print('SELECT * FROM ID')
                    if tokens[0] == 'ORDER':
                        tokens.pop(0)
                        if tokens[0] == 'BY':
                            tokens.pop(0)
                            if parserId(tokens):
                                tokens.pop(0)
                                if tokens[0] == ';':
                                    tokens.pop(0)
                                    print('SELECT * FROM ID ORDER BY ID;')
                    if tokens[0] == 'WHERE':
                        tokens.pop(0)
                        if parserId(tokens):
                            tokens.pop(0)
                            if tokens[0] == '=':
                                tokens.pop(0)
                                if parserValue(tokens):
                                    tokens.pop(0)
                                    if tokens[0] == ';':
                                        tokens.pop(0)
                                        print('SELECT * FROM ID WHERE ID = VALOR;')
        if parserId(tokens):
            tokens.pop(0)
            tokens = moreThanOneId(tokens)
            if tokens[0] == 'FROM':
                tokens.pop(0)
                if parserId(tokens):
                    tokens.pop(0)
                    if tokens[0] == ';':
                        tokens.pop(0)
                        print('SELECT ID FROM ID')
                        
                            
                                        

# tokens = ['CREATE', 'TABLE', 'Persons', '(', 'PersonID', 'int', ',', 'LastName', 'bit', ')', ';']   

def moreThanOneIdType(tokens):
    if tokens[0] == ',':
        tokens.pop(0)
        if parserId(tokens):
            tokens.pop(0)
            if parserType(tokens):
                tokens.pop(0)
                tokens = moreThanOneIdType(tokens)
    return tokens

def moreThanOneId(tokens):
    if tokens[0] == ',':
        tokens.pop(0)
        if parserId(tokens):
            tokens.pop(0)
            tokens = moreThanOneId(tokens)
    return tokens   

def moreThanOneValue(tokens):
    if tokens[0] == ',':
        tokens.pop(0)
        if parserValue(tokens):
            tokens.pop(0)
            tokens = moreThanOneValue(tokens)
    return tokens

def moreThanOneRegister(tokens):
    if tokens[0] == ',':
        tokens.pop(0)
        if tokens[0] == '(':
            tokens.pop(0)
            if parserValue(tokens):
                tokens.pop(0)
                tokens = moreThanOneValue(tokens) 
                if tokens[0] == ')':
                    tokens.pop(0)
                    tokens = moreThanOneRegister(tokens)
    return tokens
        

# Gramática

# CREATE TABLE id (id tipo D); 
# D -> ,id tipo D | e <- moreThanOneIdType

# INSERT INTO id(id I) VALUES (valor V) V';
# I -> ,id I | e <- moreThanOneId
# V -> ,valor V | e <- moreThanOneValue
# V' -> ,(valor V) V' | e  <- moreThanOneRegister

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

    # Teste 1: comando válido
    # tokens = ['CREATE', 'TABLE', 'Persons', '(', 'PersonID', 'int', ',', 'LastName', 'bit', ')', ';']
    # parser(tokens)
    
    # Teste 2: comando inválido (faltando ";")
    # tokens = ['CREATE', 'TABLE', 'Persons', '(', 'PersonID', 'int', ',', 'LastName', 'bit', ')']
    # parser(tokens)
    
    # Teste 1: comando válido
    # tokens = ['INSERT', 'INTO', 'produtos', '(', 'id', ',', 'descricao', ',', 'categoria', ',', 'preco', ')', 'VALUES', '(', '4', ',', 'Resma Ofício primeiro', ',', '2', ',', '17.50', ')', ',', '(', '5', ',', 'Resma Ofício segundo', ',', '3', ',', '23.00', ')', ';']
    # parser(tokens)

    # Teste 2: comando inválido (faltando ";")
    # tokens = ['INSERT', 'INTO', 'produtos', '(', 'id', ',', 'descricao', ',', 'categoria', ',', 'preco', ')', 'VALUES', '(', '4', ',', 'Resma Ofício primeiro', ',', '2', ',', '17.50', ')', ',', '(', '5', ',', 'Resma Ofício segundo', ',', '3', ',', '23.00', ')']
    # parser(tokens)

    # Teste 1: comando válido
    # tokens = ['SELECT', '*', 'FROM', 'alunos', ';']
    # parser(tokens)

    # Teste 2: comando inválido (faltando ";")
    # tokens = ['SELECT', '*', 'FROM', 'alunos']
    # parser(tokens)

    
if __name__ == "__main__":
    main()
