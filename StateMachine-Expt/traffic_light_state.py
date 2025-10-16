"""
State Design Pattern Example - Traffic Light System
================================================

A simpler example of the State pattern using a traffic light system.
This demonstrates a basic finite state machine with automatic transitions.
"""

from abc import ABC, abstractmethod
import time
from enum import Enum


class TrafficLightState(ABC):
    """Abstract base class for traffic light states"""
    
    @abstractmethod
    def handle_timer(self, traffic_light):
        """Handle timer expiration"""
        pass
    
    @abstractmethod
    def get_color(self):
        """Get the current light color"""
        pass
    
    @abstractmethod
    def get_duration(self):
        """Get how long this state should last (in seconds)"""
        pass
    
    @abstractmethod
    def can_cross(self):
        """Can pedestrians/cars cross?"""
        pass


class RedLightState(TrafficLightState):
    """Red light state - stop"""
    
    def handle_timer(self, traffic_light):
        print("Red light timer expired. Switching to Green.")
        traffic_light.set_state(traffic_light.green_state)
    
    def get_color(self):
        return "RED"
    
    def get_duration(self):
        return 3  # Red light lasts 3 seconds in this example
    
    def can_cross(self):
        return False


class YellowLightState(TrafficLightState):
    """Yellow light state - caution"""
    
    def handle_timer(self, traffic_light):
        print("Yellow light timer expired. Switching to Red.")
        traffic_light.set_state(traffic_light.red_state)
    
    def get_color(self):
        return "YELLOW"
    
    def get_duration(self):
        return 1  # Yellow light lasts 1 second
    
    def can_cross(self):
        return False  # Should not cross on yellow


class GreenLightState(TrafficLightState):
    """Green light state - go"""
    
    def handle_timer(self, traffic_light):
        print("Green light timer expired. Switching to Yellow.")
        traffic_light.set_state(traffic_light.yellow_state)
    
    def get_color(self):
        return "GREEN"
    
    def get_duration(self):
        return 4  # Green light lasts 4 seconds
    
    def can_cross(self):
        return True


class TrafficLight:
    """
    Context class representing a traffic light system.
    Uses the State pattern to manage different light states.
    """
    
    def __init__(self):
        # Initialize all possible states
        self.red_state = RedLightState()
        self.yellow_state = YellowLightState()
        self.green_state = GreenLightState()
        
        # Start with red light
        self._current_state = self.red_state
        self._timer_start = time.time()
    
    def set_state(self, state):
        """Change the current state"""
        self._current_state = state
        self._timer_start = time.time()  # Reset timer
        self.display_status()
    
    def get_current_color(self):
        """Get the current light color"""
        return self._current_state.get_color()
    
    def can_cross(self):
        """Check if it's safe to cross"""
        return self._current_state.can_cross()
    
    def check_timer(self):
        """Check if the timer has expired and handle state transition"""
        elapsed = time.time() - self._timer_start
        if elapsed >= self._current_state.get_duration():
            self._current_state.handle_timer(self)
    
    def display_status(self):
        """Display current traffic light status"""
        color = self.get_current_color()
        crossing = "SAFE TO CROSS" if self.can_cross() else "DO NOT CROSS"
        print(f"🚦 Traffic Light: {color} - {crossing}")
    
    def run_cycle(self, num_cycles=3):
        """Run the traffic light for a specified number of complete cycles"""
        print(f"Starting traffic light simulation for {num_cycles} cycles...\n")
        
        cycle_count = 0
        state_changes = 0
        
        self.display_status()
        
        while cycle_count < num_cycles:
            self.check_timer()
            
            # Count state changes to determine cycles
            # One cycle = Red -> Green -> Yellow -> Red
            if self.get_current_color() == "RED" and state_changes > 0 and state_changes % 3 == 0:
                cycle_count += 1
                print(f"\n--- Completed cycle {cycle_count} ---\n")
                if cycle_count >= num_cycles:
                    break
            
            # Track state changes
            current_time = time.time()
            if current_time - self._timer_start >= self._current_state.get_duration():
                state_changes += 1
            
            time.sleep(0.1)  # Small delay for simulation
        
        print("Traffic light simulation completed.")


def demonstrate_traffic_light():
    """Demonstrate the State pattern with a traffic light"""
    print("=== State Pattern Example: Traffic Light System ===\n")
    
    traffic_light = TrafficLight()
    
    # Manual state checking
    print("=== Manual State Demonstration ===")
    print(f"Initial state: {traffic_light.get_current_color()}")
    print(f"Can cross: {traffic_light.can_cross()}")
    
    # Simulate some time passing
    print("\nSimulating timer expiration...")
    traffic_light._current_state.handle_timer(traffic_light)
    
    print(f"New state: {traffic_light.get_current_color()}")
    print(f"Can cross: {traffic_light.can_cross()}")
    
    # Another transition
    print("\nAnother timer expiration...")
    traffic_light._current_state.handle_timer(traffic_light)
    
    print(f"New state: {traffic_light.get_current_color()}")
    print(f"Can cross: {traffic_light.can_cross()}")
    
    print("\n" + "="*50 + "\n")
    
    # Automated cycle demonstration
    print("=== Automated Cycle Demonstration ===")
    new_light = TrafficLight()
    new_light.run_cycle(2)  # Run for 2 complete cycles


if __name__ == "__main__":
    demonstrate_traffic_light()