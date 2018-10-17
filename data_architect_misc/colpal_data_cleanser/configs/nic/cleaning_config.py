LEADING_ROWS_TO_SKIP = 0
BOTTOM_ROWS_TO_SKIP = 0

cleaning_rules = {
    "columns_to_select": ["","",""],
    "columns_to_rename": {
        # old_name: new_standardized_column_name

    },
    "column_datatypes_to_verify": {

    },
    "column_default_values": {

    },
    "column_format_or_pattern": {

    },
    "other_rules": {
        "column_name": ['rule1','rule2',...],
    }
  #   "column_default_values"
  # # data_types allowed are 'str', 'float', 'int', 'date'
  # "column_cleaning_rules":
  #   [
  #     {
  #       "raw_column_name": "",
  #       "processed_column_name": "Sector",
  #       "expected_data_type": "str",
  #       "expected_value": "N/A",
  #       "__or_set_value_to": "N/A",
  #       "__null_allowed": false,
  #       "__if_null_or_blank": "N/A"
  #     },
  #     {
  #       "raw_column_name": "",
  #       "processed_column_name": "Subsector",
  #       "expected_data_type": "str"
  #     },
  #     {
  #       "raw_column_name": "",
  #       "processed_column_name": "Advertiser",
  #       "expected_data_type": "str",
  #       "__ignore_row_if_null": true
  #     },
  #     {
  #       "raw_column_name": "",
  #       "processed_column_name": "Category",
  #       "expected_data_type": "str"
  #     },
  #     {
  #       "raw_column_name": "",
  #       "processed_column_name": "Brand",
  #       "expected_data_type": "str"
  #     },
  #     {
  #       "raw_column_name": "",
  #       "processed_column_name": "Product",
  #       "expected_data_type": "str"
  #     },
  #     {
  #       "raw_column_name": "",
  #       "processed_column_name": "Media",
  #       "expected_data_type": "str"
  #     },
  #     {
  #       "raw_column_name": "",
  #       "processed_column_name": "Submedia1",
  #       "expected_data_type": "str",
  #       "if_null_or_blank": "N/A"
  #     },
  #     {
  #       "raw_column_name": "",
  #       "processed_column_name": "Submedia2",
  #       "expected_data_type": "str",
  #       "if_null_or_blank": "N/A"
  #     },
  #     {
  #       "raw_column_name": "",
  #       "processed_column_name": "Daypart",
  #       "expected_data_type": "str"
  #     },
  #     {
  #       "raw_column_name": "",
  #       "processed_column_name": "Format",
  #       "expected_data_type": "str"
  #     },
  #     {
  #       "raw_column_name": "",
  #       "processed_column_name": "Creative",
  #       "expected_data_type": "str"
  #     },
  #     {
  #       "raw_column_name": "",
  #       "processed_column_name": "Network",
  #       "expected_data_type": "str"
  #     },
  #     {
  #       "raw_column_name": "",
  #       "processed_column_name": "Channel",
  #       "expected_data_type": "str"
  #     },
  #     {
  #       "raw_column_name": "",
  #       "processed_column_name": "Vehicle",
  #       "expected_data_type": "str"
  #     },
  #     {
  #       "raw_column_name": "",
  #       "processed_column_name": "Total Duration",
  #       "expected_data_type": "int"
  #     },
  #     {
  #       "raw_column_name": "",
  #       "processed_column_name": "Insertions",
  #       "expected_data_type": "int"
  #     },
  #     {
  #       "raw_column_name": "Spot Length",
  #       "processed_column_name": "",
  #       "expected_data_type": "int"
  #     },
  #     {
  #       "raw_column_name": "",
  #       "processed_column_name": "Impressions",
  #       "expected_data_type": "int"
  #     },
  #     {
  #       "raw_column_name": "",
  #       "processed_column_name": "Geography",
  #       "expected_data_type": "str"
  #     },
  #     {
  #       "raw_column_name": "",
  #       "processed_column_name": "Region",
  #       "expected_data_type": "str"
  #     },
  #     {
  #       "raw_column_name": "",
  #       "processed_column_name": "Subregion",
  #       "expected_data_type": "str"
  #     },
  #     {
  #       "raw_column_name": "",
  #       "processed_column_name": "City",
  #       "expected_data_type": "str"
  #     },
  #     {
  #       "raw_column_name": "",
  #       "processed_column_name": "Country",
  #       "expected_data_type": "str"
  #     },
  #     {
  #       "raw_column_name": "",
  #       "processed_column_name": "Date",
  #       "expected_data_type": "date",
  #       "pattern": ""
  #     },
  #     {
  #       "raw_column_name": "",
  #       "processed_column_name": "Currency",
  #       "expected_data_type": "str"
  #     },
  #     {
  #       "raw_column_name": "",
  #       "processed_column_name": "Local Spend",
  #       "expected_data_type": "float"
  #     },
  #     {
  #       "raw_column_name": "",
  #       "processed_column_name": "Spend in USD",
  #       "expected_data_type": "float"
  #     },
  #     {
  #       "raw_column_name": "",
  #       "processed_column_name": "GRP",
  #       "expected_data_type": "float"
  #     },
  #     {
  #       "raw_column_name": "",
  #       "processed_column_name": "GRP 30",
  #       "expected_data_type": "float"
  #     },
  #     {
  #       "__comment": "this column is found in [DM_1219_ColgateGlobal].[dbo].[CP_DIM_DEMOGRAPHIC]",
  #       "raw_column_name": "",
  #       "processed_column_name": "GRP Demographic",
  #       "expected_data_type": "str"
  #     }
}
