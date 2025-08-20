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

todo_flask/
│
├── app/
│ ├── init.py # Cria o app e inicializa o banco
│ ├── database.py # Instância única do SQLAlchemy
│ ├── models.py # Modelos do banco (Task)
│ └── routes.py # Rotas da aplicação
│
├── templates/
│ └── index.html # Página principal da lista de tarefas
│
├── venv/ # Ambiente virtual (não versionar)
├── run.py # Arquivo principal para rodar a aplicação
├── requirements.txt # Dependências do projeto
├── .gitignore
└── README.md


---

## Configuração do Ambiente e Instalação de Dependências

1. **Criar o ambiente virtual:**

```bash
python -m venv venv
Ativar o ambiente virtual:

No Git Bash / Linux / Mac:

bash
Copiar
Editar
source venv/bin/activate
No Windows PowerShell:

bash
Copiar
Editar
venv\Scripts\activate
Instalar as dependências do projeto:

bash
Copiar
Editar
pip install -r requirements.txt
O arquivo requirements.txt deve conter pelo menos:

nginx
Copiar
Editar
Flask
Flask-SQLAlchemy
Execução da Aplicação
Rodar o projeto:

bash
Copiar
Editar
python run.py
Abrir no navegador:

cpp
Copiar
Editar
http://127.0.0.1:5000
O banco SQLite (todo.db) será criado automaticamente na primeira execução.

Todas as tabelas definidas em models.py serão inicializadas sem precisar de comandos manuais no shell.