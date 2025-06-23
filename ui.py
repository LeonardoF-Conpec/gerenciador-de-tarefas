import os
from datetime import date
from typing import List, Dict, Any, Optional

from manager import TaskManager
from models import Tarefa, ListaDeTarefas


def clear_screen():
    """Limpa a tela do terminal, compatível com Windows e Unix."""
    os.system('cls' if os.name == 'nt' else 'clear')


def pausar_e_limpar():
    """Pausa a execução até o usuário pressionar Enter e depois limpa a tela."""
    input("\nPressione Enter para continuar...")
    clear_screen()


def imprimir_cabecalho(titulo: str):
    """Imprime um cabeçalho formatado."""
    print("=" * 40)
    print(f"{titulo.center(40)}")
    print("=" * 40)
    print()


def imprimir_tarefas(tarefas: List[Tarefa], gerenciador: TaskManager):
    """
    Imprime uma lista de tarefas de forma formatada e legível.

    Args:
        tarefas (List[Tarefa]): A lista de objetos Tarefa a serem impressos.
        gerenciador (TaskManager): O gerenciador para buscar nomes de listas.
    """
    if not tarefas:
        print("Nenhuma tarefa encontrada para exibir.")
        return

    # Cria um mapa de ID de lista para nome para evitar buscas repetidas no loop
    mapa_listas = {lista.id: lista.nome for lista in gerenciador.get_todas_listas()}

    for tarefa in tarefas:
        status = "✓" if tarefa.concluida else "✗"
        data_str = tarefa.data_termino.strftime('%d/%m/%Y') if tarefa.data_termino else "Sem data"

        # Adiciona um marcador de atraso
        if tarefa.data_termino and tarefa.data_termino < date.today() and not tarefa.concluida:
            data_str += " (Atrasada!)"

        nome_lista = mapa_listas.get(tarefa.lista_id, "Desconhecida")
        tags_str = f"Tags: {', '.join(tarefa.tags)}" if tarefa.tags else ""

        print(f"[{status}] ID: {tarefa.id:<5} | {tarefa.titulo:<30} | Data: {data_str:<20} | Lista: {nome_lista:<15} | Prio: {tarefa.prioridade.capitalize():<8} {tags_str}")
        if tarefa.notas:
            print(f"    Notas: {tarefa.notas}")


def obter_dados_nova_tarefa(gerenciador: TaskManager) -> Optional[Dict[str, Any]]:
    """Coleta os dados do usuário para criar uma nova tarefa."""
    imprimir_cabecalho("Adicionar Nova Tarefa")

    listas = gerenciador.get_todas_listas()
    print("Listas disponíveis:")
    for lista in listas:
        print(f"  ID: {lista.id} - {lista.nome}")

    try:
        lista_id = int(input("Digite o ID da lista para a nova tarefa: "))
        if not gerenciador.buscar_lista_por_id(lista_id):
            print("Erro: ID de lista inválido.")
            return None
    except ValueError:
        print("Erro: ID inválido.")
        return None

    titulo = input("Título da tarefa: ")
    if not titulo:
        print("Erro: O título é obrigatório.")
        return None

    data_str = input("Data de término (AAAA-MM-DD, opcional): ")
    data_termino = None
    if data_str:
        try:
            data_termino = date.fromisoformat(data_str)
        except ValueError:
            print("Formato de data inválido. A tarefa será criada sem data.")

    prioridade = input("Prioridade (alta, media, baixa, opcional): ").lower()
    tags_str = input("Tags (separadas por vírgula, opcional): ")
    notas = input("Notas (opcional): ")
    repeticao = input("Repetição (diaria, semanal, mensal, anual, opcional): ").lower()

    return {
        "lista_id": lista_id,
        "titulo": titulo,
        "data_termino": data_termino,
        "prioridade": prioridade if prioridade in ["alta", "media", "baixa"] else "nenhuma",
        "tags": [tag.strip() for tag in tags_str.split(',')] if tags_str else [],
        "notas": notas,
        "repeticao": repeticao if repeticao in ["diaria", "semanal", "mensal", "anual"] else "nunca"
    }


def obter_id_para_acao(acao: str) -> Optional[int]:
    """Pede ao usuário um ID de tarefa para uma ação específica."""
    try:
        id_str = input(f"Digite o ID da tarefa que deseja {acao}: ")
        return int(id_str)
    except ValueError:
        print("Erro: ID inválido.")
        return None


def menu_principal():
    """Exibe o menu principal e retorna a escolha do usuário."""
    imprimir_cabecalho("Gerenciador de Tarefas")
    print("1. Visualizar Tarefas")
    print("2. Adicionar Tarefa")
    print("3. Concluir Tarefa")
    print("4. Editar/Remover Tarefa")
    print("5. Gerenciar Listas")
    print("6. Sair")
    return input("\nEscolha uma opção: ")
