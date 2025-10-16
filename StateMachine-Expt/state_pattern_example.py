"""
State Design Pattern Example - Vending Machine
==============================================

This example demonstrates the State design pattern using a vending machine
that can be in different states: Idle, Coin Inserted, Product Selected, and Out of Order.

The State pattern allows an object to alter its behavior when its internal state changes.
It appears as if the object changed its class.
"""

from abc import ABC, abstractmethod
from enum import Enum


class Product(Enum):
    """Available products in the vending machine"""
    SODA = ("Soda", 1.50)
    CHIPS = ("Chips", 1.25)
    CANDY = ("Candy", 1.00)
    WATER = ("Water", 1.00)
    
    def __init__(self, name, price):
        self.product_name = name
        self.price = price


class VendingMachineState(ABC):
    """Abstract base class for all vending machine states"""
    
    @abstractmethod
    def insert_coin(self, machine, amount):
        pass
    
    @abstractmethod
    def select_product(self, machine, product):
        pass
    
    @abstractmethod
    def dispense_product(self, machine):
        pass
    
    @abstractmethod
    def return_change(self, machine):
        pass
    
    @abstractmethod
    def get_state_name(self):
        pass


class IdleState(VendingMachineState):
    """State when the machine is waiting for coins"""
    
    def insert_coin(self, machine, amount):
        if amount <= 0:
            print("Please insert a valid amount.")
            return
        
        machine.add_money(amount)
        print(f"Inserted ${amount:.2f}. Total: ${machine.get_balance():.2f}")
        machine.set_state(machine.coin_inserted_state)
    
    def select_product(self, machine, product):
        print("Please insert coins first.")
    
    def dispense_product(self, machine):
        print("Please insert coins and select a product first.")
    
    def return_change(self, machine):
        print("No money to return.")
    
    def get_state_name(self):
        return "Idle"


class CoinInsertedState(VendingMachineState):
    """State when coins have been inserted but no product selected"""
    
    def insert_coin(self, machine, amount):
        if amount <= 0:
            print("Please insert a valid amount.")
            return
        
        machine.add_money(amount)
        print(f"Inserted ${amount:.2f}. Total: ${machine.get_balance():.2f}")
    
    def select_product(self, machine, product):
        if machine.get_balance() >= product.price:
            machine.set_selected_product(product)
            print(f"Selected {product.product_name} (${product.price:.2f})")
            machine.set_state(machine.product_selected_state)
        else:
            needed = product.price - machine.get_balance()
            print(f"Insufficient funds. Need ${needed:.2f} more for {product.product_name}")
    
    def dispense_product(self, machine):
        print("Please select a product first.")
    
    def return_change(self, machine):
        change = machine.get_balance()
        machine.reset_balance()
        print(f"Returning ${change:.2f}")
        machine.set_state(machine.idle_state)
    
    def get_state_name(self):
        return "Coin Inserted"


class ProductSelectedState(VendingMachineState):
    """State when a product has been selected and payment is sufficient"""
    
    def insert_coin(self, machine, amount):
        if amount <= 0:
            print("Please insert a valid amount.")
            return
        
        machine.add_money(amount)
        print(f"Inserted ${amount:.2f}. Total: ${machine.get_balance():.2f}")
    
    def select_product(self, machine, product):
        if machine.get_balance() >= product.price:
            machine.set_selected_product(product)
            print(f"Changed selection to {product.product_name} (${product.price:.2f})")
        else:
            needed = product.price - machine.get_balance()
            print(f"Insufficient funds. Need ${needed:.2f} more for {product.product_name}")
    
    def dispense_product(self, machine):
        product = machine.get_selected_product()
        if product and machine.get_balance() >= product.price:
            print(f"Dispensing {product.product_name}...")
            
            # Calculate change
            change = machine.get_balance() - product.price
            machine.reset_balance()
            machine.set_selected_product(None)
            
            if change > 0:
                print(f"Returning change: ${change:.2f}")
            
            print(f"Enjoy your {product.product_name}!")
            machine.set_state(machine.idle_state)
        else:
            print("Cannot dispense product. Insufficient funds or no product selected.")
    
    def return_change(self, machine):
        change = machine.get_balance()
        machine.reset_balance()
        machine.set_selected_product(None)
        print(f"Transaction cancelled. Returning ${change:.2f}")
        machine.set_state(machine.idle_state)
    
    def get_state_name(self):
        return "Product Selected"


class OutOfOrderState(VendingMachineState):
    """State when the machine is out of order"""
    
    def insert_coin(self, machine, amount):
        print("Machine is out of order. Cannot accept coins.")
    
    def select_product(self, machine, product):
        print("Machine is out of order. Cannot select products.")
    
    def dispense_product(self, machine):
        print("Machine is out of order. Cannot dispense products.")
    
    def return_change(self, machine):
        if machine.get_balance() > 0:
            change = machine.get_balance()
            machine.reset_balance()
            print(f"Machine out of order. Returning ${change:.2f}")
        else:
            print("No money to return.")
    
    def get_state_name(self):
        return "Out of Order"


class VendingMachine:
    """
    The Context class that maintains a reference to a State object
    and delegates state-specific behavior to it.
    """
    
    def __init__(self):
        # Initialize all possible states
        self.idle_state = IdleState()
        self.coin_inserted_state = CoinInsertedState()
        self.product_selected_state = ProductSelectedState()
        self.out_of_order_state = OutOfOrderState()
        
        # Start in idle state
        self._current_state = self.idle_state
        self._balance = 0.0
        self._selected_product = None
        self._is_operational = True
    
    def set_state(self, state):
        """Change the current state"""
        self._current_state = state
        print(f"State changed to: {state.get_state_name()}")
    
    def get_current_state(self):
        """Get the current state name"""
        return self._current_state.get_state_name()
    
    def add_money(self, amount):
        """Add money to the machine's balance"""
        self._balance += amount
    
    def get_balance(self):
        """Get current balance"""
        return self._balance
    
    def reset_balance(self):
        """Reset balance to zero"""
        self._balance = 0.0
    
    def set_selected_product(self, product):
        """Set the selected product"""
        self._selected_product = product
    
    def get_selected_product(self):
        """Get the selected product"""
        return self._selected_product
    
    def set_out_of_order(self):
        """Set machine to out of order state"""
        self._is_operational = False
        self.set_state(self.out_of_order_state)
    
    def set_operational(self):
        """Restore machine to operational state"""
        self._is_operational = True
        self.set_state(self.idle_state)
    
    # Delegate methods to current state
    def insert_coin(self, amount):
        """Insert a coin into the machine"""
        self._current_state.insert_coin(self, amount)
    
    def select_product(self, product):
        """Select a product"""
        self._current_state.select_product(self, product)
    
    def dispense_product(self):
        """Dispense the selected product"""
        self._current_state.dispense_product(self)
    
    def return_change(self):
        """Return change and cancel transaction"""
        self._current_state.return_change(self)
    
    def display_products(self):
        """Display available products"""
        print("\n=== Available Products ===")
        for product in Product:
            print(f"{product.name}: {product.product_name} - ${product.price:.2f}")
        print()
    
    def display_status(self):
        """Display current machine status"""
        print(f"\n=== Vending Machine Status ===")
        print(f"State: {self.get_current_state()}")
        print(f"Balance: ${self.get_balance():.2f}")
        if self._selected_product:
            print(f"Selected: {self._selected_product.product_name}")
        print()


def demonstrate_vending_machine():
    """Demonstrate the State pattern with a vending machine"""
    print("=== State Pattern Example: Vending Machine ===\n")
    
    machine = VendingMachine()
    
    # Display available products
    machine.display_products()
    
    print("=== Scenario 1: Successful Purchase ===")
    machine.display_status()
    
    # Try to select product without coins (should fail)
    machine.select_product(Product.SODA)
    
    # Insert coins
    machine.insert_coin(1.00)
    machine.insert_coin(0.50)
    
    # Select product
    machine.select_product(Product.SODA)
    
    # Dispense product
    machine.dispense_product()
    machine.display_status()
    
    print("\n=== Scenario 2: Insufficient Funds ===")
    machine.insert_coin(0.50)
    machine.select_product(Product.SODA)  # Costs $1.50, only have $0.50
    
    # Add more money
    machine.insert_coin(1.00)
    machine.select_product(Product.SODA)  # Now we have enough
    machine.dispense_product()
    
    print("\n=== Scenario 3: Change Return ===")
    machine.insert_coin(2.00)
    machine.select_product(Product.CANDY)  # Costs $1.00
    machine.return_change()  # Cancel and get money back
    machine.display_status()
    
    print("\n=== Scenario 4: Out of Order ===")
    machine.insert_coin(1.50)
    machine.set_out_of_order()
    machine.insert_coin(0.50)  # Should fail
    machine.return_change()     # Should return existing money
    
    # Restore operation
    machine.set_operational()
    machine.display_status()


if __name__ == "__main__":
    demonstrate_vending_machine()