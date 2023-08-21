import pandas as pd
import plotly.express as px

import dqfit as dq


def draw_population_path_dimensions(population_level: pd.DataFrame) -> px.scatter:
    all_dimension_keys = ["Conformant", "Complete", "Plausible", "Current","Longitudinal"]
    model_dimension_keys = [k for k in population_level.columns if k in all_dimension_keys]

    df = population_level.copy()
    df["resourceType"] = df["path"].apply(lambda x: x.split(".")[0])
    dft = df.melt(
        id_vars=["path", "weight", "resourceType", "n", "m"],
        var_name="Dimension",
        value_vars=model_dimension_keys,
        value_name="score",
    )
    dft["Dimension"] = pd.Categorical(
        dft["Dimension"], categories=model_dimension_keys, ordered=True
    )
    dft = dft.sort_values(["Dimension", "path"], ascending=True)
    return px.scatter(
        dft,
        x="score",
        y="path",
        facet_col="Dimension",
        color="resourceType",
        size="weight",
        hover_data=["n", "m"],
        size_max=10,
        title=f'{round(population_level["Score"].sum(), 1)} | n={int(population_level["n"].max())}',
        height=600,
    )


def draw_patient_level_distribution(patient_level: pd.DataFrame) -> px.histogram:
    pass
