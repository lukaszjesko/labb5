from src.models import Apartment, Bill, Parameters, Tenant, Transfer, ApartmentSettlement

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

    def get_apartment_costs(self, apartment_key: str, year: int = None, month: int = None):
        if apartment_key not in self.apartments:
            return None
            
        if month is not None and (month < 1 or month > 12):
            raise ValueError("Nieprawidłowy miesiąc!")
            
        total_costs = 0.0
        
        for bill in self.bills:
            if bill.apartment == apartment_key:
                year_match = (year is None) or (bill.settlement_year == year)
                month_match = (month is None) or (bill.settlement_month == month)
                
                if year_match and month_match:
                    total_costs += bill.amount_pln
                    
        return total_costs

    def generate_apartment_settlement(self, apartment_key: str, year: int, month: int):
        costs = self.get_apartment_costs(apartment_key, year, month)
        
        if costs is None:
            return None
            
        balance = 0.0 - costs
        
        return ApartmentSettlement(
            apartment=apartment_key,
            year=year,
            month=month,
            balance=balance,
            total_rent_pln=0.0,    
            total_bills_pln=costs, 
            total_due_pln=costs
        )