from src.models import Apartment, Bill, Parameters, Tenant, Transfer, ApartmentSettlement, TenantSettlement

class Manager:
    def __init__(self, parameters: Parameters):
        self.parameters = parameters 

        self.apartments = {}
        self.tenants = {}
        self.transfers = []
        self.bills = []
       
        self.load_data()

    def load_data(self):
        self.apartments = Apartment.from_json_file(self.parameters.apartments_json_path)
        self.tenants = Tenant.from_json_file(self.parameters.tenants_json_path)
        self.transfers = Transfer.from_json_file(self.parameters.transfers_json_path)
        self.bills = Bill.from_json_file(self.parameters.bills_json_path)

    def check_tenants_apartment_keys(self) -> bool:
        for tenant in self.tenants.values():
            if tenant.apartment not in self.apartments:
                return False
        return True
    def generate_tenant_settlements(self, apt_settlement: ApartmentSettlement):
        apartment_tenants = [
            tenant for tenant in self.tenants.values() 
            if tenant.apartment == apt_settlement.apartment
        ]
        
        if not apartment_tenants:
            return []
            
        cost_per_tenant = apt_settlement.total_bills_pln / len(apartment_tenants)
        
        settlements = []
        
        for tenant in apartment_tenants:
            total_due = tenant.rent_pln + cost_per_tenant
            
            settlement = TenantSettlement(
                tenant=tenant.name,          
                apartment=apt_settlement.apartment,
                year=apt_settlement.year,
                month=apt_settlement.month,
                rent_pln=tenant.rent_pln,
                bills_pln=cost_per_tenant,
                total_due_pln=total_due,
                
                apartment_settlement=f"{apt_settlement.apartment}_{apt_settlement.year}_{apt_settlement.month}", 
                balance_pln=0.0 - total_due          
            )
            settlements.append(settlement)
            
        return settlements