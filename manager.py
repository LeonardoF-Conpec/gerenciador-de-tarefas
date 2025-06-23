import copy
from datetime import date, timedelta
from typing import List, Optional, Dict, Any

# Importa os módulos e classes necessários
from models import Tarefa, ListaDeTarefas, gerar_id_unico
import persistence

class TaskManager:
    """
    Gerencia toda a lógica de negócios para listas e tarefas.
    """
    def __init__(self):
        """
        Inicializa o gerenciador, carregando os dados existentes do arquivo.
        """
        # Carrega as listas e tarefas usando o módulo de persistência
        self._listas, self._tarefas = persistence.carregar_dados()
        # Se não houver listas, garante que a padrão "Geral" exista e a salva
        if not self._listas:
            lista_geral = ListaDeTarefas(id=gerar_id_unico(), nome="Geral")
            self._listas.append(lista_geral)
            self._salvar_tudo()

    def _salvar_tudo(self):
        """Função auxiliar privada para salvar o estado atual no arquivo."""
        persistence.salvar_dados(self._listas, self._tarefas)

    # --- Métodos de Gerenciamento de Listas ---

    def get_todas_listas(self) -> List[ListaDeTarefas]:
        """Retorna uma cópia de todas as listas de tarefas."""
        return self._listas.copy()
    
    def buscar_lista_por_id(self, lista_id: int) -> Optional[ListaDeTarefas]:
        """Busca e retorna uma lista pelo seu ID."""
        for lista in self._listas:
            if lista.id == lista_id:
                return lista
        return None

    def adicionar_lista(self, nome: str) -> Optional[ListaDeTarefas]:
        """
        Adiciona uma nova lista, garantindo que o nome não seja duplicado.

        Retorna o objeto ListaDeTarefas criado ou None se o nome já existir.
        """
        # Validação: Verifica se já existe uma lista com o mesmo nome (ignorando maiúsculas/minúsculas)
        if any(lista.nome.lower() == nome.lower() for lista in self._listas):
            print(f"Erro: Uma lista com o nome '{nome}' já existe.")
            return None
        
        nova_lista = ListaDeTarefas(id=gerar_id_unico(), nome=nome)
        self._listas.append(nova_lista)
        self._salvar_tudo()
        return nova_lista

    def remover_lista(self, lista_id: int) -> bool:
        """
        Remove uma lista e todas as tarefas associadas a ela.
        Não permite remover a última lista existente.
        """
        # Validação: Não permite remover a última lista
        if len(self._listas) <= 1:
            print("Erro: Não é possível remover a última lista de tarefas.")
            return False

        # Remove a lista
        self._listas = [lista for lista in self._listas if lista.id != lista_id]
        
        # Remove todas as tarefas associadas à lista removida
        self._tarefas = [tarefa for tarefa in self._tarefas if tarefa.lista_id != lista_id]
        
        self._salvar_tudo()
        return True

    # --- Métodos de Gerenciamento de Tarefas ---

    def get_todas_tarefas(self) -> List[Tarefa]:
        """Retorna uma cópia de todas as tarefas."""
        return self._tarefas.copy()

    def buscar_tarefa_por_id(self, tarefa_id: int) -> Optional[Tarefa]:
        """Busca e retorna uma tarefa pelo seu ID."""
        for tarefa in self._tarefas:
            if tarefa.id == tarefa_id:
                return tarefa
        return None

    def adicionar_tarefa(self, dados_tarefa: Dict[str, Any]) -> Tarefa:
        """
        Adiciona uma nova tarefa à uma lista específica.
        """
        nova_tarefa = Tarefa(
            id=gerar_id_unico(),
            titulo=dados_tarefa['titulo'],
            lista_id=dados_tarefa['lista_id'],
            data_termino=dados_tarefa.get('data_termino'),
            prioridade=dados_tarefa.get('prioridade'),
            tags=dados_tarefa.get('tags'),
            notas=dados_tarefa.get('notas'),
            repeticao=dados_tarefa.get('repeticao')
        )
        self._tarefas.append(nova_tarefa)
        self._salvar_tudo()
        return nova_tarefa
    
    def editar_tarefa(self, tarefa_id: int, novos_dados: Dict[str, Any]) -> Optional[Tarefa]:
        """
        Edita os atributos de uma tarefa existente.
        """
        tarefa = self.buscar_tarefa_por_id(tarefa_id)
        if not tarefa:
            return None
        
        for chave, valor in novos_dados.items():
            if hasattr(tarefa, chave):
                setattr(tarefa, chave, valor)
                
        self._salvar_tudo()
        return tarefa

    def remover_tarefa(self, tarefa_id: int) -> bool:
        """Remove uma tarefa da lista."""
        tarefa = self.buscar_tarefa_por_id(tarefa_id)
        if not tarefa:
            return False
        
        self._tarefas.remove(tarefa)
        self._salvar_tudo()
        return True

    def concluir_tarefa(self, tarefa_id: int) -> Optional[Tarefa]:
        """
        Marca uma tarefa como concluída. Se for recorrente, cria a próxima ocorrência.
        """
        tarefa_original = self.buscar_tarefa_por_id(tarefa_id)
        if not tarefa_original:
            return None

        tarefa_original.concluida = True

        # Lógica para tarefas recorrentes
        if tarefa_original.repeticao != "nunca" and tarefa_original.data_termino:
            nova_tarefa = copy.deepcopy(tarefa_original) # Cria uma cópia profunda
            nova_tarefa.id = gerar_id_unico()
            nova_tarefa.concluida = False

            # Calcula a nova data de término
            if tarefa_original.repeticao == "diaria":
                nova_tarefa.data_termino += timedelta(days=1)
            elif tarefa_original.repeticao == "semanal":
                nova_tarefa.data_termino += timedelta(weeks=1)
            elif tarefa_original.repeticao == "mensal":
                # Adiciona um mês (aproximação simples, pode ser refinada)
                nova_data = tarefa_original.data_termino
                nova_tarefa.data_termino = nova_data.replace(month=nova_data.month + 1)
            elif tarefa_original.repeticao == "anual":
                nova_data = tarefa_original.data_termino
                nova_tarefa.data_termino = nova_data.replace(year=nova_data.year + 1)
            
            self._tarefas.append(nova_tarefa)

        self._salvar_tudo()
        return tarefa_original
    