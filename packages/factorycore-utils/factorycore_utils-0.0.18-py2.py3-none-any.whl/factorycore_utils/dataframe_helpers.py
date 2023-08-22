from pyspark.sql.functions import lit
from factorycore_utils.string_helpers import remove_illegal_parquet_characters_from_delimited_string


def column_to_list(df, col_name):
    return [x[col_name] for x in df.select(col_name).collect()]


def two_columns_to_dictionary(df, key_col_name, value_col_name):
    k, v = key_col_name, value_col_name
    return {x[k]: x[v] for x in df.select(k, v).collect()}


def to_list_of_dictionaries(df):
    return list(map(lambda r: r.asDict(), df.collect()))


def show_output_to_df(show_output, spark):
    lst = show_output.split("\n")
    ugly_column_names = lst[1]
    pretty_column_names = [i.strip() for i in ugly_column_names[1:-1].split("|")]
    pretty_data = []
    ugly_data = lst[3:-1]
    for row in ugly_data:
        r = [i.strip() for i in row[1:-1].split("|")]
        pretty_data.append(tuple(r))
    return spark.createDataFrame(pretty_data, pretty_column_names)


def columns_in_dataframe_not_in_exclude_list(df, exclude_column_list=[], include_column_data_type_in_return=False):
    # Return a list of columns that exist in a Dataframe that are not in the exclude list

    # Parameters:
    # df - Dataframe
    # exclude_column_list - Case-insensitive List of columns to exclude.  Default empty.
    # include_column_data_type_in_return - Boolean that, when True, forces the return of the column's Data Type along with the Name. Default False.

    result = []

    if include_column_data_type_in_return:
        result = [(col_name.strip(), data_type.lower()) for col_name, data_type in df.dtypes if col_name.strip().lower() not in [i.lower() for i in exclude_column_list] and col_name]
    else:
        result = [col_name.strip() for col_name in df.schema.names if col_name.strip().lower() not in [i.strip().lower() for i in exclude_column_list] and col_name]

    return result


def find_correctly_cased_column_name(df, col_name):
    # Perform a case-insensitive search of a dataframe for a column name and return the correct case of that column name

    # Parameters:
    # df - Dataframe
    # col_name - Column to lookup in the dataframe

    result = None

    try:
        # this uses a generator to find the index if it matches, will raise an exception if not found
        result = df.columns[next(i for i, v in enumerate(df.schema.names) if v.lower() == col_name.lower())]
    except StopIteration:
        result = None

    return result


def add_column_to_dataframe(df, col_name, col_value, data_type, add_column_to_front=False):
    # Return a dataframe that has had a column added

    # Parameters:
    # df - Dataframe
    # col_name - Name of the Column to add
    # col_value - Value of the Column
    # data_type - Data Type of the Column
    # add_column_to_front - Boolean that, when True, will position this new Column at the front of the Dataframe. Default False.

    # Only proceed if column doesn't already exist
    if find_correctly_cased_column_name(df, col_name) is None:
        # Add the DataDate column to the front of the dataframe
        df = df.withColumn(col_name, lit(col_value).cast(data_type))

        if add_column_to_front:
            column_list = df.schema.names
            column_list.remove(col_name)
            df = df.select([col_name] + column_list)

    return df


def enforce_valid_parquet_column_names(df):
    # Return the dataframe with reworked column names if any violate parquet naming conventions

    # Parameters:
    # df - Dataframe

    dataframe_changed = False

    for col_name in df.schema.names:
        new_column_name = remove_illegal_parquet_characters_from_delimited_string(col_name)

        if new_column_name != col_name:
            df = df.withColumnRenamed(col_name, new_column_name)
            dataframe_changed = True

    return dataframe_changed, df


def synchronise_columns_between_source_and_target_dataframes(df_source, df_target, exclude_column_list=[]):
    # Return df_target with the addition of missing columns that are in df_source

    # Parameters:
    # df_source - Dataframe to use as reference for sync
    # df_target - Dataframe to change to achieve Column sync
    # exclude_column_list - Columns to exclude when reading Source

    source_columns_not_in_target_list = columns_in_dataframe_not_in_exclude_list(df_source, df_target.schema.names + exclude_column_list, True)

    for col_name, data_type in source_columns_not_in_target_list:
        print(f"Column '{col_name}' (data type {data_type}) added to target dataframe.')")
        df_target = df_target.withColumn(col_name, lit(None).cast(data_type))

    target_dataframe_schema_has_changed = False if len(source_columns_not_in_target_list) == 0 else True

    return target_dataframe_schema_has_changed, df_target


def create_temp_view_from_dataframe(df, is_global=False):
    # Saves the dataframe as a (global, if is_global is True) temp view and returns the random view name

    # Parameters:
    # df - Dataframe to save as temp view
    # is_global - Boolean indicator that, when true, will create a Global temp view

    import uuid

    # Get a unique name to call the View
    temp_view_name = uuid.uuid4().hex

    # Save the dataframe as the Temp View
    if is_global:
        df.createOrReplaceGlobalTempView(temp_view_name)
    else:
        df.createOrReplaceTempView(temp_view_name)

    return temp_view_name


def read_temp_view_into_dataframe(temp_view_name, spark, is_global=False):
    # Saves the dataframe as a (global, if is_global is True) temp view and returns the random view name

    # Parameters:
    # temp_view_name - Name of the temp view
    # spark - Spark context
    # is_global - Boolean indicator that specifies whether the temp view is global

    if is_global:
        global_temp_db = spark.conf.get("spark.sql.globalTempDatabase")
        df = spark.read.table(f"{global_temp_db}.{temp_view_name}")
    else:
        df = spark.read.table(temp_view_name)

    return df


def convert_columns_to_json_array(df_in, array_column_name, column_name_json_property_name, column_value_json_property_name, spark, columns_to_exclude=None):
    # Converts a list of columns into a single column JSON array or name/value structs.  Returns the original dataframe with this new column added.

    # Parameters:
    # df_in - The dataframe containing the columns to convert.
    # array_column_name - The name to assign to the JSON array column.
    # column_name_json_property_name - The name of the JSON property for the Column Name.
    # column_value_json_property_name - The name of the JSON property for the Column Value.
    # spark - Spark context.
    # columns_to_exclude - The list of df_in columns to ignore in the construction of the JSON array. Default None.

    # Save dataframe as temporary view
    source_name = "view_source"
    df_in.createOrReplaceTempView(source_name)
  
    # Prep optional parameter
    columns_to_exclude = [] if columns_to_exclude is None else columns_to_exclude
    
    # Select relevant columns to convert
    column_list = [c for c in df_in.columns if c not in columns_to_exclude]
  
    # Collapse columns into JSON array of name/value pairs
    select_prefix = "select " + ", ".join(columns_to_exclude) + ("" if len(columns_to_exclude) == 0 else ", ") + " array(struct("
    str = f", struct(".join([f"'{col}' as {column_name_json_property_name}, cast({col} as string) as {column_value_json_property_name})" for col in column_list])
    sql_string = f"{select_prefix}{str}) as {array_column_name} from {source_name}"
  
    # Return new dataframe containing new JSON array column
    return spark.sql(sql_string)


def unpack_array_column(df_in, column_to_unpack, other_columns_to_include_in_output, spark):
    # Unpacks a JSON array of Structs into individual columns in the dataframe to return.

    # Parameters:
    # df_in - The dataframe containing the columns to convert.
    # column_to_unpack - The name of the column containing the JSON array.
    # other_columns_to_include_in_output - The list of df_in columns to also include in the outputted dataframe.
    # spark - Spark context.

    # Save dataframe as temporary view
    source_name = "view_source"
    df_in.createOrReplaceTempView(source_name)
  
    # Unpack the Array column by exploding
    sql_string = f"""
    select
      s.{', s.'.join(other_columns_to_include_in_output)}
      ,ctu.col.*
    from {source_name} s
    lateral view explode(s.{column_to_unpack}) ctu
    """
  
    # Return new dataframe containing array (of structs) column unpacked to individual columns
    return spark.sql(sql_string)