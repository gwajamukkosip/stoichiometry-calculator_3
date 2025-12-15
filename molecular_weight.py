# 📁 molecular_weight.py
import pubchempy as pcp
import re

class MolecularWeightCalculator:
    """분자량 계산기 - PubChem DB 연동"""
    
    # 기본 원자량 (오프라인 백업용)
    ATOMIC_WEIGHTS = {
        'H': 1.008, 'He': 4.003, 'Li': 6.941, 'Be': 9.012,
        'B': 10.81, 'C': 12.01, 'N': 14.01, 'O': 16.00,
        'F': 19.00, 'Ne': 20.18, 'Na': 22.99, 'Mg': 24.31,
        'Al': 26.98, 'Si': 28.09, 'P': 30.97, 'S': 32.07,
        'Cl': 35.45, 'Ar': 39.95, 'K': 39.10, 'Ca': 40.08,
        'Fe': 55.85, 'Cu': 63.55, 'Zn': 65.38, 'Br': 79.90,
        'Ag': 107.87, 'I': 126.90, 'Au': 196.97
    }
    
    def get_from_pubchem(self, compound_name: str) -> float:
        """PubChem에서 분자량 조회"""
        try:
            results = pcp.get_compounds(compound_name, 'name')
            if results:
                return float(results[0].molecular_weight)
        except:
            pass
        return None
    
    def parse_formula(self, formula: str) -> float:
        """화학식 파싱하여 분자량 계산"""
        # 예: H2O -> {'H': 2, 'O': 1}
        pattern = r'([A-Z][a-z]?)(\d*)'
        matches = re.findall(pattern, formula)
        
        total_weight = 0.0
        for element, count in matches:
            if element:
                count = int(count) if count else 1
                weight = self.ATOMIC_WEIGHTS.get(element, 0)
                total_weight += weight * count
        
        return total_weight
    
    def get_molecular_weight(self, compound: str) -> dict:
        """분자량 반환 (PubChem 우선, 실패시 로컬 계산)"""
        
        # 1. PubChem 조회 시도
        mw = self.get_from_pubchem(compound)
        if mw:
            return {"compound": compound, "mw": mw, "source": "PubChem"}
        
        # 2. 화학식으로 직접 계산
        mw = self.parse_formula(compound)
        if mw > 0:
            return {"compound": compound, "mw": mw, "source": "계산"}
        
        return {"compound": compound, "mw": None, "source": "실패"}


# 테스트
if __name__ == "__main__":
    calc = MolecularWeightCalculator()
    
    print(calc.get_molecular_weight("water"))      # PubChem
    print(calc.get_molecular_weight("H2O"))        # 로컬 계산
    print(calc.get_molecular_weight("NaCl"))       # 로컬 계산
    print(calc.get_molecular_weight("glucose"))    # PubChem
