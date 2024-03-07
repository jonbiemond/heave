"""Batch SQL operations."""
from sqlalchemy import Connection, MetaData
from sqlalchemy import Table as SqlTable
from sqlalchemy.exc import IntegrityError

from heave import Table


class InvalidDb(Exception):
    """Invalid Database Exception."""

    pass


def reflect_table(
    connection: Connection, table_name: str, schema: str | None = None
) -> SqlTable:
    """Reflect a table from the database."""
    metadata = MetaData()
    return SqlTable(table_name, metadata, autoload_with=connection, schema=schema)


def update_from_conflict(
    table: SqlTable,
    conflict: IntegrityError,
    header: tuple[str, ...],
    row: tuple[str, ...],
):
    """Write an update statement from a conflict."""
    constraint = next(
        c for c in table.constraints if c.name == conflict.orig.diag.constraint_name
    )
    id_map = {c.name: header.index(c.name) for c in constraint.c}
    val_map = {c: idx for idx, c in enumerate(header) if c not in id_map.keys()}
    update_stmt = (
        table.update()
        .where(*(getattr(table.c, c) == row[i] for c, i in id_map.items()))
        .values({c: row[i] for c, i in val_map.items()})
    )
    return update_stmt


def insert(
    connection: Connection,
    sql_table: SqlTable,
    data: Table,
    on_conflict: str | None = None,
) -> None:
    """Insert data into a table."""
    for row in data.rows:
        trans = connection.begin_nested()
        stmt = sql_table.insert().values(dict(zip(data.header, row)))
        try:
            connection.execute(stmt)
            trans.commit()
        except IntegrityError as exc:
            trans.rollback()
            if on_conflict == "nothing":
                continue
            if on_conflict == "update":
                # cannot write an update if the error does not have diagnostic info
                if not hasattr(exc.orig, "diag"):
                    raise InvalidDb(
                        "Database does not support UPDATE ON CONFLICT."
                    ) from None
                update_stmt = update_from_conflict(sql_table, exc, data.header, row)
                connection.execute(update_stmt)
                continue
            raise exc from exc


def read(connection: Connection, sql_table: SqlTable) -> Table:
    """Read data from a table."""
    result = connection.execute(sql_table.select())
    return Table([tuple(sql_table.columns.keys()), *result])
