from src.manager import Manager
from src.models import Parameters

def test_get_apartment_costs_logic():
    manager = Manager(parameters=Parameters())    
    valid_apartment = list(manager.apartments.keys())[0]    
    assert manager.get_apartment_costs('ZMYSLONE_MIESZKANIE_123', 2024, 3) is None    
    assert manager.get_apartment_costs(valid_apartment, 1999, 1) == 0.0
    if manager.bills:
        first_bill = manager.bills[0]
        test_apt = first_bill.apartment
        test_year = first_bill.settlement_year
        test_month = first_bill.settlement_month        
        expected_sum = sum(b.amount_pln for b in manager.bills 
                           if b.apartment == test_apt 
                           and b.settlement_year == test_year 
                           and b.settlement_month == test_month)
        
        assert manager.get_apartment_costs(test_apt, test_year, test_month) == expected_sum