# mendeleev-data

<!-- PROJECT LOGO -->
<br />
<p align="center">
  <a href="https://github.com/lmmentel/mendeleev">
    <img src=".assets/name_and_logo.png" alt="Logo" width="300">
  </a>

  <h3 align="center">Data assets for <a href="https://github.com/lmmentel/mendeleev">mendeleev</a> python package</h3>

## Current Version

This repository contains data for **mendeleev v0.20.1**.

[View mendeleev v0.20.1 release notes](https://github.com/lmmentel/mendeleev/releases/tag/v0.20.1)


## Previous Versions

| Data Release | Mendeleev Release |
|---|---|
| [v1.0.0](https://github.com/lmmentel/mendeleev-data/releases/tag/v1.0.0) | [mendeleev v1.0.0](https://github.com/lmmentel/mendeleev/releases/tag/v1.0.0) |
| [v0.20.1](https://github.com/lmmentel/mendeleev-data/releases/tag/v0.20.1) | [mendeleev v0.20.1](https://github.com/lmmentel/mendeleev/releases/tag/v0.20.1) |
| [v0.20.0](https://github.com/lmmentel/mendeleev-data/releases/tag/v0.20.0) | [mendeleev v0.20.0](https://github.com/lmmentel/mendeleev/releases/tag/v0.20.0) |
| [v0.19.0](https://github.com/lmmentel/mendeleev-data/releases/tag/v0.19.0) | [mendeleev v0.19.0](https://github.com/lmmentel/mendeleev/releases/tag/v0.19.0) |


## Data

All tables from the [mendeleev](https://github.com/lmmentel/mendeleev) package are exported:

- `alembic_version`: Latest database version.
- `elements`: Main table with elemental properties.
- `groups`: Periodic table group data.
- `ionicradii`: Ionic radii data.
- `ionizationenergies`: Ionization energy data.
- `isotopedecaymodes`: Decay modes for isotopes.
- `isotopes`: Main table with isotope data.
- `oxidationstates`: Oxidation states.
- `phasetransitions`: Phase tranistion data for elements.
- `propertymetadata`: Metadata about peperties in `mendeleev` such as units, references etc.
- `scattering_factors`: Atomic scattering factors data.
- `screeningconstants`: Nuclear screening constants data.
- `series`: Periodic table series data.

To get the schema details for each table see the [mendeleev.dbml](mendeleev.dbml) file.

## Available formats

All data that is stored in mendeleev's sqlite database is made available in the follwing formats:

- `csv`
- `html`
- `json`
- `sql`
- `markdown`

Except for the `sql` dump, where all contents are contained in a single file, all other formats are exported so that each file corresponds to a separate table from the mendeleev's data model. 

For more information about formats please look into [sqlite3 docs](https://www.sqlite.org/cli.html).

## Overview

You can view the complete [changelog](https://github.com/lmmentel/mendeleev/blob/master/CHANGES.rst) in the mendeleev repo or view it in the [docs](https://mendeleev.readthedocs.io/en/stable/changes_link.html).

To restore mendeleev's sqlite3 database run:

```bash
cat data/sql/mendeleev.sql | sqlite3 mendeleev.sqlite
```

## Generate schema

```bash
docker run \
  --mount type=bind,source="$(pwd)",target=/home/schcrwlr/share \
  --rm -it \
  schemacrawler/schemacrawler \
  /opt/schemacrawler/bin/schemacrawler.sh \
  --server=sqlite \
  --database=share/elements.db \
  --info-level=standard \
  --command script \
  --script-language python \
  --script dbml.py > mendeleev.dbml
```
