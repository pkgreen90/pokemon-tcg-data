# pokemon-tcg-data

A collection of files containing data for the Pokemon trading card game

## Description

This is a repository that contains the raw data for a Pokemon TCG database. Within the 'data' directory is a colelction of tab seperated files.  
The purpose of this data is to make freely available any information that would enable someone to manage their own collection, as this dataset provides additional information that other datasets do not include (hidden attributes for each card).

## Contents

- [pokemon-tcg-data](#pokemon-tcg-data)
  - [Description](#description)
  - [Contents](#contents)
  - [Structure](#structure)
  - [Schema](#schema)
    - [entity_relationship_digrams](#entity_relationship_digrams)
    - [exported_images](#exported_images)
    - [Schemas](#schemas)
  - [Contributing](#contributing)
  - [License](#license)

## Structure

The table below describes the structure of this repository.

| Directory | Purpose |
| --- | --- |
| data | This contains the raw tab files. Some files use column from other files (see schema for further information) |
| schema | The schema for the files and how they related to each other |

## Schema

The schema directory makes use of a program called [Plantuml](https://plantuml.com/). This has a dependency upon [Graphviz](https://www.graphviz.org/download/).
The schema directory contains two sub-directories:

- entity_relationship_diagrams
- exported_images

### entity_relationship_digrams

This is the raw plantuml code files that are used to produce the exported images.

### exported_images

This directory contains the exported files that are used to display within other files.

### Schemas

The files provided as part of this repository are able to be directly imported into a database.

This is the main relationship between each of the files (tables) and the data schemas for each table.
![Main Database Schema](schema/exported_images/database-schema.svg)

This is the relationship between the energy cards and other tables
![Energy Card Relationships](schema/exported_images/energy-card-relationships.svg)

This is the relationship between the pokemon cards and other tables
![Energy Card Relationships](schema/exported_images/
![Pokemon Card Relationships](schema/exported_images/pokemon-card-relationships.svg)

This is the relationship between the trainers cards and other tables
![Energy Card Relationships](schema/exported_images/
![Trainer Card Relationships](schema/exported_images/trainer-card-relationships.svg)

## Contributing

Feel free to make a branch and contribute to this repository where you see missing or incorrect data.

1. Clone the repository
2. Create your feature branch (git checkout -b feature/my-new-feature)
3. Commit your changes (git commit -am 'Add some feature')
4. Push to the branch (git push origin feature/my-new-feature)
5. Create a new Pull Request

## License

This project is licensed under the Apache License 2.0 scheme, see license file within repository for further details.
