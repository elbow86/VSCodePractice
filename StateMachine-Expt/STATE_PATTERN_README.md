# State Design Pattern Examples

This directory contains Python implementations of the **State Design Pattern**, which is one of the behavioral design patterns from the Gang of Four (GoF).

## What is the State Pattern?

The State pattern allows an object to alter its behavior when its internal state changes. It appears as if the object changed its class. This pattern is particularly useful for implementing finite state machines.

### Key Components:

1. **Context** - The class that maintains a reference to a state object
2. **State Interface** - Defines methods that all concrete states must implement
3. **Concrete States** - Classes that implement specific behaviors for each state
4. **State Transitions** - Logic for moving between different states

## Examples Included

### 1. Vending Machine (`state_pattern_example.py`)

A comprehensive example of a vending machine with the following states:
- **Idle State** - Waiting for coins
- **Coin Inserted State** - Has money, waiting for product selection
- **Product Selected State** - Ready to dispense product
- **Out of Order State** - Machine is not operational

**Features:**
- Multiple product types with different prices
- Money handling and change calculation
- Error handling for insufficient funds
- State transitions based on user actions

**Key Learning Points:**
- Complex state management
- Multiple possible transitions from each state
- Real-world business logic implementation

### 2. Traffic Light System (`traffic_light_state.py`)

A simpler example demonstrating a traffic light finite state machine:
- **Red Light** - Stop (3 seconds)
- **Green Light** - Go (4 seconds) 
- **Yellow Light** - Caution (1 second)

**Features:**
- Timer-based automatic state transitions
- Cyclic state progression
- Safety checks (can cross or not)

**Key Learning Points:**
- Automatic state transitions
- Time-based state management
- Simple finite state machine cycle

## Running the Examples

### Prerequisites
```bash
# Python 3.6 or higher required
python --version
```

### Run the Vending Machine Example
```bash
python state_pattern_example.py
```

### Run the Traffic Light Example
```bash
python traffic_light_state.py
```

## UI Visualizers (Tkinter)

This folder also includes optional Tkinter UI scripts that visualize the state machines without modifying the core examples.

### Run the Traffic Light Visualizer (step through states)

From the repo root:
```bash
python StateMachine-Expt/ui/traffic_light_visualizer.py
```

Or from inside the `StateMachine-Expt` folder:
```bash
python ui/traffic_light_visualizer.py
```

### Run the Vending Machine Visualizer

From the repo root:
```bash
python StateMachine-Expt/ui/vending_machine_visualizer.py
```

Or from inside the `StateMachine-Expt` folder:
```bash
python ui/vending_machine_visualizer.py
```

### Notes
- Tkinter typically ships with standard Python on Windows. If you see an import error for `tkinter`, your Python install may be missing Tcl/Tk.

## Benefits of the State Pattern

1. **Eliminates Complex Conditionals** - Replaces large if/else or switch statements with polymorphism
2. **Encapsulates State-Specific Behavior** - Each state class contains only the logic relevant to that state
3. **Makes State Transitions Explicit** - Clear, controlled transitions between states
4. **Follows Open/Closed Principle** - Easy to add new states without modifying existing code
5. **Single Responsibility** - Each state class has one reason to change

## When to Use the State Pattern

- When an object's behavior depends on its state and must change at runtime
- When you have complex conditional logic that depends on the object's state
- When implementing finite state machines
- When state-specific behavior is scattered across multiple methods

## Common Use Cases

- **UI Components** - Buttons (enabled/disabled), forms (valid/invalid)
- **Game Development** - Player states, AI behaviors, game phases
- **Network Protocols** - Connection states, authentication states
- **Document Processing** - Document status workflows
- **Media Players** - Playing, paused, stopped, buffering states

## Design Pattern Structure

```
Context (VendingMachine/TrafficLight)
├── Maintains reference to current state
├── Delegates behavior to current state
└── Provides interface for state transitions

State Interface (VendingMachineState/TrafficLightState)
├── Defines common interface for all states
└── Abstract methods for state-specific behavior

Concrete States (IdleState, RedLightState, etc.)
├── Implement state-specific behavior
├── Handle transitions to other states
└── Encapsulate state-related logic
```

## Advanced Features Demonstrated

### Vending Machine
- **Error Handling** - Invalid operations in wrong states
- **Data Management** - Balance tracking, product selection
- **Complex Transitions** - Multiple paths between states
- **User Feedback** - Clear messages for each action

### Traffic Light
- **Timer-Based Transitions** - Automatic state changes
- **Cyclic Behavior** - Continuous loop through states
- **Safety Logic** - Pedestrian crossing permissions

## Extending the Examples

### Add New States
1. Create a new class inheriting from the State interface
2. Implement all required methods
3. Add the state instance to the Context class
4. Update transition logic in relevant states

### Add New Functionality
1. Add new methods to the State interface
2. Implement the methods in all concrete states
3. Update the Context class to delegate new behavior

## Related Patterns

- **Strategy Pattern** - Similar structure but different intent (algorithm vs state)
- **Command Pattern** - Can be used to trigger state transitions
- **Observer Pattern** - Notify when state changes occur