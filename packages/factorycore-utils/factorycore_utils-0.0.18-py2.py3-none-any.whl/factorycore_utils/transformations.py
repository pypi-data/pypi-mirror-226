import pyspark.sql.functions as F
import json
from factorycore_utils.string_helpers import to_snake_case
from factorycore_utils.dataframe_helpers import find_correctly_cased_column_name


def with_columns_renamed(fun):
    def _(df):
        cols = list(
            map(
                lambda col_name: F.col("`{0}`".format(col_name)).alias(fun(col_name)),
                df.columns,
            )
        )
        return df.select(*cols)

    return _


def with_some_columns_renamed(fun, change_col_name):
    def _(df):
        cols = list(
            map(
                lambda col_name: F.col("`{0}`".format(col_name)).alias(fun(col_name))
                if change_col_name(col_name)
                else F.col("`{0}`".format(col_name)),
                df.columns,
            )
        )
        return df.select(*cols)

    return _


def snake_case_column_names(df):
    return with_columns_renamed(to_snake_case)(df)


def sort_columns(df, sort_order):
    sorted_col_names = None
    if sort_order == "asc":
        sorted_col_names = sorted(df.columns)
    elif sort_order == "desc":
        sorted_col_names = sorted(df.columns, reverse=True)
    else:
        raise ValueError(
            "['asc', 'desc'] are the only valid sort orders and you entered a sort order of '{sort_order}'".format(
                sort_order=sort_order
            )
        )
    return df.select(*sorted_col_names)


def refactor_columns(df, schema_change_list):
    if schema_change_list is not None:
        schema_changes = schema_change_list
        if isinstance(schema_change_list, str):
            schema_changes = json.loads(schema_change_list)

        data_type_changes = []
        name_changes = []

        for i in schema_changes:
            column_name = i.get("column_name")
            new_name = i.get("new_name")
            new_data_type = i.get("new_data_type")

            if (new_data_type is not None):
                data_type_changes.append((column_name, new_data_type))

            if (new_name is not None):
                name_changes.append((column_name, new_name))

        for (column_name, new_data_type) in data_type_changes:
            df = df.withColumn(find_correctly_cased_column_name(df, column_name), F.col(column_name).cast(new_data_type))

        for (column_name, new_name) in name_changes:
            df = df.withColumnRenamed(column_name, new_name)

    return df


def rename_or_cast_columns(df, schema_change_list):
    if schema_change_list is not None:
        schema_changes = schema_change_list
        if isinstance(schema_change_list, str):
            schema_changes = json.loads(schema_change_list)

        items = [i for i in schema_changes if i["action"].lower() == "replace"]
        for item in items:
            if "data_type" in item:
                if "renamed_from" in item:
                    df = df.withColumn(item.get("renamed_from"), F.col(item.get("renamed_from")).cast(item.get("data_type"))).withColumnRenamed(item.get("renamed_from"), item.get("column_name"))
                else:
                    df = df.withColumn(item.get("column_name"), F.col(item.get("column_name")).cast(item.get("data_type")))
            elif "renamed_from" in item:
                df = df.withColumnRenamed(item.get("renamed_from"), item.get("column_name"))

    return df
    