from enum import Enum, auto


class TrafficLightState(Enum):
    RED = auto()
    YELLOW = auto()
    GREEN = auto()

class TrafficLightFSM:
    """El estado vive dentro del objeto, no en una variable global."""
    
    def __init__(self) -> None:
        self._state: TrafficLightState = TrafficLightState.RED
        self._cycle_count: int = 0

    @property
    def state(self) -> TrafficLightState:
        """Expone el estado actual de forma segura (solo lectura)."""
        return self._state

    @property
    def cycle_count(self) -> int:
        """Expone el conteo de ciclos completos."""
        return self._cycle_count

    def transition(self) -> TrafficLightState:
        """Maneja las transiciones de estado y cuenta los ciclos completos."""
        transitions = {
            TrafficLightState.RED: TrafficLightState.GREEN,
            TrafficLightState.GREEN: TrafficLightState.YELLOW,
            TrafficLightState.YELLOW: TrafficLightState.RED,
        }
        
        self._state = transitions[self._state]
        
        # Cada vez que el ciclo regresa a ROJO, se considera un ciclo completo
        if self._state == TrafficLightState.RED:
            self._cycle_count += 1
            
        return self._state

if __name__ == "__main__":
    # Esto es solo para simulación local, la lógica no depende de time.sleep
    import time
    
    semaforo = TrafficLightFSM()
    print(f"Estado inicial: {semaforo.state}")
    
    try:
        while True:
            time.sleep(1)  # El retraso ocurre en el ciclo de ejecución, no en la FSM
            nuevo_estado = semaforo.transition()
            print(f"Transición a: {nuevo_estado} | Ciclos completos: {semaforo.cycle_count}")
    except KeyboardInterrupt:
        print("\nSimulación detenida.")