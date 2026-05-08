# Bijewelz — Sistema de Gestão Comercial

Sistema web para gestão de uma loja de bijouterias. Permite cadastro de clientes e produtos, registro de vendas com controle de estoque e geração de relatórios.

---

## Tecnologias

- **Backend:** Python 3.12 + Django 6
- **Banco de dados:** SQLite
- **Frontend:** HTML + Bootstrap 5

---

## Requisitos

- Python 3.12+
- pip

---

## Instalação

```bash
# 1. Clone o repositório
git clone https://github.com/Manomelo/Bijewelz.git
cd Bijewelz

# 2. Crie e ative o ambiente virtual
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Linux/Mac

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Aplique as migrações
python manage.py migrate

# 5. Crie o superusuário (para o painel admin)
python manage.py createsuperuser

# 6. Inicie o servidor
python manage.py runserver
```

Acesse em: http://127.0.0.1:8000

---

## Funcionalidades

| Módulo | Funcionalidades |
|--------|----------------|
| Clientes | Listar, criar, editar e excluir clientes |
| Produtos | Listar, criar, editar e excluir produtos com controle de estoque |
| Vendas | Registrar vendas com múltiplos itens, redução automática de estoque |
| Relatórios | Relatório de vendas filtrado por período |
| Admin | Painel Django Admin em `/admin/` |

---

## Páginas

| URL | Descrição |
|-----|-----------|
| `/clientes/` | Lista de clientes |
| `/clientes/novo/` | Cadastrar cliente |
| `/clientes/<id>/editar/` | Editar cliente |
| `/clientes/<id>/excluir/` | Excluir cliente |
| `/produtos/` | Lista de produtos |
| `/produtos/novo/` | Cadastrar produto |
| `/produtos/<id>/editar/` | Editar produto |
| `/produtos/<id>/excluir/` | Excluir produto |
| `/vendas/` | Lista de vendas |
| `/vendas/nova/` | Registrar nova venda |
| `/vendas/<id>/` | Detalhe da venda |
| `/relatorios/vendas/` | Relatório por período |
| `/admin/` | Painel administrativo |

---

## Testes

```bash
python manage.py test
```

21 testes cobrindo modelos e views de clientes, produtos e vendas.

---

## Estrutura do Projeto

```
bijewelz/
├── bijewelz/          # Configurações do projeto
├── clientes/          # App de clientes
├── produtos/          # App de produtos
├── vendas/            # App de vendas e relatórios
├── templates/         # Templates HTML
│   ├── base.html
│   ├── clientes/
│   ├── produtos/
│   ├── vendas/
│   └── relatorios/
├── manage.py
└── requirements.txt
```
