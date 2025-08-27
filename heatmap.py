# pip install matplotlib numpy pandas
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from matplotlib.colors import Normalize, LinearSegmentedColormap

def make_cmap(hex_list, reverse=False):
    colors = list(hex_list)[::-1] if reverse else list(hex_list)
    return LinearSegmentedColormap.from_list("custom_hexmap", colors, N=256)

def rounded_heatmap(
    data: np.ndarray,
    row_labels=None,                # pass None/[]/False to hide row labels
    col_labels=None,                # pass None/[]/False to hide column labels
    *,
    palette_hex=("#D62828","#F06A6A","#F39C12","#F6D65A","#B9E36A","#2ECC71"),
    reverse_palette=False,
    vmin=None, vmax=None,
    cell_size=1.2, corner=0.28, gap=0.14,
    show_legend=False, legend_labels=("Excellent","Good","Average"),
    legend_bbox=(0.18,0.09,0.64,0.06), legend_radius=0.22,
    figsize=None,
    row_label_rotation=0,
    col_label_rotation=0,
    col_label_xshift=0,
    col_label_yshift=0,
    show_values=True, value_fmt="{:.1f}", value_fontsize=11,
    text_color_dark=None,
    text_color_light=None
):
    def _relative_luminance(rgb):
        r, g, b = rgb[:3]
        return 0.2126*r + 0.7152*g + 0.0722*b

    data = np.asarray(data, dtype=float)
    n_rows, n_cols = data.shape
    if figsize is None:
        figsize = (max(6, 0.6*n_cols + 3), max(4, 0.6*n_rows + 1.5))

    vmin = np.nanmin(data) if vmin is None else vmin
    vmax = np.nanmax(data) if vmax is None else vmax
    cmap = make_cmap(palette_hex, reverse=reverse_palette)
    norm = Normalize(vmin=vmin, vmax=vmax)

    fig, ax = plt.subplots(figsize=figsize)
    ax.set_xlim(-1.2*cell_size, n_cols*cell_size)
    ax.set_ylim(0, n_rows*cell_size)
    ax.invert_yaxis()
    ax.set_aspect("equal")
    ax.axis("off")

    pad = gap/2.0
    w = h = cell_size - gap
    rounding = cell_size * corner

    for r in range(n_rows):
        for c in range(n_cols):
            x = c*cell_size + pad
            y = r*cell_size + pad
            val = data[r, c]
            face = (0,0,0,0) if np.isnan(val) else cmap(norm(val))
            ax.add_patch(FancyBboxPatch(
                (x, y), w, h,
                boxstyle=f"round,pad=0,rounding_size={rounding}",
                linewidth=0, facecolor=face
            ))
            if show_values and not np.isnan(val):
                lum = _relative_luminance(face)
                if text_color_dark and lum < 0.6:
                    tc = text_color_dark
                elif text_color_light and lum >= 0.6:
                    tc = text_color_light
                else:
                    tc = "#111111" if lum >= 0.6 else "#FFFFFF"
                ax.text(x + w/2, y + h/2, value_fmt.format(val),
                        ha="center", va="center",
                        fontsize=value_fontsize, color=tc)

    if row_labels:
        for r, lab in enumerate(row_labels):
            y = r*cell_size + cell_size/2
            ax.text(-0.35*cell_size, y, str(lab), va="center", ha="right",
                    fontsize=12, color="#6B7280", rotation=row_label_rotation)

    if col_labels:
        for c, lab in enumerate(col_labels):
            x = c*cell_size + cell_size/2 + col_label_xshift*cell_size  
            y = col_label_yshift*cell_size                                      
            ax.text(
                x, y, str(lab),
                ha="center" if col_label_rotation == 0 else "left", 
                va="bottom",
                rotation=col_label_rotation,
                rotation_mode="anchor",
                fontsize=11, color="#6B7280"
            )

    if show_legend:
        lax = fig.add_axes([*legend_bbox]); lax.set_axis_off()
        grad = np.linspace(vmin, vmax, 400)[None, :]
        im = lax.imshow(grad, aspect="auto", origin="lower",
                        extent=[0,1,0,1], cmap=cmap)
        clip = FancyBboxPatch((0,0), 1,1,
                              boxstyle=f"round,pad=0,rounding_size={legend_radius}",
                              transform=lax.transAxes, facecolor="none", edgecolor="none")
        lax.add_patch(clip); im.set_clip_path(clip)
        lax.text(0.00, -0.90, legend_labels[0], ha="left",  va="top", fontsize=12, color="#6B7280", transform=lax.transAxes)
        lax.text(0.50, -0.90, legend_labels[1], ha="center",va="top", fontsize=12, color="#6B7280", transform=lax.transAxes)
        lax.text(1.00, -0.90, legend_labels[2], ha="right", va="top", fontsize=12, color="#6B7280", transform=lax.transAxes)

    plt.tight_layout(rect=[0.02, (legend_bbox[1]+legend_bbox[3]+0.02) if show_legend else 0.02, 0.98, 1.0])
    return fig, ax
