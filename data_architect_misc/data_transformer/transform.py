import pdb

import argparse
import os
import sys

import xlrd
import pandas as pd

import transform_utils
from file_utils import get_file_extension


CHUNK_SIZE = 100000 # 100k chunks
## ***TODO: replace ',' with '.'
# get extension
## remove headers and footers if any
# skip rows
# skip footers

# if XLSX
# read sheet by sheet
# if CSV
# read file in chunk

# get headers

## pivot

def check_data_against_rules(df, rules):
    replace_commas = rules['replace_commas_with_decimal_for_numbers']

    # [DM_1219_ColgateGlobal].[STG].[Data_Cleansing_Rule]
    # TODO: upper, ltrim, rtrim
    # "replace_commas_with_decimal_for_numbers": false,
    # Setting the whole column such as 'SUBMEDIA_1' or 'SUBMEDIA_2' as 'N/A' regardless of the condition
    # Delete rows that were loaded with null values for advertiser and local_spend (1. mark as delete if condition met)
    # Setting DAYPART = 'N/A' for records with a media type other than Radio or Television (2. if condition in one column is met, then apply something to another column)
    # Set TOTAL_DURATION = 0 for records having 'PRESS' as media type (see #2)
    # Delete records having a investment = 0 and Rating = 0 (3. mark as delete if condition in TWO columns is met)
    # Set spot_length = Total_Duration Field Spot_Length (4. Copy value from one column to another)
    # Replace all the NULL and empty values with N/A OR 0 Field SECTOR => ("default_value": "N/A" or "0")
    pass


if __name__ == '__main__':
    # 1. Process arguments passed into the program
    parser = argparse.ArgumentParser(description=transform_utils.DESC)
    parser.add_argument('-c', required=True, type=str,
                        help=transform_utils.HELP)
    args = parser.parse_args()

    # 2. Load JSON configuration file
    if (not args.c) or (not os.path.exists(args.c)):
        sys.exit(transform_utils.CONFIG_FILE_ERROR)

    # 3. Iterate through each transform procedure
    for config in transform_utils.load_config(args.c):
        input_file = os.path.join(config['input_file_path'], config['input_file_name'])
        if not os.path.exists(input_file):
            sys.exit(' '.join([transform_utils.FILE_NOT_EXIST_ERROR, input_file]))

        cols_to_use = transform_utils.get_list_of_columns_to_use(config)
        leading_rows = transform_utils.get_leading_rows_to_skip(config)
        trailing_rows = transform_utils.get_trailing_rows_to_skip(config)

        if transform_utils.is_excel(input_file):
            sheet = transform_utils.get_sheet_index_or_name(config)
        elif transform_utils.is_csv(input_file):
            encoding = transform_utils.get_csv_encoding(config)
            input_csv_delimiter = transform_utils.get_csv_delimiter(config)
        else:
            sys.exit(' '.join([
                    transform_utils.FILE_TYPE_NOT_RECOGNIZED_ERROR,
                    input_file
            ]))


        # df = pd.read_excel(input_file,sheet_name=sheet)
        pdb.set_trace()
        print('haha')
        #     df = transform_utils.get_data_frame()
        #
        # pdb.set_trace()
        # print("Finished cleaning data.")

    # REF: reduce memory use Pandas: https://towardsdatascience.com/why-and-how-to-use-pandas-with-large-data-9594dda2ea4c
    #https://www.giacomodebidda.com/reading-large-excel-files-with-pandas/
    # REF: pandas snippets: https://jeffdelaney.me/blog/useful-snippets-in-pandas/
    # # REF: https://stackoverflow.com/q/14262433
    # extn = get_file_extension(args.i)
    # if extn == '.xlsx':
    #     # REF: https://stackoverflow.com/a/44549301
    #     xlsx = pd.read_excel(args.i, sheet_name=None,
    #                          skiprows=cc.LEADING_ROWS_TO_SKIP,
    #                          skipfooter=cc.BOTTOM_ROWS_TO_SKIP)
    #     for sheet_name, cur_df in xlsx.items():
    #         # read sheet by sheet as df and pass them onto the function
    #         pdb.set_trace()
    #         # df.to_dict(orient='records')
    #         pass
    #
    # elif extn == '.csv':
    #     if cc.BOTTOM_ROWS_TO_SKIP > 0:
    #         # Pandas doesn't allow skipping footers if we process things in
    #         # chunk, so we handle this special case here
    #         cur_df = pd.read_csv(args.i,
    #                              skiprows=cc.LEADING_ROWS_TO_SKIP,
    #                              skipfooter=cc.BOTTOM_ROWS_TO_SKIP)
    #         pdb.set_trace()
    #     else:
    #         # otherwise, read by chunk and do further processing
    #         for cur_df in pd.read_csv(args.i, chunksize=CHUNK_SIZE,
    #                                   skiprows=cc.LEADING_ROWS_TO_SKIP):
    #             pdb.set_trace()
    #             pass
    # else:
    #     print("Raw data file type is not supported.")
    #     exit(1)
    #
    #


