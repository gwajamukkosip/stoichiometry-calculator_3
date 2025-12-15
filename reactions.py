# 📁 reactions.py

REACTION_DB = {
    "물 합성 (2H2 + O2 → 2H2O)": {
        "reactants": {"H2": 2, "O2": 1},
        "products": {"H2O": 2}
    },
    "암모니아 합성 (N2 + 3H2 → 2NH3)": {
        "reactants": {"N2": 1, "H2": 3},
        "products": {"NH3": 2}
    },
    "중화반응 (NaOH + HCl → NaCl + H2O)": {
        "reactants": {"NaOH": 1, "HCl": 1},
        "products": {"NaCl": 1, "H2O": 1}
    },
    "탄산칼슘 열분해 (CaCO3 → CaO + CO2)": {
        "reactants": {"CaCO3": 1},
        "products": {"CaO": 1, "CO2": 1}
    },
    "메탄 연소 (CH4 + 2O2 → CO2 + 2H2O)": {
        "reactants": {"CH4": 1, "O2": 2},
        "products": {"CO2": 1, "H2O": 2}
    },
    # 필요하면 여기에 계속 추가
}
