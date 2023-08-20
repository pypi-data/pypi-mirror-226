import warnings
from sql import inspect
import difflib
from sql.connection import ConnectionManager
from sql.store import store, _get_dependents_for_key
from sql import exceptions, display
import json
from pathlib import Path
from ploomber_core.dependencies import requires

try:
    import toml
except ModuleNotFoundError:
    toml = None

SINGLE_QUOTE = "'"
DOUBLE_QUOTE = '"'


def sanitize_identifier(identifier):
    if (identifier[0] == SINGLE_QUOTE and identifier[-1] == SINGLE_QUOTE) or (
        identifier[0] == DOUBLE_QUOTE and identifier[-1] == DOUBLE_QUOTE
    ):
        return identifier[1:-1]
    else:
        return identifier


def convert_to_scientific(value):
    """
    Converts value to scientific notation if necessary

    Parameters
    ----------
    value : any
        Value to format.
    """
    if (
        isinstance(value, (int, float))
        and not isinstance(value, bool)
        and _is_long_number(value)
    ):
        new_value = "{:,.3e}".format(value)

    else:
        new_value = value

    return new_value


def _is_long_number(num) -> bool:
    """
    Checks if num's digits > 10
    """
    if "." in str(num):
        split_by_decimal = str(num).split(".")
        if len(split_by_decimal[0]) > 10 or len(split_by_decimal[1]) > 10:
            return True
    return False


def get_suggestions_message(suggestions):
    suggestions_message = ""
    if len(suggestions) > 0:
        _suggestions_string = pretty_print(suggestions, last_delimiter="or")
        suggestions_message = f"\nDid you mean : {_suggestions_string}"
    return suggestions_message


def is_table_exists(
    table: str,
    schema: str = None,
    ignore_error: bool = False,
    conn=None,
) -> bool:
    """
    Checks if a given table exists for a given connection

    Parameters
    ----------
    table: str
        Table name

    schema: str, default None
        Schema name

    ignore_error: bool, default False
        Avoid raising a ValueError
    """
    if table is None:
        if ignore_error:
            return False
        else:
            raise exceptions.UsageError("Table cannot be None")
    if not ConnectionManager.current:
        raise exceptions.RuntimeError("No active connection")
    if not conn:
        conn = ConnectionManager.current

    table = strip_multiple_chars(table, "\"'")

    if schema:
        table_ = f"{schema}.{table}"
    else:
        table_ = table

    _is_exist = _is_table_exists(table_, conn)

    if not _is_exist:
        if not ignore_error:
            try_find_suggestions = not conn.is_dbapi_connection
            expected = []
            existing_schemas = []
            existing_tables = []

            if try_find_suggestions:
                existing_schemas = inspect.get_schema_names()

            if schema and schema not in existing_schemas:
                expected = existing_schemas
                invalid_input = schema
            else:
                if try_find_suggestions:
                    existing_tables = _get_list_of_existing_tables()

                expected = existing_tables
                invalid_input = table

            if schema:
                err_message = (
                    f"There is no table with name {table!r} in schema {schema!r}"
                )
            else:
                err_message = (
                    f"There is no table with name {table!r} in the default schema"
                )

            if table not in list(store):
                suggestions = difflib.get_close_matches(invalid_input, expected)
                suggestions_store = difflib.get_close_matches(
                    invalid_input, list(store)
                )
                suggestions.extend(suggestions_store)
                suggestions_message = get_suggestions_message(suggestions)
                if suggestions_message:
                    err_message = f"{err_message}{suggestions_message}"
            raise exceptions.TableNotFoundError(err_message)

    return _is_exist


def _get_list_of_existing_tables() -> list:
    """
    Returns a list of table names for a given connection
    """
    tables = []
    tables_rows = inspect.get_table_names()._table
    for row in tables_rows:
        table_name = row.get_string(fields=["Name"], border=False, header=False).strip()

        tables.append(table_name)
    return tables


def pretty_print(
    obj: list, delimiter: str = ",", last_delimiter: str = "and", repr_: bool = False
) -> str:
    """
    Returns a formatted string representation of an array
    """
    if repr_:
        sorted_ = sorted(repr(element) for element in obj)
    else:
        sorted_ = sorted(f"'{element}'" for element in obj)

    if len(sorted_) > 1:
        sorted_[-1] = f"{last_delimiter} {sorted_[-1]}"

    return f"{delimiter} ".join(sorted_)


def strip_multiple_chars(string: str, chars: str) -> str:
    """
    Trims characters from the start and end of the string
    """
    return string.translate(str.maketrans("", "", chars))


def is_saved_snippet(table: str) -> bool:
    if table in list(store):
        display.message(f"Plotting using saved snippet : {table}")
        return True
    return False


def _is_table_exists(table: str, conn) -> bool:
    """
    Runs a SQL query to check if table exists
    """
    if not conn:
        conn = ConnectionManager.current

    identifiers = conn.get_curr_identifiers()

    for iden in identifiers:
        if isinstance(iden, tuple):
            query = "SELECT * FROM {0}{1}{2} WHERE 1=0".format(iden[0], table, iden[1])
        else:
            query = "SELECT * FROM {0}{1}{0} WHERE 1=0".format(iden, table)
        try:
            conn.execute(query)
            return True
        except Exception:
            pass

    return False


def flatten(src, ltypes=(list, tuple)):
    """The flatten function creates a new tuple / list
    with all sub-tuple / sub-list elements concatenated into it recursively

    Parameters
    ----------
    src : tuple / list
        Source tuple / list with all sub-tuple / sub-list elements
    ltypes : tuple, optional
        sub element's data type, by default (list, tuple)

    Returns
    -------
    tuple / list
        Flatten tuple / list
    """
    ltype = type(src)
    # Create a process list to handle flatten elements
    process_list = list(src)
    i = 0
    while i < len(process_list):
        while isinstance(process_list[i], ltypes):
            if not process_list[i]:
                process_list.pop(i)
                i -= 1
                break
            else:
                process_list[i : i + 1] = process_list[i]
        i += 1

    # If input src data type is tuple, return tuple
    if not isinstance(process_list, ltype):
        return tuple(process_list)
    return process_list


def support_only_sql_alchemy_connection(command):
    """
    Throws a sql.exceptions.RuntimeError if connection is not SQLAlchemy
    """
    if ConnectionManager.current.is_dbapi_connection:
        raise exceptions.RuntimeError(
            f"{command} is only supported with SQLAlchemy "
            "connections, not with DBAPI connections"
        )


def fetch_sql_with_pagination(
    table, offset, n_rows, sort_column=None, sort_order=None
) -> tuple:
    """
    Returns next n_rows and columns from table starting at the offset

    Parameters
    ----------
    table : str
        Table name

    offset : int
        Specifies the number of rows to skip before
        it starts to return rows from the query expression.

    n_rows : int
        Number of rows to return.

    sort_column : str, default None
        Sort by column

    sort_order : 'DESC' or 'ASC', default None
        Order list
    """
    is_table_exists(table)

    order_by = "" if not sort_column else f"ORDER BY {sort_column} {sort_order}"

    query = f"""
    SELECT * FROM {table} {order_by}
    OFFSET {offset} ROWS FETCH NEXT {n_rows} ROWS ONLY"""

    rows = ConnectionManager.current.execute(query).fetchall()

    columns = ConnectionManager.current.raw_execute(
        f"SELECT * FROM {table} WHERE 1=0"
    ).keys()

    return rows, columns


def parse_sql_results_to_json(rows, columns) -> str:
    """
    Serializes sql rows to a JSON formatted ``str``
    """
    dicts = [dict(zip(list(columns), row)) for row in rows]
    rows_json = json.dumps(dicts, indent=4, sort_keys=True, default=str).replace(
        "null", '"None"'
    )

    return rows_json


def get_all_keys():
    """

    Returns
    -------
    All stored snippets in the current session
    """
    return list(store)


def get_key_dependents(key: str) -> list:
    """
    Function to find the stored snippets dependent on key
    Parameters
    ----------
    key : str, name of the table

    Returns
    -------
    list
        List of snippets dependent on key

    """
    deps = _get_dependents_for_key(store, key)
    return deps


def del_saved_key(key: str) -> str:
    """
    Deletes a stored snippet
    Parameters
    ----------
    key : str, name of the snippet to be deleted

    Returns
    -------
    list
        Remaining stored snippets
    """
    all_keys = get_all_keys()
    if key not in all_keys:
        raise exceptions.UsageError(f"No such saved snippet found : {key}")
    del store[key]
    return get_all_keys()


def show_deprecation_warning():
    """
    Raises CTE deprecation warning
    """
    warnings.warn(
        "CTE dependencies are now automatically inferred, "
        "you can omit the --with arguments. Using --with will "
        "raise an exception in the next major release so please remove it.",
        FutureWarning,
    )


def find_path_from_root(file_name):
    """
    Recursively finds an absolute path to file_name starting
    from current to root directory
    """
    current = Path().resolve()
    while not (current / file_name).exists():
        if current == current.parent:
            return None

        current = current.parent
    display.message(f"Found {file_name} from '{current}'")

    return str(Path(current, file_name))


def find_close_match_config(word, possibilities, n=3):
    """Finds closest matching configurations and displays message"""
    closest_matches = difflib.get_close_matches(word, possibilities, n=n)
    if not closest_matches:
        display.message_html(
            f"'{word}' is an invalid configuration. Please review our "
            "<a href='https://jupysql.ploomber.io/en/latest/api/configuration.html#options'>"  # noqa
            "configuration guideline</a>."
        )
    else:
        display.message(
            f"'{word}' is an invalid configuration. Did you mean "
            f"{pretty_print(closest_matches, last_delimiter='or')}?"
        )


def get_line_content_from_toml(file_path, line_number):
    """
    Locates a line that error occurs when loading a toml file
    and returns the line, key, and value
    """
    with open(file_path, "r") as file:
        lines = file.readlines()
        eline = lines[line_number - 1].strip()
        ekey, evalue = None, None
        if "=" in eline:
            ekey, evalue = map(str.strip, eline.split("="))
        return eline, ekey, evalue


def to_upper_if_snowflake_conn(conn, upper):
    return (
        upper.upper()
        if callable(conn._get_sqlglot_dialect)
        and conn._get_sqlglot_dialect() == "snowflake"
        else upper
    )


@requires(["toml"])
def load_toml(file_path):
    """
    Returns toml file content in a dictionary format
    and raises error if it fails to load the toml file
    """
    try:
        with open(file_path, "r") as file:
            content = file.read()
            return toml.loads(content)
    except toml.TomlDecodeError as e:
        raise parse_toml_error(e, file_path)


def parse_toml_error(e, file_path):
    eline, ekey, evalue = get_line_content_from_toml(file_path, e.lineno)
    if "Duplicate keys!" in str(e):
        return exceptions.ConfigurationError(f"Duplicate key found : '{ekey}'")
    elif "Only all lowercase booleans" in str(e):
        return exceptions.ConfigurationError(
            f"Invalid value '{evalue}' in '{eline}'. "
            "Valid boolean values: true, false"
        )
    elif "invalid literal for int()" in str(e):
        return exceptions.ConfigurationError(
            f"Invalid value '{evalue}' in '{eline}'. "
            "To use str value, enclose it with ' or \"."
        )
    else:
        return e


def get_user_configs(file_path, section_names):
    """
    Returns saved configuration settings in a toml file from given file_path

    Parameters
    ----------
    file_path : str
        file path to a toml file
    section_names : list
        section names that contains the configuration settings
        (e.g., ["tool", "jupysql", "SqlMagic"])

    Returns
    -------
    dict
        saved configuration settings
    """
    data = load_toml(file_path)
    while section_names:
        section_to_find, sections_from_user = section_names.pop(0), data.keys()
        if section_to_find not in sections_from_user:
            close_match = difflib.get_close_matches(section_to_find, sections_from_user)
            if not close_match:
                return {}
            else:
                raise exceptions.ConfigurationError(
                    f"{pretty_print(close_match)} is an invalid section name. "
                    f"Did you mean '{section_to_find}'?"
                )
        data = data[section_to_find]
    return data


def get_default_configs(sql):
    """
    Returns a dictionary of SqlMagic configuration settings users can set
    with their default values.
    """
    default_configs = sql.trait_defaults()
    del default_configs["parent"]
    del default_configs["config"]
    return default_configs


def _are_numeric_values(*values):
    return all([isinstance(value, (int, float)) for value in values])


def validate_mutually_exclusive_args(arg_names, args):
    """
    Raises ValueError if a list of values from arg_names filtered by
    args' boolean representations is longer than one.

    Parameters
    ----------
    arg_names : list
        args' names in string
    args : list
        args values
    """
    specified_args = [arg_name for arg_name, arg in zip(arg_names, args) if arg]
    if len(specified_args) > 1:
        raise exceptions.ValueError(
            f"{pretty_print(specified_args)} are specified. "
            "You can only specify one of them."
        )
