# main.py
import os
import sys
from datetime import datetime
from tabulate import tabulate
from colorama import init, Fore, Style
import pandas as pd

# Import our modules
from utils.file_handler import BudgetFileHandler
from utils.visualizer import BudgetVisualizer

# Initialize colorama for colored terminal output
init(autoreset=True)

class BudgetTracker:
    """Main Budget Tracker Application"""
    
    def __init__(self):
        self.file_handler = BudgetFileHandler()
        self.visualizer = BudgetVisualizer()
        self.categories = [
            'Food', 'Transportation', 'Housing', 'Utilities', 
            'Entertainment', 'Healthcare', 'Shopping', 'Education',
            'Salary', 'Freelance', 'Investment', 'Other'
        ]
    
    def clear_screen(self):
        """Clear the terminal screen"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def print_header(self):
        """Print application header"""
        print(Fore.CYAN + Style.BRIGHT + """
╔══════════════════════════════════════════════════════════╗
║         💰 PERSONAL BUDGET TRACKER v2.0 💰               ║
║         Take control of your finances today!             ║
╚══════════════════════════════════════════════════════════╝
        """ + Style.RESET_ALL)
    
    def print_menu(self):
        """Display the main menu"""
        print(Fore.YELLOW + "\n📋 MAIN MENU" + Style.RESET_ALL)
        print("=" * 50)
        options = [
            ("1", "➕ Add Transaction"),
            ("2", "📊 View Summary"),
            ("3", "📈 Visualize Expenses"),
            ("4", "📝 View All Transactions"),
            ("5", "🗑️  Delete Transaction"),
            ("6", "🔍 Filter by Date"),
            ("7", "📉 Monthly Trends"),
            ("8", "🚪 Exit")
        ]
        
        for key, desc in options:
            print(f"  {Fore.GREEN}{key}{Style.RESET_ALL} - {desc}")
        print("=" * 50)
    
    def get_valid_input(self, prompt: str, input_type=str, 
                        valid_options=None, allow_empty=False):
        """Helper function to get validated user input"""
        while True:
            try:
                user_input = input(prompt).strip()
                
                if allow_empty and user_input == '':
                    return None
                
                if input_type == float:
                    value = float(user_input)
                    if value <= 0:
                        print(Fore.RED + "❌ Amount must be positive!" + Style.RESET_ALL)
                        continue
                    return value
                elif input_type == int:
                    return int(user_input)
                
                if valid_options and user_input not in valid_options:
                    print(Fore.RED + f"❌ Please enter one of: {', '.join(valid_options)}" + Style.RESET_ALL)
                    continue
                
                return user_input
                
            except ValueError:
                print(Fore.RED + f"❌ Invalid input! Please enter a valid {input_type.__name__}." + Style.RESET_ALL)
    
    def add_transaction_ui(self):
        """UI for adding a new transaction"""
        self.clear_screen()
        print(Fore.YELLOW + "\n➕ ADD NEW TRANSACTION" + Style.RESET_ALL)
        print("-" * 40)
        
        # Get date
        date_input = input("📅 Date (YYYY-MM-DD) or press Enter for today: ").strip()
        if date_input:
            try:
                # Validate date format
                datetime.strptime(date_input, '%Y-%m-%d')
                date = date_input
            except ValueError:
                print(Fore.RED + "❌ Invalid date format! Using today's date." + Style.RESET_ALL)
                date = datetime.now().strftime('%Y-%m-%d')
        else:
            date = datetime.now().strftime('%Y-%m-%d')
        
        # Get transaction type
        print("\n📌 Transaction Type:")
        print("  1. Income 💰")
        print("  2. Expense 💸")
        type_choice = self.get_valid_input("  Choose (1-2): ", input_type=int, valid_options=[1, 2])
        trans_type = 'income' if type_choice == 1 else 'expense'
        
        # Show categories based on type
        if trans_type == 'income':
            cat_options = ['Salary', 'Freelance', 'Investment', 'Other']
        else:
            cat_options = ['Food', 'Transportation', 'Housing', 'Utilities', 
                          'Entertainment', 'Healthcare', 'Shopping', 'Education', 'Other']
        
        print(f"\n📁 Available Categories for {trans_type}:")
        for i, cat in enumerate(cat_options, 1):
            print(f"  {i}. {cat}")
        
        cat_choice = self.get_valid_input("  Choose category number: ", input_type=int, 
                                        valid_options=range(1, len(cat_options)+1))
        category = cat_options[cat_choice - 1]
        
        # Get amount
        amount = self.get_valid_input("💰 Amount: $", input_type=float)
        
        # Get description (optional)
        description = input("📝 Description (optional): ").strip()
        
        # Add transaction
        if self.file_handler.add_transaction(date, category, amount, trans_type, description):
            print(Fore.GREEN + f"\n✅ Transaction added successfully!" + Style.RESET_ALL)
            if trans_type == 'expense':
                print(Fore.YELLOW + f"   💸 Spent: ${amount:.2f} on {category}" + Style.RESET_ALL)
            else:
                print(Fore.YELLOW + f"   💰 Earned: ${amount:.2f} from {category}" + Style.RESET_ALL)
        
        input("\nPress Enter to continue...")
    
    def view_summary_ui(self):
        """Display financial summary"""
        self.clear_screen()
        print(Fore.YELLOW + "\n📊 FINANCIAL SUMMARY" + Style.RESET_ALL)
        print("=" * 50)
        
        summary = self.file_handler.get_summary()
        
        # Calculate percentages and warnings
        savings_rate = 0
        if summary['total_income'] > 0:
            savings_rate = (summary['balance'] / summary['total_income']) * 100
        
        # Display summary with colors
        print(f"\n{Fore.CYAN}📈 Overview:{Style.RESET_ALL}")
        print(f"  Total Income:    {Fore.GREEN}${summary['total_income']:,.2f}{Style.RESET_ALL}")
        print(f"  Total Expenses:  {Fore.RED}${summary['total_expense']:,.2f}{Style.RESET_ALL}")
        print(f"  Balance:         {Fore.BLUE}${summary['balance']:,.2f}{Style.RESET_ALL}")
        print(f"  Transactions:    {summary['transaction_count']}")
        
        print(f"\n{Fore.CYAN}📊 Statistics:{Style.RESET_ALL}")
        print(f"  Savings Rate:    {savings_rate:.1f}%")
        
        if summary['total_expense'] > 0:
            avg_expense = summary['total_expense'] / summary['transaction_count'] if summary['transaction_count'] > 0 else 0
            print(f"  Avg Expense:      ${avg_expense:,.2f}")
        
        # Financial health check
        print(f"\n{Fore.CYAN}💡 Financial Health:{Style.RESET_ALL}")
        if summary['balance'] < 0:
            print(Fore.RED + "  ⚠️  Warning: You're spending more than you earn!" + Style.RESET_ALL)
        elif summary['balance'] < summary['total_income'] * 0.2:
            print(Fore.YELLOW + "  ℹ️  Tip: Try to save at least 20% of your income" + Style.RESET_ALL)
        else:
            print(Fore.GREEN + "  ✅ Great job! You're saving well!" + Style.RESET_ALL)
        
        # Category breakdown
        category_breakdown = self.file_handler.get_category_breakdown()
        if category_breakdown:
            print(f"\n{Fore.CYAN}📁 Top Expense Categories:{Style.RESET_ALL}")
            sorted_cats = sorted(category_breakdown.items(), key=lambda x: x[1], reverse=True)[:3]
            for category, amount in sorted_cats:
                percentage = (amount / summary['total_expense']) * 100 if summary['total_expense'] > 0 else 0
                print(f"  {category}: ${amount:,.2f} ({percentage:.1f}%)")
        
        print("\n" + "=" * 50)
        input("\nPress Enter to continue...")
    
    def view_transactions_ui(self):
        """Display all transactions in a table"""
        self.clear_screen()
        print(Fore.YELLOW + "\n📝 ALL TRANSACTIONS" + Style.RESET_ALL)
        print("=" * 70)
        
        df = self.file_handler.get_all_transactions()
        if df.empty:
            print(Fore.RED + "No transactions found!" + Style.RESET_ALL)
            input("\nPress Enter to continue...")
            return
        
        # Format the dataframe for display
        display_df = df.copy()
        display_df['date'] = display_df['date'].dt.strftime('%Y-%m-%d')
        display_df['amount'] = display_df.apply(
            lambda row: f"{Fore.GREEN if row['type'] == 'income' else Fore.RED}${row['amount']:,.2f}{Style.RESET_ALL}",
            axis=1
        )
        
        # Display in table format
        table_data = []
        for _, row in display_df.iterrows():
            table_data.append([
                row['id'],
                row['date'],
                row['category'],
                row['amount'],
                row['description'][:30] + '...' if len(row['description']) > 30 else row['description']
            ])
        
        headers = ['ID', 'Date', 'Category', 'Amount', 'Description']
        print(tabulate(table_data, headers=headers, tablefmt='grid'))
        
        print(f"\n{Fore.CYAN}Total: {len(df)} transactions{Style.RESET_ALL}")
        input("\nPress Enter to continue...")
    
    def delete_transaction_ui(self):
        """UI for deleting a transaction"""
        self.clear_screen()
        print(Fore.YELLOW + "\n🗑️  DELETE TRANSACTION" + Style.RESET_ALL)
        print("=" * 40)
        
        # Show recent transactions
        df = self.file_handler.get_all_transactions()
        if df.empty:
            print(Fore.RED + "No transactions to delete!" + Style.RESET_ALL)
            input("\nPress Enter to continue...")
            return
        
        print("\nRecent Transactions:")
        recent = df.tail(5)
        for _, row in recent.iterrows():
            color = Fore.GREEN if row['type'] == 'income' else Fore.RED
            print(f"  ID: {row['id']} - {row['date']} - {row['category']} - {color}${row['amount']:,.2f}{Style.RESET_ALL}")
        
        # Get transaction ID to delete
        try:
            trans_id = int(input("\nEnter transaction ID to delete (0 to cancel): "))
            if trans_id == 0:
                return
            
            if self.file_handler.delete_transaction(trans_id):
                print(Fore.GREEN + f"✅ Transaction {trans_id} deleted successfully!" + Style.RESET_ALL)
            else:
                print(Fore.RED + f"❌ Transaction {trans_id} not found!" + Style.RESET_ALL)
        
        except ValueError:
            print(Fore.RED + "❌ Invalid ID!" + Style.RESET_ALL)
        
        input("\nPress Enter to continue...")
    
    def filter_by_date_ui(self):
        """Filter and display transactions by date range"""
        self.clear_screen()
        print(Fore.YELLOW + "\n🔍 FILTER BY DATE" + Style.RESET_ALL)
        print("=" * 40)
        
        # Get date range
        print("\nEnter date range (YYYY-MM-DD):")
        start_date = input("  Start date: ").strip()
        end_date = input("  End date: ").strip()
        
        try:
            # Validate dates
            datetime.strptime(start_date, '%Y-%m-%d')
            datetime.strptime(end_date, '%Y-%m-%d')
            
            df = self.file_handler.get_transactions_by_date(start_date, end_date)
            
            if df.empty:
                print(Fore.RED + "\nNo transactions in this date range!" + Style.RESET_ALL)
            else:
                print(f"\n{Fore.GREEN}Transactions from {start_date} to {end_date}:{Style.RESET_ALL}")
                print("-" * 60)
                
                total_income = df[df['type'] == 'income']['amount'].sum()
                total_expense = df[df['type'] == 'expense']['amount'].sum()
                
                for _, row in df.iterrows():
                    color = Fore.GREEN if row['type'] == 'income' else Fore.RED
                    print(f"  {row['date']} - {row['category']}: {color}${row['amount']:,.2f}{Style.RESET_ALL}")
                
                print("-" * 60)
                print(f"  Total Income:  {Fore.GREEN}${total_income:,.2f}{Style.RESET_ALL}")
                print(f"  Total Expense: {Fore.RED}${total_expense:,.2f}{Style.RESET_ALL}")
                print(f"  Balance:       {Fore.BLUE}${(total_income - total_expense):,.2f}{Style.RESET_ALL}")
        
        except ValueError:
            print(Fore.RED + "❌ Invalid date format! Use YYYY-MM-DD" + Style.RESET_ALL)
        
        input("\nPress Enter to continue...")
    
    def visualize_ui(self):
        """UI for visualizations"""
        self.clear_screen()
        print(Fore.YELLOW + "\n📈 VISUALIZATIONS" + Style.RESET_ALL)
        print("=" * 40)
        print("1. Expense Breakdown (Pie Chart)")
        print("2. Income vs Expenses (Bar Chart)")
        print("3. Monthly Trends (Line Chart)")
        print("4. Back to Main Menu")
        
        choice = self.get_valid_input("\nChoose (1-4): ", input_type=int, valid_options=[1, 2, 3, 4])
        
        if choice == 1:
            category_data = self.file_handler.get_category_breakdown()
            self.visualizer.expense_pie_chart(category_data)
        elif choice == 2:
            summary = self.file_handler.get_summary()
            self.visualizer.income_vs_expense_bar(summary['total_income'], summary['total_expense'])
        elif choice == 3:
            df = self.file_handler.get_all_transactions()
            self.visualizer.monthly_trend(df)
        else:
            return
        
        input("\nPress Enter to continue...")
    
    def run(self):
        """Main application loop"""
        while True:
            self.clear_screen()
            self.print_header()
            self.print_menu()
            
            choice = self.get_valid_input("\n👉 Enter your choice: ", input_type=int, 
                                        valid_options=[1, 2, 3, 4, 5, 6, 7, 8])
            
            if choice == 1:
                self.add_transaction_ui()
            elif choice == 2:
                self.view_summary_ui()
            elif choice == 3:
                self.visualize_ui()
            elif choice == 4:
                self.view_transactions_ui()
            elif choice == 5:
                self.delete_transaction_ui()
            elif choice == 6:
                self.filter_by_date_ui()
            elif choice == 7:
                self.visualize_ui()  # Monthly trends option inside visualize_ui
            elif choice == 8:
                print(Fore.GREEN + "\n👋 Thanks for using Personal Budget Tracker!" + Style.RESET_ALL)
                print("   Remember: Every dollar tracked is a dollar saved! 💰")
                sys.exit(0)

# Create the utils/__init__.py file
def create_utils_init():
    """Create the __init__.py file for the utils package"""
    os.makedirs('utils', exist_ok=True)
    with open('utils/__init__.py', 'w') as f:
        f.write('"""Budget Tracker Utilities Package"""\n')
        f.write('from .file_handler import BudgetFileHandler\n')
        f.write('from .visualizer import BudgetVisualizer\n')

if __name__ == "__main__":
    # Create necessary files
    create_utils_init()
    
    # Run the application
    app = BudgetTracker()
    app.run()