# MC102 - Projeto 03: Gerenciador de Tarefas

### Integrantes:
**Leonardo Franco Silva** (205007)
**Murilo Tsuda** (239797)

---

## Como Utilizar o Programa

Para rodar o programa você deve ter o Python instalado. Navegue até a pasta do projeto e execute o seguinte comando no seu terminal:


```bash
python lista_de_tarefas.py
```

---

## Funcionalidades Principais

### Gestão de Tarefas
- **Adicionar Tarefas**: Permite a criação de novas tarefas com título, associação a uma lista, data de término, prioridade, tags, notas e frequência de repetição. O ID da tarefa é gerado automaticamente pelo sistema.
- **Editar Tarefas**: O usuário pode alterar qualquer informação de uma tarefa existente (exceto o ID), como título, notas, data, prioridade e a lista à qual pertence.
- **Concluir Tarefas**: É possível marcar tarefas como concluídas e, depois de marcadas como concluídas, é possível torná-las pendentes novamente
- **Remover Tarefas**: O usuário pode remover tarefas de forma individual ou em massa (por exemplo, remover todas as concluídas).

### Gestão de Listas de Tarefas
- **Adicionar Listas**: Crie novas listas para organizar suas tarefas (ex: "Trabalho", "Estudos", "Pessoal").
- **Editar Listas**: Altere o nome de listas já existentes.
- **Remover Listas**: É possível remover uma lista, o que também apaga todas as tarefas contidas nela. Por segurança, o sistema não permite a exclusão da última lista restante.

### Visualização e Organização
- **Filtros**: Visualize tarefas com base em múltiplos critérios:
    - Por lista de tarefas específica.
    - Por uma `tag` específica.
    - Por status (concluídas, pendentes ou todas).
    - Por data (atrasadas, para hoje, para os próximos 7 dias).
- **Ordenação**: As tarefas podem ser ordenadas por data de término (padrão) ou por nível de prioridade.

### Busca
- **Busca Rápida**: Encontre tarefas buscando por um termo que pode estar presente no título, nas notas ou nas tags da tarefa.

### Persistência de Dados
- **Salvamento Automático**: Todas as alterações, como a criação de uma nova tarefa ou a edição de uma lista, são salvas automaticamente em um arquivo `dados_tarefas.json`. Isso garante que os dados não sejam perdidos ao fechar ou sair do programa.

---

## Estrutura dos Arquivos

Este projeto é dividido em módulos para separar as responsabilidades:

### 1. `lista_de_tarefas.py`

Este é o **ponto de entrada principal** da aplicação. É o arquivo que você executa para iniciar o Gerenciador de Tarefas.

- **Responsabilidade**: Orquestrar o fluxo do programa. Ele contém o loop principal que exibe o menu inicial e direciona o usuário para as diferentes funcionalidades (visualizar, adicionar, buscar, etc.) com base na sua escolha.
- **Como funciona**: Ele cria uma instância do `TaskManager` e entra em um loop `while`, chamando funções do módulo `ui` para interagir com o usuário e, em seguida, acionando os métodos apropriados no `gerenciador` para executar as ações.

### 2. `manager.py`

Este arquivo pode ser considerado o **cérebro da aplicação**. Ele contém a classe `TaskManager`, que centraliza toda a lógica de negócios do sistema.

- **Responsabilidade**: Gerenciar as operações de CRUD (Criar, Ler, Atualizar, Deletar) para tarefas e listas. Ele lida com a lógica de:
    - Adicionar e remover listas e tarefas.
    - Editar os dados de tarefas e listas.
    - Marcar tarefas como concluídas e lidar com a recorrência.
    - Buscar tarefas por termos.
- **Como funciona**: A classe `TaskManager` mantém o estado atual das listas e tarefas em memória (`self._listas`, `self._tarefas`). Sempre que uma alteração é feita, ela chama as funções do módulo `persistence` para salvar os dados no arquivo JSON.

### 3. `models.py`

Este arquivo define as **estruturas de dados** do projeto. Ele contém as classes que representam os objetos principais do sistema: `Tarefa` e `ListaDeTarefas`.

- **`Tarefa`**: Representa uma tarefa individual com todos os seus atributos, como `id`, `titulo`, `data_termino`, `prioridade`, `tags`, etc.
- **`ListaDeTarefas`**: Representa uma lista que agrupa tarefas. Contém atributos como `id` e `nome`.
- **Funcionalidades Chave**: Ambas as classes possuem os métodos `to_dict()` e `from_dict()`, que convertem os objetos Python em um formato (dicionário) que pode ser facilmente salvo como JSON, e vice-versa.

### 4. `ui.py`

Este módulo é responsável por toda a **interação com o usuário**. Ele separa completamente a lógica de apresentação (o que o usuário vê) da lógica de negócios (o que o sistema faz).

- **Responsabilidade**:
    - **Exibir Menus**: Contém funções para mostrar todos os menus de navegação (principal, de ações, de filtros, etc.).
    - **Imprimir Dados**: Formata e imprime as listas de tarefas de maneira clara e legível no terminal.
    - **Capturar Entradas**: Contém funções para obter dados do usuário, como os detalhes de uma nova tarefa, o ID de uma tarefa a ser editada ou o termo para uma busca.
    - **Funções Auxiliares**: Inclui funções úteis como `clear_screen()` para limpar a tela do terminal e `pausar_e_limpar()` para melhorar a experiência do usuário.

### 5. `persistence.py`

Este módulo lida com a **leitura e escrita de dados** no disco. Sua única responsabilidade é a persistência dos dados.

- **Responsabilidade**: Salvar o estado atual das tarefas e listas em um arquivo `dados_tarefas.json` e carregar esses dados quando o programa inicia.
- **`salvar_dados()`**: Recebe as listas de objetos `Tarefa` e `ListaDeTarefas`, converte-as em dicionários usando os métodos `to_dict()`, e as escreve no arquivo JSON.
- **`carregar_dados()`**: Lê o arquivo JSON, converte os dados de volta para objetos Python usando os métodos `from_dict()`, e os retorna para o `TaskManager`. Se o arquivo não existir, ele cria uma estrutura de dados padrão.

### 6. `dados_tarefas.json`

Este arquivo funciona como o **banco de dados** da sua aplicação.

- **Responsabilidade**: Armazenar todas as listas e tarefas criadas pelo usuário em formato JSON.
- **Como funciona**: É um arquivo de texto simples que mantém os dados de forma estruturada, com uma chave para `listas` e outra para `tarefas`.

---

## Exemplo de Uso: Adicionando e Visualizando uma Tarefa

Este guia demonstra um fluxo de uso comum: iniciar o programa, adicionar uma nova tarefa e depois visualizá-la na lista geral.

### Passo 1: Iniciar o programa

Para começar, execute o script principal no seu terminal.

```bash
python lista_de_tarefas.py
```

Você será saudado com o menu principal:

```
========================================
        Gerenciador de Tarefas
========================================

1. Visualizar Tarefas
2. Adicionar Tarefa
3. Buscar Tarefas
4. Gerenciar Listas
5. Sair

Escolha uma opção:
```

### Passo 2: Adicionar uma nova tarefa

Vamos adicionar uma tarefa para "Terminar o projeto 3 de MC102".
1. Digite `2` e pressione Enter para escolher "Adicionar Tarefa".
2. O programa pedirá os detalhes da tarefa. Preencha-os como no exemplo abaixo.

```
========================================
         Adicionar Nova Tarefa
========================================

Listas disponíveis:
  ID: 1 - Geral
  ID: 2 - Teste

Digite o ID da lista para a nova tarefa: 1
Título da tarefa: Terminar o projeto 3 de MC102
Data de término (AAAA-MM-DD, opcional): 2025-07-04
Prioridade (alta, media, baixa, opcional): alta
Tags (separadas por vírgula, opcional): universidade, projeto
Notas (opcional): Focar na UI/UX
Repetição (diaria, semanal, mensal, anual, opcional):

Salvando dados...
Dados salvos com sucesso!

Tarefa adicionada com sucesso!

Pressione Enter para continuar...
```

Após pressionar Enter, a tela será limpa e você retornará ao menu principal.

### Passo 3: Visualizar a tarefa criada

Agora, vamos visualizar a tarefa que acabamos de criar.
1. No menu principal, digite `1` e pressione Enter para escolher "Visualizar Tarefas".
2. O programa apresentará as opções de visualização. Vamos escolher ver todas as tarefas.

```
========================================
        Opções de Visualização
========================================

Como você deseja visualizar as tarefas?
1. Todas as Tarefas (geral)
2. Por Lista de Tarefas
3. Por Tag
4. Voltar

Escolha uma opção: 1
```

3. Em seguida, escolha o filtro. Para este exemplo, vamos ver todas, sem filtrar.

```
Aplicar qual filtro?
1. Ver todas as tarefas neste contexto
2. Apenas tarefas para hoje (e atrasadas)
3. Apenas tarefas para os próximos 7 dias (e atrasadas)
4. Apenas tarefas não concluídas
5. Apenas tarefas concluídas

Escolha uma opção de filtro: 1
```

4. Finalmente, escolha a ordenação (padrão por data).

```
Escolha a ordem de visualização:
1. Ordenar por Data (Padrão)
2. Ordenar por Prioridade
Escolha uma opção de ordenação (padrão é 1): 1
```

O sistema exibirá a lista de tarefas, incluindo a que acabamos de adicionar.

```
========================================
            Todas as Tarefas
========================================

[ ] ID: 2     | Terminar o projeto 3 de MC102    | Data: 04/07/2025           | Lista: Geral          | Prioridade: Alta     | Tags: universidade, rojeto
    Notas: Focar na UI/UX
[ ] ID: 1     | Estudar para a prova             | Data: 07/07/2025           | Lista: Geral          | Prioridade: Alta     | Tags: estudos, prova
    Notas:

Ações disponíveis:
1. Concluir uma tarefa
2. Desmarcar uma tarefa (tornar pendente)
3. Editar uma tarefa
4. Remover uma tarefa
5. Voltar

Escolha uma opção:
```

A partir daqui, você pode escolher uma ação, como concluir ou editar a tarefa, ou voltar ao menu principal.