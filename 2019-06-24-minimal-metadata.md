---
title: Minimal metadata for RDA image archive
author: Colton Grainger
date: 2019-06-24
revised:
---

My goal in this document is to propose

- a set of required metadata fields,
- a data exchange format, and
- a procedure for updating a test database called `images`.

Before going into detail, there are two preliminaries to address.

### Local Installation

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
   make read
   ```

(I have only tested this installation on Linux.) Withstanding errors, one should have access to a local copy of the test database `images`. To see the fields implemented in the schema for `images`, it is perhaps useful to see the output of `make describe`. Printed here in gory detail, that reads:

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

`mysql --defaults-extra-file=mysql_args images -e "describe platform;"` (truncated below ...)

Field | Type
--- | ---
`platform_id` (PRIMARY KEY) | smallint(6)
`name` (NOT NULL) | varchar(255)
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

### Database ontology

The required fields in the 5 tables above are based on my interpretation of the following parent-child dependencies. 

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

Having outlined a suggested installation, and some preliminary justification in support of dependencies chosen for the rda-image-archive's database schema, I would like now to propose a list of required metadata.

## Required Metadata


