# kweb 0.1.1

KLayout Web Viewer ![demo](docs/_static/kweb.png)

Based on https://github.com/klayoutmatthias/canvas2canvas

## Install

Create a virtual enviroment venv

`python -m venv venv `

Activate the virtual enviroment

`source venv/bin/activate`

Clone the repository to your local

`git clone https://github.com/gdsfactory/kweb.git`

Install the necessary dependecies

`cd /kweb`

`python -m pip install .`

`make install`

## Set a folder for kweb to use when looking for gds files

`export KWEB_FILESLOCATION=/path/to/folder/with/file.gds`

## Run

`cd src/kweb`

`make run`

Copy the link http://127.0.0.1:8000/gds/file.gds (or http://localhost:8000/gds/file.gds also works) to your browser to open the waveguide example
