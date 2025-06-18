# dindinGo - Gerenciador de Finanças Pessoais

## Introdução
dindinGo é um sistema completo de gerenciamento de finanças pessoais que ajuda usuários a controlar seus gastos, receitas e economias. Possui um frontend em React para interação do usuário e um backend em Python Flask para a lógica de negócios.

## Estrutura do Projeto
```
dindinGo/
├── back/              # Aplicação backend em Python
├── front/             # Aplicação frontend em React
├── data/              # Armazenamento de dados
├── requirements.txt   # Dependências Python
└── README.md          # Este arquivo
```

## Primeiros Passos

### Pré-requisitos
- Python 3.8 ou superior
- Node.js 14 ou superior
- npm 6 ou superior

### Instalação

1. Clone o repositório:
```bash
git clone <url-do-repositorio>
cd dindinGo
```

2. Instale as dependências do backend:
```bash
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

3. Instale as dependências do frontend:
```bash
cd front
npm install
```

### Executando a Aplicação

1. Inicie o servidor backend:
```bash
cd back/src
python api/api.py
```

2. Inicie o servidor de desenvolvimento do frontend:
```bash
cd front
npm start
```

A aplicação estará disponível em:
- Frontend: http://localhost:3000
- API Backend: http://localhost:5000

## Funcionalidades
- Gerenciamento de transações (receitas e despesas)
- Controle de saldo das carteiras
- Funcionalidade de cofrinho
- Sistema de pontos para metas financeiras
- Controle mensal de despesas
- Organização por categorias

## Contribuindo
Leia nossas diretrizes de contribuição antes de enviar pull requests.

## Licença
Este projeto está licenciado sob a Licença MIT.