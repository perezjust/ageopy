IMPORT_LIST = [ 'from geoadmin_tools.schema_helper_compare_schemas import SchemaHelperCompareSchemas',
                'from geoadmin_tools.versioning_versioned_to_json import VersioningVersionedToJSON',
                'from geoadmin_tools.versioning_unregister_items import VersioningUnregisterItems',
                'from geoadmin_tools.versioning_register_items import VersioningRegisterItems',
		'from mxd_tools.update_mxd_database_connections import UpdateMXDDatabaseConnections'
               ]

TOOL_LIST = ['SchemaHelperCompareSchemas',
             'VersioningVersionedToJSON',
             'VersioningUnregisterItems',
             'VersioningRegisterItems',
             'UpdateMXDDatabaseConnections'
             ]


for import_text in IMPORT_LIST:
    exec import_text


def get_toolbox_classes():
    return [eval(tool) for tool in TOOL_LIST]
