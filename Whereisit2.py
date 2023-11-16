import tkinter as tk
import json

class Casa:
    def __init__(self, nome_arquivo):
        self.nome_arquivo = nome_arquivo
        self.dados = self.carregar_dados()

    def carregar_dados(self):
        try:
            with open(self.nome_arquivo, 'r') as arquivo:
                return json.load(arquivo)
        except FileNotFoundError:
            return {}

    def salvar_dados(self):
        with open(self.nome_arquivo, 'w') as arquivo:
            json.dump(self.dados, arquivo, indent=4)

    def adicionar_objeto(self, comodo, objeto, tipo, quantidade):
        if comodo not in self.dados:
            self.dados[comodo] = []
        self.dados[comodo].append({
            "objeto": objeto,
            "tipo": tipo,
            "quantidade": quantidade
        })
        self.salvar_dados()

    def listar_objetos_em_comodo(self, comodo):
        if comodo in self.dados:
            return [f"{obj['objeto']} ({obj['tipo']}, {obj['quantidade']})" for obj in self.dados[comodo]]
        else:
            return []

    def renomear_objeto(self, old_object, new_name, comodo):
        if comodo in self.dados and any(obj['objeto'] == old_object for obj in self.dados[comodo]):
            for obj in self.dados[comodo]:
                if obj['objeto'] == old_object:
                    obj['objeto'] = new_name
                    self.salvar_dados()
                    return f"O objeto '{old_object}' foi renomeado para '{new_name}' no cômodo '{comodo}'."
            return f"O objeto '{old_object}' não foi encontrado no cômodo '{comodo}'."
        else:
            return f"O objeto '{old_object}' não foi encontrado no cômodo '{comodo}' ou o cômodo não existe."

    def remover_objeto(self, old_object, comodo):
        if comodo in self.dados and any(obj['objeto'] == old_object for obj in self.dados[comodo]):
            for obj in self.dados[comodo]:
                if obj['objeto'] == old_object:
                    self.dados[comodo].remove(obj)
                    self.salvar_dados()
                    return f"O objeto '{old_object}' foi removido do cômodo '{comodo}'."
            return f"O objeto '{old_object}' não foi encontrado no cômodo '{comodo}'."
        else:
            return f"O objeto '{old_object}' não foi encontrado no cômodo '{comodo}' ou o cômodo não existe."

    def mover_objeto(self, old_object, old_place, new_place):
        if old_place in self.dados and old_object in [obj['objeto'] for obj in self.dados[old_place]]:
            if new_place in self.dados:
                if old_object in [obj['objeto'] for obj in self.dados[new_place]]:
                    return f"O objeto '{old_object}' já está no local '{new_place}'"
                else:
                    for obj in self.dados[old_place]:
                        if obj['objeto'] == old_object:
                            self.dados[old_place].remove(obj)
                            obj_copy = obj.copy()
                            self.dados[new_place].append(obj_copy)
                    self.salvar_dados()
                    return f"O objeto '{old_object}' foi movido de '{old_place}' para '{new_place}'."
            else:
                return f"O local '{new_place}' não existe."
        else:
            return f"O objeto '{old_object}' não está no local '{old_place}'."

    def procurar_objeto(self, old_object):
        comodos_encontrados = []

        for comodo, objetos in self.dados.items():
            for objeto in objetos:
                if objeto["objeto"] == old_object:
                    comodos_encontrados.append(comodo)

        if comodos_encontrados:
            return f"O objeto '{old_object}' foi encontrado nos cômodos: {', '.join(comodos_encontrados)}"
        else:
            return f"O objeto '{old_object}' não foi encontrado em nenhum cômodo."

class InterfaceGrafica:
    def __init__(self, casa):
        self.casa = casa
        self.janela_principal = tk.Tk()
        self.janela_principal.title('Gerenciador de Objetos')

        largura = 500
        altura = 300

        posicao_x = int(self.janela_principal.winfo_screenwidth() / 2 - largura / 2)
        posicao_y = int(self.janela_principal.winfo_screenheight() / 2 - altura / 2)

        self.janela_principal.geometry(f"{largura}x{altura}+{posicao_x}+{posicao_y}")

        self.criar_widgets()

    def criar_widgets(self):
        botao_adicionar_objeto = tk.Button(self.janela_principal, text='Adicionar Objeto', command=self.adicionar_objeto_interface)
        botao_adicionar_objeto.pack(side=tk.TOP, padx=10, pady=10)

        botao_listar_objetos = tk.Button(self.janela_principal, text='Listar Objetos em um Cômodo', command=self.listar_objetos_em_comodo_interface)
        botao_listar_objetos.pack(side=tk.TOP, padx=10, pady=10)

        botao_procurar_objeto = tk.Button(self.janela_principal, text='Procurar Objeto', command=self.procurar_objeto_interface)
        botao_procurar_objeto.pack(side=tk.TOP, padx=10, pady=10)

        botao_remover_objeto = tk.Button(self.janela_principal, text='Remover Objeto', command=self.remover_objeto_interface)
        botao_remover_objeto.pack(side=tk.TOP, padx=10, pady=10)

    def procurar_objeto_interface(self):
        janela_procurar_objeto = tk.Toplevel(self.janela_principal)
        janela_procurar_objeto.title('Procurar Objeto')

        label_objeto = tk.Label(janela_procurar_objeto, text='Objeto:')
        label_objeto.pack()

        entry_objeto = tk.Entry(janela_procurar_objeto)
        entry_objeto.pack()

        botao_procurar = tk.Button(janela_procurar_objeto, text='Procurar', command=lambda: self.procurar_objeto(entry_objeto.get()))
        botao_procurar.pack()

    def procurar_objeto(self, objeto):
        comodos = self.casa.procurar_objeto(objeto)

        if comodos:
            janela_resultado = tk.Toplevel(self.janela_principal)
            janela_resultado.title(f"Localizar {objeto}")

            largura_minima = 400  # largura mínima
            largura_maxima = 1000  # largura máxima
            janela_resultado.minsize(width=largura_minima, height=200)  # altura mínima
            janela_resultado.maxsize(width=largura_maxima, height=600)  # altura máxima

            texto_comodos = tk.Label(janela_resultado, text=comodos, wraplength=largura_maxima)
            texto_comodos.pack()
        else:
            janela_vazia = tk.Toplevel(self.janela_principal)
            janela_vazia.title("Nenhum objeto encontrado")

            texto_vazio = tk.Label(janela_vazia, text="Esse objeto não foi encontrado em nenhum cômodo.", wraplength=600)
            texto_vazio.pack()

    def adicionar_objeto_interface(self):
        janela_adicionar_objeto = tk.Toplevel(self.janela_principal)
        janela_adicionar_objeto.title('Adicionar Objeto')

        label_comodo = tk.Label(janela_adicionar_objeto, text='Comodo:')
        label_comodo.pack()

        entry_comodo = tk.Entry(janela_adicionar_objeto)
        entry_comodo.pack()

        label_objeto = tk.Label(janela_adicionar_objeto, text='Objeto:')
        label_objeto.pack()

        entry_objeto = tk.Entry(janela_adicionar_objeto)
        entry_objeto.pack()

        label_tipo = tk.Label(janela_adicionar_objeto, text='Tipo:')
        label_tipo.pack()

        entry_tipo = tk.Entry(janela_adicionar_objeto)
        entry_tipo.pack()

        label_quantidade = tk.Label(janela_adicionar_objeto, text='Quantidade:')
        label_quantidade.pack()

        entry_quantidade = tk.Entry(janela_adicionar_objeto)
        entry_quantidade.pack()

        botao_confirmar = tk.Button(janela_adicionar_objeto, text='Confirmar', command=lambda: self.adicionar_objeto(janela_adicionar_objeto, entry_comodo.get(), entry_objeto.get(), entry_tipo.get(), entry_quantidade.get()))
        botao_confirmar.pack()


    def adicionar_objeto(self, janela, comodo, objeto, tipo, quantidade):
        self.casa.adicionar_objeto(comodo, objeto, tipo, quantidade)
        janela.destroy()

    def remover_objeto_interface(self):
        janela_remover_objeto = tk.Toplevel(self.janela_principal)
        janela_remover_objeto.title('Remover Objeto')

        label_comodo = tk.Label(janela_remover_objeto, text='Comodo:')
        label_comodo.pack()

        entry_comodo = tk.Entry(janela_remover_objeto)
        entry_comodo.pack()

        label_objeto = tk.Label(janela_remover_objeto, text='Objeto:')
        label_objeto.pack()

        entry_objeto = tk.Entry(janela_remover_objeto)
        entry_objeto.pack()

        botao_remover = tk.Button(janela_remover_objeto, text='Remover', command=lambda: self.remover_objeto(entry_objeto.get(), entry_comodo.get()))
        botao_remover.pack()

    def remover_objeto(self, comodo, objeto):
        resultado = self.casa.remover_objeto(comodo, objeto)

        if resultado:
            janela_resultado = tk.Toplevel(self.janela_principal)
            janela_resultado.title("Resultado da Remoção")

            texto_resultado = tk.Label(janela_resultado, text=resultado)
            texto_resultado.pack()
        else:
            janela_vazia = tk.Toplevel(self.janela_principal)
            janela_vazia.title("Objeto não encontrado")

            texto_vazio = tk.Label(janela_vazia, text="O objeto não foi encontrado no cômodo ou o cômodo não existe.")
            texto_vazio.pack()

    def listar_objetos_em_comodo_interface(self):
        janela_listar_objetos = tk.Toplevel(self.janela_principal)
        janela_listar_objetos.title('Listar Objetos em um Cômodo')

        label_comodo = tk.Label(janela_listar_objetos, text='Comodo:')
        label_comodo.pack()

        entry_comodo = tk.Entry(janela_listar_objetos)
        entry_comodo.pack()

        botao_listar = tk.Button(janela_listar_objetos, text='Listar', command=lambda: self.listar_objetos_em_comodo(entry_comodo.get()))
        botao_listar.pack()

    def listar_objetos_em_comodo(self, comodo):
        objetos = self.casa.listar_objetos_em_comodo(comodo)

        if objetos:
            janela_resultado = tk.Toplevel(self.janela_principal)
            janela_resultado.title(f"Objetos em {comodo}")

            texto_objetos = tk.Label(janela_resultado, text="\n".join(objetos))
            texto_objetos.pack()
        else:
            janela_vazia = tk.Toplevel(self.janela_principal)
            janela_vazia.title("Nenhum objeto encontrado")

            texto_vazio = tk.Label(janela_vazia, text="Nenhum objeto encontrado neste cômodo.")
            texto_vazio.pack()

class InterfaceInicial:
    def __init__(self):
        self.janela_inicial = tk.Tk()
        self.janela_inicial.title('Bem-vindo')

        largura = 300
        altura = 100

        posicao_x = int(self.janela_inicial.winfo_screenwidth() / 2 - largura / 2)
        posicao_y = int(self.janela_inicial.winfo_screenheight() / 2 - altura / 2)

        self.janela_inicial.geometry(f"{largura}x{altura}+{posicao_x}+{posicao_y}")

        self.label_nome_casa = tk.Label(self.janela_inicial, text='Qual o nome da casa que pretende utilizar?')
        self.label_nome_casa.pack()

        self.entry_nome_casa = tk.Entry(self.janela_inicial)
        self.entry_nome_casa.pack()

        self.botao_confirmar = tk.Button(self.janela_inicial, text='Confirmar', command=self.verificar_arquivo)
        self.botao_confirmar.pack()

    def verificar_arquivo(self):
        nome_casa = self.entry_nome_casa.get()

        # Verifica se o arquivo da casa existe
        nome_arquivo = f"{nome_casa}.json"
        try:
            with open(nome_arquivo, 'r'):
                pass  # Arquivo existe
        except FileNotFoundError:
            # Arquivo não existe, cria o arquivo com um dicionário vazio
            with open(nome_arquivo, 'w') as arquivo:
                json.dump({}, arquivo)

        self.janela_inicial.destroy()

        casa = Casa(nome_arquivo)
        interface = InterfaceGrafica(casa)
        interface.janela_principal.mainloop()


if __name__ == "__main__":
    interface_inicial = InterfaceInicial()
    interface_inicial.janela_inicial.mainloop()
    # nome_arquivo = "dados_casa.json"
    # casa = Casa(nome_arquivo)
    # interface = InterfaceGrafica(casa)
    # interface.janela_principal.mainloop()
