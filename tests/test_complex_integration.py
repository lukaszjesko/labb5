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


from src.models import Bill


def test_apartment_costs_with_optional_parameters():
    manager = Manager(Parameters())
    manager.bills.append(Bill(
        apartment='apart-polanka',
        date_due='2025-03-15',
        settlement_year=2025,
        settlement_month=2,
        amount_pln=1250.0,
        type='rent'
    ))

    manager.bills.append(Bill(
        apartment='apart-polanka',
        date_due='2024-03-15',
        settlement_year=2024,
        settlement_month=2,
        amount_pln=1150.0,
        type='rent'
    ))

    manager.bills.append(Bill(
        apartment='apart-polanka',
        date_due='2024-02-02',
        settlement_year=2024,
        settlement_month=1,
        amount_pln=222.0,
        type='electricity'
    ))

    costs = manager.get_apartment_costs('apartment-1', 2024, 1)
    assert costs is None

    costs = manager.get_apartment_costs('apart-polanka', 2024, 3)
    assert costs == 0.0

    costs = manager.get_apartment_costs('apart-polanka', 2024, 1)
    assert costs == 222.0

    costs = manager.get_apartment_costs('apart-polanka', 2025, 1)
    assert costs == 910.0
    
    costs = manager.get_apartment_costs('apart-polanka', 2024)
    assert costs == 1372.0

    costs = manager.get_apartment_costs('apart-polanka')
    assert costs == 3532.0
