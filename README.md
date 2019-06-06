# rda-image-archive

This repository is for the development of a digital image archive at the National Center for Atmospheric Research.

## layout

- `sql/` is for data in MySQL format
- `api/` is for code supporting a public API
- `scripts/` is for scripts that scrape metadata

## references

The inital version of this repo was initially (2019-06-04) modelled off of <https://github.com/riceissa/aiwatch/>.

The metadata schema and API design were created after a survey of the following:

- DataCite Metadata Working Group. (2019). DataCite Metadata Schema Documentation for the Publication and Citation of Research Data. Version 4.2. DataCite e.V. https://doi.org/10.5438/bmjt-bx77
- [White Paper: Uploading to Internet Archive](https://about.biodiversitylibrary.org/help/digitization-resources/upload/#Background-Getting%20an%20identifier-Mandatory%20Metadata). Joel Richard <richardjm@si.edu>, Smithsonian Libraries. Retrieved June 6, 2019.
- [US National Archives Catalog API](https://github.com/usnationalarchives/Catalog-API/). Dominic Byrd-McDevitt. Retrieved June 6, 2019.
