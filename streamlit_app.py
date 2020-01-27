import streamlit as st
import HARK as hark

from HARK.ConsumptionSaving.ConsIndShockModel import PerfForesightConsumerType

st.header("Hello Hark!")

PF_dictionary = {
    "CRRA": st.slider("Risk aversion (CRRA)", 0.0, 10.0, 2.5),
    "DiscFac": st.slider("Discount factor", 0.0, 1.0, 0.96),
    "Rfree": 1.03,
    "LivPrb": [st.slider("Survival probability", 0.0, 1.0, 0.98)],
    "PermGroFac": [1 + st.slider("Growth factor", 0.0, 0.2, 0.01)],
    "T_cycle": 1,
    "cycles": 0,
    "AgentCount": 10000,
}

PFexample = PerfForesightConsumerType(**PF_dictionary)

PFexample.solve()

# PFexample.solution[0].cFunc

st.write(
    f"This agent's human wealth is {PFexample.solution[0].hNrm:.02f} times "
    f"his current income level."
)
st.write(
    f"This agent's consumption function is defined (consumption is positive) "
    f"down to m_t = {PFexample.solution[0].mNrmMin:.02f}"
)
