import linecache
import pyperclip

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
        texto_modificado = '\n'.join(lines)

    with open(output_file, 'w') as f_output:
        f_output.writelines(texto_modificado)
    if lines[0].startswith(' Sipser'):
        sipser_machine(output_file)
    else:
        infinite_machine(input_file,output_file)

def sipser_machine(output_file):

    lines_copy = []
    with open(output_file, 'r+') as f_input:
        lines = f_input.readlines()
        for linha in lines:
            first_position = linha[0]
            if first_position == '0':
              lines_copy.append(linha.strip())
    linhas_bkp = list(lines_copy)

    with open(output_file, 'r+') as f_input:
        last_line = linecache.getline(output_file, len(lines))
        if not last_line.endswith('\n'):
            f_input.write('\n')
        f_input.seek(0, 2) 
        f_input.write('\n;Modificações\n')
    for i in range(len(lines_copy)):
        palavras = lines_copy[i].split()
        if len(palavras) >= 4:
            if palavras[1] == '0':
                palavras[2] = "0"
            if palavras[1] == '1':
                palavras[2] = "1"
            if palavras[3] == 'r':
                palavras[3] = "l"
            palavras[4] = 'ini'
            lines_copy[i] = ' '.join(palavras)
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

        arquivo.seek(0, 2)
        arquivo.write('ini * # r a1')
        linhas_modificadas = ['a1' + string[1:] for string in linhas_bkp]
        for string in linhas_modificadas:
            arquivo.write('\n' + string) 
    final_sipser(output_file)    

def infinite_machine(input_file, output_file):
    palavras_unicas = set()

    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            parts = line.strip().split()
            if parts[0] == '0':
                parts[0] = 'ini'
                if parts[-1] == '0':
                    parts[-1] = 'ini'
            outfile.write(' '.join(parts) + '\n')
            if not line.startswith(';'):
                palavras_unicas.add(parts[0])

        additional_lines = [
            "0 0 # r passa0",
            "0 1 # r passa1 ",
            "passa0 0 0 r passa0",
            "passa0 1 0 r passa1",
            "passa0 _ 0 r marcaFim",
            "passa1 0 1 r passa0",
            "passa1 1 1 r passa1",
            "passa1 _ 1 r marcaFim",
            "marcaFim _ & l retornaInicio",
            "retornaInicio * * l retornaInicio",
            "retornaInicio # # r ini"
        ]
        outfile.write(';Modificações\n')
        for line in additional_lines:
            outfile.write(line + '\n')

    lista_palavras_unicas = list(palavras_unicas)

    append_patterns_to_file(output_file, lista_palavras_unicas)

def generate_pattern_text(palavra):
    pattern_template = """{0} # # r {0}passaHash
{0}passaHash 0 _ r {0}passaHash0
{0}passaHash 1 _ r {0}passaHash1
{0}passaHash _ _ r {0}passaHashBranco
{0}passaHashBranco _ _ r {0}passaHashBranco
{0}passaHashBranco 0 _ r {0}passaHash0
{0}passaHashBranco 1 _ r {0}passaHash1
{0}passaHash0 0 0 r {0}passaHash0
{0}passaHash0 1 0 r {0}passaHash1
{0}passaHash0 _ 0 r {0}return
{0}passaHash1 1 1 r {0}passaHash1
{0}passaHash1 0 1 r {0}passaHash0
{0}passaHash1 _ 0 r {0}return
{0}passaHash0 & _ r {0}espaçoDireitaHash0
{0}espaçoDireitaHash0 _ & l {0}passaHash0
{0}passaHash1 & _ r {0}espaçoDireitaHash1
{0}espaçoDireitaHash1 _ & l {0}passaHash1
{0} & _ r espaçoDireita{0}
espaçoDireita{0} _ & l {0}
{0}return * * l {0}return
{0}return # # r {0}
"""
    return pattern_template.format(palavra)


def append_patterns_to_file(output_file, lista_palavras):
    with open(output_file, 'a') as file:
        for palavra in lista_palavras:
            file.write(generate_pattern_text(palavra) + '\n')

def extract_first_words(output_file):
    palavras_unicas = set()
    with open(output_file, 'r') as file:
        for line in file:
            linha = line.strip()
            if not linha.startswith(";"):
                primeira_palavra = linha.split()[0]
                palavras_unicas.add(primeira_palavra)
    return list(palavras_unicas)
 
def substituir_quinta_palavra(output_file):
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
    substituir_quinta_palavra(output_file)

############################################################
def copiar_arquivo_para_clipboard(output_file):
    try:
        with open(output_file, 'r') as arquivo:
            conteudo = arquivo.read()
            pyperclip.copy(conteudo)
            notification("Conteúdo do arquivo copiado para a área de transferência.")
    except FileNotFoundError:
        notification(f"Arquivo '{output_file}' não encontrado.")

########################################################################
def notification(mensagem):
    import gi
    gi.require_version('Gtk', '3.0')
    from gi.repository import Gtk
    def show_notification_dialog(mensagem):
        dialog = Gtk.MessageDialog(parent=None, flags=0, message_type=Gtk.MessageType.INFO, buttons=Gtk.ButtonsType.OK, text=mensagem)
        dialog.run()
        dialog.destroy()
    mensagem = "A saída foi copiada para área de transferência\n Só dar um Ctrl + V   :)"
    show_notification_dialog(mensagem)

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
copiar_arquivo_para_clipboard(output_file)
