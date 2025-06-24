from datetime import date, timedelta
from typing import List, Optional, Dict, Any

class Tarefa:
    """
    Representa uma única tarefa no gerenciador.
    """
    def __init__(self,
                 titulo: str,
                 id: int, # Cada tarefa terá um ID único em todo o sistema
                 lista_id: int, # ID da lista à qual a tarefa pertence
                 concluida: bool = False,
                 data_termino: Optional[date] = None,
                 prioridade: Optional[str] = None,
                 tags: Optional[List[str]] = None,
                 notas: Optional[str] = None,
                 repeticao: Optional[str] = None):
        """
        Inicializa um objeto Tarefa.

        Args:
            titulo (str): O título ou descrição da tarefa.
            id (int): O identificador numérico único da tarefa.
            lista_id (int): O ID da lista de tarefas à qual esta tarefa está associada.
            concluida (bool): O status de conclusão da tarefa. Padrão é False.
            data_termino (Optional[date]): A data de vencimento da tarefa.
            prioridade (Optional[str]): A prioridade ('alta', 'media', 'baixa').
            tags (Optional[List[str]]): Uma lista de tags para categorização.
            notas (Optional[str]): Notas ou detalhes adicionais sobre a tarefa.
            repeticao (Optional[str]): A frequência de repetição ('diaria', 'semanal', etc.).
        """
        self.id = id
        self.titulo = titulo
        self.lista_id = lista_id
        self.concluida = concluida
        self.data_termino = data_termino
        self.prioridade = prioridade if prioridade else "nenhuma"
        self.tags = tags if tags is not None else []
        self.notas = notas if notas else ""
        self.repeticao = repeticao if repeticao else "nunca"

    def __repr__(self) -> str:
        """Retorna uma representação legível da tarefa, útil para debug."""
        status = "✓" if self.concluida else "✗"
        data_str = self.data_termino.strftime('%d/%m/%Y') if self.data_termino else "Sem data"
        return f"[{status}] ID: {self.id} | {self.titulo} (Data: {data_str}, Prio: {self.prioridade})"

    def to_dict(self) -> Dict[str, Any]:
        """Converte o objeto Tarefa para um dicionário para serialização em JSON."""
        return {
            "id": self.id,
            "titulo": self.titulo,
            "lista_id": self.lista_id,
            "concluida": self.concluida,
            # Converte a data para string no formato ISO para ser compatível com JSON
            "data_termino": self.data_termino.isoformat() if self.data_termino else None,
            "prioridade": self.prioridade,
            "tags": self.tags,
            "notas": self.notas,
            "repeticao": self.repeticao
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Tarefa':
        """Cria um objeto Tarefa a partir de um dicionário (desserialização)."""
        data_termino = None
        if data.get("data_termino"):
            # Converte a string no formato ISO de volta para um objeto date
            data_termino = date.fromisoformat(data["data_termino"])

        return cls(
            id=data["id"],
            titulo=data["titulo"],
            lista_id=data["lista_id"],
            concluida=data.get("concluida", False),
            data_termino=data_termino,
            prioridade=data.get("prioridade"),
            tags=data.get("tags"),
            notas=data.get("notas"),
            repeticao=data.get("repeticao")
        )

class ListaDeTarefas:
    """
    Representa uma lista que contém várias tarefas.
    """
    def __init__(self, nome: str, id: int):
        """
        Inicializa uma lista de tarefas.

        Args:
            nome (str): O nome da lista (ex: 'Trabalho', 'Estudos').
            id (int): O identificador numérico único da lista.
        """
        if not nome:
            raise ValueError("O nome da lista não pode ser vazio.")
        self.id = id
        self.nome = nome
        # A lista de tarefas não é armazenada diretamente aqui para evitar redundância.
        # O gerenciador principal irá associar tarefas a esta lista pelo `lista_id`.

    def __repr__(self) -> str:
        """Retorna uma representação legível da lista de tarefas."""
        return f"Lista(ID: {self.id}, Nome: '{self.nome}')"

    def to_dict(self) -> Dict[str, Any]:
        """Converte o objeto ListaDeTarefas para um dicionário para serialização."""
        return {
            "id": self.id,
            "nome": self.nome
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ListaDeTarefas':
        """Cria um objeto ListaDeTarefas a partir de um dicionário."""
        return cls(
            id=data["id"],
            nome=data["nome"]
        )
