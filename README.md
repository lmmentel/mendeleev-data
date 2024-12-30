# mendeleev-data

<!-- PROJECT LOGO -->
<br />
<p align="center">
  <a href="https://github.com/lmmentel/mendeleev">
    <img src=".assets/name_and_logo.png" alt="Logo" width="300">
  </a>

  <h3 align="center">Data assets for <a href="https://github.com/lmmentel/mendeleev">mendeleev</a> python package</h3>

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
