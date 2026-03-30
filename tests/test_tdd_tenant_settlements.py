import pytest
from src.manager import Manager
from src.models import Parameters, ApartmentSettlement, TenantSettlement, Tenant

def test_generate_tenant_settlements():
    manager = Manager(parameters=Parameters())
    apt_settlement = ApartmentSettlement(
        apartment="test_apt", year=2024, month=3,
        total_rent_pln=0.0, total_bills_pln=1200.0, total_due_pln=1200.0
    )

    result_0 = manager.generate_tenant_settlements(apt_settlement)
    assert isinstance(result_0, list)
    assert len(result_0) == 0

    manager.tenants["t1"] = Tenant(
        name="Jan Kowalski", apartment="test_apt", room="room_1", 
        rent_pln=1000.0, deposit_pln=1000.0, 
        date_agreement_from="2024-01-01", date_agreement_to="2024-12-31"
    )
    result_1 = manager.generate_tenant_settlements(apt_settlement)
    assert len(result_1) == 1
    assert type(result_1[0]) is TenantSettlement

    manager.tenants["t2"] = Tenant(
        name="Anna Nowak", apartment="test_apt", room="room_2", 
        rent_pln=1000.0, deposit_pln=1000.0, 
        date_agreement_from="2024-01-01", date_agreement_to="2024-12-31"
    )
    result_2 = manager.generate_tenant_settlements(apt_settlement)
    assert len(result_2) == 2