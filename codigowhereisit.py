from tkinter import *
import json

# Função para carregar os dados do arquivo (se existir) ou criar um novo dicionário
def carregar_dados(nome_arquivo):
    try:
        with open(nome_arquivo, 'r') as arquivo:
            dados = json.load(arquivo)
    except FileNotFoundError:
        dados = {}
    return dados

# Função para salvar os dados no arquivo
def salvar_dados(nome_arquivo, dados):
    with open(nome_arquivo, 'w') as arquivo:
        json.dump(dados, arquivo, indent=4)

# Função para adicionar ou atualizar um objeto em um cômodo
def adicionar_objeto(casa, comodo, objeto, tipo, quantidade):
    if comodo not in casa:
        casa[comodo] = []
    casa[comodo].append({
        "objeto": objeto,
        "tipo": tipo,
        "quantidade": quantidade
    })

# Função para listar os objetos em um cômodo
def listar_objetos_em_comodo(casa, comodo):
    if comodo in casa:
        return [f"{obj['objeto']} ({obj['tipo']}, {obj['quantidade']})" for obj in casa[comodo]]
    else:
        return []

# Função para criar uma nova janela
def criar_janela():
    janela = Toplevel(janela1)
    janela.title("Gerenciador de Objetos")
    return janela

# Função para adicionar um objeto em uma janela secundária
def adicionar_objeto_janela(janela, casa, comodo, objeto, tipo, quantidade):
    adicionar_objeto(casa, comodo, objeto, tipo, quantidade)
    salvar_dados(nome_arquivo, casa)
    janela.destroy()

# Função para listar objetos em um cômodo e exibir em uma nova janela
def listar_objetos_em_comodo_janela():
    comodo = entry_comodo.get()
    objetos = listar_objetos_em_comodo(casa, comodo)

    janela_objetos_comodo = criar_janela()
    janela_objetos_comodo.title(f"Objetos em {comodo}")

    if objetos:
        texto_objetos = Label(janela_objetos_comodo, text="\n".join(objetos))
        texto_objetos.pack()
    else:
        texto_vazio = Label(janela_objetos_comodo, text="Nenhum objeto encontrado neste cômodo.")
        texto_vazio.pack()

# Funcao para renomear um objeto
def rename_object():
    old_object = input("Qual o nome do objeto que deseja renomear?\n")
    new_name = input("Qual é o novo nome do objeto?\n")
    comodo = input("Em qual cômodo o objeto está localizado?\n")

    if comodo in casa and any(obj['objeto'] == old_object for obj in casa[comodo]):
        for obj in casa[comodo]:
            if obj['objeto'] == old_object:
                obj['objeto'] = new_name  # Altera o nome do objeto
                salvar_dados(nome_arquivo, casa)
                print(f"O objeto '{old_object}' foi renomeado para '{new_name}' no cômodo '{comodo}'.")
                break
    else:
        print(f"O objeto '{old_object}' não foi encontrado no cômodo '{comodo}' ou o cômodo não existe.")

# Função para remover um objeto
def remove_object():
    old_object = input("Qual o nome do objeto que deseja remover?\n")
    comodo = input("Em qual cômodo você deseja remover o objeto?\n")

    if comodo in casa and any(obj['objeto'] == old_object for obj in casa[comodo]):
        for obj in casa[comodo]:
            if obj['objeto'] == old_object:
                casa[comodo].remove(obj)
                salvar_dados(nome_arquivo, casa)
                print(f"O objeto '{old_object}' foi removido do cômodo '{comodo}'.")
                break
    else:
        print(f"O objeto '{old_object}' não foi encontrado no cômodo '{comodo}' ou o cômodo não existe.")

# Função para mover um objeto
def move_object():
    old_object = input("Qual o nome do objeto que deseja mover?\n")
    old_place = input("Qual o lugar atual do objeto?\n")

    if old_place in casa and old_object in [obj['objeto'] for obj in casa[old_place]]:
        print(f"Objeto a ser movido: {old_object}")
        
        def confirm_move(new_place):
            if new_place:
                if new_place in casa:
                    if old_object in [obj['objeto'] for obj in casa[new_place]]:
                        print(f"O objeto '{old_object}' já está no local '{new_place}'")
                    else:
                        for obj in casa[old_place]:
                            if obj['objeto'] == old_object:
                                casa[old_place].remove(obj)
                                obj_copy = obj.copy()
                                casa[new_place].append(obj_copy)
                        salvar_dados(nome_arquivo, casa)
                        janela_secundaria.destroy()
                else:
                    print(f"O local '{new_place}' não existe.")
            else:
                print("O novo local não pode ficar em branco.")
        
        # Crie uma nova janela secundária para receber o novo local do objeto
        janela_secundaria = criar_janela()
        janela_secundaria.title("Mover Objeto")
        
        texto_orientacao5 = Label(janela_secundaria, text=f'Mover o objeto "{old_object}" para:')
        texto_orientacao5.grid(column=0, row=0)
        
        label_new_place = Label(janela_secundaria, text='Novo Local:')
        label_new_place.grid(column=0, row=1)
        
        entry_new_place = Entry(janela_secundaria)
        entry_new_place.grid(column=1, row=1)
        
        botao_confirmar_move = Button(janela_secundaria, text='Confirmar', command=lambda: confirm_move(entry_new_place.get()))
        botao_confirmar_move.grid(column=0, row=2)
    else:
        print(f"O objeto '{old_object}' não está no local '{old_place}'")

# Função para procurar um objeto
def search_object():

    old_object = input("Qual o nome do objeto?\n")
    print("Objeto: " + old_object)
    
    # Lista para armazenar os cômodos onde o objeto foi encontrado
    comodos_encontrados = []

    # Iterar pelos cômodos
    for comodo, objetos in casa.items():
        for objeto in objetos:
            if objeto["objeto"] == old_object:
                comodos_encontrados.append(comodo)

    if comodos_encontrados:
        print(f"O objeto '{old_object}' foi encontrado nos cômodos: {', '.join(comodos_encontrados)}")
    else:
        print(f"O objeto '{old_object}' não foi encontrado em nenhum cômodo.")

    # Resto do seu código...

    
    # Crie uma nova janela secundária
    janela_secundaria = criar_janela()

    # Inserir texto na janela
    texto_orientacao4 = Label(janela_secundaria, text='Renomear objeto')
    texto_orientacao4.grid(column=0, row=3)

    botao4 = Button(janela_secundaria, text='Clique aqui', command=rename_object)
    botao4.grid(column=0, row=4)

    texto_orientacao5 = Label(janela_secundaria, text='Mudar local do objeto')
    texto_orientacao5.grid(column=1, row=3)

    botao5 = Button(janela_secundaria, text='Clique aqui', command=move_object)
    botao5.grid(column=1, row=4)

    texto_orientacao6 = Label(janela_secundaria, text='Remover objeto')
    texto_orientacao6.grid(column=2, row=3)

    botao6 = Button(janela_secundaria, text='Clique aqui', command=remove_object)
    botao6.grid(column=2, row=4)

# Função para listar objetos em um cômodo e exibir em uma nova janela
def objects_in_place_x():
    desired_place = input("Tu desejas saber os objetos de que lugar?\n")
    print("Lugar desejado: " + desired_place)

    if desired_place == "sala":
        objetos = listar_objetos_em_comodo(casa, desired_place)
        if objetos:
            print(f"Os objetos presentes em {desired_place} são: {', '.join(objetos)}")
        else:
            print('Não há objetos guardados nesse lugar!')
    else:
        print('Lugar não encontrado!')

# Função para adicionar um objeto
def add_object():
    new_object = input("Qual o nome do objeto?\n")
    new_object_type = input("Qual o tipo do objeto?\n")
    new_object_place = input("Qual o lugar onde o novo objeto vai ser guardado?\n")
    new_object_amount = input("Qual a quantidade do objeto?\n")

    # Crie uma nova janela secundária
    janela_secundaria = criar_janela()
    janela_secundaria.title("Adicionar Objeto")

    # Inserir texto na janela secundária
    texto_orientacao7 = Label(janela_secundaria, text='Adicionar objeto')
    texto_orientacao7.grid(column=0, row=0)

    label_comodo = Label(janela_secundaria, text='Comodo:')
    label_comodo.grid(column=0, row=1)

    entry_comodo = Entry(janela_secundaria)
    entry_comodo.grid(column=1, row=1)

    label_objeto = Label(janela_secundaria, text='Objeto:')
    label_objeto.grid(column=0, row=2)

    entry_objeto = Entry(janela_secundaria)
    entry_objeto.grid(column=1, row=2)

    botao_adicionar = Button(janela_secundaria, text='Adicionar', command=lambda: adicionar_objeto_janela(janela_secundaria, casa, entry_comodo.get(), entry_objeto.get(), new_object_type, new_object_amount))
    botao_adicionar.grid(column=0, row=3)

# Nome do arquivo para salvar os dados
nome_arquivo = "dados_casa.json"

# Carrega os dados existentes (ou cria um novo dicionário)
casa = carregar_dados(nome_arquivo)

# Início
janela1 = Tk()
janela1.title('Clique no que desejas fazer:')

texto_orientacao1 = Label(janela1, text='Procurar objeto')
texto_orientacao1.grid(column=0, row=0)

botao1 = Button(janela1, text='clique aqui', command=search_object)
botao1.grid(column=0, row=1)

texto_orientacao2 = Label(janela1, text='Quais objetos num local x')
texto_orientacao2.grid(column=1, row=0)

entry_comodo = Entry(janela1)
entry_comodo.grid(column=1, row=1)

botao2 = Button(janela1, text='clique aqui', command=listar_objetos_em_comodo_janela)
botao2.grid(column=1, row=2)

texto_orientacao3 = Label(janela1, text='Adicionar objeto')
texto_orientacao3.grid(column=2, row=0)

botao3 = Button(janela1, text='clique aqui', command=add_object)
botao3.grid(column=2, row=1)

janela1.mainloop()
