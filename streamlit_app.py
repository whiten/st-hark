import streamlit as st
import HARK as hark

from HARK.ConsumptionSaving.ConsIndShockModel import PerfForesightConsumerType
from HARK.utilities import plotFuncs

st.header("Hello Hark!")

PF_dictionary = {
    "CRRA": 2.5, # st.slider("Risk aversion (CRRA)", 0.0, 10.0, 2.5),
    "DiscFac": .96, #st.slider("Discount factor", 0.0, 1.0, 0.96),
    "Rfree": 1.03,
    "Rfree": st.slider("Interest factor", 1.0, 1.5, 1.03),
    "LivPrb": [.98],
    "PermGroFac": [st.slider("Growth factor", 1.0, 1.2, 1.01)],
    "T_cycle": 1,
    "cycles": 0,
    "AgentCount": 10000,
}

PFexample = PerfForesightConsumerType(**PF_dictionary)

PFexample.solve()

# PFexample.solution[0].cFunc

#st.write("Plot funcs")
#plotFuncs(PFexample.solution[0].cFunc, 0.0, 10)
#st.write("Plotted funcs")

st.write(
    f"This agent's human wealth is {PFexample.solution[0].hNrm:.02f} times "
    f"his current income level."
)
st.write(
    f"This agent's consumption function is defined (consumption is positive) "
    f"down to m_t = {PFexample.solution[0].mNrmMin:.02f}"
)
