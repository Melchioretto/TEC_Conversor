import linecache

# Fiz essa função para tirar os comentarios do texto... só não está tirando os que estão na mesma linha d comando.
def filtrar_linhas(input_file, output_file):
    with open(input_file, 'r') as f_input:
        lines = f_input.readlines()

    if lines[0].startswith(';S'):
        lines[0] = 'Sipser\n'
        
    elif lines[0].startswith(';I'):
        lines[0] = 'Infinite\n'
    for i in range(len(lines)):
        if ';' in lines[i]:
            partes = lines[i].split(';')    
            lines[i] = partes[0]

        # Juntar as linhas de volta em um único texto
        texto_modificado = '\n'.join(lines)

    with open(output_file, 'w') as f_output:
        f_output.writelines(texto_modificado)
    if lines[0].startswith('Sipser'):
        sipser_machine(output_file)
    else:
        infinite_machine()

def sipser_machine(output_file):
# Tenho quer ver
    lines_copy = []
    with open(output_file, 'r+') as f_input:
        lines = f_input.readlines()
        if lines[0].startswith('Sipser'):
           lines[0] =  ';Spiser\n'
        for linha in lines:
            first_position = linha[0]
            if first_position == '0':
              lines_copy.append(linha.strip())
    linhas_bkp = list(lines_copy)

    print(lines_copy)
#########################################################################
# Modificar o arquivo original para adicionar texto na última linha
    with open(output_file, 'r+') as f_input:
        last_line = linecache.getline(output_file, len(lines))
        if not last_line.endswith('\n'):
            f_input.write('\n')
        f_input.seek(0, 2) 
        f_input.write(';Modificações\n')
#########################################################################
#tenho que ver

#########################################################################
# Tenho que ver
    for i in range(len(lines_copy)):
    # Dividir a linha em palavras
        palavras = lines_copy[i].split()
        # Verificar se existem pelo menos três palavras na linha
        if len(palavras) >= 4:
            # Substituir a palavra na posição 3 (índice 2) por "nova_palavra"
            if palavras[1] == '0':
                palavras[2] = "0"
            if palavras[1] == '1':
                palavras[2] = "1"
            if palavras[3] == 'r':
                palavras[3] = "l"
            palavras[4] = 'ini'
            # Juntar as palavras de volta em uma linha modificada
            lines_copy[i] = ' '.join(palavras)
    print (lines_copy)
    with open(output_file, 'r+') as arquivo:
        linhas = arquivo.readlines()
        for i, linha in enumerate(linhas):
            if linha.startswith("0"):
                linhas[i] = lines_copy[i % len(lines_copy)] + "\n" 
        arquivo.seek(0)
        arquivo.writelines(linhas)
        arquivo.truncate()  
#aqui é a parte da rotina que coloca o # no começo
        arquivo.seek(0, 2)
        arquivo.write('ini * # a1')
        print(linhas_bkp)
        linhas_modificadas = ['ini' + string[1:] for string in linhas_bkp]
        print(linhas_modificadas)
#########################################################################

def infinite_machine():
    pass


input_file = 'entrada.txt'
output_file = 'saida.txt'
filtrar_linhas(input_file, output_file)


