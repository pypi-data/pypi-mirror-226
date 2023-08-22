This is the official machine data format package.

It supports csv importing, exporting and format compliance checking.
Machine data is parsed into a python object that provides typed views on the contained measurement and event timeseries.
Furthermore, the repository contains extraction/conversion code for various IoP datasets, as well as some synthetic mock data.

There is also a web-app that gives some of the aforementioned features a visual interface [mdata_app](https://git-ce.rwth-aachen.de/machine-data/mdata_app).
An instance is publicly hosted at [https://mdata.cluster.iop.rwth-aachen.de/](https://mdata.cluster.iop.rwth-aachen.de/), however there are no guarantees about security or privacy of the uploaded data. 

For an overview over the format specification, see\
[![Download PDF](https://img.shields.io/badge/Machine_Data_Format-PDF-green)](files/info/iop-machine-data-proposal.pdf)