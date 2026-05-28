#!/usr/bin/env python3
"""Generate mathematical/scientific diagrams for Obsidian notes.

Usage:
    python generate_diagram.py --type <type> --output <path> [options]

Examples:
    python generate_diagram.py --type sigmoid --output sigmoid.png
    python generate_diagram.py --type function --output plot.png --expr "np.sin(x) * np.exp(-x/5)" --xrange -10 10
    python generate_diagram.py --type scatter --output scatter.png --x "1,2,3,4,5" --y "2,4,1,5,3"
"""

import argparse
import os
import sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator


def setup_style(dark_mode=False, style="seaborn-v0_8-whitegrid"):
    """Apply matplotlib style."""
    try:
        plt.style.use(style)
    except OSError:
        plt.style.use("default")
    if dark_mode:
        plt.rcParams.update({
            "figure.facecolor": "#1e1e1e",
            "axes.facecolor": "#2d2d2d",
            "axes.edgecolor": "#cccccc",
            "axes.labelcolor": "#cccccc",
            "text.color": "#cccccc",
            "xtick.color": "#cccccc",
            "ytick.color": "#cccccc",
            "grid.color": "#444444",
        })


def plot_sigmoid(output, dark_mode=False, title="Sigmoid Function", xlabel="x", ylabel="σ(x)", xrange=(-6, 6), dpi=150):
    """Plot sigmoid function: σ(x) = 1 / (1 + e^-x)"""
    setup_style(dark_mode)
    fig, ax = plt.subplots(figsize=(8, 5))

    x = np.linspace(xrange[0], xrange[1], 500)
    y = 1 / (1 + np.exp(-x))

    ax.plot(x, y, linewidth=2.5, color="#4C72B0")
    ax.axhline(y=0.5, color="#888888", linestyle="--", linewidth=1, alpha=0.7)
    ax.axvline(x=0, color="#888888", linestyle="--", linewidth=1, alpha=0.7)
    ax.set_title(title, fontsize=14, fontweight="bold")
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_ylim(-0.1, 1.1)
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(output, dpi=dpi, bbox_inches="tight")
    plt.close()
    print(f"Saved: {output}")


def plot_tanh(output, dark_mode=False, title="Tanh Function", xlabel="x", ylabel="tanh(x)", xrange=(-6, 6), dpi=150):
    """Plot tanh function."""
    setup_style(dark_mode)
    fig, ax = plt.subplots(figsize=(8, 5))

    x = np.linspace(xrange[0], xrange[1], 500)
    y = np.tanh(x)

    ax.plot(x, y, linewidth=2.5, color="#DD8452")
    ax.axhline(y=0, color="#888888", linestyle="--", linewidth=1, alpha=0.7)
    ax.axvline(x=0, color="#888888", linestyle="--", linewidth=1, alpha=0.7)
    ax.set_title(title, fontsize=14, fontweight="bold")
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_ylim(-1.2, 1.2)
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(output, dpi=dpi, bbox_inches="tight")
    plt.close()
    print(f"Saved: {output}")


def plot_relu(output, dark_mode=False, title="ReLU Function", xlabel="x", ylabel="ReLU(x)", xrange=(-3, 3), dpi=150):
    """Plot ReLU activation function."""
    setup_style(dark_mode)
    fig, ax = plt.subplots(figsize=(8, 5))

    x = np.linspace(xrange[0], xrange[1], 500)
    y = np.maximum(0, x)

    ax.plot(x, y, linewidth=2.5, color="#55A868")
    ax.axhline(y=0, color="#888888", linestyle="--", linewidth=1, alpha=0.7)
    ax.axvline(x=0, color="#888888", linestyle="--", linewidth=1, alpha=0.7)
    ax.set_title(title, fontsize=14, fontweight="bold")
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(output, dpi=dpi, bbox_inches="tight")
    plt.close()
    print(f"Saved: {output}")


def plot_function(output, expr, dark_mode=False, title="Function Plot", xlabel="x", ylabel="y", xrange=(-10, 10), npoints=500, dpi=150):
    """Plot an arbitrary numpy expression."""
    setup_style(dark_mode)
    fig, ax = plt.subplots(figsize=(8, 5))

    x = np.linspace(xrange[0], xrange[1], npoints)
    y = eval(expr, {"np": np, "x": x, "sin": np.sin, "cos": np.cos, "tan": np.tan,
                     "exp": np.exp, "log": np.log, "sqrt": np.sqrt, "abs": np.abs,
                     "pi": np.pi, "e": np.e})

    ax.plot(x, y, linewidth=2.5, color="#4C72B0")
    ax.axhline(y=0, color="#888888", linestyle="--", linewidth=1, alpha=0.5)
    ax.axvline(x=0, color="#888888", linestyle="--", linewidth=1, alpha=0.5)
    ax.set_title(title, fontsize=14, fontweight="bold")
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(output, dpi=dpi, bbox_inches="tight")
    plt.close()
    print(f"Saved: {output}")


def plot_scatter(output, x_vals, y_vals, dark_mode=False, title="Scatter Plot", xlabel="x", ylabel="y", color="#4C72B0", dpi=150):
    """Plot scatter data."""
    setup_style(dark_mode)
    fig, ax = plt.subplots(figsize=(8, 5))

    ax.scatter(x_vals, y_vals, c=color, s=60, alpha=0.8, edgecolors="white", linewidth=0.5)
    ax.set_title(title, fontsize=14, fontweight="bold")
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(output, dpi=dpi, bbox_inches="tight")
    plt.close()
    print(f"Saved: {output}")


def plot_bar(output, labels, values, dark_mode=False, title="Bar Chart", xlabel="Category", ylabel="Value", color="#4C72B0", dpi=150):
    """Plot bar chart."""
    setup_style(dark_mode)
    fig, ax = plt.subplots(figsize=(8, 5))

    ax.bar(labels, values, color=color, edgecolor="white", linewidth=0.5)
    ax.set_title(title, fontsize=14, fontweight="bold")
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.grid(True, alpha=0.3, axis="y")

    plt.tight_layout()
    plt.savefig(output, dpi=dpi, bbox_inches="tight")
    plt.close()
    print(f"Saved: {output}")


def plot_heatmap(output, matrix, dark_mode=False, title="Heatmap", xlabel="X", ylabel="Y", cmap="viridis", dpi=150):
    """Plot heatmap from 2D matrix."""
    setup_style(dark_mode)
    fig, ax = plt.subplots(figsize=(8, 6))

    im = ax.imshow(matrix, cmap=cmap, aspect="auto")
    ax.set_title(title, fontsize=14, fontweight="bold")
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    fig.colorbar(im, ax=ax)

    plt.tight_layout()
    plt.savefig(output, dpi=dpi, bbox_inches="tight")
    plt.close()
    print(f"Saved: {output}")


def parse_list(s):
    """Parse comma-separated string to list of floats."""
    return [float(v.strip()) for v in s.split(",")]


def main():
    parser = argparse.ArgumentParser(description="Generate diagrams for Obsidian notes")
    parser.add_argument("--type", required=True, choices=["sigmoid", "tanh", "relu", "function", "scatter", "bar", "heatmap"],
                        help="Diagram type")
    parser.add_argument("--output", required=True, help="Output image path (png, pdf, svg)")
    parser.add_argument("--dark", action="store_true", help="Dark mode styling")
    parser.add_argument("--title", default=None, help="Plot title")
    parser.add_argument("--xlabel", default="x", help="X-axis label")
    parser.add_argument("--ylabel", default="y", help="Y-axis label")
    parser.add_argument("--xrange", type=float, nargs=2, default=None, help="X range: --xrange -6 6")
    parser.add_argument("--dpi", type=int, default=150, help="Output DPI")
    parser.add_argument("--expr", help="Expression for function type (use np, x, sin, cos, exp, etc.)")
    parser.add_argument("--x", help="Comma-separated x values (scatter/bar)")
    parser.add_argument("--y", help="Comma-separated y values (scatter/bar)")
    parser.add_argument("--labels", help="Comma-separated labels (bar chart)")
    parser.add_argument("--matrix", help="2D matrix as semicolon-separated rows, comma-separated values: '1,2;3,4'")
    parser.add_argument("--cmap", default="viridis", help="Colormap for heatmap")

    args = parser.parse_args()

    defaults = {
        "sigmoid": {"title": "Sigmoid Function", "ylabel": "σ(x)", "xrange": (-6, 6)},
        "tanh": {"title": "Tanh Function", "ylabel": "tanh(x)", "xrange": (-6, 6)},
        "relu": {"title": "ReLU Function", "ylabel": "ReLU(x)", "xrange": (-3, 3)},
    }

    title = args.title or defaults.get(args.type, {}).get("title", "Plot")
    ylabel = args.ylabel or defaults.get(args.type, {}).get("ylabel", "y")
    xrange = args.xrange or defaults.get(args.type, {}).get("xrange", (-10, 10))

    if args.type == "sigmoid":
        plot_sigmoid(args.output, args.dark, title, args.xlabel, ylabel, xrange, args.dpi)
    elif args.type == "tanh":
        plot_tanh(args.output, args.dark, title, args.xlabel, ylabel, xrange, args.dpi)
    elif args.type == "relu":
        plot_relu(args.output, args.dark, title, args.xlabel, ylabel, xrange, args.dpi)
    elif args.type == "function":
        if not args.expr:
            parser.error("--expr required for function type")
        plot_function(args.output, args.expr, args.dark, title, args.xlabel, ylabel, xrange, dpi=args.dpi)
    elif args.type == "scatter":
        if not args.x or not args.y:
            parser.error("--x and --y required for scatter type")
        plot_scatter(args.output, parse_list(args.x), parse_list(args.y), args.dark, title, args.xlabel, ylabel, dpi=args.dpi)
    elif args.type == "bar":
        if not args.y:
            parser.error("--y required for bar type")
        y_vals = parse_list(args.y)
        labels = args.labels.split(",") if args.labels else [str(i+1) for i in range(len(y_vals))]
        plot_bar(args.output, labels, y_vals, args.dark, title, args.xlabel, ylabel, dpi=args.dpi)
    elif args.type == "heatmap":
        if not args.matrix:
            parser.error("--matrix required for heatmap type")
        rows = args.matrix.split(";")
        matrix = [[float(v) for v in row.split(",")] for row in rows]
        plot_heatmap(args.output, matrix, args.dark, title, args.xlabel, ylabel, args.cmap, args.dpi)


if __name__ == "__main__":
    main()
