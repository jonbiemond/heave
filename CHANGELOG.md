# CHANGELOG



## v0.3.0 (2024-03-12)

### Chore

* chore: extend ruff lint rules ([`1026b08`](https://github.com/jonbiemond/heave/commit/1026b08ccbd8942fb111f10bce46bbc2f85d8d09))

### Documentation

* docs: add on-conflict option ([`d6980f6`](https://github.com/jonbiemond/heave/commit/d6980f64c7f17e6ff65b0420028a7d4de4384db8))

### Feature

* feat(cli): neatly handle invalid directory

Raise a user friendly CLick error
if user passes a directory that doesn&#39;t exist to the read command.

Closes #5 ([`b10c891`](https://github.com/jonbiemond/heave/commit/b10c8914e6597f0e6c37571ea5d6787e431c3ea3))

* feat(cli): add on-conflict option to insert

Allow user to specify how insert conflicts should be handled.

Closes #14 ([`c27986a`](https://github.com/jonbiemond/heave/commit/c27986a6a272f58af78edd24976ee2e6c46ba2d7))

* feat(sql): handle conflicts on insert

Add parameter to handle conflicts by doing nothing or emitting an update. ([`c8a75e1`](https://github.com/jonbiemond/heave/commit/c8a75e1fd805b7090545f1bc90c9e98bfde1a7a9))


## v0.2.0 (2024-03-05)

### Documentation

* docs: add contributing instructions ([`4feb311`](https://github.com/jonbiemond/heave/commit/4feb3114214906af47d7785e89fbbbbcb365b963))

### Feature

* feat(cli): add schema option

Allow user to specify table schema.

Closes #11 ([`e348668`](https://github.com/jonbiemond/heave/commit/e34866851ecc13ffb3d481c6717d84e3e0f96f7e))


## v0.1.0 (2024-03-01)

### Chore

* chore: ignore fleet config files ([`5f77d8c`](https://github.com/jonbiemond/heave/commit/5f77d8c87f9f023bd66d5a354402fde9ba3d24ac))

* chore: add lint and format hooks ([`c4ec67c`](https://github.com/jonbiemond/heave/commit/c4ec67c897356818748500ab2817366e9b205742))

* chore: ruff and semantic-release config ([`752caf9`](https://github.com/jonbiemond/heave/commit/752caf967a651e5a2b110d20959c42c57cbcdb3d))

* chore: declare dependencies ([`ed11653`](https://github.com/jonbiemond/heave/commit/ed1165379c2e6e7de127091c8282323d73fd0042))

### Ci

* ci: add semantic release workflow ([`9ce601e`](https://github.com/jonbiemond/heave/commit/9ce601ed475c8aaa4032f906044891451bc5ed25))

* ci: init ci.yml

Add GitHub Action config to run linter, formatter and tests as CI. ([`27debb3`](https://github.com/jonbiemond/heave/commit/27debb3fd3607e6ab36484aaa71767c736a98ab9))

### Documentation

* docs: add install instructions ([`b60500c`](https://github.com/jonbiemond/heave/commit/b60500c97e5325a5549723aef50dea765cfd44f4))

* docs: list supported formats ([`6e56bb5`](https://github.com/jonbiemond/heave/commit/6e56bb53af8962e85541af45f9c580a7a09a7664))

* docs: add usage instructions ([`fa6c835`](https://github.com/jonbiemond/heave/commit/fa6c835d1e01cd40181d8be13d9da01405e02bd4))

* docs: initialize README.md ([`9e29a63`](https://github.com/jonbiemond/heave/commit/9e29a6380cf7a41d53bf45188258e246021ea479))

### Feature

* feat(cli): add read command

Add command to read data from an SQL table
and write it to a CSV file. ([`e67ba58`](https://github.com/jonbiemond/heave/commit/e67ba58a7ffa68c6252595a3d6fc478c48c0dd72))

* feat: add sql.read and file.write_csv functions

Add a function to read data from an SQL table.
Add a function to write data to a CSV file. ([`450797a`](https://github.com/jonbiemond/heave/commit/450797a1e0c3269f75470ad9cc32d5898823428b))

* feat: store table data in tuples

Table data should not be altered from read to write,
so it is sensible to store as a list of immutable tuples rather than lists. ([`0d93043`](https://github.com/jonbiemond/heave/commit/0d930438154948d39fc8d9c76b9f97772bb290f7))

* feat(cli): read connection parameters from environment variables

Add missing variables for user and database name. ([`e322202`](https://github.com/jonbiemond/heave/commit/e3222023417edda42f608446c33f62e0956b2baa))

* feat(cli): add cli to connect to a database and insert data

Create a connect function to handle creating and validating database connections.
Define the base command to accept connection parameters,
especially for PostgreSQL databases.
Create an insert command to read data from a CSV file
and insert it into an SQL table. ([`c376054`](https://github.com/jonbiemond/heave/commit/c3760547f7c63be7ae3e2e611009015f0e353c79))

* feat: create extract and batch functions

Add a function to read a csv into a custom Table object.
Add function to batch insert data into an SQL table. ([`bb2b712`](https://github.com/jonbiemond/heave/commit/bb2b7120a6b2c75a3340262b3448737c23b133b5))

### Refactor

* refactor: rename modules extract to file and batch to sql

Module names now reflect the data source rather than direction. ([`da70f9b`](https://github.com/jonbiemond/heave/commit/da70f9b7c255216ba6a052c136c4641e4f307ff3))

### Test

* test(cli): assert changes are not applied on error

Add a test inserts are rolled back if there is a SQL error. ([`306877e`](https://github.com/jonbiemond/heave/commit/306877e3f8b010e5133e0896cd085b36cb0e3e81))

* test: clear env vars before testing cli connection

If any of the database connection parameter environment variables are set
on the host, then they will be passed instead of the testing defaults. ([`ee4de45`](https://github.com/jonbiemond/heave/commit/ee4de4580f470c7ac67d4ff3ec8cd1c82af57a83))

* test: create test database and pytest fixture ([`b5b0f9d`](https://github.com/jonbiemond/heave/commit/b5b0f9dd765ea28f37f1bb233b47f7d667a9a52b))
