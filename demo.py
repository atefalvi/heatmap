import pandas as pd
from heatmap import rounded_heatmap

df = pd.read_csv("data/example.csv", index_col=0)

fig, ax = rounded_heatmap(
    df.values,
    row_labels=df.index.tolist(),
    col_labels=df.columns.tolist(),
    col_label_rotation=45,
    col_label_xshift=0,
    col_label_yshift=0,
    show_values=True,
    value_fmt="{:.1f}",
    value_fontsize=12,
    text_color_dark="#F5F5F5",
    text_color_light="#515151",
    show_legend=False
)


fig.savefig("images/heatmap.png", bbox_inches="tight")

