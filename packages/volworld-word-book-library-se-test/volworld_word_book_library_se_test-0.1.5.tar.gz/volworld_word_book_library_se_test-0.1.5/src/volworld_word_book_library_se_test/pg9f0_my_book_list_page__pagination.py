import base64

from volworld_aws_api_common.api.FrontEndUrl import FrontEndUrl
from volworld_common.test.behave.BehaveUtil import BehaveUtil
from api.A import A
from volworld_word_book_library_se_test.book_row_utils import assert_book_count_and_total_page
from behave import *
from volworld_aws_api_common.test.behave.selenium_utils import (
    w__get_element_by_shown_dom_id, w__click_element_by_dom_id, w__assert_element_existing, \
    w__key_in_element_by_dom_id, w__get_element_by_presence_dom_id, w__assert_element_not_existing)

from volworld_aws_api_common.test.ProjectMode import ProjectMode
from test.behave.CotA import CotA
from test.behave.Page import Page


@then('there are {count_str} showing books and total {total_page_count_str} pages with total {total_count_str} books')
def then_book_count_page_total_count(c, count_str: str, total_page_count_str: str, total_count_str: str):
    target_page = getattr(c, CotA.TargetPage)
    if target_page == Page.Pg9F0_My_Book_List_Page:
        assert_book_count_and_total_page(c, count_str, total_page_count_str, total_count_str)
    else:
        assert False, f"Unknown target page {target_page}"


@then('there are {book_count_str} showing books and total {total_page_count_str} pages')
def then_showing_books_and_total_pages(c, book_count_str: str, total_page_count_str: str):
    target_page = getattr(c, CotA.TargetPage)
    if target_page == Page.Pg9F0_My_Book_List_Page:
        assert_book_count_and_total_page(c, book_count_str, total_page_count_str)
    else:
        assert False, f"Unknown target page {target_page}"


@when('{mentor} open target testing page with search keyword {keywords} and item per page is {item_per_page_str}')
def when_open_page_with_keywords_and_item_per_page(c, mentor: str, keywords: str, item_per_page_str: str):
    target_page = getattr(c, CotA.TargetPage)
    assert target_page == Page.Pg9F0_My_Book_List_Page
    ks = BehaveUtil.clear_string(keywords).split(" ")
    kwb64 = list()
    for k in ks:
        kwb64.append(base64.b64encode(bytes(k, "utf-8")).decode('utf-8'))
    sch = '%'.join(kwb64)
    print(f'sch = [{sch}]')

    url = f"{FrontEndUrl.Root}/#/{ProjectMode.testUrlPrefix}{A.Book}/{A.List}?sch={sch}&impp={BehaveUtil.clear_int(item_per_page_str)}"

    print(f"open default [9F0_My-Book-List-Page] url={url}")
    c.browser.get(url)