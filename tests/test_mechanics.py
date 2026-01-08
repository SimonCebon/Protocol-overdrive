import pytest

class MockPlayer:
    def __init__(self):
        self.charge = 0.0
        self.charge_cap = 8.0

    def add_charge(self, amount):
        self.charge += amount
        if self.charge > self.charge_cap:
            self.charge = self.charge_cap

def test_charge_accumulation():
    # Setup
    player = MockPlayer()
    
    # Action: Hit an enemy
    player.add_charge(0.2)
    
    # Assert: Check result
    assert player.charge == 0.2

def test_charge_cap():
    # Setup
    player = MockPlayer()
    player.charge = 7.9
    
    # Action: Hit an enemy (adds 0.2)
    player.add_charge(0.2)
    
    # Assert: Should not exceed 8.0
    assert player.charge == 8.0

def test_floating_point_precision():
    # Setup
    player = MockPlayer()
    
    # Action: Add 0.1 ten times
    for _ in range(10):
        player.add_charge(0.1)
        
    # Assert: Should be 1.0 (handling float errors effectively)
    # Note: simple addition might result in 0.99999999, so we use approx
    assert player.charge == pytest.approx(1.0)
