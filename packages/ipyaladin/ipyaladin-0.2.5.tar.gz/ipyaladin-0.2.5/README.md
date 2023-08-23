# ipyaladin

A bridge between Jupyter and Aladin Lite, enabling interactive sky visualization in IPython notebooks.
With a couple of lines, you can display Aladin Lite, center it on the target of your choice, and overlay an Astropy table:

![ipyaladin example](assets/ipyaladin-screencast.gif)

- [ipyaladin](#ipyaladin)
  - [Examples](#examples)
  - [Installation](#installation)
  - [New features corner](#new-features-corner)
  - [Development installation](#development-installation)

## Examples

Some example notebooks can be found in the [examples directory](examples).

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/cds-astro/ipyaladin/master). You can also try it directly [in mybinder](https://mybinder.org/v2/gh/cds-astro/ipyaladin/master), without installing anything.

## Installation

To install use pip:

    pip install ipyaladin

Then, make sure to enable widgetsnbextension:

    jupyter nbextension enable --py widgetsnbextension

Finally, enable ipyaladin:

    jupyter nbextension enable --py --sys-prefix ipyaladin

And you are ready to use ipyaladin inside your notebooks!
Additionny, for a jupyterlab usage you will need to:

    jupyter labextension develop ipyaladin --overwrite

There is also a conda package that can be installed with:

    conda install -c bmatthieu3 ipyaladin==0.2.5

## New features corner

![new_features](assets/new_features.gif)

## Development installation

First, make sure you have installed jupyter on your python environnement: `pip install jupyter`.
For a development installation [Node.js](https://nodejs.org) and [Yarn version 1](https://classic.yarnpkg.com/) are also required,

    git clone https://github.com/cds-astro/ipyaladin.git
    cd ipyaladin
    npm install yarn
    cd js
    npm install
    cd ..
    pip install -e .

For Jupyter Notebook, do
 
    jupyter nbextension install --py --symlink --overwrite --sys-prefix ipyaladin
    jupyter nbextension enable --py --sys-prefix ipyaladin

For JupyterLab, you will need to run this command too:

    jupyter labextension develop --overwrite ipyaladin

Then you need to rebuild the JS when you make a code change:

    cd js
    yarn run build

You then need to refresh the JupyterLab page when your javascript changes.
