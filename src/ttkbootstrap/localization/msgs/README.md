# Message Catalog Setup

Instructions for setting up a message catalog file for ttkbootstrap

1. Create a new .msg file with the language prefix codes. See the zh_cn.msg file as an example of this. The codes should be separated with an underscore '\_' as in 'zh_cn' >>
    https://wiki.freepascal.org/Language_Codes

2. Add the following pattern for each word you want to translate:

    ::msgcat::mcset  zh_cn "Letter " "信 "

    - The first item is "::msgcat::mcset"
    - The second item is the language code
    - The third item is the source English word
    - The last item is the English word translated into the target language

3. The following words / phrases should be translated for a new language in ttkbootstrap at a minimum:

    - "Ok"
    - "Retry"
    - "Delete"
    - "Next"
    - "Prev"
    - "Yes"
    - "No"
    - "Open"
    - "Close"
    - "Add"
    - "Remove"
    - "Submit"
    - "Family"
    - "Weight"
    - "Slant"
    - "Effects"
    - "Preview"
    - "Size"
    - "Should be of data type"
    - "Invalid data type"
    - "Number cannot be greater than"
    - "Out of range"
    - "Previous"
    - "The quick brown fox jumps over the lazy dog."
