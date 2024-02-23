# Heave

Heave is a CLI tool for batch inserting or updating data into a database.

## Installation

...

## Usage

`heave [OPTIONS] COMMAND [ARGS]...`

Create a connection to a PostgreSQL database.

Defaults to the `postgres` database on `localhost` with the `postgres` user.
Pass alternate connection parameters as options.

#### Options

`-h`, `--host TEXT (default: localhost)`
- Host name of the database.

`-p`, `--port INTEGER (default: 5432)`
- Port number at which the database is listening.

`-U`, `--username TEXT`
- Username to connect as.

`-d`, `--dbname TEXT (default: postgres)`
- Name of the database to connect to.

#### Examples

```bash
heave --host myhost --port 5433 --username myuser --dbname mydb
```

### heave insert

`heave insert --table TEXT <file>`

Insert data from a file into a table.

#### Options

`-t`, `--table TEXT`
- Name of the table to insert into. Required.

#### Examples

```bash
heave insert --table mytable data.csv
```

## Supported Formats

...

### Sources

...

### Databases

...

## Examples

...

## Contributing

...