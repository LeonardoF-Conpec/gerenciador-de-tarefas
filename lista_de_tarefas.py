from manager import TaskManager
import ui

def visualizar_tarefas(gerenciador: TaskManager):
    """Lógica para o submenu de visualização de tarefas."""
    ui.imprimir_cabecalho("Visualizar Tarefas")
    tarefas_nao_concluidas = [t for t in gerenciador.get_todas_tarefas() if not t.concluida]
    
    if not tarefas_nao_concluidas:
        print("Você não tem tarefas pendentes. Ótimo trabalho!")
        return

    print("Tarefas Pendentes:")
    # Aqui você pode adicionar mais opções de filtro (por lista, tag, etc.)
    # Por simplicidade, exibimos todas as não concluídas.
    ui.imprimir_tarefas(tarefas_nao_concluidas, gerenciador)


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
        # Lógica de edição (pode ser expandida em ui.py)
        novo_titulo = input(f"Novo título (atual: {tarefa.titulo}): ")
        if novo_titulo:
            gerenciador.editar_tarefa(tarefa_id, {"titulo": novo_titulo})
            print("Tarefa editada com sucesso!")
    elif escolha == '2':
        # Lógica de remoção
        if gerenciador.remover_tarefa(tarefa_id):
            print("Tarefa removida com sucesso!")
        else:
            print("Não foi possível remover a tarefa.")

def gerenciar_listas(gerenciador: TaskManager):
    """Lógica para o submenu de gerenciamento de listas."""
    ui.imprimir_cabecalho("Gerenciar Listas")
    listas = gerenciador.get_todas_listas()
    print("Listas existentes:")
    for lista in listas:
        print(f"  ID: {lista.id} - {lista.nome}")
    
    print("\nOpções:")
    print("1. Adicionar nova lista")
    print("2. Remover uma lista")
    escolha = input("O que você deseja fazer? ")

    if escolha == '1':
        nome_lista = input("Digite o nome da nova lista: ")
        if nome_lista:
            gerenciador.adicionar_lista(nome_lista)
            print(f"Lista '{nome_lista}' adicionada.")
    elif escolha == '2':
        try:
            lista_id = int(input("Digite o ID da lista a ser removida: "))
            if gerenciador.remover_lista(lista_id):
                print("Lista e todas as suas tarefas foram removidas.")
        except ValueError:
            print("ID inválido.")

def main():
    """Função principal que executa o loop da aplicação."""
    gerenciador = TaskManager()
    
    while True:
        escolha = ui.menu_principal()

        if escolha == '1':
            ui.clear_screen()
            visualizar_tarefas(gerenciador)
            ui.pausar_e_limpar()
        
        elif escolha == '2':
            ui.clear_screen()
            dados = ui.obter_dados_nova_tarefa(gerenciador)
            if dados:
                gerenciador.adicionar_tarefa(dados)
                print("\nTarefa adicionada com sucesso!")
            ui.pausar_e_limpar()

        elif escolha == '3':
            ui.clear_screen()
            ui.imprimir_cabecalho("Concluir Tarefa")
            visualizar_tarefas(gerenciador)
            tarefa_id = ui.obter_id_para_acao("concluir")
            if tarefa_id:
                tarefa_concluida = gerenciador.concluir_tarefa(tarefa_id)
                if tarefa_concluida:
                    print(f"\nTarefa '{tarefa_concluida.titulo}' marcada como concluída!")
                else:
                    print("Tarefa não encontrada.")
            ui.pausar_e_limpar()

        elif escolha == '4':
            ui.clear_screen()
            gerenciar_tarefas_crud(gerenciador)
            ui.pausar_e_limpar()

        elif escolha == '5':
            ui.clear_screen()
            gerenciar_listas(gerenciador)
            ui.pausar_e_limpar()

        elif escolha == '6':
            print("Obrigado por usar o Gerenciador de Tarefas! Até mais!")
            break
        
        else:
            print("Opção inválida, por favor tente novamente.")
            ui.pausar_e_limpar()

if __name__ == "__main__":
    main()
