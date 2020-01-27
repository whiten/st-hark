import copy
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st
import HARK as hark

from HARK.ConsumptionSaving import ConsIndShockModel
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

parameterSets = st.sidebar.slider("Parameter sets:", 1, 5, 2)

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

examples = []
for i in range(parameterSets):
    st.sidebar.markdown(f"#### Parameter Set {i + 1}:")
    params = copy.deepcopy(baseParams)
    params["Rfree"] = st.sidebar.slider(
        "Interest factor", 1.0, 1.5, 1.03 + i * 0.03, key=f"rfree{i}"
    )
    params["PermGroFac"] = [
        st.sidebar.slider(
            "Growth factor", 1.0, 1.2, 1.01 + i * 0.03, key=f"growth{i}"
        )
    ]
    shocks = st.sidebar.checkbox("Apply income shocks?", key=f"shocks{i}")
    if shocks:
        params["PermShkStd"] = [
            st.sidebar.slider(
                "Permanent Income Shock", 0.0, 0.5, 0.1, key=f"PermShkStd{i}"
            )
        ]
        params["PermShkCount"] = 7
        params["TranShkStd"] = [
            st.sidebar.slider(
                "Transitory Income Shock", 0.0, 0.5, 0.1, key=f"TranShkStd{i}"
            )
        ]
        params["TranShkCount"] = 7
        params["T_retire"] = 0
        params["UnempPrb"] = 0.05
        params["IncUnemp"] = 0.3
        params["UnempPrbRet"] = 0.0
        params["IncUnempRet"] = 0.0

        params.update(
            {
                "BoroCnstArt": 0.0,
                "vFuncBool": False,
                "CubicBool": False,
                "aXtraMin": 0.001,
                "aXtraMax": 50.0,
                "aXtraNestFac": 3,
                "aXtraCount": 48,
                "aXtraExtra": [None],
            }
        )
    if shocks:
        example = ConsIndShockModel.IndShockConsumerType(**params)
    else:
        example = ConsIndShockModel.PerfForesightConsumerType(**params)
    example.solve()
    examples.append(example)
    st.markdown(f"#### Solution {1 + i}")
    st.write(
        f"This agent's human wealth is {example.solution[0].hNrm:.02f} times "
        f"his current income level."
    )
    st.write(
        f"This agent's consumption function is defined (consumption is "
        f"positive) down to m_t = {example.solution[0].mNrmMin:.02f}"
    )

st.pyplot(plotFuncs([e.solution[0].cFunc for e in examples], 0.0, 10))
