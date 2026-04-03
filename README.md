# Bijewelz — Sistema de Gestão Comercial

Sistema web para gestão de uma loja de bijouterias. Permite cadastro de clientes e produtos, registro de vendas e geração de relatórios.

---

## Tecnologias

- **Backend:** Python 3.12 + Django 5 + Django REST Framework
- **Banco de dados:** SQLite
- **Autenticação:** JWT via `djangorestframework-simplejwt`
- **Frontend:** HTML + CSS + JavaScript (fetch API)

---

## Requisitos

- Python 3.12+
- pip

---

## Instalação

```bash
# 1. Clone o repositório
git clone https://github.com/seu-usuario/bijewelz.git
cd bijewelz

# 2. Crie e ative o ambiente virtual
python -m venv venv
source venv/bin/activate        # Linux/Mac
venv\Scripts\activate           # Windows

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Aplique as migrações
python manage.py migrate

# 5. Crie o superusuário
python manage.py createsuperuser

# 6. Inicie o servidor
python manage.py runserver
```
---

## Perfis de Acesso

| Perfil | Permissões |
|--------|-----------|
| `ADMIN` | Acesso total ao sistema |
| `FUNCIONARIO` | Cadastros e registro de vendas |

---

## Principais Endpoints

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| POST | `/auth/login/` | Login e geração do token JWT |
| GET/POST | `/clientes/` | Listar e cadastrar clientes |
| GET/POST | `/produtos/` | Listar e cadastrar produtos |
| GET/POST | `/vendas/` | Listar e registrar vendas |
| GET | `/relatorios/periodo/` | Vendas por período |

---

## Estrutura do Projeto

```
bijewelz/
├── apps/
│   ├── autenticacao/
│   ├── clientes/
│   ├── produtos/
│   ├── vendas/
│   └── relatorios/
├── static/
├── templates/
├── manage.py
└── requirements.txt
```

