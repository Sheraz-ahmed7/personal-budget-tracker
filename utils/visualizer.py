# utils/visualizer.py
import matplotlib.pyplot as plt
import pandas as pd
from typing import Dict
import matplotlib
matplotlib.use('TkAgg')  # Use TkAgg backend for better compatibility

class BudgetVisualizer:
    """Handles all data visualization for the budget tracker"""
    
    @staticmethod
    def expense_pie_chart(category_data: Dict, title: str = "Expenses by Category"):
        """Create a pie chart of expenses by category"""
        if not category_data:
            print("📊 No expense data to visualize!")
            return
        
        # Prepare data
        categories = list(category_data.keys())
        amounts = list(category_data.values())
        
        # Create figure with a clean style
        plt.style.use('seaborn-v0_8-darkgrid')
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Create pie chart
        colors = plt.cm.Set3(range(len(categories)))
        wedges, texts, autotexts = ax.pie(amounts, labels=categories, 
                                          autopct='%1.1f%%',
                                          colors=colors,
                                          startangle=90)
        
        # Style the chart
        for text in texts:
            text.set_fontsize(10)
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontsize(10)
            autotext.set_fontweight('bold')
        
        ax.set_title(title, fontsize=16, fontweight='bold', pad=20)
        ax.axis('equal')  # Equal aspect ratio ensures pie is circular
        
        plt.tight_layout()
        plt.show()
    
    @staticmethod
    def income_vs_expense_bar(income: float, expense: float):
        """Create a bar chart comparing income and expenses"""
        plt.style.use('seaborn-v0_8-darkgrid')
        fig, ax = plt.subplots(figsize=(8, 6))
        
        categories = ['Income', 'Expenses']
        values = [income, expense]
        colors = ['#2ecc71', '#e74c3c']  # Green for income, red for expenses
        
        bars = ax.bar(categories, values, color=colors, alpha=0.8, 
                     edgecolor='black', linewidth=2)
        
        # Add value labels on top of bars
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'${height:,.2f}',
                   ha='center', va='bottom', fontsize=12, fontweight='bold')
        
        ax.set_ylabel('Amount ($)', fontsize=12)
        ax.set_title('Income vs Expenses', fontsize=16, fontweight='bold', pad=20)
        ax.grid(axis='y', alpha=0.3)
        
        plt.tight_layout()
        plt.show()
    
    @staticmethod
    def monthly_trend(transactions_df: pd.DataFrame):
        """Show spending trends over time"""
        if transactions_df.empty:
            print("📊 No transaction data for trend analysis!")
            return
        
        # Group by month and type
        df = transactions_df.copy()
        df['month'] = df['date'].dt.to_period('M')
        
        monthly_summary = df.pivot_table(index='month', columns='type', 
                                        values='amount', aggfunc='sum', 
                                        fill_value=0)
        
        if 'expense' not in monthly_summary.columns:
            monthly_summary['expense'] = 0
        if 'income' not in monthly_summary.columns:
            monthly_summary['income'] = 0
        
        # Convert period to string for plotting
        months = monthly_summary.index.astype(str)
        
        plt.style.use('seaborn-v0_8-darkgrid')
        fig, ax = plt.subplots(figsize=(12, 6))
        
        ax.plot(months, monthly_summary['income'], marker='o', linewidth=2, 
               label='Income', color='#2ecc71')
        ax.plot(months, monthly_summary['expense'], marker='s', linewidth=2, 
               label='Expenses', color='#e74c3c')
        
        ax.set_xlabel('Month', fontsize=12)
        ax.set_ylabel('Amount ($)', fontsize=12)
        ax.set_title('Monthly Financial Trends', fontsize=16, fontweight='bold', pad=20)
        ax.legend(fontsize=11)
        ax.grid(True, alpha=0.3)
        
        # Rotate x-axis labels for better readability
        plt.xticks(rotation=45)
        
        plt.tight_layout()
        plt.show()