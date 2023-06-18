import re

def parserId(tokens):
    return tokens[0].isidentifier()

def parserType(tokens):
    return tokens[0] in ['INTEGER', 'VARCHAR', 'BOOLEAN', 'FLOAT']

def parserValue(tokens):
    return True

def parser(tokens):
    if len(tokens) == 0:
        return True
    
    try:
        if tokens[0] == 'CREATE':
            tokens.pop(0)
            if tokens[0] == 'DATABASE':
                tokens.pop(0)
                if parserId(tokens):
                    tokens.pop(0)
                    if tokens[0] == ';':
                        # É necessário verificar se ainda tem comandos seguintes depois de reconhecer um comando, se sim, chama parser() recursivamente
                        tokens.pop(0) # pop() deve ser feito apenas se ainda tiver comandos
                        print('CREATE DATABASE')
                        
                        
            elif tokens[0] == 'TABLE':
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
                                        
        elif tokens[0] == 'USE':
            tokens.pop(0)
            if parserId(tokens):
                tokens.pop(0)
                if tokens[0] == ';':
                    tokens.pop(0)
                    print('USE ID')
                    
                    
        elif tokens[0] == 'INSERT':
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
                                                    
        elif tokens[0] == 'SELECT':
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
                            
                            
                        elif tokens[0] == 'ORDER':
                            tokens.pop(0)
                            if tokens[0] == 'BY':
                                tokens.pop(0)
                                if parserId(tokens):
                                    tokens.pop(0)
                                    if tokens[0] == ';':
                                        tokens.pop(0)
                                        print('SELECT * FROM ID ORDER BY ID;')
                                        
                                        
                        elif tokens[0] == 'WHERE':
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
                                            
                                            
            elif parserId(tokens):
                tokens.pop(0)
                tokens = moreThanOneId(tokens)
                if tokens[0] == 'FROM':
                    tokens.pop(0)
                    if parserId(tokens):
                        tokens.pop(0)
                        if tokens[0] == ';':
                            tokens.pop(0)
                            print('SELECT ID FROM ID')
                            
                            
        elif tokens[0] == 'UPDATE':
            tokens.pop(0)
            if parserId(tokens):    
                tokens.pop(0)
                if tokens[0] == 'SET':
                    tokens.pop(0)
                    if parserId(tokens):
                        tokens.pop(0)
                        if tokens[0] == '=':
                            tokens.pop(0)
                            if parserValue(tokens):
                                tokens.pop(0)
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
                                                    print('UPDATE')
                                                    
        elif tokens[0] == 'DELETE':
            tokens.pop(0)
            if tokens[0] == 'FROM':
                tokens.pop(0)
                if parserId(tokens):
                    tokens.pop(0)
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
                                        print('DELETE')
                                                  

        elif tokens[0] == 'TRUNCATE':
            tokens.pop(0)
            if tokens[0] == 'TABLE':
                tokens.pop(0)
                if parserId(tokens):
                    tokens.pop(0)
                    if tokens[0] == ';':
                        tokens.pop(0)
                        print('TRUNCATE TABLE')
                                            
        
        tokens = parser(tokens)
        return tokens 
        
    except:
        return False
            
# tem que botaros else e disparar excessao
# falta colocar o try except                            

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

# O que falta:
# Separador de tokens
# Fazer a recursão do parser
# Separar comandos em funcoes
# Fazer interface gráfica
# Fazer vídeo
# Fazer relatório
# Enviar

def tokenize_sql(sql):
    # Define as expressões regulares para os diferentes tipos de tokens
    patterns = [
        ('KEYWORD', r'(CREATE|DATABASE|USE|TABLE|INSERT|INTO|VALUES|SELECT|FROM|ORDER|BY|WHERE|UPDATE|SET|DELETE|TRUNCATE)'),
        ('TYPE', r'(INTEGER|VARCHAR|BOOLEAN|FLOAT)'),
        ('IDENTIFIER', r'[a-zA-Z_]\w*'),
        ('NUMBER', r'\d+(\.\d+)?'),
        ('VALUE', r'"[^"]*"|\'[^\']*\''),
        ('SEMICOLON', r';'),
        ('COMMA', r','),
        ('LPAREN', r'\('),
        ('RPAREN', r'\)'),
        ('ASTERISK', r'\*'),
        ('EQUAL', r'='),
        ('EOF', r'$')
    ]

    # Concatena as expressões regulares em uma única expressão
    regex = '|'.join('(?P<%s>%s)' % pair for pair in patterns)

    # Itera pelos tokens encontrados na string de entrada
    for match in re.finditer(regex, sql, re.IGNORECASE):
        token_type = match.lastgroup
        token_value = match.group(token_type)
        yield token_type, token_value.strip('\'"')

def main():
    # Comandos SQL de exemplo
    sql_commands = [
        'CREATE',
        'USE mydb;',
        'CREATE TABLE Persons (PersonID INTEGER, LastName VARCHAR);',
        'INSERT INTO produtos (id, descricao, categoria, preco) VALUES (4, "Resma Ofício primeiro", 2, 17.50 ), (5, "Resma Ofício segundo", 3, 23.00 );',
        'SELECT * FROM alunos;',
        'SELECT * FROM produtos ORDER BY id;',
        'SELECT * FROM produtos WHERE categoria = 1;',
        'SELECT id, descricao, preco FROM produtos;',
        'UPDATE produtos SET preco = 2.00 WHERE id = 1;',
        'DELETE FROM produtos WHERE id = 2;',
        'TRUNCATE TABLE produtos;'
    ]

    lista = []
    # Processa cada comando SQL e imprime os tokens correspondentes
    for sql_command in sql_commands:
        #print("SQL Command:", sql_command)
        tokens = tokenize_sql(sql_command)
        for token_type, token_value in tokens:
            #print("Token:", token_type, "Value:", token_value)
            lista.append(token_value)
        lista.pop()

    #print(lista)
    #print()

    # Teste
    teste = parser(lista)
    print(teste)
    
if __name__ == "__main__":
    main()