# Mini-To-Do List com Flask

Este é um projeto simples de uma aplicação **Mini-To-Do List** desenvolvida em **Python** utilizando **Flask** e **SQLite** como banco de dados.

---

## Funcionalidades

- Adicionar tarefas
- Marcar tarefas como concluídas
- Listar todas as tarefas
- Persistência em banco SQLite (`todo.db`)

---

## Estrutura de pastas

todo-flask
  app
    init.py        # Cria o app e inicializa o banco
    database.py    # Instância única do SQLAlchemy
    models.py      # Modelos do banco (Task)
    routes.py      # Rotas da aplicação
  templates
    index.html     # Página principal da lista de tarefas
    base.html    
    add_task.html 
  venv             # Ambiente virtual (não versionar)
  run.py           # Arquivo principal para rodar a aplicação
  requirements.txt # Dependências do projeto
  gitignore        # Arquivo de exclusão para Git
  README.md



---

## Configuração do Ambiente e Instalação de Dependências

1. **Criar o ambiente virtual:**

```bash
python -m venv venv
```

2. **Ativar o ambiente virtual:**

No Git Bash / Linux / Mac:

```bash
source venv/bin/activate
```

No Windows PowerShell:

```bash
venv\Scripts\activate
```

3. **Instalar as dependências do projeto:**

```bash
pip install -r requirements.txt
```

O arquivo requirements.txt deve conter pelo menos:

```bash
Flask
Flask-SQLAlchemy
```


## Execução da Aplicação

Rodar o projeto:

```bash
python run.py
```

Abrir no navegador:

```bash
http://127.0.0.1:5000
```

O banco SQLite (todo.db) será criado automaticamente na primeira execução.