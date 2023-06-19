import re
import tkinter as tk

# Lista para armazenar o reconhecimento dos padrões
log = []

def parserId(tokens):
    if tokens:
        return tokens[0].isidentifier()
    return False

def parserType(tokens):
    return tokens[0].upper() in ['INTEGER', 'VARCHAR', 'BOOLEAN', 'FLOAT', 'DATE', 'TIME', 'DATETIME', 'TEXT', 'CHAR', 'BINARY', 'DOUBLE', 'NUMERIC', 'DECIMAL', 'BIT']

def parserValue(tokens):
    return True
    
def createDatabaseParser(tokens):
    completedCommand = False
    if parserId(tokens):
        tokens.pop(0)
        if tokens and tokens[0] == ';':
            # É necessário verificar se ainda tem comandos seguintes depois de reconhecer um comando, se sim, chama parser() recursivamente
            tokens.pop(0) # pop() deve ser feito apenas se ainda tiver comandos
            log.append('CREATE DATABASE <id>;')
            completedCommand = True
    if not completedCommand:
        return False
    return tokens

def createTableParser(tokens):
    completedCommand = False
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
                        if tokens and tokens[0] == ';':
                            tokens.pop(0)
                            log.append('CREATE TABLE <id> (<id> <tipo> [, <id> <tipo>]*);')
                            completedCommand = True
    if not completedCommand:
        return False
    return tokens

def useParser(tokens):
    completedCommand = False
    if parserId(tokens):
        tokens.pop(0)
        if tokens and tokens[0] == ';':
            tokens.pop(0)
            log.append('USE <id>;')
            completedCommand = True
    if not completedCommand:
        return False
    return tokens
    
def insertParser(tokens):
    completedCommand = False
    if tokens[0].upper() == 'INTO':
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
                        if tokens[0].upper() == 'VALUES':
                            tokens.pop(0)
                            if tokens[0] == '(':
                                tokens.pop(0)
                                if parserValue(tokens):
                                    tokens.pop(0)
                                    tokens = moreThanOneValue(tokens)
                                    if tokens[0] == ')':
                                        tokens.pop(0)
                                        tokens = moreThanOneRegister(tokens)
                                        if tokens and tokens[0] == ';':
                                            tokens.pop(0)
                                            log.append('INSERT INTO <id> (<id> [, <id>]*) VALUES (<valor> [, <valor>]*) [, (<valor> [, <valor>]*)]*;')
                                            completedCommand = True
    if not completedCommand:
        return False
    return tokens
    
def selectAllFromIdParser(tokens):
    completedCommand = False
    log.append('SELECT * FROM <id>;')
    completedCommand = True
    if not completedCommand:
        return False
    return tokens
    
def selectOrderByParser(tokens):
    completedCommand = False
    if tokens[0].upper() == 'BY':
        tokens.pop(0)
        if parserId(tokens):
            tokens.pop(0)
            if tokens and tokens[0] == ';':
                tokens.pop(0)
                log.append('SELECT * FROM <id> ORDER BY <id>;')
                completedCommand = True
    if not completedCommand:
        return False
    return tokens
    
def selectWhereParser(tokens):
    completedCommand = False
    if parserId(tokens):
        tokens.pop(0)
        if tokens[0] == '=':
            tokens.pop(0)
            if parserValue(tokens):
                tokens.pop(0)
                if tokens and tokens[0] == ';':
                    tokens.pop(0)
                    log.append('SELECT * FROM <id> WHERE <id> = <valor>;')
                    completedCommand = True
    if not completedCommand:
        return False
    return tokens  
        
def selectIdFromIdParser(tokens):
    completedCommand = False
    tokens = moreThanOneId(tokens)
    if tokens[0].upper() == 'FROM':
        tokens.pop(0)
        if parserId(tokens):
            tokens.pop(0)
            if tokens and tokens[0] == ';':
                tokens.pop(0)
                log.append('SELECT <id> [, <id>]* FROM <id>;')
                completedCommand = True
    if not completedCommand:
        return False
    return tokens         
    
def updateParser(tokens):
    completedCommand = False
    if parserId(tokens):    
        tokens.pop(0)
        if tokens[0].upper() == 'SET':
            tokens.pop(0)
            if parserId(tokens):
                tokens.pop(0)
                if tokens[0] == '=':
                    tokens.pop(0)
                    if parserValue(tokens):
                        tokens.pop(0)
                        if tokens[0].upper() == 'WHERE':
                            tokens.pop(0)
                            if parserId(tokens):
                                tokens.pop(0)
                                if tokens[0] == '=':
                                    tokens.pop(0)
                                    if parserValue(tokens):
                                        tokens.pop(0)
                                        if tokens and tokens[0] == ';':
                                            tokens.pop(0)
                                            log.append('UPDATE <id> SET <id> = <valor> WHERE <id> = <valor>;')
                                            completedCommand = True
    if not completedCommand:
        return False
    return tokens     
    
def deleteParser(tokens):
    completedCommand = False
    if tokens[0].upper() == 'FROM':
        tokens.pop(0)
        if parserId(tokens):
            tokens.pop(0)
            if tokens[0].upper() == 'WHERE':
                tokens.pop(0)
                if parserId(tokens):
                    tokens.pop(0)
                    if tokens[0] == '=':
                        tokens.pop(0)
                        if parserValue(tokens):
                            tokens.pop(0)
                            if tokens and tokens[0] == ';':
                                tokens.pop(0)
                                log.append('DELETE FROM <id> WHERE <id> = <valor>;')
                                completedCommand = True
    if not completedCommand:
        return False
    return tokens 
    
def truncateParser(tokens):
    completedCommand = False
    if tokens[0].upper() == 'TABLE':
        tokens.pop(0)
        if parserId(tokens):
            tokens.pop(0)
            if tokens and tokens[0] == ';':
                tokens.pop(0)
                log.append('TRUNCATE TABLE <id>;')
                completedCommand = True
                
    if not completedCommand:
        return False
    return tokens 
 
def parser(tokens):
    
    try:
        if tokens[0].upper() == 'CREATE':
            tokens.pop(0)
            
            if tokens[0].upper() == 'DATABASE':
                tokens.pop(0)
                tokens = createDatabaseParser(tokens)
                                       
            elif tokens[0].upper() == 'TABLE':
                tokens.pop(0)
                tokens = createTableParser(tokens)
                                        
        elif tokens[0].upper() == 'USE':
            tokens.pop(0)
            tokens = useParser(tokens)
                    
        elif tokens[0].upper() == 'INSERT':
            tokens.pop(0)
            tokens = insertParser(tokens)
                                                    
        elif tokens[0].upper() == 'SELECT':
            tokens.pop(0)
            if tokens[0] == '*':
                tokens.pop(0)
                if tokens[0].upper() == 'FROM':
                    tokens.pop(0)
                    if parserId(tokens):
                        tokens.pop(0)
                        if tokens and tokens[0] == ';':
                            tokens.pop(0)
                            tokens = selectAllFromIdParser(tokens)
                            
                        elif tokens[0].upper() == 'ORDER':
                            tokens.pop(0)
                            tokens = selectOrderByParser(tokens)
                                        
                        elif tokens[0].upper() == 'WHERE':
                            tokens.pop(0)
                            tokens = selectWhereParser(tokens)
                            
                        else: 
                            return False
                                                                        
            elif parserId(tokens):
                tokens.pop(0)
                tokens = selectIdFromIdParser(tokens)                     
                            
        elif tokens[0].upper() == 'UPDATE':
            tokens.pop(0)
            tokens = updateParser(tokens)
                                                    
        elif tokens[0].upper() == 'DELETE':
            tokens.pop(0)
            tokens = deleteParser(tokens)

        elif tokens[0].upper() == 'TRUNCATE':
            tokens.pop(0)
            tokens = truncateParser(tokens)

        if tokens != False:                                            
            tokens = parser(tokens)
            return tokens
        else:
            return False
        
    except:
        if tokens == []:
            return tokens
        return False 

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

# CREATE DATABASE <id>;
# USE <id>;
# CREATE TABLE <id> (<id> tipo D)

# D -> ,<id> tipo D | e 

# INSERT INTO <id> (<id> I) VALUES (<id> I);

# I -> ,<id> I | e
# V -> ,valor V | e 
# V' -> ,(valor V) V' | e 

# SELECT FROM <id>;
# SELECT <id> [, <id>]* FROM <id>;
# SELECT * FROM <id> ORDER BY <id>;
# SELECT * FROM <id> WHERE <id> = <valor>;
# UPDATE <id> SET <id> = <valor> WHERE <id> = <valor>;
# DELETE FROM <id> WHERE <id> = <valor>;
# TRUNCATE TABLE <id>;

def tokenize_sql(sql):
    patterns = [
        ('KEYWORD', r'(CREATE|DATABASE|USE|TABLE|INSERT|INTO|VALUES|SELECT|FROM|ORDER|BY|WHERE|UPDATE|SET|DELETE|TRUNCATE)', re.IGNORECASE),
        ('TYPE', r'(INTEGER|VARCHAR|BOOLEAN|FLOAT)', re.IGNORECASE),
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

    regex = '|'.join('(?P<%s>%s)' % pair[:2] for pair in patterns)

    for match in re.finditer(regex, sql, re.IGNORECASE):
        token_type = match.lastgroup
        token_value = match.group(token_type)
        yield token_type, token_value.strip('\'"')


def main():
    window = tk.Tk()
    window.title("Parser Descendente Recursivo")
    window.geometry("800x500")
    window.config(bg="#b3d9ff")

    label = tk.Label(window, text="Digite os Comandos SQL:", font=("Arial", 20), bg="#b3d9ff")
    label.pack(pady=(10, 10))

    entry = tk.Text(window, height=15, width=70,font=("Arial", 14), bg="#a0d5f0")
    entry.pack(pady=(10, 10))

    def get_input():
        input = entry.get("1.0", tk.END)
        
        sql_commands = input.splitlines()

        lista_tokens = []
        
        for sql_command in sql_commands:
            tokens = tokenize_sql(sql_command)
            for token_type, token_value in tokens:
                lista_tokens.append(token_value)
            lista_tokens.pop()

        if parser(lista_tokens) == []:
            string_unica = 'PARSER CONCLUÍDO COM SUCESSO!\n\nPadrões reconhecidos (em sequência):\n\n'
            string_unica += '\n'.join(log)
        else:
            string_unica = 'ERRO NO PARSER!'
        
        for widget in window.winfo_children():
            widget.destroy()
    
        window.config(bg="#5776a2")
        output = tk.Label(window, text="RESULTADO:", font=("Arial", 14), bg="#576976")
        output.pack(pady=(10, 10))
        
        mensagem = tk.Message(window, text=string_unica ,font=("Arial", 12))
        mensagem.config(width=800)
        mensagem.pack()

    button = tk.Button(window, text="Enviar", font=("Arial", 14), command=get_input)
    button.pack()

    window.mainloop()
    
if __name__ == "__main__":
    main()