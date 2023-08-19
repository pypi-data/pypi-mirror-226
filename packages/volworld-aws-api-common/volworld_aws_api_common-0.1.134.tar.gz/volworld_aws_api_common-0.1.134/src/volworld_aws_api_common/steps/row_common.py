from behave import *
from volworld_aws_api_common.test.behave.row_utils import (
    update_order_type_of_list, w__tags_of_all_rows_are_showing, w__tags_of_all_rows_are_not_showing)


@when('{mentor} update [Order] type of list page to {sort_dir}')
def when_update_order_type_of_list_page(c, mentor: str, sort_dir: str):
    update_order_type_of_list(c, sort_dir)


@then('tags of all rows are showing')
def then_tags_of_all_rows_are_showing(c):
    w__tags_of_all_rows_are_showing(c)


@then('tags of all rows are not showing')
def then_tags_of_all_rows_are_not_showing(c):
    w__tags_of_all_rows_are_not_showing(c)