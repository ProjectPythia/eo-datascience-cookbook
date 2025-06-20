<img src="notebooks/images/logos/tuw-geo_eodc_logo_horizontal.png" alt="tuw-geo-logo" width="500"/>

# Earth Observation Data Science Cookbook

[![nightly-build](https://github.com/ProjectPythia/eo-datascience-cookbook/actions/workflows/nightly-build.yaml/badge.svg)](https://github.com/ProjectPythia/eo-datascience-cookbook/actions/workflows/nightly-build.yaml)
[![Binder](https://binder.projectpythia.org/badge_logo.svg)](https://binder.projectpythia.org/v2/gh/ProjectPythia/eo-datascience-cookbook/main?labpath=notebooks)
[![DOI](https://zenodo.org/badge/830421828.svg)](https://zenodo.org/badge/latestdoi/830421828)

This Project Pythia Cookbook covers a range of Earth observation examples employing
the Pangeo philosophy. The examples represent the main research lines and BSc/MSc
courses at the Department of Geodesy and Geoinformation at the TU Wien (Austria).
The department has strong ties with the EODC (Earth Observation Data Centre For
Water Resources Monitoring), which hosts e.g., analysis-ready Sentinel-1
(imaging radar mission) data, and has the computational resources to process
large data volumes.

## Motivation

The motivation behind this book is to provide examples of Pangeo-based workflows
applied to realistic examples in Earth observation data science. Creating an
effective learning environment for Earth observation students is a challenging
task due to the rapidly growing volume of remotely sensed, climate, and other
Earth observation data, along with the evolving demands from the tech industry.
Today's Earth observation students are increasingly becoming a blend of traditional
Earth system scientists and "big data scientists", with expertise spanning computer
architectures, programming paradigms, statistics, and machine learning for
predictive modeling. As a result, it is essential to equip educators with the
proper tools for instruction, including training materials, access to data, and
the necessary skills to support scalable and reproducible research.

## Authors

[Wolfgang Wagner](https://github.com/wagner-wolfgang), [Martin Schobben](https://github.com/martinschobben),
[Nikolas Pikall](https://github.com/npikall), [Joseph Wagner](https://github.com/wagnerjoseph), [Davide Festa](https://github.com/maybedave),
[Felix David Reuß](https://github.com/FelixReuss), [Luka Jovic](https://github.com/lukojovic)

### Contributors

<a href="https://github.com/ProjectPythia/eo-datascience-cookbook/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=ProjectPythia/eo-datascience-cookbook" />
</a>

## Structure

This book comprises examples of data science concerning Earth Observation (EO) data,
including course material on remote sensing and data products produced by the TU
Wien. It also serves to showcase the data and services offered by the EODC, including
a [STAC](https://docs.eodc.eu/services/stac.html) catalogue and a
[Dask Gateway](https://docs.eodc.eu/services/dask.html) for distributed data processing.

### Courses

This section offers an overview of notebooks, which are used in **courses** from
the Department of Geodesy and Geoinformation at TU Wien.

### Templates

This section provides a collection of general **examples** of earth observation
related tasks and workflows, which are not directly related to a specific course
or product.

### Tutorials

In this section you will find a collection of lessons, which explain certain
**products** or methods that have been developed at the Department of Geodesy and
Geoinformation at TU Wien.

## Running the Notebooks

You can either run the notebook using [Binder](https://binder.projectpythia.org/v2/gh/ProjectPythia/eo-datascience-cookbook/main?labpath=notebooks)
or on your local machine.

### Running on Binder

The simplest way to interact with a Jupyter Notebook is through
[Binder](https://binder.projectpythia.org/v2/gh/ProjectPythia/eo-datascience-cookbook/main?labpath=notebooks), which enables the execution of a
[Jupyter Book](https://jupyterbook.org) in the cloud. The details of how this works are not
important for now. All you need to know is how to launch a Pythia
Cookbooks chapter via Binder. Simply navigate your mouse to
the top right corner of the book chapter you are viewing and click
on the rocket ship icon, (see figure below), and be sure to select
“launch Binder”. After a moment you should be presented with a
notebook that you can interact with. I.e. you'll be able to execute
and even change the example programs. You'll see that the code cells
have no output at first, until you execute them by pressing
{kbd}`Shift`\+{kbd}`Enter`. Complete details on how to interact with
a live Jupyter notebook are described in [Getting Started with
Jupyter](https://foundations.projectpythia.org/foundations/getting-started-jupyter.html).

### Running on Your Own Machine

If you are interested in running this material locally on your computer, you will
need to follow this workflow:

1. Clone the `https://github.com/ProjectPythia/eo-datascience-cookbook` repository:

   ```bash
    git clone https://github.com/TUW-GEO/eo-datascience-cookbook
   ```

1. Move into the `eo-datascience-cookbook` directory
   ```bash
   cd eo-datascience-cookbook
   ```
1. Create and activate your conda environment from the ``environment.yml`` file
   ```bash
   conda env create -f environment.yml
   conda activate eo-datascience-cookbook-dev
   ```
1. Move into the `notebooks` directory and start up Jupyterlab
   ```bash
   cd notebooks/
   jupyter lab
   ```
