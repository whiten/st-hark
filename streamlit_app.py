import copy
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st
import HARK as hark

from HARK.ConsumptionSaving.ConsIndShockModel import PerfForesightConsumerType
from HARK.utilities import plotFuncs


def plotFuncs(functions, bottom, top, N=1000, legend_kwds=None):
    if isinstance(functions, list):
        function_list = functions
    else:
        function_list = [functions]

    for function in function_list:
        x = np.linspace(bottom, top, N, endpoint=True)
        y = function(x)
        plt.plot(x, y)
    plt.xlim([bottom, top])
    if legend_kwds is not None:
        plt.legend(**legend_kwds)
    return plt


st.header("Hello Hark!")

parameterSets = st.slider("Parameter sets:", 1, 5)

baseParams = {
    "CRRA": 2.5,
    "DiscFac": 0.96,
    "Rfree": 1.03,
    "Rfree": 1.03,
    "LivPrb": [0.98],
    "PermGroFac": [1.01],
    "T_cycle": 1,
    "cycles": 0,
    "AgentCount": 10000,
}

paramsList = []
for i in range(parameterSets):
    st.markdown(f"#### Parameter Set {i + 1}:")
    params = copy.deepcopy(baseParams)
    params["Rfree"] = st.slider(
        "Interest factor", 1.0, 1.5, 1.03, key=f"rfree{i}")
    params["PermGroFac"] = [
        st.slider("Growth factor", 1.0, 1.2, 1.01, key=f"growth{i}")
    ]
    paramsList.append(params)

examples = []
for i, params in enumerate(paramsList):
    example = PerfForesightConsumerType(**params)
    example.solve()
    examples.append(example)
    st.markdown(f"#### Solution {i + 1}:")
    st.write(
        f"This agent's human wealth is {example.solution[0].hNrm:.02f} times "
        f"his current income level."
    )
    st.write(
        f"This agent's consumption function is defined (consumption is "
        f"positive) down to m_t = {example.solution[0].mNrmMin:.02f}"
    )

st.markdown("### Plot")
st.pyplot(plotFuncs([e.solution[0].cFunc for e in examples], 0.0, 10))
