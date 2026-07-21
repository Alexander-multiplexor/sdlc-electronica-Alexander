from semana1.fsm_demo import TrafficLightFSM, TrafficLightState


def test_estado_inicial():
    """Test 1: Verifica que el estado inicial sea RED."""
    fsm = TrafficLightFSM()
    assert fsm.state == TrafficLightState.RED

def test_transicion_red_to_green():
    """Test 2: Verifica la transición directa de RED a GREEN."""
    fsm = TrafficLightFSM()
    fsm.transition()  # Primera transición: RED -> GREEN
    assert fsm.state == TrafficLightState.GREEN

def test_ciclo_completo_vuelve_a_red():
    """Test 3: Verifica que el ciclo completo avance por todos los estados y regrese a RED."""
    fsm = TrafficLightFSM()
    fsm.transition()  # RED -> GREEN
    fsm.transition()  # GREEN -> YELLOW
    fsm.transition()  # YELLOW -> RED
    assert fsm.state == TrafficLightState.RED

def test_conteo_de_ciclos():
    """Test 4: Verifica que el contador incremente solo al completar el ciclo de vuelta a RED."""
    fsm = TrafficLightFSM()
    
    # Vuelta 1
    fsm.transition()  # GREEN
    fsm.transition()  # YELLOW
    fsm.transition()  # RED (Aquí se cumple 1 ciclo)
    assert fsm.cycle_count == 1
    
    # Vuelta 2
    fsm.transition()  # GREEN
    fsm.transition()  # YELLOW
    fsm.transition()  # RED (Aquí se cumplen 2 ciclos)
    assert fsm.cycle_count == 2