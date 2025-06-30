import json
import os
from typing import List, Tuple
from models import Tarefa, ListaDeTarefas

# Define o nome do arquivo de dados como uma constante.
# Facilita a alteração do nome do arquivo em um só lugar, se necessário.
DATA_FILE = "dados_tarefas.json"


def salvar_dados(listas: List[ListaDeTarefas], tarefas: List[Tarefa]) -> None:
    """
    Salva todas as listas e tarefas em um arquivo JSON.
    Esta função é chamada sempre que há uma alteração nos dados.

    Parâmetros:

    listas (List[ListaDeTarefas]): A lista contendo todos os objetos ListaDeTarefas.
    tarefas (List[Tarefa]): A lista contendo todos os objetos Tarefa.
    """

    print("Salvando dados...") # Feedback
    try:
        # Cria um dicionário principal para armazenar ambas as listas de objetos
        dados_para_salvar = {
            # Converte cada objeto para seu formato de dicionário usando o método to_dict()
            "listas": [lista.to_dict() for lista in listas],
            "tarefas": [tarefa.to_dict() for tarefa in tarefas]
        }

        # Abre o arquivo em modo de escrita ('w')
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            # Usa json.dump para escrever o dicionário no arquivo.
            # indent=4 para deixar o JSON identado e mais legível.
            json.dump(dados_para_salvar, f, indent=4, ensure_ascii=False)
        print("Dados salvos com sucesso!")

    except IOError as e:
        print(f"Erro ao salvar o arquivo: {e}")
    except Exception as e:
        print(f"Ocorreu um erro inesperado ao salvar os dados: {e}")


def carregar_dados() -> Tuple[List[ListaDeTarefas], List[Tarefa]]:
    """
    Carrega as listas e tarefas do arquivo JSON.
    Se o arquivo não existir, cria uma lista padrão "Geral".

    Returns:
        Tuple[List[ListaDeTarefas], List[Tarefa]]: Uma tupla contendo a lista
        de objetos ListaDeTarefas e a lista de objetos Tarefa.
    """

    # Verifica se o arquivo de dados não existe
    if not os.path.exists(DATA_FILE):
        print("Arquivo de dados não encontrado. Criando uma lista padrão 'Geral'.")
        # Cria uma lista inicial "Geral" para que o programa sempre tenha pelo menos uma lista.
        lista_geral = ListaDeTarefas(id=1, nome="Geral")
        # Retorna a lista padrão e uma lista de tarefas vazia
        return [lista_geral], []

    try:
        # Abre o arquivo em modo de leitura
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            # Verifica se o arquivo está vazio para evitar erros de decodificação
            if os.path.getsize(DATA_FILE) == 0:
                print("Arquivo de dados vazio. Criando uma lista padrão 'Geral'.")
                lista_geral = ListaDeTarefas(id=1, nome="Geral")
                return [lista_geral], []

            dados = json.load(f)

            # Recria os objetos ListaDeTarefas a partir dos dicionários no arquivo
            listas_carregadas = [ListaDeTarefas.from_dict(d) for d in dados.get("listas", [])]

            # Recria os objetos Tarefa a partir dos dicionários no arquivo
            tarefas_carregadas = [Tarefa.from_dict(d) for d in dados.get("tarefas", [])]

            print("Dados carregados com sucesso!")
            return listas_carregadas, tarefas_carregadas

    except (json.JSONDecodeError, KeyError) as error:
        print(f"Erro ao ler ou decodificar o arquivo JSON: {error}. Iniciando com dados padrão.")
        # Se o arquivo estiver corrompido ou mal formatado, começa com uma lista padrão.
        lista_geral = ListaDeTarefas(id=1, nome="Geral")
        return [lista_geral], []
    except Exception as error:
        print(f"Ocorreu um erro inesperado ao carregar os dados: {error}. Iniciando com dados padrão.")
        lista_geral = ListaDeTarefas(id=1, nome="Geral")
        return [lista_geral], []
