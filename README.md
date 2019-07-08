# rda-image-archive

This repository is for the development of a digital image archive (for historical climate documents) at the National Center for Atmospheric Research. Its anticipated uses include:

1. storing image files,
1. subsetting image files for bulk access,
1. associating images with rich meteorological metadata, and
1. providing a public API.

## layout

- `sql/` is for the metadata schema,
- `import/` and `export/` are for manual data processing,
- `stage/` and `deploy/` are for programmatic data processing,
- `scripts/` is for python modules and executables, and lastly
    - `scripts/demos/` contains demonstrations as Jupyter notebooks.

## references

This repository was initially derived from the source code in <https://github.com/riceissa/aiwatch/>.

Additionally, this repo was based on a survey of the following:

- DataCite Metadata Working Group. (2019). DataCite Metadata Schema Documentation for the Publication and Citation of Research Data. Version 4.2. DataCite e.V. https://doi.org/10.5438/bmjt-bx77
- [White Paper: Uploading to Internet Archive](https://about.biodiversitylibrary.org/help/digitization-resources/upload/#Background-Getting%20an%20identifier-Mandatory%20Metadata). Joel Richard <richardjm@si.edu>, Smithsonian Libraries. Retrieved June 6, 2019.
- [US National Archives Catadocument API](https://github.com/usnationalarchives/Catadocument-API/). Dominic Byrd-McDevitt. Retrieved June 6, 2019.

# Documentation

This part of the README aims to propose

1. a set of required metadata fields,
1. a data exchange format, and
1. a procedure for updating a test database called `images`.

Before going into detail, there are a few preliminaries to address.

### Local installation

First, if one has a local mysql installation, I suggest initializing a test database `images`.

1. Clone the repository and create a new database.
   ```bash
   git clone https://github.com/ncar/rda-image-archive.git
   cd rda-image-archive 
   mysql -e "create database images"
   ```
   
1. Create a configuration file `mysql_args` 
   ```
   vi mysql_args
   ```
   with these three lines:
   ```
   [client]
   user=<my_user>
   password=<my_password>
   ```
   (These will be passed as arguments to `mysql`, see the `Makefile`.)  

1. Now make the database.
   ```
   make
   ```

(I have only tested this installation on Linux.) Withstanding errors, one should have access to a local copy of the test database `images`. 

### Most recent database schema

One may checkout the repository at a certain date, then run `make describe` for the revised schema at that date. The `Makefile` will be configured correctly for commits after 2019-06-25, but `make describe` is only guaranteed to return sensible output after 2019-07-08.

### Outline of database schema (as of 2019-06-25)

Second, to get a handle on the schema designed (as of 2019-06-25) for `images`, it is perhaps useful to see the output of `make describe` (one should run this command on their own to see updates to the schema since the time of this document's writing). 

Printed here in gory detail, that reads:

`mysql --defaults-extra-file=mysql_args images -e "describe archive;"`

Field | Type | Null | Key | Default | Extra
--- | --- | --- | --- | --- | ---
`archive_id` | smallint(6) | NO | PRI | NULL | 
`name` | varchar(100) | NO |  | NULL | 
`host_country` | char(3) | NO |  | NULL | 
`search_url` | varchar(255) | YES |  | NULL | 
`search_documentation` | varchar(255) | YES |  | NULL | 
`api_url` | varchar(255) | YES |  | NULL | 
`api_documentation` | varchar(255) | YES |  | NULL | 
`notes` | varchar(1000) | YES |  | NULL | 

`mysql --defaults-extra-file=mysql_args images -e "describe platform;"` (truncated for space ...)

Field | Type
--- | ---
`platform_id` | smallint(6)
`name` | varchar(255)
`compass_type_of_instrument` | enum(`gyro`,`magnetic`,`unknown`) 
`compass_units` | enum(`degrees`,`cardinal directions`) 
`navigation_speed_type_of_instrument` | enum(`chip log`,`patent log`,`pit log`,`electromagnetic log`,`propeller rpm`) 
`navigation_speed_units` | enum(`knots`,`kilometers per second`) 
`scale_used_for_measuring_waves` | varchar(40) 
`scale_used_for_wind_speed` | enum(`beaufort`,`meters per second`) 
`anemometer_instrument_make_and_number` | varchar(40) 
`anemometer_instrument_exposure` | varchar(40) 
`atmospheric_pressure_units` | enum(`inches`,`hectopascals`,`millibars`) 
`atmospheric_pressure_type_of_instrument` | varchar(40) 
`atmospheric_pressure_instrument_make_and_number` | varchar(40) 
`atmospheric_pressure_instrument_exposure` | varchar(40) 
`temperature_units` | enum(`celcius`,`fahrenheit`) 
`dry_bulb_thermometer_make_and_number` | varchar(40) 
`dry_bulb_thermometer_exposure` | varchar(40) 
`wet_bulb_thermometer_exposure` | varchar(40) 
`wet_bulb_thermometer_make_and_number` | varchar(40) 
`sea_temperature_type_of_instrument` | varchar(40) 
`sea_temperature_instrument_make_and_number` | varchar(40) 
`sea_temperature_instrument_exposure` | varchar(40) 
`facility_description` | varchar(1000) 

`mysql --defaults-extra-file=mysql_args images -e "describe document;"`

Field | Type | Null | Key | Default | Extra
--- | --- | --- | --- | --- | ---
`document_id` | smallint(6) | NO | PRI | NULL | 
`platform_id` | smallint(6) | NO | MUL | NULL | 
`archive_id` | smallint(6) | NO | MUL | NULL | 
`start_date` | date | NO |  | NULL | 
`end_date` | date | NO |  | NULL | 
`relative_id_item` | varchar(255) | NO |  | NULL | 
`relative_id_value` | varchar(255) | NO |  | NULL | 
`marine_region_description` | varchar(1000) | YES |  | NULL | 
`create_date` | date | YES |  | NULL | 
`relative_parent_item` | varchar(255) | YES |  | NULL | 
`relative_parent_value` | varchar(255) | YES |  | NULL | 

`mysql --defaults-extra-file=mysql_args images -e "describe image;"`

Field | Type | Null | Key | Default | Extra
--- | --- | --- | --- | --- | ---
`image_id` | char(32) | NO | PRI | NULL | 
`document_id` | smallint(6) | NO | MUL | NULL | 
`relative_order` | int(4) | NO |  | NULL | 
`media_subtype` | enum(`bmp`,`gif`,`jp2`,`jpeg`,`png`,`tiff`) | NO |  | NULL | 
`file_size` | smallint(6) | YES |  | NULL | 
`location_description` | varchar(255) | YES |  | NULL | 
`local_start_date` | date | YES |  | NULL | 
`local_start_time` | time | YES |  | 00:00:00 | 
`local_time_zone` | time | YES |  | NULL | 
`ut1_start_datetime` | datetime | YES |  | NULL | VIRTUAL GENERATED
`mime_type` | varchar(10) | YES |  | NULL | VIRTUAL GENERATED

`mysql --defaults-extra-file=mysql_args images -e "describe observation;"`

Field | Type | Null | Key | Default | Extra
--- | --- | --- | --- | --- | ---
`image_id` | char(32) | NO | PRI | NULL | 
`time_after_image_start` | time | NO | PRI | NULL | 
`atmospheric_pressure_indicator` | tinyint(1) | YES |  | NULL | 
`dry_bulb_temperature_indicator` | tinyint(1) | YES |  | NULL | 
`wet_bulb_temperature_indicator` | tinyint(1) | YES |  | NULL | 
`unspecified_air_temperature_indicator` | tinyint(1) | YES |  | NULL | 
`sea_temperature_indicator` | tinyint(1) | YES |  | NULL | 
`wind_direction_indicator` | tinyint(1) | YES |  | NULL | 
`wind_speed_indicator` | tinyint(1) | YES |  | NULL | 
`cloud_form_indicator` | tinyint(1) | YES |  | NULL | 
`cloud_direction_indicator` | tinyint(1) | YES |  | NULL | 
`cloud_amount_indicator` | tinyint(1) | YES |  | NULL | 
`longitude` | float(10,6) | YES |  | NULL | 
`latitude` | float(10,6) | YES |  | NULL | 
`location_fix_indicator` | tinyint(1) | YES |  | 0 | 
`local_course` | float(6,3) | YES |  | NULL | 
`local_speed` | float(6,3) | YES |  | NULL | 

### Parent-child dependencies

Now, the required fields in the 5 tables above are based on my interpretation of the following parent-child dependencies. 

```
archive   platform
    \     /
    document
       |
    image
       |
    observation
```

In the partially-ordered diagram of tables above, an entry in a lower table depends on metadata from its parent entry in each upper table. For example, an entry in the `document` table makes foreign key references to parent entries who are defined (at minimum) by the fields

- in `archive`, namely,
    - `archive_id`
    - `name`
    - `host_country`; and
- in `platform`, namely,
    - `platform_id`
    - `name`.

As a result (and of relevance to our immediate use case), to insert metadata for one (binary) image file in the table `image` (formerly called `page`), the following parent fields will have had to be previously defined.

Field | Comment
--- | ---
`archive.archive_id` | *primary key, automatically generated*.
`archive.name` | Archive responsible for "fullest descriptive metadata" of child records, e.g., "The National Archives".
`archive.host_country` | Host country of archive. Format: ISO 3166-1 3-letter country code, e.g., "GBR".
`platform.platform_id` | *automatically generated*.
`platform.name` | Name of platform (e.g., a ship or weather station) generating climate documents.
`document.document_id` | *primary key, automatically generated*.
`document.platform_id` | *foreign key, automatically generated*.
`document.archive_id` | *foreign key, automatically generated*.
`document.start_date` | Corresponds roughly to NARA's `fileUnit.coverageStartDate` field for a given document.
`document.end_date` | Corresponds roughly to NARA's `fileUnit.coverageEndDate`.
`document.relative_id_item` | Names the field that serves as a document's unique identifier relative to its parent archive. E.g., `naId` for NARA ID.
`document.relative_id_value` | Valuates the field that serves as the document's unique identifier (relative its parent archive). E.g., `17298664`, the NARA ID for the document "Idaho (BB-42) - May, 1944".

### Initial database ontology

The assumptions underlying the ontology so far (that is, all tables above and including the table `image`) are:

- Documents produce images;
- Platforms produce documents;
- Archives produce documents;
- Documents from a single platform could be housed in distinct archives;
- A single archive could be responsible for documents from distinct platforms.

The motivations underlying the ontology so far are:

- We aim to preserve metadata from an image's archive in order to maintain *continuity of record*. 
- We want to document platform metadata as a means to qualify the *instruments and methods of observation* which determine an image's meteorological content. 
- (And these two motivations are independent.)

I am open to feedback and criticism with respect to this ontology. 

## Minimal metadata

Having outlined a suggested installation, and some preliminary justification in support of dependencies chosen for the rda-image-archive's database schema, I would like now to propose a subset of fields that should be required as *minimal metadata*. We'll start with image files.

### Image files

Ignoring surrogate keys (these are generated incrementally), I propose that an image file should be accompanied by, at minimum, the following metadata.

Field | Comment 
--- | ---
`image.image_id` | 32-char hexidecimal image UUID. Generated during image file import (by removing hyphens from 36-char UUID).
`image.relative_order` | Format: 0000--9999. Describes the order of an image relative to other images in a given document. 
`image.media_subtype` | Describes filetype as `bmp`, `gif`, `jp2`, `jpeg`, `png`, or `tiff`.
`document.relative_id_item` | Names the field that serves as a document's unique identifier relative to its parent archive. E.g., `naId` for NARA ID.
`document.relative_id_value` | Valuates the field that serves as the document's unique identifier (relative its parent archive). E.g., `17298664`, the NARA ID for the document "Idaho (BB-42) - May, 1944".
`document.start_date` | Corresponds roughly to NARA's `fileUnit.coverageStartDate` field for a given document.
`document.end_date` | Corresponds roughly to NARA's `fileUnit.coverageEndDate`.
`platform.name` | Name of platform (e.g., a ship or weather station) generating climate documents.
`archive.name` | Archive responsible for "fullest descriptive metadata" of child records, e.g., "The National Archives".
`archive.host_country` | Host country of archive. Format: ISO 3166-1 3-letter country code, e.g., "GBR".

### Observations

My initial impression is that an observation record (e.g., a transcription) should be accompanied by the following metadata.

Field | Comment
--- | ---
`image.image_id` | *foreign key reference*
`time_after_image_start` | Format: a non-negative time entered as "HH:MM" (or HHMMSS). Defined as the displacement in hours and minutes from the start of the parent image (explicitly from `image.ut1_start_datetime`). Note: If `image.local_start_time` of the parent image takes its default value "00:00:00", then `time_after_image_start` for an observation would be given by the local time of this observation. If `image.local_start_time` is nonzero, say, "06:00:00", then an observation made at local time "18:00:00" would have `time_after_image_start` entered as "12:00" (or 120000).

Understandably, this requirement may be too much to ask for: `time_after_image_start` could be ill-defined, illegible, incorrect, or only available from deduction. I would appreciate feedback with respect to this level of temporal granularity for the `observation` table in the database ontology.


## Recommended metadata

We proceed to describe the recommended metadata, beginning from the tables `archive` and `platform` and working down the child tables.

### Archives

For archives, given that a document will have an identifier relative to its parent archive, I recommend providing links to the archive's catalog search and the archive's API (if one exists).

Field | Description
--- | ---
`archive.search_url`  | Link to advanced search provided by archive, e.g., "https://discovery.nationalarchives.gov.uk/advanced-search"
`archive.search_documentation`  | Link to documentation for advanced search, e.g., "http://www.nationalarchives.gov.uk/help-with-your-research/discovery-help/sorting-and-filtering-your-search-results/"
`archive.api_url`  | Base URL of API provided by archive, e.g., "https://catalog.archives.gov/api/v1/".
`archive.api_documentation`  | Link to documentation for API provided by archive, e.g., "https://github.com/usnationalarchives/Catalog-API".

### Platforms

For platforms, my initial recommendation is to include descriptions of meteorological instruments along with unit conventions. However, if either the unit conventions (e.g., degrees vs. cardinal directions) or the instrumentation (e.g., pre- vs. post- gyrocompass) vary with time, then these fields may need to be demoted to the `document` table.

Field | Type
--- | ---
`compass_type_of_instrument` | enum('gyro', 'magnetic', 'unknown')
`compass_units` | enum('degrees', 'cardinal directions')
`navigation_speed_type_of_instrument` | enum('chip log', 'patent log', 'pit log', 'electromagnetic log', 'propeller rpm')
`navigation_speed_units` | enum('knots', 'kilometers per second')
`scale_used_for_measuring_waves` | varchar(40)
`scale_used_for_wind_speed` | enum('beaufort', 'meters per second')
`anemometer_instrument_make_and_number` | varchar(40)
`anemometer_instrument_exposure` | varchar(40)
`atmospheric_pressure_units` | enum('inches', 'hectopascals', 'millibars'),
`atmospheric_pressure_type_of_instrument` | varchar(40)
`atmospheric_pressure_instrument_make_and_number` | varchar(40)
`atmospheric_pressure_instrument_exposure` | varchar(40)
`temperature_units` | enum('celcius', 'fahrenheit')
`dry_bulb_thermometer_make_and_number` | varchar(40)
`dry_bulb_thermometer_exposure` | varchar(40)
`wet_bulb_thermometer_exposure` | varchar(40)
`wet_bulb_thermometer_make_and_number` | varchar(40)
`sea_temperature_type_of_instrument` | varchar(40)
`sea_temperature_instrument_make_and_number` | varchar(40)
`sea_temperature_instrument_exposure` | varchar(40)

### Documents

For documents, I recommend metadata that refers to what NARA calls the "parent series", i.e., the collection-level class to which a given document belongs. This field is broken into the `item` and the `value`, to accommodate for different names^[Perhaps there is a SKOS concept to describe the parent-child relationship at the collection-level?] for the "parent series". I also recommend including a list of place names. This field would enable one to perform a reverse dictionary (fuzzy) search against the `http://marineregions.org/gazetteer.php?p=webservices` REST API, in order to associate documents with boundary polygons. The goal here is to enable queries for records by (fuzzy) georeference (e.g., within a certain radius, or a certain region). Lastly, I recommend a `create_date` indicating when a document file was created/imported/scanned into its parent archive. 

In summary, it is recommended that a document includes metadata for:

- `create_date` as the date the document was moved an archive.
- `relative_parent_item` as the "type of parent object" relative to an archive.
- `relative_parent_value` as the "value of the parent object" within an archive.
- `marine_region_description` as a comma separated list of colloquial marine region names. (Could include seas, sandbanks, seamounts, ridges, bays, sampling stations, or ports.)

### Images

For images, I highly recommend including `file_size` (in bytes) for the sake of providing metadata for users who would like to download images in bulk; this field is not required because it is trivial to deduce `file_size` programmatically. 

Optionally, I recommend the following "fine resolution" metadata. (It has been mentioned that these fields are perhaps "out of scope" of metadata, and should properly be classified as data; nonetheless, I would prefer to provide fields at a fine enough granularity to enable georeferencing.)

Field | Type | Comment
--- | --- | ---
`location_description` | varchar(255) | Colloquial name or description of location. Should be entered verbatim.
`local_start_date` | date | Format: "YYYY-MM-DD", or, numerically, YYYYMMDD. Local date at image start.
`local_start_time` | time | "00:00:00" comment format: "HH:MM:SS", or, numerically, HHMMSS. Local time at image start. should be entered as a postive value between "00:00" (or 000000) and "23:59" (or 235900).
`local_time_zone` | time | Format: should be entered as a signed value between "-12:00" (or -120000) and "12:00" (or 120000). The local timezone at image start is defined to be the (signed) hours and minutes from ut1 solar time to local time. For example, in timezone -03:30, the local time 15:00 refers to the ut1 time 18:30.

The logic behind this section of the `image` table schema is to deduce the "virtual" field `ut1_start_datetime` from the MySQL command `date_sub(local_start_date, interval local_time_zone hour_second)`, which gives the UT1 (solar) datetime at image start.

### Observations

Because observations have fine (perhaps as fine as ~30 minute) time resolution, georeferencing metadata may be too much to ask a provider for. Again, however, my philosophy here is to provide fields at a fine enough granularity to enable time-series analyses. 

The following fields are boolean indicators and are recommended.

- atmospheric pressure indicators
   - `atmospheric_pressure_indicator`

- temperature indicators
   - `dry_bulb_temperature_indicator`
   - `wet_bulb_temperature_indicator`
   - `unspecified_air_temperature_indicator`
   - `sea_temperature_indicator`

- wind speed indicators
    - `wind_direction_indicator`
    - `wind_speed_indicator`

- cloud indicators
    - `cloud_form_indicator`
    - `cloud_direction_indicator`
    - `cloud_amount_indicator`

Other recommended indicators might include

- humidity indicators
- weather indicators
- visibility indicators
- precipitation indicators
- ocean sea waves and swell indicators

but, as of 2019-06-25, these fields have not yet been implemented into the schema.

The finest level of granuality would be obtained from the following *optional* fields (with the end goal of determining a platform's location).

Field | Type | Description
--- | --- | ---
`longitude` | float(10,6) | 
`latitude` | float(10,6) |
`location_fix_indicator` | bool | An indicator equal to 1 if longitude and latitude are "fixed" by georeference. Else equal to 0, e.g., when location is unspecified or "dead-reckoned".
`local_course` | float(6,3) | Local course is defined as the direction of movement in degrees clockwise (e.g., convert ne to 315 and nne to 337.5) from "local north". This field should be entered verbatim, without correction for the compass type of instrument. True course thus depends on this field, the date, and the parent field `platform.compass_type_of_instrument`.
`local_speed` | float(6,3) | Should be entered verbatim. This field depends on the parent field `platform.navigation_speed_units`. 

This concludes the discussion of required and recommended metadata. Again, I am open to feedback and criticism with respect to any part of the database ontology. 

## File exchange formats

We proceed to document two (hopefully equivalent) file exchange formats:

- a *flattened* (or *unnormalized*) `csv` format, and
- a *normalized* `json` format.

> TODO <ccg, 2019-06-25> > 
