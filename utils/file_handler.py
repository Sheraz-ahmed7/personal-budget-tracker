# utils/file_handler.py
import csv
import os
from datetime import datetime
from typing import List, Dict, Tuple
import pandas as pd

class BudgetFileHandler:
    """Handles all file operations for the budget tracker"""
    
    def __init__(self, data_dir='data', filename='transactions.csv'):
        self.data_dir = data_dir
        self.filename = filename
        self.filepath = os.path.join(data_dir, filename)
        self._initialize()
    
    def _initialize(self):
        """Create data directory and file if they don't exist"""
        # Create directory if needed
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
            print(f"📁 Created data directory: {self.data_dir}")
        
        # Create file with headers if needed
        if not os.path.exists(self.filepath):
            with open(self.filepath, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(['id', 'date', 'category', 'amount', 'type', 'description'])
            print(f"📄 Created new transaction file: {self.filename}")
    
    def add_transaction(self, date: str, category: str, amount: float, 
                       trans_type: str, description: str = '') -> bool:
        """Add a new transaction to the CSV file"""
        try:
            # Generate a simple ID based on timestamp
            transaction_id = int(datetime.now().timestamp())
            
            with open(self.filepath, 'a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow([transaction_id, date, category, amount, 
                               trans_type, description])
            return True
        except Exception as e:
            print(f"❌ Error adding transaction: {e}")
            return False
    
    def get_all_transactions(self) -> pd.DataFrame:
        """Load all transactions into a pandas DataFrame"""
        try:
            df = pd.read_csv(self.filepath)
            # Convert date column to datetime for better handling
            df['date'] = pd.to_datetime(df['date'])
            return df
        except Exception as e:
            print(f"❌ Error reading transactions: {e}")
            return pd.DataFrame()
    
    def get_transactions_by_date(self, start_date: str, end_date: str) -> pd.DataFrame:
        """Get transactions within a date range"""
        df = self.get_all_transactions()
        if df.empty:
            return df
        
        mask = (df['date'] >= start_date) & (df['date'] <= end_date)
        return df.loc[mask]
    
    def delete_transaction(self, transaction_id: int) -> bool:
        """Delete a transaction by ID"""
        try:
            df = self.get_all_transactions()
            if df.empty:
                return False
            
            # Filter out the transaction
            df = df[df['id'] != transaction_id]
            
            # Save back to CSV
            df.to_csv(self.filepath, index=False)
            return True
        except Exception as e:
            print(f"❌ Error deleting transaction: {e}")
            return False
    
    def get_summary(self) -> Dict:
        """Calculate financial summary"""
        df = self.get_all_transactions()
        if df.empty:
            return {
                'total_income': 0,
                'total_expense': 0,
                'balance': 0,
                'transaction_count': 0
            }
        
        total_income = df[df['type'] == 'income']['amount'].sum()
        total_expense = df[df['type'] == 'expense']['amount'].sum()
        
        return {
            'total_income': round(total_income, 2),
            'total_expense': round(total_expense, 2),
            'balance': round(total_income - total_expense, 2),
            'transaction_count': len(df)
        }
    
    def get_category_breakdown(self) -> Dict:
        """Get expense breakdown by category"""
        df = self.get_all_transactions()
        if df.empty:
            return {}
        
        expenses = df[df['type'] == 'expense']
        if expenses.empty:
            return {}
        
        return expenses.groupby('category')['amount'].sum().to_dict()