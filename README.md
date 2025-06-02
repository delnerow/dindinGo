# dindinGo Project

## Introdução
intro

## Estrutura do Projeto
```
dindinGo
├── src
│   ├── interfacePemba.py  
│   ├── transacao.py        
│   └── storage.py          
├── requirements.txt        
└── README.md               
```

## Installation
1. Clone the repository:
   ```
   git clone <repository-url>
   cd dindinGo
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage
1. Run the application:
   ```
   python src/interfacePemba.py
   ```

2. Follow the on-screen prompts to:
   - Create new transactions (income or expenses)
   - Add funds to your savings (cofrinho)
   - Break your savings jar to retrieve funds

## Functionality
- **Carteira**: Represents the current wallet, allowing users to check their balance and update it with transactions.
- **Cofrinho**: Represents a savings jar where users can save money and retrieve it when needed.
- **Despesa**: Represents an expense transaction, capturing details such as name, value, type, date, and frequency.
- **Receita**: Represents an income transaction with similar properties to Despesa.


## License
This project is licensed under the MIT License.