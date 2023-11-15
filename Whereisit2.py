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

        self.criar_widgets()

    def criar_widgets(self):
        botao_adicionar_objeto = tk.Button(self.janela_principal, text='Adicionar Objeto', command=self.adicionar_objeto_interface)
        botao_adicionar_objeto.pack()

        botao_listar_objetos = tk.Button(self.janela_principal, text='Listar Objetos em um Cômodo', command=self.listar_objetos_em_comodo_interface)
        botao_listar_objetos.pack()

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

        botao_confirmar = tk.Button(janela_adicionar_objeto, text='Confirmar', command=lambda: self.adicionar_objeto(entry_comodo.get(), entry_objeto.get(), entry_tipo.get(), entry_quantidade.get()))
        botao_confirmar.pack()

    def adicionar_objeto(self, comodo, objeto, tipo, quantidade):
        self.casa.adicionar_objeto(comodo, objeto, tipo, quantidade)

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

if __name__ == "__main__":
    nome_arquivo = "dados_casa.json"
    casa = Casa(nome_arquivo)
    interface = InterfaceGrafica(casa)
    interface.janela_principal.mainloop()
