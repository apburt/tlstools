# tlstools

* Combine [treeseg](https://github.com/apburt/treeseg), [optqsm](https://github.com/apburt/optqsm) and [nlallom](https://github.com/apburt/treeseg) results for analysis.
* Plot tree-level points clouds and quantitative structural models.

## Overview

The Python script sortResults.py formats the results from treeseg, optqsm and nlallom into an accessible format for analysis.

That is, this script amalgamates the outputs of [runallom.m](https://github.com/apburt/nlallom/blob/master/src/runallom.r) and [runopt.m](https://github.com/apburt/optqsm/blob/master/src/runopt.m) into two NumPy files describing tree- and plot-scale volume- and allometric-derived above-ground biomass, alongside other structural parameters.

The variables comprising these NumPy files are described in [VARIABLES](VARIABLES).

This repository also contains a number of scripts for plotting tree-level point clouds and quantitative structural models.

## Prerequisites

Python (v3.6.5 or later)

Python packages:
* numpy
* matplotlib

## Installation

On macOS 10.13, dependencies were installed using Homebrew (https://brew.sh), as:

```
brew install python 
pip3 install –upgrade pip setuptools wheel 
pip3 install numpy 
pip3 install scipy 
pip3 install matplotlib 
```

tlstools can then be installed as:

```
cd [INSTALLATION_DIR];
git clone https://github.com/apburt/nlallom.git;
```

## Usage

sortResults.py is called as:

```
sortResults.py -at [PLOT_ID]_tree.txt -ap [PLOT_ID]_plot.txt -m [PLOT_ID]_models.dat 
```

Where [PLOT_ID]_tree.txt and [PLOT_ID]_plot.txt are the results files from runallom.m, and [PLOT_ID]_models.dat the results file from runopt.m. The combined results will be written in the current working directory as [PLOT_ID]_tree.npy and [PLOT_ID]_plot.npy.

The plotting scripts can be called, such as in the example of plotModels.py, as:

```
plotModels.py -m [QSM].mat
```

Where [QSM].mat is any quantitative structural models generated from [TreeQSM](https://github.com/InverseTampere/TreeQSM) or [optqsm](https://github.com/apburt/optqsm).
The optional flags -a, -e, -o, -q, -ax, define azimuth/elevation angles, output image file name, high quality cylinder rendering and axes display respectively. Further optional flags are defined in the parser section of each script.

By default, these plots are written as vector images in PDF format. These can be rasterised via ImageMagick, e.g.,:

```
convert -trim +repage -density 600 -units pixelsperinch OUTFILE.pdf OUTFILE.png
```

## Authors

* **Andrew Burt**

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details
