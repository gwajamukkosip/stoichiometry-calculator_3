# 📁 app.py
import streamlit as st
from reactions import REACTION_DB
from stoichiometry import StoichiometryCalculator
from molecular_weight import MolecularWeightCalculator

st.set_page_config(
    page_title="🧪 화학양론 계산기",
    page_icon="🧪",
    layout="centered"
)

st.title("🧪 화학양론 계산기")
st.markdown("자주 사용하는 반응식을 선택하고, 기준 물질의 질량을 넣으면 나머지를 자동 계산합니다.")

calc = StoichiometryCalculator()

# --- 1. 반응식 선택 ---
st.header("1️⃣ 반응식 선택")

reaction_name = st.selectbox(
    "반응식을 선택하세요",
    options=list(REACTION_DB.keys())
)

selected_reaction = REACTION_DB[reaction_name]
reactants = selected_reaction["reactants"]
products = selected_reaction["products"]

# 반응식 문자열 표시
reac_str = " + ".join([f"{v}{k}" for k, v in reactants.items()])
prod_str = " + ".join([f"{v}{k}" for k, v in products.items()])
st.info(f"**반응식:** {reac_str} → {prod_str}")

# --- 2. 기준 물질 및 질량 입력 ---
st.header("2️⃣ 기준 물질 및 질량 입력")

basis_compound = st.selectbox(
    "기준 물질을 선택하세요",
    options=list(reactants.keys())
)

given_mass = st.number_input(
    f"{basis_compound}의 질량 (g)",
    min_value=0.0,
    value=10.0,
    step=0.1
)

if st.button("🧮 계산하기"):
    if given_mass <= 0:
        st.error("질량은 0보다 커야 합니다.")
    else:
        result = calc.calculate_amounts(
            reactants=reactants,
            products=products,
            given_compound=basis_compound,
            given_mass=given_mass
        )
        
        # --- 3. 결과 표시 ---
        st.header("3️⃣ 계산 결과")
        
        # 입력 정보
        st.subheader("📥 입력")
        inp = result["input"]
        st.info(
            f"**{inp['compound']}**: {inp['mass_g']} g\n\n"
            f"몰수: {inp['moles']} mol\n\n"
            f"분자량: {inp['mw']:.2f} g/mol"
        )
        
        # 필요한 다른 반응물
        if result["required"]:
            st.subheader("⚗️ 필요한 반응물")
            for compound, data in result["required"].items():
                st.warning(
                    f"**{compound}**\n"
                    f"- 계수: {data['coefficient']}\n"
                    f"- 몰수: {data['moles']} mol\n"
                    f"- 질량: {data['mass_g']} g\n"
                    f"- 분자량: {data['mw']:.2f} g/mol"
                )
        
        # 생성물
        st.subheader("✨ 생성물")
        for compound, data in result["produced"].items():
            st.success(
                f"**{compound}**\n"
                f"- 계수: {data['coefficient']}\n"
                f"- 몰수: {data['moles']} mol\n"
                f"- 질량: {data['mass_g']} g\n"
                f"- 분자량: {data['mw']:.2f} g/mol"
            )

# 사이드바: 분자량 조회
st.sidebar.header("🔍 분자량 조회")
compound_query = st.sidebar.text_input("화합물명 또는 화학식", value="NaCl")

if st.sidebar.button("조회"):
    mw_calc = MolecularWeightCalculator()
    result = mw_calc.get_molecular_weight(compound_query)
    
    if result["mw"]:
        st.sidebar.success(
            f"**{result['compound']}**\n\n"
            f"분자량: **{result['mw']:.2f}** g/mol\n\n"
            f"(출처: {result['source']})"
        )
    else:
        st.sidebar.error("분자량을 찾을 수 없습니다.")

st.markdown("---")
st.caption("Made with ❤️ using Streamlit, ChemPy, PubChemPy")