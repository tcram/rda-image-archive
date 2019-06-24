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
- `export/` is for "deployed images"
- `api/` is for code supporting an API

## installation

Adapted from Issa Rice:

> First, clone the repo and set up the database:
> 
> ```bash
> git clone https://github.com/ncar/rda-image-archive.git
> cd rda-image-archive 
> mysql -e "create database images"
> make read  # read in data from sql/
> ```
> 
> Now set up the password file to allow PHP to log in to the database:
> 
> ```bash
> cp access-portal/backend/globalVariables/{dummyPasswordFile.inc,passwordFile.inc}
> vi access-portal/backend/globalVariables/passwordFile.inc  # change to add database login info
> ```
> 
> If you're hosting this on a server, make sure to disable public access to the
> password file.
> 
> Finally start the service:
> 
> ```bash
> cd api
> php -S localhost:8000
> ```
> 
> To get AnchorJS and tablesorter, run:
> 
> ```bash
> make fetch_anchorjs
> make fetch_tablesorter
> ```
> 
> You can now visit `http://localhost:8000/` in your browser.

## references

I would not have been able to develop this repository without reading the source code in <https://github.com/riceissa/aiwatch/>.

Additionally, this repo was based on a survey of the following:

- DataCite Metadata Working Group. (2019). DataCite Metadata Schema Documentation for the Publication and Citation of Research Data. Version 4.2. DataCite e.V. https://doi.org/10.5438/bmjt-bx77
- [White Paper: Uploading to Internet Archive](https://about.biodiversitylibrary.org/help/digitization-resources/upload/#Background-Getting%20an%20identifier-Mandatory%20Metadata). Joel Richard <richardjm@si.edu>, Smithsonian Libraries. Retrieved June 6, 2019.
- [US National Archives Catalog API](https://github.com/usnationalarchives/Catalog-API/). Dominic Byrd-McDevitt. Retrieved June 6, 2019.
