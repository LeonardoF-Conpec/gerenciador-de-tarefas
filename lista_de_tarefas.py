from datetime import date, timedelta
from typing import List
from manager import TaskManager
from models import Tarefa
import ui


def visualizar_tarefas(gerenciador: TaskManager):
    """Guia o usuário através de um processo de filtragem em cascata."""

    while True:
        contexto_escolha = ui.menu_contexto_visualizacao()
        if contexto_escolha == '4':
            break

        tarefas_base = []
        titulo_cabecalho = "Tarefas"
        todas_as_tarefas = gerenciador.get_todas_tarefas()

        if contexto_escolha == '1': # Por Lista
            listas = gerenciador.get_todas_listas()

            for lista in listas:
                print(f"  ID: {lista.id} - {lista.nome}")

            try:
                lista_id = int(input("Digite o ID da lista desejada: "))
                lista_obj = gerenciador.buscar_lista_por_id(lista_id)
                if lista_obj:
                    tarefas_base = [t for t in todas_as_tarefas if t.lista_id == lista_id]
                    titulo_cabecalho = f"Tarefas da Lista: {lista_obj.nome}"
                else:
                    print("ID de lista inválido.")
                    continue
            except ValueError:
                print("ID inválido.")
                continue
        elif contexto_escolha == '2': # Por Tag
            tag_escolhida = input("Digite a tag que deseja filtrar: ").lower()

            if not tag_escolhida:
                continue

            tarefas_base = [t for t in todas_as_tarefas if tag_escolhida in [tag.lower() for tag in t.tags]]
            titulo_cabecalho = f"Tarefas com a Tag: {tag_escolhida}"
        elif contexto_escolha == '3': # Todas
            tarefas_base = todas_as_tarefas
            titulo_cabecalho = "Todas as Tarefas"
        else:
            print("Opção de contexto inválida.")
            continue

        filtro_escolha = ui.menu_filtro_secundario()
        tarefas_filtradas = []
        hoje = date.today()

        if filtro_escolha == '1':
            tarefas_filtradas = tarefas_base

        elif filtro_escolha == '2':
            tarefas_filtradas = [t for t in tarefas_base if t.data_termino and t.data_termino <= hoje]

        elif filtro_escolha == '3':
            limite = hoje + timedelta(days=7)
            tarefas_filtradas = [t for t in tarefas_base if t.data_termino and t.data_termino <= limite]

        elif filtro_escolha == '4':
            tarefas_filtradas = [t for t in tarefas_base if not t.concluida]

        else:
            print("Opção de filtro inválida.")
            continue

        # Se não houver tarefas após o filtro, exibe a mensagem e volta
        if not tarefas_filtradas:
            ui.clear_screen()
            ui.imprimir_cabecalho(titulo_cabecalho)
            ui.imprimir_tarefas(tarefas_filtradas, gerenciador) # Exibe "Nenhuma tarefa..."
            ui.pausar_e_limpar()
            continue

        # --- ESCOLHA DA ORDENAÇÃO ---
        ordenacao_escolha = ui.menu_escolha_ordenacao()

        if ordenacao_escolha == '2':
            tarefas_finais = ordenar_tarefas_por_prioridade(tarefas_filtradas)

        else: # Padrão é 1 ou qualquer outra coisa
            tarefas_finais = ordenar_tarefas_padrao(tarefas_filtradas)

        # Exibição final
        ui.clear_screen()
        ui.imprimir_cabecalho(titulo_cabecalho)
        ui.imprimir_tarefas(tarefas_finais, gerenciador)
        ui.pausar_e_limpar()


def ordenar_tarefas_padrao(tarefas: List[Tarefa]) -> List[Tarefa]:
    """
    Ordena uma lista de tarefas pela regra padrão especificada no projeto.
    1. Data de término (tarefas sem data vão para o final).
    2. Prioridade (Alta > Média > Baixa > Nenhuma).
    3. ID da Lista (ordem crescente).
    """

    # Mapeia a prioridade para um valor numérico para ordenação correta.
    # Números menores têm maior prioridade.
    prioridade_map = {"alta": 0, "media": 1, "baixa": 2, "nenhuma": 3}

    def sort_key(tarefa: Tarefa):
        # Para tarefas sem data, usamos uma data muito distante (date.max)
        # para garantir que elas fiquem no final.
        data_key = tarefa.data_termino if tarefa.data_termino is not None else date.max

        # Pega o valor da prioridade do mapa. Usa 4 como padrão para casos inesperados.
        prioridade_key = prioridade_map.get(tarefa.prioridade.lower(), 4)

        # O ID da lista já é numérico e serve para o desempate final.
        lista_key = tarefa.lista_id

        # Retorna uma tupla. O Python ordena pelo primeiro elemento,
        # depois pelo segundo em caso de empate, e assim por diante.
        return (data_key, prioridade_key, lista_key)

    return sorted(tarefas, key=sort_key)


def ordenar_tarefas_por_prioridade(tarefas: List[Tarefa]) -> List[Tarefa]:
    """
    Ordena uma lista de tarefas por Prioridade, Data e ID da Lista.
    """

    prioridade_map = {"alta": 0, "media": 1, "baixa": 2, "nenhuma": 3}

    def sort_key(tarefa: Tarefa):
        data_key = tarefa.data_termino if tarefa.data_termino is not None else date.max
        prioridade_key = prioridade_map.get(tarefa.prioridade.lower(), 4)
        lista_key = tarefa.lista_id
        # Apenas a ordem da tupla é alterada aqui
        return (prioridade_key, data_key, lista_key)

    return sorted(tarefas, key=sort_key)


def gerenciar_tarefas_pendentes(gerenciador: TaskManager):
    """Exibe tarefas pendentes e permite ações sobre elas."""

    ui.imprimir_cabecalho("Tarefas Pendentes")
    tarefas_pendentes = [t for t in gerenciador.get_todas_tarefas() if not t.concluida]
    tarefas_pendentes_ordenadas = ordenar_tarefas_padrao(tarefas_pendentes)
    ui.imprimir_tarefas(tarefas_pendentes_ordenadas, gerenciador)

    if not tarefas_pendentes:
        ui.pausar_e_limpar()
        return

    while True:
        escolha = ui.menu_acoes_pendentes()

        if escolha == '4': # Voltar
            break

        acao_str = ""

        if escolha == '1':
            acao_str = "concluir"
        elif escolha == '2':
            acao_str = "editar"
        elif escolha == '3':
            acao_str = "remover"
        else:
            print("Opção inválida.")
            continue

        tarefa_id = ui.obter_id_para_acao(acao_str)
        if tarefa_id:
            tarefa = gerenciador.buscar_tarefa_por_id(tarefa_id)
            # Verifica se a tarefa existe e se está na lista de pendentes
            if tarefa and not tarefa.concluida:
                if escolha == '1': # Concluir
                    gerenciador.concluir_tarefa(tarefa_id)
                    print("Tarefa concluída com sucesso!")
                    break # Retorna ao menu de visualização
                elif escolha == '2': # Editar
                    novos_dados = ui.obter_dados_edicao_tarefa(tarefa, gerenciador)
                    if novos_dados:
                        gerenciador.editar_tarefa(tarefa_id, novos_dados)
                        print("\nTarefa editada com sucesso!")
                    break # Retorna ao menu de visualização
                elif escolha == '3': # Remover
                    confirmacao = input("Tem certeza que deseja remover esta tarefa? (s/n): ").lower()
                    if confirmacao == 's':
                        gerenciador.remover_tarefa(tarefa_id)
                        print("Tarefa removida com sucesso!")
                    else:
                        print("Remoção cancelada.")
                    break # Retorna ao menu de visualização
            else:
                print("Erro: ID não corresponde a uma tarefa pendente.")


def gerenciar_tarefas_concluidas(gerenciador: TaskManager):
    """Exibe tarefas concluídas e permite ações sobre elas."""

    ui.imprimir_cabecalho("Tarefas Concluídas")
    tarefas_concluidas = [t for t in gerenciador.get_todas_tarefas() if t.concluida]
    tarefas_concluidas_ordenadas = ordenar_tarefas_padrao(tarefas_concluidas)
    ui.imprimir_tarefas(tarefas_concluidas_ordenadas, gerenciador)

    # Se não houver tarefas concluídas, apenas informa e retorna.
    if not tarefas_concluidas:
        ui.pausar_e_limpar()
        return

    escolha_acao = ui.menu_acoes_concluidas()

    if escolha_acao == '1': # Desmarcar
        tarefa_id = ui.obter_id_para_acao("desmarcar")
        if tarefa_id:
            if gerenciador.desmarcar_tarefa(tarefa_id):
                print("Tarefa desmarcada com sucesso!")
            else:
                print("Erro: Tarefa não encontrada.")

    elif escolha_acao == '2': # Remover uma
        tarefa_id = ui.obter_id_para_acao("remover")
        if tarefa_id:
            if gerenciador.remover_tarefa(tarefa_id):
                print("Tarefa removida com sucesso!")
            else:
                print("Erro: Tarefa não encontrada.")

    elif escolha_acao == '3': # Remover todas
        confirmacao = input("Isso removerá PERMANENTEMENTE todas as tarefas concluídas. Tem certeza? (s/n): ").lower()
        if confirmacao == 's':
            num_removidas = gerenciador.remover_tarefas_concluidas()
            print(f"{num_removidas} tarefas concluídas foram removidas.")
        else:
            print("Operação cancelada.")

    # Pausa para o usuário ver o resultado antes de voltar ao menu anterior
    ui.pausar_e_limpar()


def gerenciar_todas_as_tarefas(gerenciador: TaskManager):
    """Exibe todas as tarefas e permite ações sobre elas."""

    ui.imprimir_cabecalho("Todas as Tarefas")
    todas_as_tarefas = gerenciador.get_todas_tarefas()
    todas_as_tarefas_ordenadas = ordenar_tarefas_padrao(todas_as_tarefas)
    ui.imprimir_tarefas(todas_as_tarefas_ordenadas, gerenciador)

    if not todas_as_tarefas:
        ui.pausar_e_limpar()
        return

    while True:
        escolha = ui.menu_acoes_gerais()
        if escolha == '5':
            break

        acao_str = ""

        if escolha == '1':
            acao_str = "concluir"
        elif escolha == '2':
            acao_str = "desmarcar"
        elif escolha == '3':
            acao_str = "editar"
        elif escolha == '4':
            acao_str = "remover"
        else:
            print("Opção inválida.")
            continue

        tarefa_id = ui.obter_id_para_acao(acao_str)
        if tarefa_id:
            tarefa = gerenciador.buscar_tarefa_por_id(tarefa_id)
            if tarefa:
                if escolha == '1': # Concluir
                    gerenciador.concluir_tarefa(tarefa_id)
                    print("Tarefa concluída!")
                    break
                elif escolha == '2': # Desmarcar
                    gerenciador.desmarcar_tarefa(tarefa_id)
                    print("Tarefa desmarcada!")
                    break
                elif escolha == '3': # Editar
                    novos_dados = ui.obter_dados_edicao_tarefa(tarefa, gerenciador)
                    if novos_dados:
                        gerenciador.editar_tarefa(tarefa_id, novos_dados)
                        print("\nTarefa editada!")
                        break
                elif escolha == '4': # Remover
                    gerenciador.remover_tarefa(tarefa_id)
                    print("Tarefa removida!")
                    break
            else:
                print("Erro: Tarefa não encontrada.")


def gerenciar_tarefas_crud(gerenciador: TaskManager):
    """Lógica para o submenu de edição e remoção de tarefas."""

    ui.imprimir_cabecalho("Editar ou Remover Tarefa")

    # Exibe as tarefas para que o usuário saiba qual ID escolher
    visualizar_tarefas(gerenciador)
    print("-" * 20)

    tarefa_id = ui.obter_id_para_acao("editar ou remover")

    if tarefa_id is None:
        return

    tarefa = gerenciador.buscar_tarefa_por_id(tarefa_id)

    if not tarefa:
        print("Tarefa não encontrada.")
        return

    print("\nOpções para a tarefa selecionada:")
    print("1. Editar")
    print("2. Remover")
    escolha = input("O que você deseja fazer? ")

    if escolha == '1':
        # Chama a nova função de UI para obter os dados de edição
        novos_dados = ui.obter_dados_edicao_tarefa(tarefa, gerenciador)

        # Se o usuário fez alguma alteração, o dicionário não estará vazio
        if novos_dados:
            gerenciador.editar_tarefa(tarefa_id, novos_dados)
            print("\nTarefa editada com sucesso!")
        else:
            print("\nNenhuma alteração foi feita.")

    elif escolha == '2':
        confirmacao = input("Tem certeza que deseja remover esta tarefa? (s/n): ").lower()
        if confirmacao == 's':
            if gerenciador.remover_tarefa(tarefa_id):
                print("Tarefa removida com sucesso!")
            else:
                print("Não foi possível remover a tarefa.")
        else:
            print("Remoção cancelada.")


def gerenciar_listas(gerenciador: TaskManager):
    """Lógica para o submenu de gerenciamento de listas."""

    ui.imprimir_cabecalho("Gerenciar Listas")
    listas = gerenciador.get_todas_listas()
    print("Listas existentes:")

    for lista in listas:
        print(f"  ID: {lista.id} - {lista.nome}")

    print("\nOpções:")
    print("1. Adicionar nova lista")
    print("2. Editar uma lista")
    print("3. Remover uma lista")
    escolha = input("O que você deseja fazer? ")

    if escolha == '1':
        nome_lista = input("Digite o nome da nova lista: ")

        if nome_lista:
            nova_lista_obj = gerenciador.adicionar_lista(nome_lista)

            if nova_lista_obj:
                print(f"Lista '{nome_lista}' adicionada com sucesso.")

    elif escolha == '2':
        try:
            lista_id_str = input("Digite o ID da lista que deseja editar: ")
            lista_id = int(lista_id_str)

            # Verifica se a lista existe antes de pedir o novo nome
            if gerenciador.buscar_lista_por_id(lista_id):
                novo_nome = input("Digite o novo nome para a lista: ")

                if novo_nome:
                    lista_editada = gerenciador.editar_lista(lista_id, novo_nome)

                    if lista_editada:
                        print("Nome da lista atualizado com sucesso!")

                else:
                    print("O nome não pode ser vazio.")

            else:
                print("Erro: Lista com o ID informado não encontrada.")

        except ValueError:
            print("Erro: ID inválido.")

    elif escolha == '3':
        try:
            lista_id = int(input("Digite o ID da lista a ser removida: "))

            # Confirmação para evitar remoção acidental
            lista = gerenciador.buscar_lista_por_id(lista_id)

            if lista:
                confirmacao = input(f"Isso removerá a lista '{lista.nome}' e todas as suas tarefas. Tem certeza? (s/n): ").lower()

                if confirmacao == 's':

                    if gerenciador.remover_lista(lista_id):
                        print("Lista removida com sucesso.")

                else:
                    print("Remoção cancelada.")

            else:
                print("Erro: Lista com o ID informado não encontrada.")

        except ValueError:
            print("ID inválido.")


def iniciar_busca(gerenciador: TaskManager):
    """Inicia o fluxo de busca de tarefas."""

    ui.imprimir_cabecalho("Busca por Tarefas")
    termo = ui.obter_termo_busca()

    if not termo:
        print("A busca foi cancelada.")
        return

    resultados = gerenciador.buscar_tarefas_por_termo(termo)
    resultados = ordenar_tarefas_padrao(resultados)

    print("\n--- Resultados da Busca ---")
    ui.imprimir_tarefas(resultados, gerenciador)
    print("---------------------------\n")

    if not resultados:
        return

    while True:
        escolha = ui.menu_busca_acoes()

        if escolha == '4':
            break

        acao_str = ""

        if escolha == '1':
            acao_str = "concluir"
        elif escolha == '2':
            acao_str = "editar"
        elif escolha == '3':
            acao_str = "remover"
        else:
            print("Opção inválida.")
            continue # Volta para o início do loop de ações

        tarefa_id = ui.obter_id_para_acao(acao_str)

        if tarefa_id:
            # Verifica se o ID fornecido está nos resultados da busca
            if any(t.id == tarefa_id for t in resultados):
                if escolha == '1': # Concluir
                    tarefa_concluida = gerenciador.concluir_tarefa(tarefa_id)
                    if tarefa_concluida:
                        print(f"Tarefa '{tarefa_concluida.titulo}' concluída!")
                    break # Sai do loop de ações após concluir
                elif escolha == '2': # Editar
                    tarefa = gerenciador.buscar_tarefa_por_id(tarefa_id)
                    novos_dados = ui.obter_dados_edicao_tarefa(tarefa, gerenciador)
                    if novos_dados:
                        gerenciador.editar_tarefa(tarefa_id, novos_dados)
                        print("\nTarefa editada com sucesso!")
                    break # Sai do loop de ações após editar
                elif escolha == '3': # Remover
                    if gerenciador.remover_tarefa(tarefa_id):
                        print("Tarefa removida com sucesso!")
                    break # Sai do loop de ações após remover

            else:
                print("Erro: O ID fornecido não corresponde a uma tarefa nos resultados da busca.")


def main():
    """Função principal que executa o loop da aplicação."""

    gerenciador = TaskManager()

    while True:
        escolha = ui.menu_principal()

        if escolha == '1':
            ui.clear_screen()
            visualizar_tarefas(gerenciador)

        elif escolha == '2':
            ui.clear_screen()
            dados = ui.obter_dados_nova_tarefa(gerenciador)
            if dados:
                gerenciador.adicionar_tarefa(dados)
                print("\nTarefa adicionada com sucesso!")
            ui.pausar_e_limpar()

        elif escolha == '3':
            ui.clear_screen()
            iniciar_busca(gerenciador)
            ui.pausar_e_limpar()

        elif escolha == '4':
            ui.clear_screen()
            gerenciar_listas(gerenciador)
            ui.pausar_e_limpar()

        elif escolha == '5':
            print("Obrigado por usar o Gerenciador de Tarefas! Até mais!")
            break

        else:
            print("Opção inválida, por favor tente novamente.")
            ui.pausar_e_limpar()


if __name__ == "__main__":
    main()
