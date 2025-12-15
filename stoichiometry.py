# 📁 stoichiometry.py
from chempy import balance_stoichiometry, Substance
from molecular_weight import MolecularWeightCalculator

class StoichiometryCalculator:
    """화학양론 계산기"""
    
    def __init__(self):
        self.mw_calc = MolecularWeightCalculator()
    
    def balance_equation(self, reactants: set, products: set) -> dict:
        """반응식 균형 맞추기"""
        try:
            reac, prod = balance_stoichiometry(reactants, products)
            return {
                "reactants": dict(reac),
                "products": dict(prod),
                "balanced": True
            }
        except Exception as e:
            return {"error": str(e), "balanced": False}
    
    def calculate_amounts(self, 
                          reactants: dict,    # {'H2': 2, 'O2': 1}
                          products: dict,     # {'H2O': 2}
                          given_compound: str,
                          given_mass: float) -> dict:
        """
        주어진 반응물 질량으로 다른 물질 양 계산
        
        예시:
        - reactants: {'H2': 2, 'O2': 1}
        - products: {'H2O': 2}
        - given_compound: 'H2'
        - given_mass: 10 (g)
        """
        
        results = {"input": {}, "required": {}, "produced": {}}
        
        # 주어진 물질의 분자량
        given_mw = self.mw_calc.get_molecular_weight(given_compound)["mw"]
        given_coef = reactants.get(given_compound, products.get(given_compound, 1))
        
        # 몰수 계산
        given_moles = given_mass / given_mw
        
        # 기준 몰비 (계수 1당 몰수)
        base_moles = given_moles / given_coef
        
        results["input"] = {
            "compound": given_compound,
            "mass_g": given_mass,
            "moles": round(given_moles, 4),
            "mw": given_mw
        }
        
        # 필요한 반응물 계산
        for compound, coef in reactants.items():
            if compound == given_compound:
                continue
            mw = self.mw_calc.get_molecular_weight(compound)["mw"]
            moles = base_moles * coef
            mass = moles * mw
            
            results["required"][compound] = {
                "coefficient": coef,
                "moles": round(moles, 4),
                "mass_g": round(mass, 4),
                "mw": mw
            }
        
        # 생성물 계산
        for compound, coef in products.items():
            mw = self.mw_calc.get_molecular_weight(compound)["mw"]
            moles = base_moles * coef
            mass = moles * mw
            
            results["produced"][compound] = {
                "coefficient": coef,
                "moles": round(moles, 4),
                "mass_g": round(mass, 4),
                "mw": mw
            }
        
        return results


# 테스트
if __name__ == "__main__":
    calc = StoichiometryCalculator()
    
    # 반응식: 2H2 + O2 -> 2H2O
    # H2 10g 넣으면?
    result = calc.calculate_amounts(
        reactants={'H2': 2, 'O2': 1},
        products={'H2O': 2},
        given_compound='H2',
        given_mass=10.0
    )
    
    print("=== 계산 결과 ===")
    print(f"입력: {result['input']}")
    print(f"필요한 반응물: {result['required']}")
    print(f"생성물: {result['produced']}")