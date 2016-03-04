IMPORT_LIST = [ 'from geoadmin_tools.schema_helper_compare_schemas import SchemaHelperCompareSchemas',
		'from mxd_tools.update_mxd_database_connections import UpdateMXDDatabaseConnections'
               ]

TOOL_LIST = ['SchemaHelperCompareSchemas',
             'UpdateMXDDatabaseConnections'
             ]


for import_text in IMPORT_LIST:
    exec import_text


def get_toolbox_classes():
    return [eval(tool) for tool in TOOL_LIST]
