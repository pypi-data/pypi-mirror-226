import math
import json
from pyspark.sql.functions import length
from factorycore_utils.string_helpers import Case, convert_case, list_to_delimited_string


def prepare_replace_partition_clause(df, partition_columns_to_replace_list):
    """
    Return a ReplacePartition clause containing the Partition Columns and their distinct list of values.

    Parameters:
    df - Dataframe
    partition_columns_to_replace_list - List of column names of the Partitions to replace
    """

    replace_partition_clause = ""

    for col_name in partition_columns_to_replace_list:
        distinct_values = [str(ele[col_name]) for ele in df.select(col_name).distinct().collect()]

        if len(distinct_values) > 0:
            replace_partition_clause += f" and {col_name} in ('" + "', '".join(distinct_values) + "')"

    if len(replace_partition_clause) > 0:
        replace_partition_clause = replace_partition_clause[5:]

    return replace_partition_clause


def prepare_merge_statement_generic(source_name, target_table_name, business_key_column_list):
    """
    Return a SQL Statement that will perform a generic Merge

    Parameters:
    source_name - Name of the Source View/Table
    target_table_name - Fully qualified name of the target Table
    business_key_column_list - List of the Business Keys of the Table
    """

    generic_merge_sql = f"""
    merge into {target_table_name} t
    using {source_name} s
        on """ \
    + """
        and """.join(f"t.{i} <=> s.{i}" for i in business_key_column_list) \
    + """
    when matched then update set *
    when not matched then insert *
    """

    return generic_merge_sql


def prepare_dimension_create_table_script(df, database_name, table_name, table_location, table_data_view_name, business_key_column_list, surrogate_key_column_name, row_is_current_column_name, row_start_date_column_name, row_end_date_column_name):
    """
    Return two SQL statements; one that will CREATE the Dimension table with Identity Surrogate Key column; one that will populate the Dimension table with initial data.

    Parameters:
    df - The Dataframe containing the data and structure for the Dimension Table
    database_name - Name of the Database where the Dimension Table will be created
    table_name - Name of the Dimension Table
    table_location - Path to the Data Lake location housing the External Table
    table_data_view_name - The temporary view name that the Dataframe will be represented by
    business_key_column_list - List of the Business Keys of the Table
    surrogate_key_column_name - Column name of the Surrogate Key
    row_is_current_column_name - Column name of the Dimension control column 'Row Is Current' 
    row_start_date_column_name - Column name of the Dimension control column 'Row Start Date' 
    row_end_date_column_name - Column name of the Dimension control column 'Row End Date' 
    """

    column_list = ", ".join(df.schema.names)
    dimension_table_columns = f"{surrogate_key_column_name} bigint generated always as identity, {row_is_current_column_name} boolean generated always as (if({row_end_date_column_name} = '9999-12-31', true, false)), {row_start_date_column_name} timestamp, {row_end_date_column_name} timestamp, " + ", ".join(f"{n} {t}" for n,t in df.dtypes)
    
    create_dimension_table_script = f"create table if not exists {database_name}.{table_name} ({dimension_table_columns}) using delta location '{table_location}';"

    populate_dimension_table_script = f"""
    insert into {database_name}.{table_name} 
        ({row_start_date_column_name}
        ,{row_end_date_column_name}
        ,{column_list})

    select 
        current_timestamp
        ,'9999-12-31'
        ,{column_list} 
    from {table_data_view_name}
    order by {business_key_column_list};"""
    
    return create_dimension_table_script, populate_dimension_table_script


def prepare_create_table_script_external_and_managed(df, fully_qualified_table_name, table_location, surrogate_key_column_name, row_is_current_column_name, row_start_date_column_name, row_end_date_column_name, is_dimension, generated_column_list):
    """
    Return the CREATE table script.

    Parameters:
    df - The Dataframe containing the data and structure for the Dimension Table
    fully_qualified_table_name - The fully-qualified name of the Dimension Table i.e. catalog.database.table
    table_location - Path to the Data Lake location housing the External Table
    table_data_view_name - The temporary view name that the Dataframe will be represented by
    surrogate_key_column_name - Column name of the Surrogate Key
    row_is_current_column_name - Column name of the Dimension control column 'Row Is Current' 
    row_start_date_column_name - Column name of the Dimension control column 'Row Start Date' 
    row_end_date_column_name - Column name of the Dimension control column 'Row End Date' 
    is_dimension - Boolean indicating if this table is a Dimension
    generated_column_list - List of columns to create as Generated
    """

    table_columns = ", ".join(f"{n} {t}" for n,t in df.dtypes)

    generated_columns = [i for i in generated_column_list if i["action"].lower() == "generated"]
    identity_columns = [i for i in generated_column_list if i["action"].lower() == "identity"]

    if len(generated_column_list) > 0:
        table_columns += ("" if len(generated_columns) == 0 else ", ") + ", ".join(f'{i.get("column_name")} {i.get("data_type")} generated always as ({i.get("generated_as")})' for i in generated_columns) + ("" if len(identity_columns) == 0 else ", ") + ", ".join(f'{i.get("column_name")} bigint generated always as identity {"" if i.get("starts_with") is None else "(start with " + i.get("starts_with") + ")"}' for i in identity_columns)

    if is_dimension:
        table_columns = f"{surrogate_key_column_name} bigint generated always as identity, {row_is_current_column_name} boolean generated always as (if({row_end_date_column_name} = '9999-12-31', true, false)), {row_start_date_column_name} timestamp, {row_end_date_column_name} timestamp, " + table_columns
    
    return f"create or replace table {fully_qualified_table_name} ({table_columns})" + (";" if table_location is None else f" using delta location '{table_location}';")


def prepare_merge_statement_for_type_1_dimension(source_name, target_table_name, surrogate_key_column_name, row_is_current_column_name, row_start_date_column_name, row_end_date_column_name, business_key_column_list, type_1_column_list, target_table_column_list):
    """
    Return a SQL Statement that will perform a Merge for a Type-1 Dimension

    Parameters:
    source_name - Name of the Source View/Table
    target_table_name - Fully qualified name of the target Table
    surrogate_key_column_name - Column name of the Surrogate Key
    row_is_current_column_name - Column name of the Dimension control column 'Row Is Current' 
    row_start_date_column_name - Column name of the Dimension control column 'Row Start Date' 
    row_end_date_column_name - Column name of the Dimension control column 'Row End Date' 
    business_key_column_list - List of the Business Keys of the Table
    type_1_column_list - List of Type-1 Columns
    target_table_column_list - List of Columns in the target Table with the exception of the Surrogate Key column
    """

    merge_type_1_sql = f"""
    merge into {target_table_name} t
    using {source_name} s
        on """ \
    + """
        and """.join(f"t.{i} <=> s.{i}" for i in business_key_column_list) \
    + """

    when matched then update set
        """ \
    + """
        ,""".join(f"t.{i} = s.{i}" for i in type_1_column_list) \
    + """

    when not matched then insert
    (
        """ \
    + """
        ,""".join(f"{i}" for i in target_table_column_list if i.lower() != row_is_current_column_name.lower()) \
    + """
    )
    values
    (
        """ \
    + """
        ,""".join("current_timestamp" if i.lower() == row_start_date_column_name.lower() else "'9999-12-31'" if i.lower() == row_end_date_column_name.lower() else f"s.{i}" for i in target_table_column_list if i.lower() != row_is_current_column_name.lower()) \
    + """
    )
    """

    return merge_type_1_sql

  
def prepare_merge_statement_for_type_2_dimension(source_name, target_table_name, surrogate_key_column_name, row_is_current_column_name, row_start_date_column_name, row_end_date_column_name, business_key_column_list, source_column_list, target_table_column_list):
    # Return a SQL Statement that will perform a Merge for a Type-2 Dimension

    # Parameters:
    # source_name - Name of the Source View/Table
    # target_table_name - Fully qualified name of the target Table
    # surrogate_key_column_name - Column name of the Surrogate Key
    # row_is_current_column_name - Column name of the Dimension control column 'Row Is Current' 
    # row_start_date_column_name - Column name of the Dimension control column 'Row Start Date' 
    # row_end_date_column_name - Column name of the Dimension control column 'Row End Date' 
    # business_key_column_list - List of the Business Keys of the Table
    # source_column_list - List of Columns in the Source
    # target_table_column_list - List of Columns in the target Table with the exception of the Surrogate Key column

    merge_type_2_sql = f"""
    merge into {target_table_name} t
    using (select
            """ \
    + """
            ,""".join(f"{i} as pk_{i}" for i in business_key_column_list) \
    + """
            ,""" \
    + """
            ,""".join(f"{i}" for i in source_column_list) \
    + f"""
        from {source_name}
        union all
        select
            """ \
    + """
            ,""".join(f"null as pk_{i}" for i in business_key_column_list) \
    + """
            ,""" \
    + """
            ,""".join(f"s.{i}" for i in source_column_list) \
    + f"""
        from {source_name} s
        join {target_table_name} t
            on """ \
    + """
            and """.join(f"s.{i} <=> t.{i}" for i in business_key_column_list) \
    + f"""
            and t.{row_is_current_column_name} = True) s
        on """ \
    + """
        and """.join(f"t.{i} <=> s.pk_{i}" for i in business_key_column_list) \
    + f"""

    when matched and t.{row_is_current_column_name} = True then update set
        t.{row_is_current_column_name} = False
        ,t.{row_end_date_column_name} = current_timestamp""" \
    + """

    when not matched then insert
    (
        """ \
    + """
        ,""".join(f"{i}" for i in target_table_column_list if i.lower() != row_is_current_column_name.lower()) \
    + """
    )
    values
    (
        """ \
    + """
        ,""".join("current_timestamp" if i.lower() == row_start_date_column_name.lower() else "'9999-12-31'" if i.lower() == row_end_date_column_name.lower() else f"s.{i}" for i in target_table_column_list if i.lower() != row_is_current_column_name.lower()) \
    + """
    )
    """

    return merge_type_2_sql


def prepare_source_for_type_1_dimension(source_name, source_column_list, changeset_name, target_table_name, target_column_list, business_key_column_list, row_start_date_column_name, row_end_date_column_name):
    """
    Return a SQL Statement that will represent the Source of the Merge for a Type-1 Dimension

    Parameters:
    source_name - Name of the Source View/Table
    source_column_list - List of all columns from Source
    changeset_name - Name of the Changeset that represents SCD Type-1 changes
    target_table_name - Fully qualified name of the target Table
    target_column_list - List of all columns from Target
    business_key_column_list - List of the Business Keys of the Table
    row_start_date_column_name - Column name of the Dimension control column 'Row Start Date' 
    row_end_date_column_name - Column name of the Dimension control column 'Row End Date' 
    """

    query = ("""
    select
      """ + ", ".join(f"s.{i}" for i in source_column_list) + f", t.{row_start_date_column_name}, t.{row_end_date_column_name}" + 
    f"""
    from {source_name} s
    join {changeset_name} d
      on """ + " and ".join(f"s.{i} = d.{i}" for i in business_key_column_list) +
    f"""
    join {target_table_name} t
      on """ + " and ".join(f"s.{i} = t.{i}" for i in business_key_column_list) +
    """

    union all

    select
      """ + ", ".join(f"s.{i}" for i in source_column_list) + f", current_timestamp as {row_start_date_column_name}, '9999-12-31' as {row_end_date_column_name}" +
    f"""
    from {source_name} s
    join {changeset_name} d
      on """ + " and ".join(f"s.{i} = d.{i}" for i in business_key_column_list) +
    f"""
    left join {target_table_name} t
      on """ + " and ".join(f"s.{i} = t.{i}" for i in business_key_column_list) +
    f"""
    where """ + " and ".join(f"t.{i} is null" for i in business_key_column_list))    

    return query


def prepare_source_for_type_2_dimension(source_name, source_column_list, changeset_name, target_table_name, target_column_list, business_key_column_list, row_start_date_column_name, row_end_date_column_name):
    """
    Return a SQL Statement that will represent the Source of the Merge for a Type-2 Dimension

    Parameters:
    source_name - Name of the Source View/Table
    source_column_list - List of all columns from Source
    changeset_name - Name of the Changeset that represents SCD Type-2 changes
    target_table_name - Fully qualified name of the target Table
    target_column_list - List of all columns from Target
    business_key_column_list - List of the Business Keys of the Table
    row_start_date_column_name - Column name of the Dimension control column 'Row Start Date' 
    row_end_date_column_name - Column name of the Dimension control column 'Row End Date' 
    """

    select_list = ""

    for i in source_column_list:
      if i.lower() in [j.lower() for j in business_key_column_list]:
        select_list += f", s.{i}"
      elif i.lower() not in  [j.lower() for j in target_column_list]:
        select_list += f", s.{i}"
      else:
        select_list += f", t.{i}"
    
    select_list += f", t.{row_start_date_column_name}, current_timestamp as {row_end_date_column_name}, 'End Current Row' as scd2_action"
    
    query = (f"""
    select
      {select_list[2:]}
    from {source_name} s
    join {changeset_name} d
      on """ + " and ".join(f"s.{i} = d.{i}" for i in business_key_column_list) +
    f"""
    join {target_table_name} t
      on """ + " and ".join(f"s.{i} = t.{i}" for i in business_key_column_list) +
    """

    union all 

    select 
      """ + ", ".join(f"s.{i}" for i in source_column_list) + f", current_timestamp as {row_start_date_column_name}, '9999-12-31' as {row_end_date_column_name}, if(" + " and ".join(f"t.{i} is null" for i in business_key_column_list) + f""", null, 'New Current Row') as scd2_action
    from {source_name} s
    join {changeset_name} d
      on """ + " and ".join(f"s.{i} = d.{i}" for i in business_key_column_list) +
    f"""
    left join {target_table_name} t
      on """ + " and ".join(f"s.{i} = t.{i}" for i in business_key_column_list))

    return query

  
def prepare_merge_statement_for_type_1_dimension_automerge(source_name, target_table_name, business_key_column_list, row_is_current_column_name):
    """
    Return a SQL Statement that will perform a Merge for a Type-1 Dimension

    Parameters:
    source_name - Name of the Source View/Table
    target_table_name - Fully qualified name of the target Table
    business_key_column_list - List of the Business Keys of the Table
    row_is_current_column_name - Column name of the Dimension control column 'Row Is Current'
    """

    merge_type_1_sql = (f"""
    merge into {target_table_name} t
    using {source_name} s
      on """ +
    """
      and """.join(f"t.{i} = s.{i}" for i in business_key_column_list) +
    f"""
      and t.{row_is_current_column_name} = True

    when matched then update set *
    when not matched then insert *;
    """)

    return merge_type_1_sql

  
def prepare_merge_statement_for_type_2_dimension_automerge(source_name, target_table_name, business_key_column_list, row_is_current_column_name):
    """
    Return a SQL Statement that will perform a Merge for a Type-1 Dimension

    Parameters:
    source_name - Name of the Source View/Table
    target_table_name - Fully qualified name of the target Table
    business_key_column_list - List of the Business Keys of the Table
    row_is_current_column_name - Column name of the Dimension control column 'Row Is Current' 
    """

    merge_type_2_sql = (f"""
    merge into {target_table_name} t
    using {source_name} s
      on """ +
    """
      and """.join(f"t.{i} = s.{i}" for i in business_key_column_list) +
    f"""
      and s.scd2_action = 'End Current Row'
      and t.{row_is_current_column_name} = True

    when matched then update set *
    when not matched then insert *
    """)

    return merge_type_2_sql


def prepare_surrogate_key_statement(table_name, surrogate_key_column_name, business_key_column_list):
    """
    Return a SQL statement that will update any NULL Surrogate Keys in a Dimension table

    Parameters:
    table_name - Fully qualified name of the Table
    surrogate_key_column_name - Column name of the Surrogate Key
    business_key_column_list - List of the Business Keys of the Table
    """

    surrogate_sql = f"""
    with max_surrogate_key_value as
    (
    select
        {surrogate_key_column_name}
        ,{list_to_delimited_string(business_key_column_list)}
        ,max({surrogate_key_column_name}) over () as MaxSurrogateKey
        ,row_number() over (order by case when {surrogate_key_column_name} is null then 0 else {surrogate_key_column_name} end, {list_to_delimited_string(business_key_column_list)}) as RowNum
    from {table_name}
    )
    ,new_surrogates as
    (
    select
        case
        when {surrogate_key_column_name} is null then RowNum + MaxSurrogateKey
        else {surrogate_key_column_name}
        end as new_surrogate_key
        ,{list_to_delimited_string(business_key_column_list)}
    from max_surrogate_key_value
    where {surrogate_key_column_name} is null
    )
    merge into {table_name} t
    using new_surrogates s
        on """ \
    + """
        and """.join(f"s.{i} <=> t.{i}" for i in business_key_column_list) \
    + f"""
    when matched and t.{surrogate_key_column_name} is null then update
        set t.{surrogate_key_column_name} = s.new_surrogate_key
    """

    return surrogate_sql


def prepare_dimension_view_statement(table_name, row_is_current_column_name):
    """
    Return a SQL statement that will create or replace a Dimension view that will return only the current records

    Parameters:
    table_name - Fully qualified name of the Table
    row_is_current_column_name - Column name of the Dimension control column RowIsCurrent 
    """

    view_name = ".view_".join(table_name.rsplit(".", 1))

    view_sql = f"""
    CREATE OR REPLACE VIEW {view_name}
    COMMENT 'Returns only the records where {row_is_current_column_name} is True'
    AS
    select *
    from {table_name}
    where {row_is_current_column_name} = True
    """

    return view_name, view_sql


def prepare_optimize_statement(table_name, zorder_columns_string="", replace_partition_clause=""):
    """
    Return a SQL statement that will optimize the Delta table

    Parameters:
    table_name - Fully qualified name of the Table
    zorder_columns_string - Comma-delimited string of Z-Order Columns
    replace_partition_clause - Clause representing the Partition(s) to replace
    """

    optimisation_sql = f"OPTIMIZE {table_name}"

    if replace_partition_clause != "":
        optimisation_sql += f"""
    WHERE {replace_partition_clause}"""

    if zorder_columns_string != "":
        optimisation_sql += f"""
    ZORDER BY ({zorder_columns_string})"""

    return optimisation_sql


def prepare_synapse_view_statement(df, database_name, table_name, destination_schema_name, alias_case: Case = Case.NO_CONVERSION, destination_data_source_name="DeltaLake", delta_path=None):
    if delta_path is None:
        delta_path = f"{database_name}/{table_name}"

    select_list = ""
    with_list = ""
    for col_name, data_type in df.dtypes:
        alias = "" if alias_case is Case.NO_CONVERSION else f" AS [{convert_case(col_name, alias_case)}]"
        select_list += f"        [{col_name}]{alias},\n"
        with_list += f"        [{col_name}] {convert_column_data_type_for_sql_server(data_type, df, col_name)},\n"

    view_sql = f"""
    CREATE OR ALTER VIEW [{destination_schema_name}].[{table_name}]
    AS

    SELECT
    {select_list[4:-2]}
    FROM OPENROWSET (
        BULK '{delta_path}',
        DATA_SOURCE = '{destination_data_source_name}',
        FORMAT = 'delta'
    )
    WITH (
    {with_list[4:-2]}
    ) as rows;
    GO
    """

    return view_sql


def prepare_synapse_view_from_unity_catalog(df, table_name, delta_path, destination_schema_name, alias_case: Case = Case.NO_CONVERSION, destination_data_source_name="DeltaLake"):

    select_list = ""
    with_list = ""

    for col_name, data_type in df.dtypes:
        alias = "" if alias_case is Case.NO_CONVERSION else f" AS [{convert_case(col_name, alias_case)}]"
        select_list += f"        [{col_name}]{alias},\n"
        with_list += f"        [{col_name}] {convert_column_data_type_for_sql_server(data_type, df, col_name)},\n"

    view_sql = f"""
    CREATE OR ALTER VIEW [{destination_schema_name}].[{table_name}]
    AS

    SELECT
    {select_list[4:-2]}
    FROM OPENROWSET (
        BULK '{delta_path}',
        DATA_SOURCE = '{destination_data_source_name}',
        FORMAT = 'delta'
    )
    WITH (
    {with_list[4:-2]}
    ) as rows;
    GO
    """

    return view_sql


def prepare_databricks_view_statement(df, database_name, table_name, destination_database_name, alias_case: Case = Case.NO_CONVERSION, view_name=None):
    view_name = f"view_{table_name}" if view_name is None else view_name

    select_list = ""
    for col_name in df.columns:
        alias = "" if alias_case is Case.NO_CONVERSION else f" AS `{convert_case(col_name, alias_case)}`"
        select_list += f"        {col_name}{alias},\n"

    view_sql = f"""
    CREATE OR REPLACE VIEW {destination_database_name}.{view_name}
    AS

    SELECT
    {select_list[4:-2]}
    FROM {database_name}.{table_name};
    """

    return view_sql


def scale_column_length(length):
    new_length = 0

    if length <= 2:
        new_length = length
    elif length <= 5:
        new_length = 10
    elif length <= 15:
        new_length = 20
    elif length <= 30:
        new_length = 50
    elif length <= 80:
        new_length = 100
    else:
        new_length = int(math.ceil((length + length) / 100.0)) * 100

    return new_length


def convert_column_data_type_for_sql_server(data_type, df=None, col_name=None):
    result = ""

    if data_type == 'string':
        length = scale_column_length(get_max_length(df, col_name))
        # If there's no data in a column, default the length to 100.
        length = 100 if length == 0 else length
        result = f"varchar({length})"
    elif data_type == 'timestamp':
        result = "datetime"
    elif data_type == 'boolean':
        result = "bit"
    elif data_type == 'double':
        result = "float"
    else:
        result = data_type

    return result


def get_max_length(df, col_name):
    max_length = df.select(length(col_name)).groupby().max().collect()[0][0]
    # If every row contains None, return zero instead.
    return 0 if max_length is None else max_length


def prepare_create_table_script_if_schema_additions(df, schema_change_list, fully_qualified_table_name):
    """
    Return a CREATE TABLE script with the generated columns included.

    Parameters:
    df - The Dataframe containing the data and structure for the Table
    schema_change_list - JSON array containing the changes to the schema
    fully_qualified_table_name - The fully-qualified name of the Delta Table i.e. database.table
    """

    if schema_change_list is not None:
        schema_changes = schema_change_list
        if isinstance(schema_change_list, str):
            schema_changes = json.loads(schema_change_list)

        generated_items = [i for i in schema_changes if i["action"].lower() == "generated"]
        identity_items = [i for i in schema_changes if i["action"].lower() == "identity"]

        create_table_script = ""

        if len(generated_items) + len(identity_items) > 0:
            create_table_script = f"create table {fully_qualified_table_name} (" + ", ".join([f"{col_name} {data_type}" for col_name, data_type in df.dtypes])

        if len(generated_items) > 0:
            create_table_script += ", " + ", ".join([f'{item.get("column_name")} {item.get("data_type")} generated always as ({item.get("generated_as")})' for item in generated_items])

        if len(identity_items) > 0:
            create_table_script += ", " + ", ".join([f'{item.get("column_name")} bigint generated always as identity' for item in identity_items])
            
        create_table_script += ")"

    return create_table_script
