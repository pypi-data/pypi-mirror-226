def create_catalog(spark, databases_to_ignore = [], only_these_databases = []):
    # Creates the Catalog describing the Delta Lake.

    # Parameters:
    # spark - Spark context
    # databases_to_ignore - List of Databases to ignore from this process 
    # only_these_databases - List of Databases to focus on for this process

    # Returns:
    # df_objects_to_create
    # df_table_catalog
    # df_column_catalog
    # df_error_catalog
    import re

    df_databases = spark.sql("SHOW DATABASES")

    objects_to_create = []
    table_catalog = []
    column_catalog = []
    error_catalog = []

    for db in df_databases.collect():
        if db.databaseName not in databases_to_ignore and ((len(only_these_databases) > 0 and db.databaseName in only_these_databases) or len(only_these_databases) == 0):
            #if debug: print(f"Adding Database '{db.databaseName}'")
            objects_to_create.append(("database", f"CREATE DATABASE IF NOT EXISTS {db.databaseName};"))

            df_tables = spark.sql(f"show tables in {db.databaseName}")

            for tbl in df_tables.collect():
                try:

                    df_show = spark.sql(f"show table extended in {db.databaseName} like '{tbl.tableName}'")
                    table_information = df_show.collect()[0].information.strip()

                    df_describe = spark.sql(f"describe extended {db.databaseName}.{tbl.tableName}")

                    end_of_column_section = False
                    table_info_section = False

                    table_comment = ""
                    table_type = ""
                    table_location = ""
                    view_text = ""
                    i = 1

                    for row in df_describe.collect():
                        if row['col_name'] == '':
                            end_of_column_section = True

                        if not end_of_column_section:
                            column_catalog.append((f"{db.databaseName}.{tbl.tableName}", i, row.col_name, row.data_type, row.comment))
                            i += 1

                        if row.col_name.lower() == '# detailed table information':
                            table_info_section = True

                        if table_info_section == True and row.col_name.lower() == 'comment':
                            table_comment = row.data_type

                        if table_info_section == True and row.col_name.lower() == 'type':
                            table_type = row.data_type.lower()

                        if table_info_section == True and row.col_name.lower() == 'location':
                            table_location = row.data_type

                        if table_info_section == True and row.col_name.lower() == 'view text':
                            view_text = row.data_type            

                    if table_type == "view":
                        #if debug: print(f"Adding View '{db.databaseName}.{tbl.tableName}'")
                        objects_to_create.append(("view", f"""CREATE OR REPLACE VIEW {db.databaseName}.{tbl.tableName} AS {view_text};"""))
                    else:
                        #if debug: print(f"Adding Table '{db.databaseName}.{tbl.tableName}'")
                        objects_to_create.append(("table", f"CREATE TABLE IF NOT EXISTS {db.databaseName}.{tbl.tableName} USING DELTA LOCATION '{re.sub('dbfs:/mnt/[^/]+', 'delta_mount', table_location)}';"))

                    table_catalog.append((table_type, f"{db.databaseName}.{tbl.tableName}", table_comment, table_information, table_location))

                except Exception as e:
                    #if debug: print(f"Adding Error for '{db.databaseName}.{tbl.tableName}' - {str(e)}")
                    error_catalog.append((f"{db.databaseName}.{tbl.tableName}", str(e)))
                    continue

    df_objects_to_create = spark.createDataFrame(objects_to_create, "object_type string, create_script string")    
    df_table_catalog = spark.createDataFrame(table_catalog, "type string, delta_table string, comment string, information string, location string")    
    df_column_catalog = spark.createDataFrame(column_catalog, "delta_table string, position int, column_name string, data_type string, comment string")    
    df_error_catalog = spark.createDataFrame(error_catalog, "delta_table string, error_message string")    

    return df_objects_to_create, df_table_catalog, df_column_catalog, df_error_catalog