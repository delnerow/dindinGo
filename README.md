# dindinGo Project

## Overview
The dindinGo project is a financial management application that allows users to manage their transactions, savings (cofrinho), and current wallet (corrente). The application provides a user-friendly interface for creating and tracking expenses and income, as well as managing savings.

## Project Structure
```
dindinGo
├── src
│   ├── interfacePemba.py  # Main interface for managing financial transactions
│   ├── transacao.py        # Defines the transaction-related classes
│   └── storage.py          # Handles saving and loading data
├── requirements.txt        # Lists project dependencies
└── README.md               # Project documentation
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
- **Data Persistence**: The application remembers the state of transactions, cofrinho, and corrente between runs by saving data to a file.

## Contributing
Contributions are welcome! Please submit a pull request or open an issue for any enhancements or bug fixes.

## License
This project is licensed under the MIT License.