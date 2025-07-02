import os
from datetime import date, datetime
from typing import List, Dict, Any, Optional
from manager import TaskManager
from models import Tarefa


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

    Parâmetros:
    tarefas (List[Tarefa]): A lista de objetos Tarefa a serem impressos.
    gerenciador (TaskManager): O gerenciador para buscar nomes de listas.
    """

    if not tarefas:
        print("Nenhuma tarefa encontrada para exibir.")
        return

    # Cria um mapa de ID de lista para nome para evitar buscas repetidas no loop
    mapa_listas = {lista.id: lista.nome for lista in gerenciador.get_todas_listas()}

    for tarefa in tarefas:
        status = "✓" if tarefa.concluida else " "
        data_str = tarefa.data_termino.strftime('%d/%m/%Y') if tarefa.data_termino else "Sem data"

        # Adiciona um marcador de atraso
        if tarefa.data_termino and tarefa.data_termino < date.today() and not tarefa.concluida:
            data_str += " (Atrasada!)"

        nome_lista = mapa_listas.get(tarefa.lista_id, "Desconhecida")
        tags_str = f"Tags: {', '.join(tarefa.tags)}" if tarefa.tags else ""

        print(f"[{status}] ID: {tarefa.id:<4} | {tarefa.titulo:<30} | Data: {data_str:<14} | Lista: {nome_lista:<16} | Prioridade: {tarefa.prioridade.capitalize():<8} | Repetição: {tarefa.repeticao.capitalize():<8} | {tags_str}")
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
        lista_id = int(input("\nDigite o ID da lista para a nova tarefa: "))
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

    data_str = input("Data de término (DD/MM/AAAA, opcional): ")
    data_termino = None
    if data_str:
        try:
            data_termino = datetime.strptime(data_str, '%d/%m/%Y').date()
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


def obter_dados_edicao_tarefa(tarefa: Tarefa, gerenciador: TaskManager) -> Dict[str, Any]:
    """Exibe um formulário de edição para a tarefa e retorna um dicionário com os campos alterados."""

    imprimir_cabecalho(f"Editando Tarefa ID: {tarefa.id}")
    print("Deixe o campo em branco e pressione Enter para manter o valor atual.")

    novos_dados = {}

    # Editar Título
    novo_titulo = input(f"Título (atual: {tarefa.titulo}): ")
    if novo_titulo:
        novos_dados["titulo"] = novo_titulo

    # Editar Notas
    novas_notas = input(f"Notas (atual: {tarefa.notas}): ")
    if novas_notas:
        novos_dados["notas"] = novas_notas

    # Editar Data de Término
    data_atual_str = tarefa.data_termino.strftime('%d/%m/%Y') if tarefa.data_termino else "Nenhuma"
    nova_data_str = input(f"Data de término (DD/MM/AAAA, atual: {data_atual_str}): ")
    if nova_data_str:
        try:
            novos_dados["data_termino"] = datetime.strptime(nova_data_str, '%d/%m/%Y').date()
        except ValueError:
            print("Formato de data inválido. A data não será alterada.")

    # Editar Prioridade
    nova_prioridade = input(f"Prioridade (alta, media, baixa, atual: {tarefa.prioridade}): ").lower()
    if nova_prioridade in ["alta", "media", "baixa", "nenhuma"]:
        novos_dados["prioridade"] = nova_prioridade

    # Editar Tags
    tags_atuais_str = ', '.join(tarefa.tags)
    novas_tags_str = input(f"Tags (separadas por vírgula, atual: {tags_atuais_str}): ")
    if novas_tags_str:
        novos_dados["tags"] = [tag.strip() for tag in novas_tags_str.split(',')]

    # Editar Repetição
    nova_repeticao = input(f"Repetição (diaria, semanal, mensal, anual, atual: {tarefa.repeticao}): ").lower()
    if nova_repeticao in ["diaria", "semanal", "mensal", "anual", "nunca"]:
        novos_dados["repeticao"] = nova_repeticao

    # Editar Lista de Tarefas associada
    print("\nListas disponíveis para mover a tarefa:")
    listas = gerenciador.get_todas_listas()
    for lista in listas:
        print(f"  ID: {lista.id} - {lista.nome}")

    mapa_listas = {lista.id: lista.nome for lista in listas}
    lista_atual_nome = mapa_listas.get(tarefa.lista_id, "Desconhecida")

    novo_lista_id_str = input(f"Novo ID da lista (atual: {tarefa.lista_id} - {lista_atual_nome}): ")
    if novo_lista_id_str:
        try:
            novo_lista_id = int(novo_lista_id_str)
            if gerenciador.buscar_lista_por_id(novo_lista_id):
                novos_dados["lista_id"] = novo_lista_id
            else:
                print("ID de lista inválido. A lista não será alterada.")
        except ValueError:
            print("ID inválido. A lista não será alterada.")

    return novos_dados


def obter_id_para_acao(acao: str) -> Optional[int]:
    """Pede ao usuário um ID de tarefa para uma ação específica."""

    try:
        id_str = input(f"Digite o ID da tarefa que deseja {acao}: ")
        return int(id_str)
    except ValueError:
        print("Erro: ID inválido.")
        return None


def obter_termo_busca() -> str:
    """Pede ao usuário um termo para a busca."""

    return input("Digite o termo que deseja buscar no título, notas ou tags: ")


def menu_busca_acoes() -> str:
    """Exibe as opções de ação após uma busca e retorna a escolha."""

    print("Ações disponíveis para os resultados da busca:")
    print("1. Concluir uma tarefa")
    print("2. Desmarcar uma tarefa (tornar pendente)")
    print("3. Editar uma tarefa")
    print("4. Remover uma tarefa")
    print("4. Voltar ao menu principal")
    return input("\nEscolha uma opção: ")


def menu_contexto_visualizacao() -> str:
    """Pergunta ao usuário o contexto principal da visualização."""

    imprimir_cabecalho("Opções de Visualização")
    print("Como você deseja visualizar as tarefas?")
    print("1. Todas as Tarefas (geral)")
    print("2. Por Lista de Tarefas")
    print("3. Por Tag")
    print("4. Voltar")
    return input("\nEscolha uma opção: ")


def menu_filtro_secundario() -> str:
    """Pergunta ao usuário o filtro secundário a ser aplicado."""

    print("\nAplicar qual filtro?")
    print("1. Ver todas as tarefas neste contexto")
    print("2. Apenas tarefas para hoje (e atrasadas)")
    print("3. Apenas tarefas para os próximos 7 dias (e atrasadas)")
    print("4. Apenas tarefas não concluídas")
    print("5. Apenas tarefas concluídas")
    return input("\nEscolha uma opção de filtro: ")


def menu_escolha_ordenacao() -> str:
    """Pergunta ao usuário como ele deseja ordenar as tarefas."""

    print("\nEscolha a ordem de visualização:")
    print("1. Ordenar por Data (Padrão)")
    print("2. Ordenar por Prioridade")
    return input("Escolha uma opção de ordenação (padrão é 1): ")


def menu_acoes_gerais() -> str:
    """Exibe o menu de ações para a lista de todas as tarefas."""

    print("\nAções disponíveis:")
    print("1. Concluir uma tarefa")
    print("2. Desmarcar uma tarefa (tornar pendente)")
    print("3. Editar uma tarefa")
    print("4. Remover uma tarefa")
    print("5. Voltar")
    return input("\nEscolha uma opção: ")


def menu_acoes_pendentes() -> str:
    """Exibe o menu de ações para a lista de tarefas pendentes."""

    print("\nAções para tarefas pendentes:")
    print("1. Concluir uma tarefa")
    print("2. Editar uma tarefa")
    print("3. Remover uma tarefa")
    print("4. Voltar")
    return input("\nEscolha uma opção: ")


def menu_acoes_concluidas() -> str:
    """Exibe o menu de ações para a lista de tarefas concluídas."""

    print("\nAções para tarefas concluídas:")
    print("1. Desmarcar uma tarefa (tornar pendente)")
    print("2. Remover uma tarefa permanentemente")
    print("3. Remover TODAS as tarefas concluídas")
    print("4. Voltar")
    return input("\nEscolha uma opção: ")


def menu_principal():
    """Exibe o menu principal e retorna a escolha do usuário."""

    imprimir_cabecalho("Gerenciador de Tarefas")
    print("1. Visualizar Tarefas")
    print("2. Adicionar Tarefa")
    print("3. Buscar Tarefas")
    print("4. Gerenciar Listas")
    print("5. Sair")
    return input("\nEscolha uma opção: ")
