# Python-Generated Diagrams

When Obsidian plugins (Mermaid, Charts) cannot accurately render mathematical functions, scientific plots, or complex visualizations, use Python with matplotlib to generate high-quality images and embed them in notes.

## When to Use

| Scenario | Recommended Approach |
|----------|---------------------|
| Simple flowcharts, sequences | Mermaid (core plugin) |
| Basic bar/line/pie charts | Charts plugin |
| **Mathematical functions** (sigmoid, tanh, custom) | **Python + matplotlib** |
| **Scientific plots** (heatmaps, 3D surfaces) | **Python + matplotlib** |
| **Statistical visualizations** (distributions, histograms) | **Python + matplotlib** |
| **Precise data plots** from CSV/data | **Python + matplotlib** |

## Prerequisites

```bash
pip install matplotlib numpy
```

## Quick Start

### Activation Functions

```bash
# Sigmoid function
python scripts/generate_diagram.py --type sigmoid --output assets/sigmoid.png

# Tanh function
python scripts/generate_diagram.py --type tanh --output assets/tanh.png

# ReLU function
python scripts/generate_diagram.py --type relu --output assets/relu.png
```

### Custom Mathematical Functions

```bash
# Any numpy expression
python scripts/generate_diagram.py --type function --output assets/sin_decay.png \
  --expr "np.sin(x) * np.exp(-x/5)" --xrange -10 10 \
  --title "Damped Sine Wave"

# Gaussian
python scripts/generate_diagram.py --type function --output assets/gaussian.png \
  --expr "np.exp(-x**2 / 2) / np.sqrt(2 * np.pi)" --xrange -4 4 \
  --title "Standard Normal Distribution"

# Polynomial
python scripts/generate_diagram.py --type function --output assets/poly.png \
  --expr "x**3 - 3*x + 1" --xrange -3 3
```

### Scatter Plots

```bash
python scripts/generate_diagram.py --type scatter --output assets/scatter.png \
  --x "1,2,3,4,5,6,7,8" --y "2.1,4.0,5.8,8.2,9.9,12.1,14.0,16.2" \
  --title "Linear Relationship"
```

### Bar Charts

```bash
python scripts/generate_diagram.py --type bar --output assets/bar.png \
  --y "30,50,20,40" --labels "Marketing,Engineering,Ops,Sales" \
  --title "Budget Allocation"
```

### Heatmaps

```bash
python scripts/generate_diagram.py --type heatmap --output assets/heatmap.png \
  --matrix "1,2,3;4,5,6;7,8,9" --title "Correlation Matrix"
```

### Dark Mode

Add `--dark` for notes using Obsidian dark theme:

```bash
python scripts/generate_diagram.py --type sigmoid --output assets/sigmoid-dark.png --dark
```

## Embedding in Obsidian

After generating the image, embed it in your note:

```markdown
### Sigmoid Activation Function

The sigmoid function maps any real value to (0, 1):

$$\sigma(x) = \frac{1}{1 + e^{-x}}$$

![[assets/sigmoid.png]]

*Generated with matplotlib*
```

Or with sizing and alignment:

```markdown
<div align="center">

![[assets/sigmoid.png|600]]

</div>
```

## Supported Diagram Types

| Type | Description | Required Args |
|------|-------------|---------------|
| `sigmoid` | Sigmoid activation | `--output` |
| `tanh` | Tanh activation | `--output` |
| `relu` | ReLU activation | `--output` |
| `function` | Custom numpy expression | `--output`, `--expr` |
| `scatter` | Scatter plot | `--output`, `--x`, `--y` |
| `bar` | Bar chart | `--output`, `--y` |
| `heatmap` | 2D heatmap | `--output`, `--matrix` |

## Common Options

| Option | Description | Default |
|--------|-------------|---------|
| `--output` | Output file path (png/pdf/svg) | required |
| `--title` | Plot title | auto-generated |
| `--xlabel` | X-axis label | "x" |
| `--ylabel` | Y-axis label | "y" |
| `--xrange` | X axis range | varies by type |
| `--dpi` | Image resolution | 150 |
| `--dark` | Dark mode styling | false |

## Expression Syntax (function type)

Available in `--expr`:

| Symbol | Meaning |
|--------|---------|
| `x` | The x variable |
| `np` | NumPy module |
| `sin`, `cos`, `tan` | Trig functions |
| `exp` | Exponential e^x |
| `log` | Natural logarithm |
| `sqrt` | Square root |
| `abs` | Absolute value |
| `pi`, `e` | Constants |

Examples:
- `"np.sin(x)"` - sine wave
- `"np.exp(-x**2)"` - Gaussian
- `"1 / (1 + np.exp(-x))"` - sigmoid
- `"np.maximum(0, x)"` - ReLU
- `"np.sin(x) / x"` - sinc function

## Output Formats

| Extension | Use Case |
|-----------|----------|
| `.png` | Standard embedding (recommended) |
| `.pdf` | Vector quality, zoomable |
| `.svg` | Vector, but limited Obsidian support |

## Workflow Decision Tree

1. **Can Mermaid render it?** → Use Mermaid (flowcharts, sequences, etc.)
2. **Is it a basic chart?** → Use Charts plugin (bar, line, pie)
3. **Is it a math function or scientific plot?** → Use Python + matplotlib
4. **Need precise control over styling?** → Use Python + matplotlib
