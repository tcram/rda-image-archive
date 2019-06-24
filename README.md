# rda-image-archive

This repository is for the development of a digital image archive (for historical climate documents) at the National Center for Atmospheric Research. Its anticipated uses include:

1. subsetting images for bulk access (and for storage at the RDA)
1. associating images with meteorological metadata 
    - boolean observations 
    - spatio-temporal ranges
1. providing a public API

## layout

- `sql/` is for data in MySQL format
- `import/` is for data-processing
- `api/` is for code supporting an API

## references

I would not have been able to develop this repository without reading the source code in <https://github.com/riceissa/aiwatch/>.

Additionally, this repo was based on a survey of the following:

- DataCite Metadata Working Group. (2019). DataCite Metadata Schema Documentation for the Publication and Citation of Research Data. Version 4.2. DataCite e.V. https://doi.org/10.5438/bmjt-bx77
- [White Paper: Uploading to Internet Archive](https://about.biodiversitylibrary.org/help/digitization-resources/upload/#Background-Getting%20an%20identifier-Mandatory%20Metadata). Joel Richard <richardjm@si.edu>, Smithsonian Libraries. Retrieved June 6, 2019.
- [US National Archives Catalog API](https://github.com/usnationalarchives/Catalog-API/). Dominic Byrd-McDevitt. Retrieved June 6, 2019.

## examples

![](https://catalog.archives.gov/OpaAPI/media/24357119/content/dc-metro/rg-024/594258/0001-A1/Dale-DD-353-1943-03/Dale-DD-353-1943-03_0003.JPG)
