# Bijewelz — Sistema de Gestão Comercial

Sistema web para gestão de uma loja de bijouterias. Permite cadastro de clientes e produtos, registro de vendas com controle de estoque, loja online para clientes e geração de relatórios.

---

## Tecnologias

- **Backend:** Python 3.12 + Django 6 + Django REST Framework
- **Banco de dados:** SQLite
- **Autenticação:** Sessão Django (loja) + JWT via `djangorestframework-simplejwt` (API)
- **Frontend:** Django Templates + Bootstrap 5
- **Imagens:** Pillow

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
source venv/bin/activate        # Linux/Mac
venv\Scripts\activate           # Windows

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

## Módulos

| Módulo | Descrição |
|--------|-----------|
| **Loja** | Vitrine pública com página inicial, listagem, filtros e detalhe de produto |
| **Carrinho** | Carrinho persistido no banco por usuário autenticado |
| **Pedidos** | Finalização de compra com controle de estoque e confirmação |
| **Clientes** | CRUD de clientes no painel admin |
| **Produtos** | CRUD de produtos e categorias com imagens e controle de estoque |
| **Vendas** | Registro de vendas com múltiplos itens |
| **Relatórios** | Vendas por período, produto, categoria e cliente com gráfico |
| **API REST** | Endpoints protegidos por JWT para clientes, produtos e vendas |

---

## Páginas da Loja

| URL | Descrição |
|-----|-----------|
| `/loja/` | Página inicial com categorias e produtos em destaque |
| `/loja/produtos/` | Listagem com filtro por nome, preço, categoria e ordenação |
| `/loja/produtos/<id>/` | Detalhe do produto |
| `/loja/carrinho/` | Carrinho de compras |
| `/loja/finalizar/` | Finalizar pedido |
| `/loja/pedido/<id>/` | Confirmação do pedido |
| `/loja/conta/login/` | Login do cliente |
| `/loja/conta/registro/` | Cadastro de cliente |

---

## Painel Administrativo

| URL | Descrição |
|-----|-----------|
| `/clientes/` | Lista de clientes |
| `/produtos/` | Lista de produtos |
| `/produtos/categorias/` | Lista de categorias |
| `/vendas/` | Lista de vendas |
| `/relatorios/vendas/` | Relatório de vendas |
| `/admin/` | Painel Django Admin |

---

## API REST

Todos os endpoints requerem autenticação JWT.

### Obter token
```
POST /api/token/
Body: { "username": "...", "password": "..." }
```

### Renovar token
```
POST /api/token/refresh/
Body: { "refresh": "..." }
```

### Endpoints

| Método | URL | Descrição |
|--------|-----|-----------|
| GET | `/api/produtos/` | Listar produtos |
| POST | `/api/produtos/` | Criar produto |
| GET | `/api/produtos/<id>/` | Detalhe do produto |
| PUT/PATCH | `/api/produtos/<id>/` | Editar produto |
| DELETE | `/api/produtos/<id>/` | Excluir produto |
| GET | `/api/clientes/` | Listar clientes |
| POST | `/api/clientes/` | Criar cliente |
| GET | `/api/clientes/<id>/` | Detalhe do cliente |
| PUT/PATCH | `/api/clientes/<id>/` | Editar cliente |
| DELETE | `/api/clientes/<id>/` | Excluir cliente |
| GET | `/api/vendas/` | Listar vendas |
| GET | `/api/vendas/<id>/` | Detalhe da venda com itens |

---

## Testes

```bash
python manage.py test
```

Cobertura:
- Models e views de clientes, produtos e vendas
- Endpoints da API REST
- Loja: página inicial, listagem, detalhe, filtros
- Carrinho: adicionar, remover, incrementar quantidade
- Login, registro e logout
- Finalizar pedido: controle de estoque, esvaziamento do carrinho

---

## Estrutura do Projeto

```
Bijewelz/
├── bijewelz/          # Configurações do projeto
│   ├── settings.py
│   ├── urls.py
│   └── api_urls.py
├── clientes/          # App de clientes
├── produtos/          # App de produtos e categorias
├── vendas/            # App de vendas, carrinho e relatórios
├── loja/              # App da loja online
├── templates/
│   ├── base.html
│   ├── loja/
│   ├── clientes/
│   ├── produtos/
│   ├── vendas/
│   └── relatorios/
├── media/             # Imagens de produtos e categorias
├── manage.py
└── requirements.txt
```