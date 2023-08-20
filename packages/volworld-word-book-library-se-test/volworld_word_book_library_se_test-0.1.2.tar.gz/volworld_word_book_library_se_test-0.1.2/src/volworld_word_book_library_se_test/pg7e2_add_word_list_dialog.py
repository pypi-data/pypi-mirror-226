
import pyperclip
from selenium.webdriver import Keys
from behave import *
from api.A import A
from volworld_aws_api_common.test.behave.selenium_utils import w__get_element_by_shown_dom_id, w__click_element_by_dom_id, \
    click_element, scroll_to_bottom
from volworld_aws_api_common.test.behave.row_utils import assert_tag_icon_class_of_list
from selenium.webdriver.common.by import By
from volworld_common.test.behave.BehaveUtil import BehaveUtil

from src.volworld_word_book_library_se_test.nav_utils import open_nav_more_actions_drawer
from test.behave.CotA import CotA
from test.behave.PageGroup import PageGroup


@when('"{mentor}" paste in word list of [add word list dialog] as "{word_list}"')
def clear_word_list(c, mentor: str, word_list: str):
    pyperclip.copy(BehaveUtil.clear_string(word_list))
    input_elm = w__get_element_by_shown_dom_id(c, [A.Word, A.List, A.Dialog, A.Input])
    input_elm.click()
    input_elm.send_keys(Keys.CONTROL, 'v')


@then('[save button] of [add word list dialog] is "{active}"')
def check_add_word_list_dialog_btn(c, active: str):
    btn = w__get_element_by_shown_dom_id(c, [A.Word, A.List, A.Dialog, A.Save, A.Button])
    assert btn is not None
    enabled = BehaveUtil.clear_string(active).lower() == 'enabled'
    assert btn.is_enabled() == enabled