"""
Include this python file in the common_post_transform_qa_config.json
file with the key like this:
"custom_transform_functions_file": "./transform_functions/common_post_transform_qa_functions.py",

and run the transform.py like this:
>> python transform.py

Author: Phyo Thiha
Last Modified: April 13, 2020
"""
import datetime
import logging
import re

import pandas as pd

import comp_harm_constants
import qa_errors


class CustomFunctions:
    """
    This class is the collection of QA functions that must be run
    against the transformed data. The QA functions here will either
    give warnings or throw errors (if the impact is serious).

    Note: This class is named 'CustomFunctions' instead of
    'CustomQAFunctions' because the way we load custom function
    modules (in transform_utils.py) is expecting a class named,
    'CustomFunctions' if any custom function file is provided.

    Technically, we can create a 'CustomQAFunctions' class first
    and then have 'CustomFunctions' class inherit the former
    in this module. That is, create
    class CustomFunctions(CustomQAFunctions).

    But I personally don't like creating multiple-layered
    classes just because it follows OOP best practices.
    As a result, I have decided not inherit 'CustomFunctions' from
    'CustomQAFunctions'.
    """
    EXPECTED_COLUMNS = {
        # Standard column names we use in competitive harmonization project
        comp_harm_constants.PROCESSED_DATE_COLUMN,
        comp_harm_constants.YEAR_COLUMN,
        comp_harm_constants.MONTH_COLUMN,
        comp_harm_constants.DATE_COLUMN,
        comp_harm_constants.REGION_COLUMN,
        comp_harm_constants.COUNTRY_COLUMN,
        comp_harm_constants.ADVERTISER_COLUMN,
        comp_harm_constants.MEDIA_TYPE_COLUMN,
        comp_harm_constants.CURRENCY_COLUMN,
        comp_harm_constants.GROSS_SPEND_COLUMN,
        comp_harm_constants.CATEGORY_COLUMN,
        comp_harm_constants.RAW_SUBCATEGORY_COLUMN,
        comp_harm_constants.RAW_BRAND_COLUMN,
        comp_harm_constants.RAW_SUBBRAND_COLUMN,
        comp_harm_constants.RAW_PRODUCT_NAME_COLUMN,
        comp_harm_constants.PRODUCT_NAME_COLUMN
    }
    # the earliest year we started collecting data for comp. harm project
    MIN_YEAR = 2015
    MIN_MONTH = 1
    MAX_MONTH = 12
    # one billion is already quite big for a spend line item in comp. harm project
    MAX_SPEND = 1000000000
    ESSENTIAL_COLUMNS = [
        comp_harm_constants.YEAR_COLUMN,
        comp_harm_constants.MONTH_COLUMN,
        comp_harm_constants.DATE_COLUMN,
        comp_harm_constants.REGION_COLUMN,
        comp_harm_constants.COUNTRY_COLUMN,
        comp_harm_constants.ADVERTISER_COLUMN,
        comp_harm_constants.MEDIA_TYPE_COLUMN,
        comp_harm_constants.CATEGORY_COLUMN,
        comp_harm_constants.GROSS_SPEND_COLUMN
    ]

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def check_expected_columns_are_present(self, df) -> pd.DataFrame:
        """
        The transformed data must have at least the minimal set of
        columns that we expect for competitive harmonization project.
        """
        if set(self.EXPECTED_COLUMNS) - set(df.columns):
            self.logger.warning(
                f"QA => Missing these expected/standard columns in the "
                f"transformed data: {set(self.EXPECTED_COLUMNS) - set(df.columns)}")

        if set(df.columns) - set(self.EXPECTED_COLUMNS):
            self.logger.info(
                f"QA => Found these columns in transformed data that are not "
                f"part of the expected column set: "
                f"{set(df.columns) - set(self.EXPECTED_COLUMNS)}\n")

        return df

    def assert_number_of_columns_equals(self, df, num_of_cols_expected) -> pd.DataFrame:
        """
        Assert that the total number of columns in the dataframe
        is equal to num_of_cols_expected (int).

        Args:
            df: Raw dataframe to transform.
            num_of_cols_expected: Number of columns expected (int).

        Returns:
            The original dataframe is returned if the assertion is successful.

        Raises:
            ColumnCountMismatchError: If the number of columns found
            does not equal to what is expected.
        """
        if df.shape[1] != num_of_cols_expected:
            raise qa_errors.ColumnCountError(
                f"Expected column count of: "
                f"{num_of_cols_expected} but found: "
                f"{df.shape[1]} in the current dataframe.")

        return df

    def check_distinct_year_values_in_year_column(self, df) -> pd.DataFrame:
        """
        Display distinct year values in the transformed data.
        If there are more than one year (which is unusual for
        typical data file in competitive harmonization project),
        the WARNING log message will be used. Otherwise, INFO
        log message will be used.
        """
        years = sorted(df[comp_harm_constants.YEAR_COLUMN].unique())

        if len(years) > 1:
            self.logger.warning(f"QA => More than ONE year value is found: "
                                f"{years}"
                                f"\nMake sure this is expected for the data.")
        else:
            self.logger.info(f"QA => Year value found in the data: {years}")

        return df

    def assert_if_year_values_are_within_valid_range(self, df) -> pd.DataFrame:
        """
        Checks if distinct year values found in the transformed
        data are within valid range. The valid range is between
        2015 (the year we started collecting data for competitive
        harmonization project) to the current year.
        """
        years = sorted(df[comp_harm_constants.YEAR_COLUMN].unique())
        cur_year = datetime.datetime.now().year

        if not all([(y >= self.MIN_YEAR) and (y <= cur_year) for y in years]):
            raise qa_errors.InvalidValueFoundError(
                f"Unexpected year found in the data. Please inspect the "
                f"following year values: {years} to make sure that none of "
                f"them are beyond the expected range and match what's in "
                f"the raw data."
            )
        return df

    def check_distinct_month_values_in_month_column(self, df) -> pd.DataFrame:
        """
        Display distinct month values in the transformed data.
        If there are more than one month, the WARNING log
        message will be used. Otherwise, INFO log message
        will be used.
        """
        months = sorted(df[comp_harm_constants.MONTH_COLUMN].unique())

        if len(months) > 1:
            self.logger.warning(f"QA => More than ONE month value is found: "
                                f"{months}"
                                f"\nMake sure this is expected for the data.")
        else:
            self.logger.info(f"QA => Month value found in the data: {months}")

        return df

    def assert_if_month_values_are_within_valid_range(self, df) -> pd.DataFrame:
        """
        Asserts if month values found in the transformed data
        are within the valid range (from 1 to 12). If not,
        raises InvalidValueFoundError.
        """
        months = sorted(df[comp_harm_constants.MONTH_COLUMN].unique())

        if not all([(y >= self.MIN_MONTH) and
                    (y <= self.MAX_MONTH) for y in months]):
            raise qa_errors.InvalidValueFoundError(
                f"Unexpected month value found in the data. Please inspect "
                f"the following month values: {months} to make sure that "
                f"none of these are beyond the expected range (1 to 12) "
                f"and match what's in the raw data."
            )

        return df

    def assert_if_date_values_matches_with_year_and_month_column_values(
            self,
            df) -> pd.DataFrame:
        """
        Asserts that the year and month values in respective harmonized
        columns are the same as the ones in harmonized date column.

        REF: https://stackoverflow.com/a/25149272/1330974

        If year or month values don't match with what's in the date
        column, raise ValueComparisonError.
        """
        df_year_comparison = df.loc[df[comp_harm_constants.YEAR_COLUMN]
            != pd.DatetimeIndex(df[comp_harm_constants.DATE_COLUMN]).year]
        df_month_comparison = df.loc[df[comp_harm_constants.MONTH_COLUMN]
            != pd.DatetimeIndex(df[comp_harm_constants.DATE_COLUMN]).month]

        if not df_year_comparison.empty:
            raise qa_errors.ValueComparisonError(
                f"Value in harmonized year column does not match the value "
                f"in harmonized date column as shown in row(s) below:\n"
                f"{df_year_comparison}")

        if not df_month_comparison.empty:
            raise qa_errors.ValueComparisonError(
                f"Value in harmonized month column does not match the value "
                f"in harmonized date column as shown in row(s) below:\n"
                f"{df_month_comparison}")

        return df

    def assert_no_null_value_in_columns(self,
                                        df,
                                        list_of_col_names) -> pd.DataFrame:
        """
        Asserts if there is any NULL (NaN) values in the list of
        columns provided. If there is any, raise NullValueFoundError.

        Args:
            df: Raw dataframe to check for NULL/NaN values.
            list_of_col_names: List of column names (each is of string type)
            in which we should look for NULL/NaN values.
            REF1: https://stackoverflow.com/a/42923089
            REF2: https://stackoverflow.com/a/27159258
            REF3: https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.isnull.html

        Returns:
            The original dataframe is returned if the assertion is successful.

        Raises:
            NullValueFoundError: If there is any NULL/NaN value in the given list
            of columns.
        """
        if not isinstance(list_of_col_names, list):
            raise qa_errors.InputDataTypeError(f"List of column names must "
                                               f"be of list type with individual "
                                               f"column names being string values.")

        if df[list_of_col_names].isnull().values.any():
            raise qa_errors.NullValueFoundError(f"Null (NaN) value is "
                                                f"found in one of these "
                                                f"columns: {list_of_col_names}")

        return df

    def assert_no_null_value_in_some_essential_columns(self,
                                                       df) -> pd.DataFrame:
        """
        Asserts that essential columns (i.e. HARMONIZED_YEAR,
        HARMONIZED_MONTH, HARMONIZED_DATE, HARMONIZED_REGION,
        HARMONIZED_COUNTRY, HARMONIZED_ADVERTISER,
        HARMONIZED_MEDIA_TYPE and HARMONIZED_CATEGORY)
        do not have NULL (NaN) value in them.

        If there is any NULL (NaN) value, throw NullValueFoundError
        and force the data person to take a look at it.
        """
        cols_with_null = []
        for col_name in self.ESSENTIAL_COLUMNS:
            if df[[col_name]].isnull().values.any():
                cols_with_null.append(col_name)

        if cols_with_null:
            raise qa_errors.NullValueFoundError(f"Null (NaN) value is "
                                                f"found in one of these "
                                                f"columns: {cols_with_null}")

        return df

    def assert_no_empty_str_values_in_columns(self,
                                              df,
                                              list_of_col_names) -> pd.DataFrame:
        """
        Check if there is any empty string values in the list of
        columns provided. If there is any, raise EmptyStringFoundError.

        Args:
            df: Raw dataframe to check for empty string values.
            list_of_col_names: List of column names (each is of string type)
            in which we should look for empty string values.
            REF1: https://stackoverflow.com/a/52843708

        Returns:
            The original dataframe is returned if the assertion is successful.

        Raises:
            EmptyStringFoundError: If there is any empty string value
            in the given list of columns.
        """
        if not isinstance(list_of_col_names, list):
            raise qa_errors.InputDataTypeError(f"List of column names must "
                                               f"be of list type with "
                                               f"individual column names being "
                                               f"string values.")

        cols_with_empty_str = []
        for col_name in list_of_col_names:
            # Here, I am converting df[col_name] to str type first
            # to avoid the dreaded FutureWarning from numpy
            # Read more here:
            # https://stackoverflow.com/a/46721064/1330974
            if not df.loc[df[col_name].astype(str) == ''].empty:
                cols_with_empty_str.append(col_name)

        if cols_with_empty_str:
            raise qa_errors.EmptyStringFoundError(
                f"Empty string value found in these column(s): "
                f"{cols_with_empty_str}")

        return df

    def assert_no_empty_string_in_some_essential_columns(
            self,
            df) -> pd.DataFrame:
        """
        Asserts that essential columns (i.e. HARMONIZED_YEAR,
        HARMONIZED_MONTH, HARMONIZED_DATE, HARMONIZED_REGION,
        HARMONIZED_COUNTRY, HARMONIZED_ADVERTISER,
        HARMONIZED_MEDIA_TYPE and HARMONIZED_CATEGORY)
        do not have any empty string value in them.

        If there is any empty string value, throw NullValueFoundError
        and force the data person to take a look at it.
        """
        return self.assert_no_empty_str_values_in_columns(
            df, self.ESSENTIAL_COLUMNS)

    def assert_only_expected_constants_exist_in_column(
            self,
            df,
            column_name,
            set_of_expected_values
    ) -> pd.DataFrame:
        """
        Some columns in the transformed data must only contain
        specific values (e.g., either 'M' or 'F' for gender).

        This methods inspects distinct values from a given column
        and if any of these values is not found within the
        standard/expected set, it raises InvalidValueFoundError.
        """
        diff = set(df[column_name]) - set(set_of_expected_values)
        if diff:
            raise qa_errors.InvalidValueFoundError(
                f"'{column_name}' column has some unexpected values "
                f"as listed here:\n{diff}")

        return df

    def check_expected_constants_exist_in_column(
            self,
            df,
            column_name,
            set_of_expected_values
    ) -> pd.DataFrame:
        """
        Some columns in the transformed data should only contain
        specific values (e.g., either 'M' or 'F' for gender).

        This methods inspects distinct values from a given column
        and if any of these values is not found within the
        standard/expected set, it warns the data person so that
        s/he can add the unexpected values to the expected values
        set as needed.
        """
        diff = set(df[column_name]) - set(set_of_expected_values)
        if diff:
            self.logger.warning(
                f"QA => '{column_name}' column has some unexpected "
                f"values as listed here:\n{diff}")

        return df

    def assert_REGION_values_are_valid(self,
                                       df) -> pd.DataFrame:
        """
        Checks to make sure the values in REGION column are
        based on standard region values for competitive
        harmonization project. If not, throw InvalidValueError.
        """
        return self.assert_only_expected_constants_exist_in_column(
            df,
            comp_harm_constants.REGION_COLUMN,
            comp_harm_constants.REGIONS
        )

    def assert_COUNTRY_values_are_valid(self,
                                        df) -> pd.DataFrame:
        """
        Checks to make sure the values in COUNTRY column are
        based on standard region values for competitive
        harmonization project. If not, throw InvalidValueError.
        """
        return self.assert_only_expected_constants_exist_in_column(
            df,
            comp_harm_constants.COUNTRY_COLUMN,
            comp_harm_constants.COUNTRIES
        )

    def checks_ADVERTISER_values_that_do_not_have_mapping(
            self,
            df) -> pd.DataFrame:
        """
        Checks to make sure the values in ADVERTISER column are
        based on the ADVERTISER_MAPPINGS that we have been building
        gradually for competitive harmonization project.

        If any new advertiser value is found, this method will
        output an WARNING message so that data person can add
        new advertisers to the mapping if relevant.
        """
        potentially_new_advertisers = (
                set(df[comp_harm_constants.ADVERTISER_COLUMN]) -
                set(comp_harm_constants.ADVERTISER_MAPPINGS.values())
        )
        if potentially_new_advertisers:
            self.logger.warning(
                f"QA => We do NOT have these advertisers in our mapping list. "
                f"Make sure to add them to ADVERTISER_MAPPINGS as relevant:\n"
                f"{sorted(potentially_new_advertisers)}")

        return df

    def assert_MEDIA_TYPE_values_are_valid(
            self,
            df) -> pd.DataFrame:
        """
        Checks to make sure the values in MEDIA_TYPE column are
        based on standard media type values for competitive
        harmonization project. If not, throw InvalidValueError.
        """
        return self.assert_only_expected_constants_exist_in_column(
            df,
            comp_harm_constants.MEDIA_TYPE_COLUMN,
            comp_harm_constants.MEDIA_TYPES
        )

    def assert_CATEGORY_values_are_valid(
            self,
            df) -> pd.DataFrame:
        """
        Checks to make sure the values in CATEGORY column are
        based on standard category values for competitive
        harmonization project. If not, throw InvalidValueError.
        """
        return self.assert_only_expected_constants_exist_in_column(
            df,
            comp_harm_constants.CATEGORY_COLUMN,
            comp_harm_constants.CATEGORIES
        )

    def assert_no_less_than_values_in_columns(self,
                                              df,
                                              threshold_value,
                                              list_of_col_names) -> pd.DataFrame:
        """
        Check if there is any value which is less than the threshold_value
        in the list of columns provided.
        If there is any, raise InvalidValueFoundError.

        Args:
            df: Raw dataframe to check for values.
            threshold_value: Value to compare against individual values in
            the given dataframe's columns.
            list_of_col_names: List of column names (each is of string type)
            whose values we should compare against the threshold value.

        Returns:
            The original dataframe is returned if the assertion is successful.

        Raises:
            InvalidValueFoundError: If there is any empty string value
            in the given list of columns.
        """
        if not isinstance(list_of_col_names, list):
            raise qa_errors.InputDataTypeError(f"List of column names must "
                                               f"be of list type with individual "
                                               f"column names being string values.")

        for col_name in list_of_col_names:
            if any(df[col_name] < threshold_value):
                raise qa_errors.InvalidValueFoundError(
                    f"Value(s) less than {threshold_value} are "
                    f"found in this column: {col_name}")

        return df

    def assert_GROSS_SPEND_column_has_no_negative_value(self,
                                                        df) -> pd.DataFrame:
        """
        Asserts that GROSS_SPEND column has no negative value in it.
        If found, throw InvalidValueFoundError.
        """
        return self.assert_no_less_than_values_in_columns(
            df,
            0,
            [comp_harm_constants.GROSS_SPEND_COLUMN])

    def assert_no_greater_than_values_in_columns(
            self,
            df,
            threshold_value,
            list_of_col_names) -> pd.DataFrame:
        """
        Check if there is any value which is greater than the threshold_value
        in the list of columns provided.

        If there is any, WARN data person to inspect it.

        Args:
            df: Dataframe to check for values.
            threshold_value: Value to compare against individual values in
            the given dataframe's columns.
            list_of_col_names: List of column names (each is of string type)
            whose values we should compare against the threshold value.

        Returns:
            The original dataframe is returned if the assertion is successful.
        """
        if not isinstance(list_of_col_names, list):
            raise qa_errors.InputDataTypeError(f"List of column names must "
                                               f"be of list type with individual "
                                               f"column names being string values.")

        for col_name in list_of_col_names:
            if any(df[col_name] > threshold_value):
                self.logger.warning(
                    f"Value(s) greater than {threshold_value} are "
                    f"found in this column: {col_name}")

        return df

    def assert_GROSS_SPEND_column_has_no_ridiculously_high_spend_value(
            self,
            df) -> pd.DataFrame:
        """
        Asserts that GROSS_SPEND column has no ridiculously big
        (now, set to 1 billion) values in it for each cell.
        In competitive harmonization project's context, any spend
        line bigger than 1 billion should be inspected by data person.

        If found, WARN data person about it.
        """
        return self.assert_no_greater_than_values_in_columns(
            df,
            self.MAX_SPEND,
            [comp_harm_constants.GROSS_SPEND_COLUMN])

    def assert_GROSS_SPEND_column_values_have_two_decimals(
            self,
            df) -> pd.DataFrame:
        """
        Asserts that GROSS_SPEND column values are only two
        decimals.

        If any violate found, raise InvalidValueFoundError
        """
        # Convert float to string type and then split by decimal character
        gc = comp_harm_constants.GROSS_SPEND_COLUMN
        df1 = df[gc].astype(str).map(lambda x: x.split('.'))
        if any([len(x[1]) > 2 for x in df1.values]):
            raise qa_errors.InvalidValueFoundError(
                f"Some of the values in '{gc}' column have "
                f"more than two decimal digits.")

        return df

    def check_possible_duplicates_in_columns(self,
                                             df,
                                             list_of_col_names) -> pd.DataFrame:
        """
        This method will check if any of the given list of columns
        has duplicate values in it. It will do so by first
        turning all letters of each value in individual column to small case.
        Then it will retain alpha-numerical values of the aforementioned
        values. Then by comparing the difference between the set of
        original values vs. that of modified values, this method will
        raise an Alert/Error message telling user that they should
        look at possible duplicate values and re-map them as necessary.

        For example, these values in 'Channel' column are possible
        duplicates: ['YouTube', 'Youtube', 'Other social', 'other social',
        'E-commerce',' ECommerce']. This method will create a new set of
        values like this: {'youtube', 'other social', 'ecommerce'} and
        by comparing it against the original set of values, it will detect
        possible duplicates

        NOTE: In Python, \W = [^a-zA-Z0-9_]
        REF: https://docs.python.org/3/library/re.html

        Args:
            df: Raw dataframe to search for duplicates.
            list_of_col_names: List of column names in which
             the code will look for duplicates.

        Returns:
            Original dataframe if no duplicates are found.

        Raises:
            PossibleDuplicateError, if there's a possible duplicate values.
        """
        non_alpha_numerical_chars_pattern = re.compile(r'\W', re.UNICODE)
        for col_name in list_of_col_names:
            orig_values = set(df[col_name].values)
            simplified_values = {non_alpha_numerical_chars_pattern.sub('', s).lower()
                                 for s in orig_values}
            if len(orig_values) != len(simplified_values):
                err_msg = ''.join(["Possible duplicates found in the values of column, '",
                                   col_name, "':\n", str(sorted(orig_values)),
                                   ".\nPlease update/map these values to new, standardized values."
                                   ])
                raise qa_errors.PossibleDuplicateError(err_msg)

        return df