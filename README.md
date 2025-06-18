# dindinGo - Personal Finance Manager

## Introduction
dindinGo is a comprehensive personal finance management system that helps users track their expenses, income, and savings. It features a React frontend for user interaction and a Python Flask backend for business logic.

## Project Structure
```
dindinGo/
├── back/              # Backend Python application
├── front/            # Frontend React application
├── data/            # Data storage
├── requirements.txt  # Python dependencies
└── README.md        # This file
```

## Getting Started

### Prerequisites
- Python 3.8 or higher
- Node.js 14 or higher
- npm 6 or higher

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd dindinGo
```

2. Install backend dependencies:
```bash
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

3. Install frontend dependencies:
```bash
cd front
npm install
```

### Running the Application

1. Start the backend server:
```bash
cd back/src
python api/api.py
```

2. Start the frontend development server:
```bash
cd front
npm start
```

The application will be available at:
- Frontend: http://localhost:3000
- Backend API: http://localhost:5000

## Features
- Transaction management (income and expenses)
- Wallet balance tracking
- Savings box functionality
- Points system for financial goals
- Monthly expense tracking
- Category-based organization

## Contributing
Please read our contributing guidelines before submitting pull requests.

## License
This project is licensed under the MIT License.