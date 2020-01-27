import streamlit as st
import HARK as hark

from HARK.ConsumptionSaving.ConsIndShockModel import PerfForesightConsumerType

st.header("Hello Hark!")

PF_dictionary = {
    'CRRA' : 2.5,
    'DiscFac' : 0.96,
    'Rfree' : 1.03,
    'LivPrb' : [0.98],
    'PermGroFac' : [1.01],
    'T_cycle' : 1,
    'cycles' : 0,
    'AgentCount' : 10000
}

PFexample = PerfForesightConsumerType(**PF_dictionary)

PFexample.solve()

# PFexample.solution[0].cFunc

humanWealth = PFexample.solution[0].hNrm
mMinimum = PFexample.solution[0].mNrmMin
st.write(f"This agent's human wealth is {PFexample.solution[0].hNrm:.02f} "
         f"times his current income level.")
st.write(f"This agent's consumption function is defined (consumption is "
         f"positive) down to m_t = {PFexample.solution[0].mNrmMin:.02f}")
