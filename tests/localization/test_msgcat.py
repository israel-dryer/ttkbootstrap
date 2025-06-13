
from ttkbootstrap.localization.msgcat import MessageCatalog
from ttkbootstrap.localization.msgs import initialize_localities

initialize_localities()

def test_msgcat():
    """Basic translate() checks."""
    # unknown strings will return untranslated:
    MessageCatalog.locale("en")
    expect = "__unknown_string__"
    result = MessageCatalog.translate(expect)
    assert result == '__unknown_string__'

    expect = "Cancel"
    result = MessageCatalog.translate(expect)
    assert result == 'Cancel'

    MessageCatalog.locale("nl")
    expect = "Cancel"
    result = MessageCatalog.translate(expect)
    assert result == 'Annuleren'

    MessageCatalog.locale("zh_cn")
    result = MessageCatalog.translate("Skip Messages")
    assert result == "跳过信息"

    result = MessageCatalog.translate("yes")
    assert result == "确认"


def test_variables():
    """Tests using parameters."""
    MessageCatalog.locale("en")
    num = 2
    string = "string value"
    real = 3.14

    template = "test with string: '%s'"
    expect = "test with string: 'string value'"
    result = MessageCatalog.translate(template, string)
    assert result == expect

    template = "test with int: %d"
    expect = "test with int: 2"
    result = MessageCatalog.translate(template, num)
    assert result == expect

    template = "test with signed int: %+d"
    expect = "test with signed int: +2"
    result = MessageCatalog.translate(template, num)
    assert result == expect

    template = "test with real: €%.2f"
    expect = "test with real: €3.14"
    result = MessageCatalog.translate(template, real)
    assert result == expect

    template = "test with multiple variables: %s, %d, %.3f"
    expect = "test with multiple variables: string value, 2, 3.140"
    result = MessageCatalog.translate(template, string, num, real)
    assert result == expect


def test_positional_variables():
    """Tests using positonal parameters in its message."""
    MessageCatalog.locale("en")
    num = 2
    string ="string value"
    real = 3.14

    template = "test with string: '%1$s'"
    expect = "test with string: 'string value'"
    result = MessageCatalog.translate(template, string)
    assert result == expect

    template = "test with int: %1$d"
    expect = "test with int: 2"
    result = MessageCatalog.translate(template, num)
    assert result == expect

    template = "test with signed int: %1$+d"
    expect = "test with signed int: +2"
    result = MessageCatalog.translate(template, num)
    assert result == expect

    template = "test with real: $%1$.2f"
    expect = "test with real: $3.14"
    result = MessageCatalog.translate(template, real)
    assert result == expect

    template = "test with multiple variables: %1$s, %2$d, %3$.3f"
    expect = "test with multiple variables: string value, 2, 3.140"
    result = MessageCatalog.translate(template, string, num, real)
    assert result == expect

    template = "test with reordering variables: %2$d, %1$s, %3$.3f"
    expect = "test with reordering variables: 2, string value, 3.140"
    result = MessageCatalog.translate(template, string, num, real)
    assert result == expect

    # using %1d syntax (without ending $) works as well
    # (except changing parameter order):
    template = "test with string: '%1s'"
    expect = "test with string: 'string value'"
    result = MessageCatalog.translate(template, string)
    assert result == expect

    template = "test with int: %1d"
    expect = "test with int: 2"
    result = MessageCatalog.translate(template, num)
    assert result == expect

    template = "test with signed int: %+1d"
    expect = "test with signed int: +2"
    result = MessageCatalog.translate(template, num)
    assert result == expect

    template = "test with int as string: %1s"
    expect = "test with int as string: 2"
    result = MessageCatalog.translate(template, num)
    assert result == expect

    template = "test with hex: %1x"
    expect = "test with hex: ff"
    result = MessageCatalog.translate(template, 255)
    assert result == expect

    template = "test with binary: %1b"
    expect = "test with binary: 11110001"
    result = MessageCatalog.translate(template, 241)
    assert result == expect

    template = "test with octal: %1o"
    expect = "test with octal: 361"
    result = MessageCatalog.translate(template, 241)
    assert result == expect

    template = "test with real: $%1.2f"
    expect = "test with real: $3.14"
    result = MessageCatalog.translate(template, real)
    assert result == expect

    template = "test with multiple variables: %1s, %+2d, %3.3f"
    expect = "test with multiple variables: string value, +2, 3.140"
    result = MessageCatalog.translate(template, string, num, real)
    assert result == expect

    # reordering variables like this will fail with a TclError:
    # template = "test with reordering variables: %+2d, %1s, %3.3f"
    # expect = "test with multiple variables: +2, string value, 3.140"
    # result = MessageCatalog.translate(template, string, num, real)
    # assert result == expect

def test_string_escaping():
    """Check escaping of characters with special meaning in Tcl."""
    MessageCatalog.locale("en")

    template = "test with string: '%s'"
    result = MessageCatalog.translate(template, "string")
    assert result == "test with string: 'string'"

    # escape test "
    result = MessageCatalog.translate(template, 'string " with quote')
    assert result == "test with string: 'string \" with quote'"

    # escape test [
    result = MessageCatalog.translate(template, 'string [test] with braces')
    assert result == "test with string: 'string [test] with braces'"

    # escape test no need to escape { or }:
    result = MessageCatalog.translate(template, 'string {test} with curly braces')
    assert result == "test with string: 'string {test} with curly braces'"

    result = MessageCatalog.translate(template, '{string with curly braces}')
    assert result == "test with string: '{string with curly braces}'"

    # escape test \
    result = MessageCatalog.translate(template, 'string \ with backslash')
    assert result == "test with string: 'string \ with backslash'"


def test_set():
    """Add a translated string with formating patterns and use is to localize a text."""
    string = "string value"

    MessageCatalog.locale("nl")

    # add 2 tranlslated strings with parameters in them:
    template = "test with string: '%1$s'"
    MessageCatalog.set("nl", template, "test met een string: '%1$s'")
    MessageCatalog.set("nl", "product: '%1$s , price: %2$.2f", "Prijs: %2$.2f, Product: %1$s")

    # expect NL translation:
    expect = "test met een string: 'string value'"
    result = MessageCatalog.translate(template, string)
    assert result == expect

    # expect NL translation; order of variables reversed:
    expect = "Prijs: 3.14, Product: ABC-123"
    result = MessageCatalog.translate("product: '%1$s , price: %2$.2f", 'ABC-123', 3.14)
    assert result == expect

    # no French translation, expect English string:
    MessageCatalog.locale("fr")
    expect = "test with string: 'string value'"
    result = MessageCatalog.translate(template, string)
    assert result == expect


def test_set_many():
    """Add multiple translated strings with formating patterns and use them."""
    string ="string value"
    num = 2

    MessageCatalog.locale("nl")

    template1 = "test with [string]: '%1$s'"
    trans1 = "test met een [tekst]: '%1$s'"

    template2 = "test with [int]: %1$d"
    trans2 = "test met een [nummer]: %1$d"

    MessageCatalog.set_many("nl", template1, trans1, template2, trans2)

    # expect NL translated string with variable expansion:
    result = MessageCatalog.translate(template1, string)
    expect = "test met een [tekst]: 'string value'"
    assert result == expect
    result = MessageCatalog.translate(template2, num)
    expect = "test met een [nummer]: 2"
    assert result == expect
    result = MessageCatalog.translate(template1, "$")
    expect = "test met een [tekst]: '$'"
    assert result == expect
    result = MessageCatalog.translate(template1, "[test]")
    expect = "test met een [tekst]: '[test]'"
    assert result == expect

    # no French ranslations, so expect English/original string with variable expansion:
    MessageCatalog.locale("fr")
    expect = "test with [string]: 'string value'"
    result = MessageCatalog.translate(template1, string)
    assert result == expect
    result = MessageCatalog.translate(template2, num)
    expect = "test with [int]: 2"
    assert result == expect


if __name__ == '__main__':
    test_msgcat()
    test_variables()
    test_positional_variables()
    test_string_escaping()
    test_set()
    test_set_many()
