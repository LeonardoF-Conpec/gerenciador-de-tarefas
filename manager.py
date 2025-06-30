import copy
from datetime import timedelta
from typing import List, Optional, Dict, Any

# Importa os módulos e classes necessários
from models import Tarefa, ListaDeTarefas
import persistence


class TaskManager:
    """Gerencia toda a lógica de negócios para listas e tarefas."""

    def __init__(self):
        """Inicializa o gerenciador, carregando os dados existentes do arquivo."""

        # Carrega as listas e tarefas usando o módulo de persistência
        self._listas, self._tarefas = persistence.carregar_dados()
        # Se não houver listas, garante que a padrão "Geral" exista e a salva
        if not self._listas:
            lista_geral = ListaDeTarefas(id=1, nome="Geral")
            self._listas.append(lista_geral)
            self._salvar_tudo()

    def _salvar_tudo(self):
        """Função auxiliar privada para salvar o estado atual no arquivo."""

        persistence.salvar_dados(self._listas, self._tarefas)

    def _gerar_proximo_id_lista(self) -> int:
        """Gera o próximo ID sequencial para uma lista."""

        if not self._listas:
            return 1
        # Encontra o maior ID atual e retorna o próximo número
        return max(lista.id for lista in self._listas) + 1

    def _gerar_proximo_id_tarefa(self) -> int:
        """Gera o próximo ID sequencial para uma tarefa."""

        if not self._tarefas:
            return 1
        return max(tarefa.id for tarefa in self._tarefas) + 1

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

        novo_id = self._gerar_proximo_id_lista()
        nova_lista = ListaDeTarefas(id=novo_id, nome=nome)
        self._listas.append(nova_lista)
        self._salvar_tudo()
        return nova_lista

    def editar_lista(self, lista_id: int, novo_nome: str) -> Optional[ListaDeTarefas]:
        """Edita o nome de uma lista existente, prevenindo nomes duplicados."""

        # Validação para nome duplicado (ignorando a própria lista que está sendo editada)
        if any(l.nome.lower() == novo_nome.lower() for l in self._listas if l.id != lista_id):
            print(f"Erro: Uma lista com o nome '{novo_nome}' já existe.")
            return None

        lista_para_editar = self.buscar_lista_por_id(lista_id)
        if not lista_para_editar:
            print("Erro: Lista não encontrada.")
            return None

        lista_para_editar.nome = novo_nome
        self._salvar_tudo()
        return lista_para_editar

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

    def get_todas_tarefas(self) -> List[Tarefa]:
        """Retorna uma cópia de todas as tarefas."""

        return self._tarefas.copy()

    def buscar_tarefas_por_termo(self, termo: str) -> List[Tarefa]:
        """
        Busca tarefas que contenham o termo no título, notas ou tags.

        A busca não diferencia maiúsculas de minúsculas.
        """

        termo = termo.lower()
        tarefas_encontradas = []
        for tarefa in self._tarefas:
            # Verifica o título
            if termo in tarefa.titulo.lower():
                tarefas_encontradas.append(tarefa)
                continue # Pula para a próxima tarefa para não adicionar duplicado

            # Verifica as notas
            if tarefa.notas and termo in tarefa.notas.lower():
                tarefas_encontradas.append(tarefa)
                continue

            # Verifica as tags
            for tag in tarefa.tags:
                if termo in tag.lower():
                    tarefas_encontradas.append(tarefa)
                    break # Sai do loop de tags e vai para a próxima tarefa

        return tarefas_encontradas

    def buscar_tarefa_por_id(self, tarefa_id: int) -> Optional[Tarefa]:
        """Busca e retorna uma tarefa pelo seu ID."""

        for tarefa in self._tarefas:
            if tarefa.id == tarefa_id:
                return tarefa
        return None

    def adicionar_tarefa(self, dados_tarefa: Dict[str, Any]) -> Tarefa:
        """Adiciona uma nova tarefa à uma lista específica."""

        novo_id = self._gerar_proximo_id_tarefa()
        nova_tarefa = Tarefa(
            id=novo_id,
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
        """Edita os atributos de uma tarefa existente."""

        tarefa = self.buscar_tarefa_por_id(tarefa_id)
        if not tarefa:
            return None

        for chave, valor in novos_dados.items():
            # Esse hasattr verifica se um objeto, no caso aqui a tarefa a ser editada, possui um determinado atributo (titulo, data, prioridade, etc.).
            # Se tiver, o setattr atribui a aquele atributo o novo valor que foi passado.
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
        """Marca uma tarefa como concluída. Se for recorrente, cria a próxima ocorrência."""

        tarefa_original = self.buscar_tarefa_por_id(tarefa_id)
        if not tarefa_original:
            return None

        tarefa_original.concluida = True

        # Lógica para tarefas recorrentes
        if tarefa_original.repeticao != "nunca" and tarefa_original.data_termino:
            nova_tarefa = copy.deepcopy(tarefa_original) # Cria uma cópia profunda
            nova_tarefa.id = self._gerar_proximo_id_tarefa()
            nova_tarefa.concluida = False

            # Calcula a nova data de término
            if tarefa_original.repeticao == "diaria":
                nova_tarefa.data_termino += timedelta(days=1)
            elif tarefa_original.repeticao == "semanal":
                nova_tarefa.data_termino += timedelta(weeks=1)
            elif tarefa_original.repeticao == "mensal":
                # Adiciona um mês (aproximação simples)
                nova_data = tarefa_original.data_termino
                nova_tarefa.data_termino = nova_data.replace(month=nova_data.month + 1)
            elif tarefa_original.repeticao == "anual":
                nova_data = tarefa_original.data_termino
                nova_tarefa.data_termino = nova_data.replace(year=nova_data.year + 1)

            self._tarefas.append(nova_tarefa)

        self._salvar_tudo()
        return tarefa_original

    def desmarcar_tarefa(self, tarefa_id: int) -> Optional[Tarefa]:
        """Marca uma tarefa como não concluída."""

        tarefa = self.buscar_tarefa_por_id(tarefa_id)
        if tarefa:
            tarefa.concluida = False
            self._salvar_tudo()
        return tarefa

    def remover_tarefas_concluidas(self) -> int:
        """Remove todas as tarefas concluídas e retorna o número de tarefas removidas."""

        tarefas_para_manter = [t for t in self._tarefas if not t.concluida]
        num_removidas = len(self._tarefas) - len(tarefas_para_manter)
        self._tarefas = tarefas_para_manter
        if num_removidas > 0:
            self._salvar_tudo()
        return num_removidas
