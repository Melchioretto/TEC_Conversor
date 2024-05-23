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
    
    # Corrigir a posição do texto_modificado
    texto_modificado = '\n'.join(lines)

    with open(output_file, 'w') as f_output:
        f_output.writelines(texto_modificado)
    
    if lines[0].startswith(' Sipser'):
        pass
    else:
        escreve_multiplas(input_file,output_file)

def rotina_duplamente(input_file, output_file):
    palavras_unicas = set()
    simbolos_fita = set()
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
                if parts[1] != '_':
                    simbolos_fita.add(parts[1])
        print(palavras_unicas)
        print(simbolos_fita)
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
    return palavras_unicas, simbolos_fita

def escreve_multiplas(input_file, output_file):
    palavras_unicas, simbolos_fita = rotina_duplamente(input_file, output_file)
    lista_palavras_unicas = list(palavras_unicas)
    lista_palavras_fita = list(simbolos_fita)
    pattern_template = """
{prefix}passaHash {palavra} _ r {prefix}passaHash{palavra}
"""
    with open(output_file, 'a') as outfile:  # Abrir em modo append
        for prefix in lista_palavras_unicas:
            for palavra in lista_palavras_fita:
                outfile.write(pattern_template.format(prefix=prefix, palavra=palavra) + '\n')

#################################################################
    pattern_template = """
{prefix} # # r {prefix}passaHash
{prefix}passaHash _ _ r {prefix}passaHashBranco
{prefix}passaHashBranco _ _ r {prefix}passaHashBranco
"""
    with open(output_file, 'a') as outfile:  # Abrir em modo append
        for prefix in lista_palavras_unicas:
            outfile.write(pattern_template.format(prefix=prefix) + '\n')
# Chamada da função escreve_multipla

#################################################################
    pattern_template = """
{prefix}passaHashBranco {palavra} _ r {prefix}passaHash{palavra}
"""
    with open(output_file, 'a') as outfile: 
        for palavra in lista_palavras_fita:
            for prefix in lista_palavras_unicas:
                outfile.write(pattern_template.format(prefix=prefix, palavra=palavra) + '\n')

#################################################################
    pattern_template = """
{prefix}passaHash{palavra} {palavra2} {palavra} r {prefix}passaHash{palavra2}
"""
    with open(output_file, 'a') as outfile: 
        for prefix in lista_palavras_unicas:
            for palavra in lista_palavras_fita:
                    for palavra2 in lista_palavras_fita:
                        outfile.write(pattern_template.format(prefix=prefix, palavra=palavra, palavra2=palavra2) + '\n')


#################################################################
    pattern_template = """
{prefix}passaHashBranco{palavra} _ 0 r {prefix}
{prefix}passaHash{palavra} _ {palavra} r {palavra}volta{prefix}
{palavra}volta{prefix} * * l {palavra}volta{prefix}
{palavra}volta{prefix} # # r {prefix}
"""
    with open(output_file, 'a') as outfile: 
        for palavra in lista_palavras_fita:
            for prefix in lista_palavras_unicas:
                outfile.write(pattern_template.format(prefix=prefix, palavra=palavra) + '\n')
########################################################################
    lista_exclusao = ['0', 'passa0', 'passa1', 'marcaFim', 'retornaInicio']
    primeiras_palavras = set()  # Usar um conjunto para evitar duplicatas

 
    with open(output_file, 'r') as f:
        for line in f:
            # Ignora linhas que começam com ';'
            if line.startswith(';'):
                continue

            # Divide a linha em palavras
            palavras = line.strip().split()
            if palavras:
                # Pega a primeira palavra
                primeira_palavra = palavras[0]

                # Verifica se a primeira palavra não está na lista de exclusão
                if primeira_palavra not in lista_exclusao:
                    primeiras_palavras.add(primeira_palavra)  # Adiciona ao conjunto
    pattern_template = """{palavra} & _ r espaçoDireita{palavra}
espaçoDireita{palavra} _ & l {palavra}
"""
    with open(output_file, 'a') as outfile: 
        for palavra in primeiras_palavras:
                outfile.write(pattern_template.format(palavra=palavra) + '\n')


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
