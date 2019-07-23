---
title: todo
author: Colton Grainger
date: 2019-07-22
---

# todo

## 0. done

### send bibliography and summary of metadata to Jeff DLB

On 16-Jul-2019 17:28:32 UTC,  Philip Brohan <philip@brohan.org> wrote:

Hi Jeff

  Colton Grainger (cc'd) is maintaining the list of metadata elements - see his
repository at https://github.com/coltongrainger/rda-image-archive

 They were decided on by RDA, but based on external sources - Colton, where did
we get these from?

Thanks, Philip

On Fri, 12 Jul 2019 at 14:08, Jeff de La Beaujardiere <jeffdlb@ucar.edu> wrote:

> PS. Can you send me a copy of the list of metadata elements? Did RDA come up
> with them or were they previously established?
>
> Thanks, Jeff

### Ocean area specification for images.

On 05-Jul-2019 20:23:12 UTC, Steven Worley <worley@ucar.edu> wrote:

Attached are some thoughts about specifying broad regional locations for images
as metadata. Steve

 RegionalOceanAreas_definitions
<https://docs.google.com/a/ucar.edu/document/d/1E5upM9mjQvKoiwGlfMQY-UcbO9z2w4u_
ArQXrcjvgRM/edit?usp=drive_web>

Steven J. Worley worley@ucar.edu orcid.org/0000-0003-2797-6284 mobile:
720.468.1961

### adopt CF standard names
 

### initialize MySQL test database; local and remote versions
 

### realize sequential UUIDs
 

### mock up metadata schema
 

### feedback on rda-image schema from Philip Brohan

### feedback for georeferencing metadata from Philip Brohan and Kevin Wood 

which metadata fields are dependent?

- location under what projection?
- velocity?
- exactness?
- buffer?
- latitude / longitude

### document metadata schema
 
### Geospatial bounding box look-up 10-Jun-2019 15:53:22

mayernik@ucar.edu Geospatial bounding box look-up 10-Jun-2019 15:53:22
Hi Sky,
It was good to see you last week. During one conversation, I asked you
about a service that would allow us to look up geospatial bounding boxes
based on geographic names. For example, we might know that a ship was in
the Bering Sea, and would want to add a standard bounding box for the
Bering Sea to our database.

You told me the name of a service that did something like this, but of
course Ididn't write it down. Could you send me the name/link to that
service again?

I"m copying Tom Cram and Colton Grainger, who are working on a database of
images for historic ship logs.

Best,
Matt

### bulk download samples, /glade/collections/rda/work/image_archive

- I've put a Jupyter notebook on the team drive demonstrating how to download a single image from the National Archives catalog.  You will need to
generalize it to download a bulk set of images in a for loop.  Don't get
too carried away; just a few ship logs will suffice.

- The spreadsheet 'NARA_Master_Manifest_20180516.xlsx' has all the URLs to
the image catalogs.  Pick out a few that look interesting to you and
download those.

### ask Bob Dattore for comments
 

### metadata example: arctic sea ice 1900--1938
 

### 1st report on metadata schema
 

### metadata example: BHL OAI-PMH

Metadata about the books and journals in the BHL collection is published via OAI-PMH (Open Archives Initiative Protocol for Metadata Harvesting). OAI-PMH is a protocol used for publishing and harvesting metadata descriptions of records in an archive. More information about the protocol can be found at http://www.openarchives.org/pmh/. Descriptive metadata is provided better as MODS (http://www.loc.gov/standards/mods/v3/mods-3-0.xsd), but also as Dublin Core (http://www.openarchives.org/OAI/2.0/oai_dc.xsd) and OLEF. OLEF is a format defined to facilitate metadata harmonization among BHL Partners (see http://www.bhle.eu/bhl-schema/v1/ to find out more about the schema and also review this presentation).

The OAI-PMH endpoint for BHL is https://www.biodiversitylibrary.org/oai.

We provide 5 sets in BHL:

    item
    title
    part
    itemexternal
    partexternal

### metadata records examples: OAI-PMH at ESG-CET, wiki.ucar.edu

Metadata Records Examples

Following are examples of metadata records served by an ESG-CET Gateway acting
as an OAI-PMH repository. All examples refer to the same OAI item (i.e. object),
but for different metadata formats.

RDF
http://esg.prototype.ucar.edu/oai/repository.htm?verb=GetRecord&metadataPrefix=r
df&identifier=narccap_crcm_ncep_table3_psl_files

    <?xml version="1.0" encoding="UTF-8"?> <OAI-PMH
    xmlns="http://www.openarchives.org/OAI/2.0/"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation="http://www.openarchives.org/OAI/2.0/
    http://www.openarchives.org/OAI/2.0/OAI-PMH.xsd">
    <responseDate>2009-09-25T10:15:32Z</responseDate> <request
    verb="GetRecord" identifier="narccap_crcm_ncep_table3_psl_files"
    metadataPrefix="rdf">http://esg.prototype.ucar.edu/oai/repository.htm</reque
    st> <GetRecord> <record> <header>
    <identifier>narccap_crcm_ncep_table3_psl_files</identifier>
    <datestamp>2009-0

### high level overview of digital image curation

16aeb876cb0f8cad
24-May-2019 20:28:02

Hi Laura, Jennifer,
[…] I just sent a calendar invite … to get your
perspective on image management, based on your experiences to date with the
UCAR communications image collection. I thought that our project would
benefit from hearing about any software systems you have looked into, and
on how to structure metadata for large hierarchically nested collections.
If you think it would be helpful, we can send along examples of the images
we are dealing with to give you a bit more context.
Best,
Matt

### grok bulk processing, esp. National Archives

You can access the images by volume/box using the National Archives URLs in the attached spreadsheet. For a small set of images a sample download would be sufficient - though I understand Philip is bringing a collection as well. You will see that some ship URLs have not been integrated here -- I will follow up with NARA to get an updated list. 

## 1. in-progress

### choose method of abstraction (Tom's or SQLalchemy) for database connection

## 2. next/high-priority

### how to query the database locally? how to bulk download images matching a query?
 
### Python and Flask API

### assimilation timeline

Hi Philip and Kevin,

when you have a moment, can you please send us an inventory of the images
you would like to ingest into Colton's system.  Specifically:

- Total number of images
- Total volume/size
- Average size of a single image, if known

### metadata mapping for NARA
 
### php wrapper to at least print to image-level metadata
 
## 3. needs-attention

### tools for pre-ingest metadata validation
 
### Process for uploading images and metadata to the RDA, post-metadata verification.

### Unpack old_weather MongoDB Backup

On 11-Jul-2019 21:13:23 UTC, Philip Brohan <philip@brohan.org> wrote:

On Sun, 7 Jul 2019, at 20:23, team@zooniverse.org wrote:

> Backed up Old Weather (269.423) MB
> (https://zooniverse-backups.s3.amazonaws.com/ouroboros/2019-07-08/standalone_p
> rojects/old_weather.tar.gz?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=A
> KIAJP2JR7SIDMCRNUAQ%2F20190708%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=2019
> 0708T022313Z&X-Amz-Expires=604800&X-Amz-SignedHeaders=host&X-Amz-Signature=d6a
> d1d3f0dbcf1eb212e0d83f63911a5ad884f1b0f3c3319d1fe9ae112ddd513)

## 4. waiting/planning/scheduling

### Media for SIParCS talk

On 11-Jul-2019 21:17:14 UTC,  Philip Brohan <philip@brohan.org> wrote:

https://vimeo.com/62031717
https://vimeo.com/71894765
https://vimeo.com/128684414

### practice SIParCS talk with cohort

## 5. goals/benchmarks

### talk abstract deadline
On 16-Jul-2019 16:11:33 UTC, Blake Lewis <bjlewis@ucar.edu> wrote:

Hi everyone,

[T]he due date for your project abstract is the morning of July 26th.
This abstract will go on your project webpages, which you can see here
<https://www2.cisl.ucar.edu/siparcs/presentations-2019>. Your talk and slides
will be archived on this site.

### reflect on initial rda-image-archive requirements/expectations/goals

## Project/System requirements

> - Bulk access for image packages - HTTPS addresses for images at some
> granularity - support programmatic discoverability and access.

> - Design a metadata schema to meet our discoverability and use cases

> - Web Service API to query database metadata

> - UI to query DB metadata through web service API. - Image storage as objects,
> probably not hierarchical see item 1.a) - any use from existing GeoTiff (e.g.
> landsat or sentinel image object discovery?) - Potentially, deployable in a
> public cloud

> - Easy import/export from storage - Transfer to end user via HTTPS or Globus

### implement boundary polygons at logbook level
 

### topology prelim
 

### algebra prelim
 
