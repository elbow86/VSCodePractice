"""
State Design Pattern Example - Simple Traffic Light
===============================================

A simplified traffic light example focusing on state transitions
without complex timing logic.
"""

from abc import ABC, abstractmethod


class TrafficLightState(ABC):
    """Abstract base class for traffic light states"""
    
    @abstractmethod
    def next_state(self, traffic_light):
        """Transition to the next state"""
        pass
    
    @abstractmethod
    def get_color(self):
        """Get the current light color"""
        pass
    
    @abstractmethod
    def can_cross(self):
        """Can pedestrians cross safely?"""
        pass
    
    @abstractmethod
    def get_action(self):
        """Get the action drivers should take"""
        pass


class RedLightState(TrafficLightState):
    def next_state(self, traffic_light):
        traffic_light.set_state(traffic_light.green_state)
    
    def get_color(self):
        return "RED"
    
    def can_cross(self):
        return True  # Pedestrians can cross when traffic light is red
    
    def get_action(self):
        return "STOP"


class YellowLightState(TrafficLightState):
    def next_state(self, traffic_light):
        traffic_light.set_state(traffic_light.red_state)
    
    def get_color(self):
        return "YELLOW"
    
    def can_cross(self):
        return False
    
    def get_action(self):
        return "CAUTION - PREPARE TO STOP"


class GreenLightState(TrafficLightState):
    def next_state(self, traffic_light):
        traffic_light.set_state(traffic_light.yellow_state)
    
    def get_color(self):
        return "GREEN"
    
    def can_cross(self):
        return False  # Pedestrians should not cross when cars have green
    
    def get_action(self):
        return "GO"


class SimpleTrafficLight:
    """Simplified traffic light context class"""
    
    def __init__(self):
        # Initialize all states
        self.red_state = RedLightState()
        self.yellow_state = YellowLightState()
        self.green_state = GreenLightState()
        
        # Start with red light
        self._current_state = self.red_state
    
    def set_state(self, state):
        """Change the current state"""
        self._current_state = state
    
    def next_light(self):
        """Advance to the next light in sequence"""
        self._current_state.next_state(self)
    
    def get_status(self):
        """Get current status information"""
        return {
            'color': self._current_state.get_color(),
            'action': self._current_state.get_action(),
            'pedestrians_can_cross': self._current_state.can_cross()
        }
    
    def display_status(self):
        """Display current status"""
        status = self.get_status()
        crossing = "YES" if status['pedestrians_can_cross'] else "NO"
        print(f"🚦 {status['color']} - {status['action']} | Pedestrians cross: {crossing}")


def demonstrate_simple_traffic_light():
    """Demonstrate the simplified traffic light"""
    print("=== Simple State Pattern: Traffic Light ===\n")
    
    light = SimpleTrafficLight()
    
    # Show several state transitions
    for i in range(8):  # Show two complete cycles
        print(f"Step {i + 1}:")
        light.display_status()
        light.next_light()
        print()
    
    print("Demonstration complete!")


if __name__ == "__main__":
    demonstrate_simple_traffic_light()