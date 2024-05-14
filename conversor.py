import fileinput
import linecache


# a maquina verifica se a entrada ´[e impar, pega o tamanho da entrada (num) e escreva num * x seguiddos de num * 1

# o problema é que quando volta para o incio da palravra depóis de fazer as trocas, nao possui uma leitura de #, que da pau na maquina

# Fiz essa função para tirar os comentarios do texto... só não está tirando os que estão na mesma linha d comando.
def filtrar_linhas(input_file, output_file):
    with open(input_file, 'r') as f_input:
        lines = f_input.readlines()

    if lines[0].startswith(';S'):
        lines[0] = ' Sipser\n'
        
    elif lines[0].startswith(';I'):
        lines[0] = ' Infinite\n'
    for i in range(len(lines)):
        if ';' in lines[i]:
            partes = lines[i].split(';')    
            lines[i] = partes[0]

        # Juntar as linhas de volta em um único texto
        texto_modificado = '\n'.join(lines)

    with open(output_file, 'w') as f_output:
        f_output.writelines(texto_modificado)
    if lines[0].startswith(' Sipser'):
        sipser_machine(output_file)
    else:
        infinite_machine()

def sipser_machine(output_file):
# Tenho quer ver
    lines_copy = []
    with open(output_file, 'r+') as f_input:
        lines = f_input.readlines()
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
        f_input.write('\n;Modificações\n')
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
    print(lines_copy)
    with open(output_file, 'r+') as arquivo:
        linhas = arquivo.readlines()
        n = 0
        for i, linha in enumerate(linhas):
            if linha.startswith("0"):
                linhas[i] = lines_copy[n] + "\n"
                n=n+1
        arquivo.seek(0)
        arquivo.writelines(linhas)
        arquivo.truncate()
       
#aqui é a parte da rotina que coloca o # no começo
        arquivo.seek(0, 2)
        arquivo.write('ini * # r a1')
        print(linhas_bkp)
        linhas_modificadas = ['a1' + string[1:] for string in linhas_bkp]
        print(linhas_modificadas)
        for string in linhas_modificadas:
            arquivo.write('\n' + string)      
#########################################################################

def infinite_machine():
    pass

def substituir_quinta_palavra(output_file):
    # Lista para armazenar as linhas modificadas
    linhas_modificadas = []

    with open(output_file, 'r+') as arquivo:
        for linha in arquivo:
            if linha.startswith(';'):
                linhas_modificadas.append(linha)
                continue

            palavras = linha.strip().split()
            
            if len(palavras) >= 5:
                quinta_palavra = palavras[4]  
                if quinta_palavra == '0':
                    palavras[4] = 'a1'

            linha_modificada = ' '.join(palavras) + '\n'
            linhas_modificadas.append(linha_modificada)

        arquivo.seek(0)
        arquivo.writelines(linhas_modificadas)
        arquivo.truncate()


def final_sipser(output_file):
    palavras_vistas = set()

    with open(output_file, 'r') as arquivo_leitura:
        linhas = arquivo_leitura.readlines()

    with open(output_file, 'a') as arquivo_escrita:
        for linha in linhas:
            if linha.startswith(';'):
                continue
            
            palavras = linha.strip().split()
            if palavras:
                primeira_palavra = palavras[0]
                if primeira_palavra not in palavras_vistas:
                    palavras_vistas.add(primeira_palavra)
                    linha_formatada = primeira_palavra + ' # # r *'
                    arquivo_escrita.write('\n'+linha_formatada )

input_file = 'entrada.txt'
output_file = 'saida.txt'
filtrar_linhas(input_file, output_file)
with open(output_file, 'r+') as arquivo:
    linhas = arquivo.readlines()
    linhas_sem_branco = [linha for linha in linhas if linha.strip()]
    arquivo.seek(0)
    arquivo.writelines(linhas_sem_branco)
    arquivo.truncate()
    linhas = arquivo.read()
    arquivo.seek(0)
    arquivo.write(';' + linhas)
    print("aaaaaaaa")
final_sipser(output_file)
substituir_quinta_palavra(output_file)