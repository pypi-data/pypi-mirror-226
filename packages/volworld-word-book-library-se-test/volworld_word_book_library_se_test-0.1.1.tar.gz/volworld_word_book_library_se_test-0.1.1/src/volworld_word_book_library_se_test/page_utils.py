import base64

from behave.step_registry import __all__
from volworld_aws_api_common.api.FrontEndUrl import FrontEndUrl
from volworld_common.test.behave.BehaveUtil import BehaveUtil
from api.A import A
from api.PageId import PageId
from src.volworld_word_book_library_se_test.book_row_utils import assert_book_count_and_total_page
from behave import *
from volworld_aws_api_common.test.behave.selenium_utils import (
    w__get_element_by_shown_dom_id, w__click_element_by_dom_id, w__assert_element_existing, \
    w__key_in_element_by_dom_id, w__get_element_by_presence_dom_id, w__assert_element_not_existing, assert_page_id)

from volworld_aws_api_common.test.ProjectMode import ProjectMode
from test.behave.CotA import CotA
from test.behave.Page import Page


@when('{mentor} open target page')
def open_default_testing_page(c, mentor: str):
    target_page = getattr(c, CotA.TargetPage)
    url = None
    if target_page == Page.Pg9F0_My_Book_List_Page:
        url = f"{FrontEndUrl.Root}/#/{ProjectMode.testUrlPrefix}{A.Book}/{A.List}?impp=3"
    elif target_page == Page.Pg29D_Create_My_Book_Page:
        url = f"{FrontEndUrl.Root}/#/{ProjectMode.testUrlPrefix}{A.Book}/{A.Create}"
    elif target_page == Page.NGSL__PgD6F_Book_Chapter_List_Editor_Page:
        url = f"{FrontEndUrl.Root}/#/{ProjectMode.testUrlPrefix}{A.Book}/{A.Chapter}/{A.List}/" \
              f"50632b56-6d78-4e81-8e85-be99e80a247c"
    elif target_page == Page.NGSL__PgD6F_Book_Chapter_List_Editor_Page__Non_head_version:
        url = f"{FrontEndUrl.Root}/#/{ProjectMode.testUrlPrefix}{A.Book}/{A.Chapter}/{A.List}/" \
              f"50632b56-6d78-4e81-8e85-be99e80a247d"
    elif target_page == Page.Pg32E_Chapter_Word_List_Editor_Page__ch1_update_1_head_ver:
        url = f"{FrontEndUrl.Root}/#/{ProjectMode.testUrlPrefix}{A.Chapter}/{A.Word}/{A.List}/" \
              f"5c73b89a-3512-4830-b6f3-0a89c66bc47d"
    elif target_page == Page.Pg32E_Chapter_Word_List_Editor_Page__ch1_update_1_NOT_head_ver:
        url = f"{FrontEndUrl.Root}/#/{ProjectMode.testUrlPrefix}{A.Chapter}/{A.Word}/{A.List}/" \
              f"5c73b89a-3512-4830-b6f3-0a89c66bc47e"
    elif target_page == Page.Pg32E_Chapter_Word_List_Editor_Page__empty:
        url = f"{FrontEndUrl.Root}/#/{ProjectMode.testUrlPrefix}{A.Chapter}/{A.Word}/{A.List}/" \
              f"925acfc2-0f96-4404-ab0e-8f7c18457a30"
    else:
        assert f"Unknown target_page url = {target_page}"

    print(f"open default [9F0_My-Book-List-Page] url={url}")
    c.browser.get(url)


@then('default target page is shown')
def then_default_target_testing_page_is_shown(c):
    target_page = getattr(c, CotA.TargetPage)
    pg_id = None
    if target_page == Page.Pg29D_Create_My_Book_Page:
        pg_id = PageId.WordBookLibrary_CreateMyBookPage
    else:
        assert f"Unknown target_page url = {target_page}"
    assert_page_id(c, pg_id)


@then('the current page showing in page list bar is {page_str}')
def then_the_current_page_showing_in_page_controller(c, page_str: str):
    elm = w__get_element_by_shown_dom_id(c, [A.Page, BehaveUtil.clear_string(page_str), A.Button])
    class_list = elm.get_attribute("class").split()
    found_curr_class = False
    for c in class_list:
        if c.find('StPagination_CurrButton') > -1:
            found_curr_class = True
            break
    assert found_curr_class


@then('[previous page button] is NOT showing in bottom app bar')
def then__previous_page_button_is_not_showing_in_bottom_app_bar(c):
    w__assert_element_not_existing(c, [A.BottomAppBar, A.PreviousPage, A.Button])


@then('[previous page button] is showing in bottom app bar')
def check_previous_page_btn_showing(c):
    elm = w__get_element_by_shown_dom_id(c, [A.BottomAppBar, A.Add, A.Book, A.Button])
    w__assert_element_existing(c, [A.BottomAppBar, A.PreviousPage, A.Button])


@then('[next page button] is NOT showing in bottom app bar')
def then_next_page_button_is_not_showing_in_bottom_app_bar(c):
    elm = w__get_element_by_shown_dom_id(c, [A.BottomAppBar, A.Add, A.Book, A.Button])
    w__assert_element_not_existing(c, [A.BottomAppBar, A.NextPage, A.Button])


@then('[next page button] is showing in bottom app bar')
def then_next_page_button_is_showing_in_bottom_app_bar(c):
    elm = w__get_element_by_shown_dom_id(c, [A.BottomAppBar, A.NextPage, A.Button])
    assert elm is not None


@when('{mentor} click on [next page button] on bottom app bar')
def when_click_on_next_page_button__on_bottom_app_bar(c, mentor: str):
    w__click_element_by_dom_id(c, [A.BottomAppBar, A.NextPage, A.Button])


@when('{mentor} click on [Page {page_str} Button] on page list bar')
def when_click_on_page_button_on_page_controller(c, mentor: str, page_str: str):
    page_str = BehaveUtil.clear_string(page_str)
    w__click_element_by_dom_id(c, [A.Page, page_str, A.Button])


@then('["{page}"] page is shown')
def check_page_show(c, page: str):
    page = BehaveUtil.clear_string(page)
    page_id = ''
    if page == '9F0_My-Book-List-Page':
        page_id = '9F0D60'
    if page == '32E_Chapter-Word-List-Editor-Page':
        page_id = '32E1C5'

    if page == 'FF8_Word-Info-Page':
        page_id = 'FF8382'
    if page == 'F15_Voice-of-Word-Page':
        page_id = 'F15AB0'
    if page == 'D6F_Book-Chapter-List-Editor-Page':
        page_id = 'D6FC58'
    if page == '1BF_Create-New-Chapter-Page':
        page_id = '1BF3D8'

    assert_page_id(c, page_id)


@then('[WordLearn_291_Book-Chapter-List-Page] is shown')
def then_show_word_learn__book_chapter_list_page(c):
    assert_page_id(c, PageId.WordLearn_BookChapterListPage)


@then('[WordLearn_154_Chapter-Word-List-Page] is shown')
def then_ChapterWordListPage_is_shown(c):
    assert_page_id(c, PageId.WordLearn_ChapterWordListPage)

