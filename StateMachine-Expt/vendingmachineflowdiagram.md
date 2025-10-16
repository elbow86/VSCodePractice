# Vending Machine State Flow Diagram

This diagram shows the finite state machine for the vending machine implementation using the State design pattern.

```mermaid
stateDiagram-v2
    [*] --> Idle
    
    Idle --> CoinInserted: insert_coin(amount > 0)
    Idle --> OutOfOrder: set_out_of_order()
    
    CoinInserted --> CoinInserted: insert_coin(amount > 0)
    CoinInserted --> ProductSelected: select_product(balance >= price)
    CoinInserted --> Idle: return_change()
    CoinInserted --> OutOfOrder: set_out_of_order()
    
    ProductSelected --> ProductSelected: select_product(balance >= price)
    ProductSelected --> ProductSelected: insert_coin(amount > 0)
    ProductSelected --> Idle: dispense_product()
    ProductSelected --> Idle: return_change()
    ProductSelected --> OutOfOrder: set_out_of_order()
    
    OutOfOrder --> Idle: set_operational()
    OutOfOrder --> OutOfOrder: any_operation_rejected
    
    note right of Idle
        Machine waiting for coins
        Balance: $0.00
    end note
    
    note right of CoinInserted
        Coins inserted, awaiting
        product selection
    end note
    
    note right of ProductSelected
        Product chosen, ready
        to dispense or add more coins
    end note
    
    note right of OutOfOrder
        Machine maintenance mode
        Returns any inserted money
    end note
```

## State Descriptions

- **Idle**: Initial state, waiting for coins
- **CoinInserted**: Money inserted, waiting for product selection
- **ProductSelected**: Product chosen with sufficient funds, ready to dispense
- **OutOfOrder**: Maintenance mode, all operations rejected except money return

## Key Transitions

1. **insert_coin()** - Add money to machine balance
2. **select_product()** - Choose a product (requires sufficient balance)
3. **dispense_product()** - Complete transaction and return to idle
4. **return_change()** - Cancel transaction and refund money
5. **set_out_of_order()** - Enter maintenance mode
6. **set_operational()** - Return to normal 