import pytest
from src.manager import Manager
from src.models import Parameters, ApartmentSettlement

def test_generate_apartment_settlement():
    manager = Manager(parameters=Parameters())
    valid_apartment = list(manager.apartments.keys())[0]

    first_bill = manager.bills[0]
    test_apt = first_bill.apartment
    test_year = first_bill.settlement_year
    test_month = first_bill.settlement_month

    settlement = manager.generate_apartment_settlement(test_apt, test_year, test_month)

    assert settlement is not None, "Rozliczenie nie powinno byc puste"
    assert type(settlement) is ApartmentSettlement, "Funkcja musi zwracac obiekt ApartmentSettlement"
    assert settlement.apartment == test_apt, "Zle przypisane ID mieszkania"
    assert settlement.year == test_year, "Zly rok rozliczenia"
    assert settlement.total_bills_pln > 0.0, "Suma rachunkow powinna byc wieksza od zera"

    settlement_empty = manager.generate_apartment_settlement(valid_apartment, 1999, 1)

    assert settlement_empty is not None, "Rozliczenie musi powstac"
    assert type(settlement_empty) is ApartmentSettlement, "To nadal musi byc obiekt"
    assert settlement_empty.apartment == valid_apartment, "Zle przypisane ID mieszkania"
    assert settlement_empty.year == 1999, "Zly rok rozliczenia"
    assert settlement_empty.total_due_pln == 0.0, "Brak kosztow = 0 do zaplaty"