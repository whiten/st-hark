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
    plt.ylim([0, None])
    if legend_kwds is not None:
        plt.legend(**legend_kwds)
    return plt


st.header(
    "[Heterogenous Agent ToolKit](https://github.com/econ-ark/HARK) (HARK) "
    "Income Models"
)
st.markdown(
    "### Based on the [Gentle Intro To HARK]"
    "(https://github.com/econ-ark/DemARK/blob/master/notebooks/Gentle-Intro-To-HARK.py) example"
)


parameterSets = st.sidebar.slider("Number of models", 1, 5, 2)


baseParams = {
    "show": False,
    "shocks": False,
    "CRRA": 2.5,
    "DiscFac": 0.96,
    "Rfree": 1.03,
    "Rfree": 1.03,
    "LivPrb": [0.98],
    "PermGroFac": [1.01],
    "T_cycle": 1,
    "cycles": 0,
    "AgentCount": 10000,
    "PermShkStd": [0.1],
    "TranShkStd": [0.1],
}

paramList = []


@st.cache(allow_output_mutation=True)
def getParams(i):
    while i >= len(paramList):
        params = copy.deepcopy(baseParams)
        n = len(paramList)
        params["Rfree"] = 1.03 + n * 0.03
        params["PermGroFac"] = [1.01 + n * 0.03]
        paramList.append(params)
    return paramList[i]


examples = []
results = []
for i in range(parameterSets):
    params = getParams(i)
    st.sidebar.markdown(f"### Model {i + 1}:")
    shocks = False
    rfree = st.sidebar.empty()
    growth = st.sidebar.empty()
    shocks = st.sidebar.empty()
    permshk = st.sidebar.empty()
    transhk = st.sidebar.empty()

    if st.sidebar.button("Edit/Hide", key=f"show{i}"):
        params["show"] = not params["show"]

    if params["show"]:
        params["Rfree"] = rfree.slider(
            "Interest factor", 1.0, 1.5, params["Rfree"], key=f"rfree{i}"
        )
        params["PermGroFac"] = [
            growth.slider(
                "Growth factor",
                1.0,
                1.2,
                params["PermGroFac"][0],
                key=f"growth{i}",
            )
        ]
        params["shocks"] = shocks.checkbox(
            "Apply income shocks?", params["shocks"], key=f"shocks{i}"
        )
        if params["shocks"]:
            params["PermShkStd"] = [
                permshk.slider(
                    "Permanent Income Shock",
                    0.0,
                    0.5,
                    params["PermShkStd"][0],
                    key=f"PermShkStd{i}",
                )
            ]
            params["TranShkStd"] = [
                st.sidebar.slider(
                    "Transitory Income Shock",
                    0.0,
                    0.5,
                    params["TranShkStd"][0],
                    key=f"TranShkStd{i}",
                )
            ]
    else:
        text = (
            f"Interest factor: {params['Rfree']:.02f}  \n"
            f"Growth factor: {params['PermGroFac'][0]:.02f}  \n"
        )
        if params["shocks"]:
            text += (
                f"Permanent income shock: {params['PermShkStd'][0]:.02f}  \n"
                f"Transitory income shock: {params['TranShkStd'][0]:.02f}"
            )
        else:
            text += "No income shocks"
        rfree.markdown(text)

    if params["shocks"]:
        params = copy.deepcopy(params)
        params["PermShkCount"] = 7
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
        example = ConsIndShockModel.IndShockConsumerType(**params)
    else:
        params = copy.deepcopy(params)
        params.pop("PermShkStd", None)
        params.pop("TranShkStd", None)
        example = ConsIndShockModel.PerfForesightConsumerType(**params)
    examples.append(example)
    results.append(st.empty())

for i, example in enumerate(examples):
    example.solve()
    results[i].markdown(
        f"**Model {1+i}** agent's human wealth is {example.solution[0].hNrm:.02f} times "
        f"his current income level, with its consumption function is defined (consumption is "
        f"positive) down to m_t = {example.solution[0].mNrmMin:.02f}."
    )

st.pyplot(
    plotFuncs(
        [e.solution[0].cFunc for e in examples],
        0.0,
        10,
        legend_kwds={
            "labels": [f"Model {1 + i}" for i in range(len(examples))]
        },
    )
)
