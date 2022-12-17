"""
    A module various classes that can be used either in text as `Emoji` 
    or in the tkinter.PhotoImage class as in `Icon`.
"""


class Icon:
    """A container class that contains base64 image attributes that can
    be used in the `PhotoImage` class using the `data` parameter.

    Attributes:

        icon (str): The ttkbootstrap icon.
        error (str): An error image.
        warning (str): A warning image.
        question (str): A question image.
        info (str): An info image.

    Examples:

        ```python
        img = tk.PhotoImage(data=Icon.warning)
        ```
    """

    icon = "iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAAFxEAABcRAcom8z8AAAT/SURBVFhHzZd9TNR1HMff/O64BwKOp+NRnkIScJI2n7ZqFmqjVhkrHExrrDFZLnPkqmEyW2WtlQ1SQawWPSAYiJLNGvK0VhJOaDgVBDPCw0PwEOUQfsfd/fp+v/cFbt0Bd6yxXvfP5+F79/l+P9+H+3w8wMnO3r40I+P5vOCQ4I1ymVzrQeCu/wSJYDabB/sHbp45XlnzQUnJgcvcBRQUHEjX6/vH6aCFQK/XjxcWHnyBxpbRle/Ysf3n0NAQJTWMmiRUnB/FNy1GNHaNYdwsIS7IE4JdPqxWKxoam3D0aAVq6+rR39+P2NhYKBQKPsJGx3Abyq8dxGldBbrvXkSoVyR8Pf3g7e0tj46O2mQ0Gqs96urqv1u/PmUL/cLfQ2a8/O0t9A2b2Q9MsjpGicOZQfBSeEAURbyZtxstLee410awVovCgk8RGxPD9NLuT1B6dT+TJ/EUFMhL/gwpYZuYXl/fUCbQPaeKVQJyqwwOwSnnekR8VDvM5JIjnzsEpwwMDmL32/mwWCxoHqhzCE6ZsJrw4YWduHGvh+k0tkAPHFXadSZc1k8whzNOtt+DcWwCJ2p+4BZH/urpwfnWNpzs/YpbHJmwivjxehmTaWxh8rTT9M+GSM7CpZ5BjI2NcYtzdH069PEVzsSkn8YWmETQek+JTpER9/3h/pDL5dzinKDAQAQqg7nmHHv/VNRV5KCFaWRcc2RdvBpajRopjz/GLY4EBARgzerVeCKc3TCneJDPxohp/9QEFDIPfJwWwE76v1nkL8fep/yYnLvzNURFRTLZHqVSib35e6BSqfDkokysC32ae6ahwbPidyFRs4JbiK2jo1NKSFjCVaDHYMaRX0fQ3mcikwIeiVMh+2EfaNTTW2Q0jqKsvBxnzzaza5mYmICXXtw6dQUpVslK7n85ztyogkEcQIRXLNKis7BWu4GPADo7rzhOYCGZ9wQmxi249NN19P5xCxaTFdo4XyQ/Gw3fEDUf4RrzmoA4MoFT77RiqNfILTY8VTKk5i1HWJI/t8wNncDsd88JzV93OQSn0Kw0FF5kGXEHtyZgJj/+5283uebI6JAI3QUD11zDrQmIIyZYzLOvcNQgcsk13JqASqOAXDnzY0XxcfMgujUBmVzAkpRwrjmiCfNCxLIArrmG24dwzZbFTk+6mmRnw+vLIJAX1R3m9Q5IpHjo/kWP3jYDOZgW9g4sTY2EyseTj3CN/8VL6PYWMO70A1W7gHeTgfzFwBcZpBpp4U7OuAl4jxQm8ZvJ/pB/0IeygC9P0fKYD7DhfgaGeoFDzwAjA9zAEcjtyDwEPEjqPZFUVqm5QFMbd9rxShpQ9AYT55eBmj2OwSlWC1D9Fln5XaC42nlwSvEJoLGVK+7eApE8wVcauOKEsTtAVxPwfT03zMCxab9AGwUuz834iG2lszF6GzCQLMzGkM1PYwu0XWKaK/iQAlqt4coMhDwAJE0XJk7hfhpboL0a01xBIAXpo9u44oRIUmrFriV1G7kV9q2UPb73AdueYyKNLfNSazpXrlyRTdslZp2LmFXAbR2gn+4tGSHkJmWVkgz5AtGhpOsgT3ItaWBIGzeFnw9QuQ9YHk/bObG4qGgrs9NGkTaMdE9c5trvknR6nyTV5EtS23HS+pq4w46rOkl6v1SSXt0vSQXHJGlwmJltzWkhK42n8pSTk5OUnr5598K055WkPS8hKQT+AVyRrtzM5URAAAAAAElFTkSuQmCC"
    error = "iVBORw0KGgoAAAANSUhEUgAAAB4AAAAeCAYAAAA7MK6iAAAABmJLR0QA/wD/AP+gvaeTAAAEc0lEQVRIDcVXbU8bRxCee7MxkGBTSIJt0UAjRES+tKDKUfoFm5I0UVuFUKr+h/ZTf0Wr/pK2BFlKKkUmqOqHJKC8NFKiJKqJAEGNgRIIAcy97PWZde8EfgGnQcLy7M0+MzvP7e3ezB7REf2UWnnvDAx8qKrqkKZpl1zXPSWECJPrkqppa6Qoi2Tbv1lEYxcymT9ribkvsUukTKZSXyua9pNmGMcj8Xhd04kThh4Mkm4YMr5tWWTv7NDrfN5cXVgwhW2vOY7zfWJ8/BcERwjpVtbAVoZJAIRdrqalA6FQPN7T03istVXiBzWvl5dp4enTN2ahMOdY1hcXJiamK42pSDyZTCZJ19PR7u76lo4OtdLAg7Clly/F4osXW1iSz8+Pj/9OJb8y4nupVD8e7c2Ovr5QrbMsiel3efYz9+9v27Z9CTP/wzdA2UM81d/f4+r65AeJRENDczPM7/7fXF2l7NTUBgnRm8hk/vIiqp6CXaBQMPhz7Ny50GGRcmyOFcOS4W34VXIwCPGJ7w4MfBOsr29/r73dx2A/lH/L6dOaEQp13hscHPECShK+E9zRD21nzzZ6htKrduYMKXV1pbDfV0IhYh8fKFE4tqYoP3qwJL6TSvXhPW061tLi4XuuWlcXGVeuUODaNWKCPUZ0GGMb+7AvoLL/cbyOqmFE7iaTH7FREuua9lUkFqs6HTE7S2JpiRQMDoyMkNLQwGOlsC4x3DT7OPCVhgpNpK0tiDdmmE2SGJ1PMdtiKmK0RFxkJvP6dRL5PCmRCAWGhyW5JGUdGNvYh+BbMtzv4vUM4MkOMqBzg61+ChlKqlUbBOTAgaEhUk+eJJ4l+ypNTfKG2LYfKftig5ErRJR1OWN0Ipx/GdhX/iMXSItMyOJCr4WU4xrYnK7jNLMuiVmpVRQUBxbfn/t68cH5WA2KJFZUdZUrzEH+SmNjcX3DYbnZeDMp0L01P2i8hScGrn/YzyPOW9vb3K8qe0gXF8kcHZUioPsbDjdWNQAM1tYWYSPnoJIkRv28sYZ6ykAlKSMdGyO5kTADE3qt5KjZBdTrG8xRJHbd0fVczmSgkqjRKHkbyUqni6SeI8gZc1dWpA/7eqbS66tcznGEGGVcVidOmVMXL8519PbG8a4xXiacDsX8PLmFQpmNAc5eaixGTjbL3TLhEjn74MHcx7duvc9GOWOwu45tfzf/5MkbnKcYLxMOWI2UnV3sEfZhvVQ45vzjx5s4kXzr2SQxd87fvp22TXNueWZGcP8wZWV62hGOM52YmJDry7F9Yp61ZZqXc8+ebawjNbLxMGQduz6Xza7vOM5nzOHF9IkZwPEE1UBcnX34cHsDGYmxdxG5ro8ebeMkevWTTObv3bFwE7u7RV0e9jRtrK27u661szNQRN+uxWHPzD1/XsD6flnTYc8LfyTHW4/c3XWgV3U9HI5GAyjoRgD12KtmJrLRzuYm4bFanAtQBF4hIf3/A71H7l13fcJcRjWLYpe2sA2fMCv4tFlARrppvcUnDI89EvkXuxHzVm+w/WUAAAAASUVORK5CYII="
    warning = "iVBORw0KGgoAAAANSUhEUgAAAB4AAAAeCAYAAAA7MK6iAAAABmJLR0QA/wD/AP+gvaeTAAADO0lEQVRIDe1V3UtTYRh/P87HPo815+zoNlHb5tzUbTmnQiUU6QZGBN4UBBURIgR1E9TNkkIi8SIw2BKi226iG5cfMKiLoIT+hO4qRSIIg3Tb6TxHtpbbzs4RIogO5znvc37P7/n9zns+3oPQX9rwfnyz8yOWvMl8nyAs7dDtm6MXlrf06jB6G4BfMAtPmhziOEIS2tz42CxjE3Lo2okutkxeWkgcIwTHg9EhPhAd5gmhccDkkq5dl3EymSQMJQu+3n4ToRRROSAHDGp6nHUZDzvfXjJbG0TR3VZ6NyA3WQVxyPXu4h8xXkmdbJBv8aw/PGBBCJd5YNQdjlkYgmeBU1ZQTTXPmLLGaYfTzQkHbRWCgDW1unjCGZNI46bJeDWd8EpYuuLrCRtr6e7WpKvArcUpxzUZE54+6vAFOY7/5Rs7+wxBFMWg1uELcIRn5ouY2ljXeCU9NkopG3N7/VRNCGpubzelDDMIPXCuFqrGa6kjLGGZtD/UbyFElap4AKerL2qBnmxyRHVxUlX7yjZPCgdstqYWlyKs5eBocSLoybnMk2r8msbZ1LgdY3LXH4nJn4+aRGXNHxmwEIzvrT490VhZ3UVqGhd4NCO621mzVdhl6jjKiwwS29pZjIwztdqqGq+kEj3y+n/ucCBkqNVYD1d6C/i8olWFXNWYGuhjT7DPwHJclRZtEPR6gr0GytN0tY4K4+X02GmWMwScHd6KWjUBNczZ4SMszweXFuLje3nliy5afBjnOYH5EB48Ltoc8JvdS9d//mVjHb1/k/20/a3QnriW+VFU+G1WnAXfsDXaBS2mnze/I4iiUK0RtGyNDoG34uvlnJLxy9SoiBG51RUaMJcTquVgODG1iCamMmhdvoBqnHKsKyxrSuQ2eBTxkjFn4GZdnV7WaNbw2UpSsV9++UtpzQQ0nZ0eluP5B0WS8oxX02NRynPZo/EzZsqwxZrqCLMGwiG7CYa6kc/toFeZ51u5XH7k1OXFNWXGhOPmPMGQUaspuIAhBORaArS9gYiRpcwc8BXjQj4fsYutSg7gnwrwyBdyEdBX/iCUkOnXmRfTUqGw/xUD1OoEJmSbEuZOHdr/8j9yB34CUBepV8n7RlcAAAAASUVORK5CYII="
    question = "iVBORw0KGgoAAAANSUhEUgAAAB4AAAAeCAYAAAA7MK6iAAAABmJLR0QA/wD/AP+gvaeTAAAEvElEQVRIDcVX208cVRj/5sxlB1j2Aiyy2lpgEZVaUvXBeIvERCOwC1Qlvhj/gcYnE1PAR1tsU598bOK7sV6A3ZVEX9pqE32yFzDKdlkS6ILslUXYmT0z4zlnmbLtzt76oJPznXO+y+/7zsy5fQPwPz1cvXEnpkMnDZ4/JSA0AobRpem6i2J5hDKAuLiGtTAu4O+C5wM3qLwW1QhscIHp8KTAo88FQXR2dnps7rY2SRIFEAWB+S5gDGoBQzqVVLf+TigYa2kDax/NzQ5/A8AZzMiiqhh47MxiHxKNOZvNdsTn8zncLqcFvFyUTmcgEo3m1Ly6RgY1HvrMHy23IkOyEk58sjDEceL33d3HWr1eL+IqDs8KTWUGbGzEtVhsbdfQtMDcrP8alZZSmcvAVPg1XkTzJ5453upobS3Tl4Jr9bM7OWNpaXkHa7p/4ezwz6X29zk+NRXqB4H/dXDwhMtubym1e+j+7u4u3Lh5K40N/ELw08CK6UgwOwAGB/zi1729PS3VgjpkBENPy3DUXYSupzFc+TMPmT390FVJz263Q09Pt31tNfYVADxHiBXEalKNTYfea25ufryr6xGRsJallQT94GU79BOTJokDSk+Q/vsv2oHqLEFE+KjXK9pkuXd8KvwuYVk5CGxwCAkXen09bG8yjUX1OnlTWeQguo3h0pUcXLqaY30qG3pKtkAcinx9PifiuYumhAUemwk/L0mCgzym3LI91l78vD8u7UN2X4cs+bw/Le8z2+6Ooo4xFpXT4QBRFF1jZ8LPUjULjBA36fF4mqmgGklCcS3m8ofzWdAOzoiDphre0+lpQgI3SW3YMBEnvOFyuyrOLTWkdHExS5v76ORRifFbOY211Sqn0yltxjffJDbT7I3B0L02SSJ8Y8XXKcJLfcW5/S2q1ATLsg3It/JSQxaYHPhuSbJRvm5qa0EwOtgE9FS7HslDLIFrYiXycrqmtVNDFph2GqVX+2Wgc35rXYXrEaUBeHGdsMCI51Oq2ggY4GgbWx5w9a983UEVRQHEoyQFFANzsKWoKuXrJrp3qfG+WsdypoaEFEUFEjBOusCGXcB6MJlIDbjIqqPCeshqhdfCpVKpPFlPQWpHBgCgY3w5kdhu7JUpukHaTmxrBV27TGEscPC8/6amGelMtnyfUiMr6rDzQMlKZyWjCYKO9UTonP821bPAJB8wsI4/jKxEdow6poxuJXpZUHKTbUUdVScDViJ3cpqunTbtDgIDLJwdmVcVNba1tVkwlfW0xc1R3fJufLOgFdTI/Dl/yLRki6vIcIamzg1H76z+Tq6wDrfLVdFn6h8dvryWY7BK9zBTkiqZShmrq7Es0rhRwt4rZc5Z6sNzoYHjA80kwSvT30PW0UlnMsby0h975B55q2rqY/oKzPzwCrmI5rpJ5kCSPYkei6auvtaA9Y14PrZGkj1sTMzPjvzyII57UGDyb38cPgIy+laUpCcfJr3FamEJ5/PvzF8Yv2v6LG0rBjaNAjOhcQEJX/A8cne0t5OE3iXKsgyUqI2i5GF/Lw+pTEZNJhIFklEmyV/F6YXZ0SDVV6KagU2g+Qsj8tyorhmPkROogySIwCM+QVKaDUxOv0Z+YUy//3n7L6y2u/Lkn4gSAAAAAElFTkSuQmCC"
    info = "iVBORw0KGgoAAAANSUhEUgAAAB4AAAAeCAYAAAA7MK6iAAAABmJLR0QA/wD/AP+gvaeTAAADzElEQVRIDcWXzXPbRBTAn7SSrJbEH8Vp4rjFjjPDUCgz0PbMDMwAwRknE4aP4dpe4QSHEigHSDNDp/9C+wfQr6RNTLgxvXGDoaEpxDSJmzYhtpSPUluydpd9InJE4yTqpCYaPe3Te2/fb3dlrZ8A9uiQgnL7TudfVQh/V1LUHuC8gzIWxb5ElpdBkhYcxvISpddGhnt/RvtOsgOYS32D4x8SQs4TRQ23H4zrsQPPqpqqgKoobu6a40DNroFhmvbi4l82pXTZofTTG8PZSwASd4MaXLYED3w+/jwoZFTT1EPd3d0tsVi0QffNJtM0oVC4+9CyrTmxMn0jQ9nC5igxpEbG3Jf5NxSQR1Pp1P5kskPeIqxR13Ubh/n5+2x2pviIQy03MpT7ER47Ns24b3DsdSKT8SMvHtkXdJaP5azf4uxv/zZVoZz1XD/be7PuEMp/wLkzEy8Rzn86+vLRZyLhVuHe/bm6sgq3JifXatw5PjaU+8PLKHsKAJcUCb7LZLr2BYGGdRlQNvo31sKRMKS60vs1Wb2MDC+qDu4/k/9ID+nPJRL4TD134xaBp15rhZNCWsUAGkdtWJOJBAmF9Ez/F99/4FnXwVySgXybyaRbPMe2re8B+dRtu3R1pVokIp/zglxw7vTECaIokWg02CuzWmFw4eYaXBSyWmVerm3bWCwm3k4llhu8cQwDXbCssPfbD7bpaAgqCEQJGo9x7W1tISIr76Hubj+KrL4ppquiIYh81hOph52fWKnrOymRaERbWFh4S8QNujPmnHXoIU3cBzufBObPqOshYJx3os0Fiw0/pmkhvG+qaJoGjPEDCHHBqPzf4oJlQgzbtprOtiwLZCKXEfQvWIJFy7bxvqliWTYI4AOEiBaAOmzMKBlNJxumURW/p7E6GDi7slQqNR28tLREucSu1MEjw9lfsHIwzWW0NUVMwwTKeHn0m95fEeAutfij547DPpmeLjzkfMtqBeNd8W8gft11NrhgzunCn39zyj723L49nksDX/1wK3X48AvJQ8n1AXlhu2uL9+bpvWJx8urXb7+Ck8RsPoDELUqzM7Nza4ZYFnQ+DSmXDSjOFVecqvWOB8W8PjBA/mzvLGN0YOr275Wn8byx9LkzdadCRc7r5/rvI9AT31J7JgAs9sSIrmXSab0zmdDESDecgTQs9h7Yd2dmqhLQ/kDFnpd3T8pbD441Ur2gJyQaj8c1UXmquq4DCsZZVhUqj6qioF+ulcslUdAzc1cFPSb1y8YnjJLljHeKHSiOfvEJU5KJNF+jfPxJPmGw757IPxpVi5HvZ9PZAAAAAElFTkSuQmCC"


class EmojiItem:

    """A container for an emoji character used by the Emoji class"""

    def __init__(self, name, category, subcategory, char):
        """
        Parameters:

            name (str):
                The name of the emoji character.

            category (str):
                The major category of the emoji character.

            subcategory (str):
                The subcategory of the emoji character.

            char (str):
                The unicode character.
        """
        self.name = name
        self.category = category
        self.subcategory = subcategory
        self.char = char

    def __repr__(self) -> str:
        return self.char


class Emoji:
    """A class that contains emoji characters that can be used in the
    `text` parameter in any tkinter widget with the option.
    """

    _ITEMS = [
        EmojiItem("KNOT", "activities", "arts & crafts", "🪢"),
        EmojiItem("SEWING NEEDLE", "activities", "arts & crafts", "🪡"),
        EmojiItem("BALL OF YARN", "activities", "arts & crafts", "🧶"),
        EmojiItem("SPOOL OF THREAD", "activities", "arts & crafts", "🧵"),
        EmojiItem("FRAME WITH PICTURE", "activities", "arts & crafts", "🖼"),
        EmojiItem("PERFORMING ARTS", "activities", "arts & crafts", "🎭"),
        EmojiItem("ARTIST PALETTE", "activities", "arts & crafts", "🎨"),
        EmojiItem("THIRD PLACE MEDAL", "activities", "award-medal", "🥉"),
        EmojiItem("SECOND PLACE MEDAL", "activities", "award-medal", "🥈"),
        EmojiItem("FIRST PLACE MEDAL", "activities", "award-medal", "🥇"),
        EmojiItem("TROPHY", "activities", "award-medal", "🏆"),
        EmojiItem("SPORTS MEDAL", "activities", "award-medal", "🏅"),
        EmojiItem("MILITARY MEDAL", "activities", "award-medal", "🎖"),
        EmojiItem("SPARKLES", "activities", "event", "✨"),
        EmojiItem("FIRECRACKER", "activities", "event", "🧨"),
        EmojiItem("RED GIFT ENVELOPE", "activities", "event", "🧧"),
        EmojiItem("TICKET", "activities", "event", "🎫"),
        EmojiItem("ADMISSION TICKETS", "activities", "event", "🎟"),
        EmojiItem("REMINDER RIBBON", "activities", "event", "🎗"),
        EmojiItem("MOON VIEWING CEREMONY", "activities", "event", "🎑"),
        EmojiItem("WIND CHIME", "activities", "event", "🎐"),
        EmojiItem("CARP STREAMER", "activities", "event", "🎏"),
        EmojiItem("JAPANESE DOLLS", "activities", "event", "🎎"),
        EmojiItem("PINE DECORATION", "activities", "event", "🎍"),
        EmojiItem("TANABATA TREE", "activities", "event", "🎋"),
        EmojiItem("CONFETTI BALL", "activities", "event", "🎊"),
        EmojiItem("PARTY POPPER", "activities", "event", "🎉"),
        EmojiItem("BALLOON", "activities", "event", "🎈"),
        EmojiItem("FIREWORK SPARKLER", "activities", "event", "🎇"),
        EmojiItem("FIREWORKS", "activities", "event", "🎆"),
        EmojiItem("CHRISTMAS TREE", "activities", "event", "🎄"),
        EmojiItem("JACK-O-LANTERN", "activities", "event", "🎃"),
        EmojiItem("WRAPPED PRESENT", "activities", "event", "🎁"),
        EmojiItem("RIBBON", "activities", "event", "🎀"),
        EmojiItem("BLACK CHESS PAWN", "activities", "game", "♟"),
        EmojiItem("BLACK DIAMOND SUIT", "activities", "game", "♦"),
        EmojiItem("BLACK HEART SUIT", "activities", "game", "♥"),
        EmojiItem("BLACK CLUB SUIT", "activities", "game", "♣"),
        EmojiItem("BLACK SPADE SUIT", "activities", "game", "♠"),
        EmojiItem("NESTING DOLLS", "activities", "game", "🪆"),
        EmojiItem("PINATA", "activities", "game", "🪅"),
        EmojiItem("MAGIC WAND", "activities", "game", "🪄"),
        EmojiItem("KITE", "activities", "game", "🪁"),
        EmojiItem("YO-YO", "activities", "game", "🪀"),
        EmojiItem("NAZAR AMULET", "activities", "game", "🧿"),
        EmojiItem("TEDDY BEAR", "activities", "game", "🧸"),
        EmojiItem("JIGSAW PUZZLE PIECE", "activities", "game", "🧩"),
        EmojiItem("JOYSTICK", "activities", "game", "🕹"),
        EmojiItem("CRYSTAL BALL", "activities", "game", "🔮"),
        EmojiItem("FLOWER PLAYING CARDS", "activities", "game", "🎴"),
        EmojiItem("GAME DIE", "activities", "game", "🎲"),
        EmojiItem("BILLIARDS", "activities", "game", "🎱"),
        EmojiItem("SLOT MACHINE", "activities", "game", "🎰"),
        EmojiItem("DIRECT HIT", "activities", "game", "🎯"),
        EmojiItem("VIDEO GAME", "activities", "game", "🎮"),
        EmojiItem("PLAYING CARD BLACK JOKER", "activities", "game", "🃏"),
        EmojiItem("MAHJONG TILE RED DRAGON", "activities", "game", "🀄"),
        EmojiItem("ICE SKATE", "activities", "sport", "⛸"),
        EmojiItem("FLAG IN HOLE", "activities", "sport", "⛳"),
        EmojiItem("BASEBALL", "activities", "sport", "⚾"),
        EmojiItem("SOCCER BALL", "activities", "sport", "⚽"),
        EmojiItem("FLYING DISC", "activities", "sport", "🥏"),
        EmojiItem("SOFTBALL", "activities", "sport", "🥎"),
        EmojiItem("LACROSSE STICK AND BALL", "activities", "sport", "🥍"),
        EmojiItem("CURLING STONE", "activities", "sport", "🥌"),
        EmojiItem("MARTIAL ARTS UNIFORM", "activities", "sport", "🥋"),
        EmojiItem("BOXING GLOVE", "activities", "sport", "🥊"),
        EmojiItem("GOAL NET", "activities", "sport", "🥅"),
        EmojiItem("DIVING MASK", "activities", "sport", "🤿"),
        EmojiItem("SLED", "activities", "sport", "🛷"),
        EmojiItem(
            "BADMINTON RACQUET AND SHUTTLECOCK", "activities", "sport", "🏸"
        ),
        EmojiItem("TABLE TENNIS PADDLE AND BALL", "activities", "sport", "🏓"),
        EmojiItem("ICE HOCKEY STICK AND PUCK", "activities", "sport", "🏒"),
        EmojiItem("FIELD HOCKEY STICK AND BALL", "activities", "sport", "🏑"),
        EmojiItem("VOLLEYBALL", "activities", "sport", "🏐"),
        EmojiItem("CRICKET BAT AND BALL", "activities", "sport", "🏏"),
        EmojiItem("RUGBY FOOTBALL", "activities", "sport", "🏉"),
        EmojiItem("AMERICAN FOOTBALL", "activities", "sport", "🏈"),
        EmojiItem("BASKETBALL AND HOOP", "activities", "sport", "🏀"),
        EmojiItem("SKI AND SKI BOOT", "activities", "sport", "🎿"),
        EmojiItem("TENNIS RACQUET AND BALL", "activities", "sport", "🎾"),
        EmojiItem("RUNNING SHIRT WITH SASH", "activities", "sport", "🎽"),
        EmojiItem("BOWLING", "activities", "sport", "🎳"),
        EmojiItem("FISHING POLE AND FISH", "activities", "sport", "🎣"),
        EmojiItem("FROG FACE", "animal-nature", "animal-amphibian", "🐸"),
        EmojiItem("FEATHER", "animal-nature", "animal-bird", "🪶"),
        EmojiItem("FLAMINGO", "animal-nature", "animal-bird", "🦩"),
        EmojiItem("DODO", "animal-nature", "animal-bird", "🦤"),
        EmojiItem("SWAN", "animal-nature", "animal-bird", "🦢"),
        EmojiItem("PARROT", "animal-nature", "animal-bird", "🦜"),
        EmojiItem("PEACOCK", "animal-nature", "animal-bird", "🦚"),
        EmojiItem("OWL", "animal-nature", "animal-bird", "🦉"),
        EmojiItem("DUCK", "animal-nature", "animal-bird", "🦆"),
        EmojiItem("EAGLE", "animal-nature", "animal-bird", "🦅"),
        EmojiItem("TURKEY", "animal-nature", "animal-bird", "🦃"),
        EmojiItem("DOVE OF PEACE", "animal-nature", "animal-bird", "🕊"),
        EmojiItem("PENGUIN", "animal-nature", "animal-bird", "🐧"),
        EmojiItem("BIRD", "animal-nature", "animal-bird", "🐦"),
        EmojiItem(
            "FRONT-FACING BABY CHICK", "animal-nature", "animal-bird", "🐥"
        ),
        EmojiItem("BABY CHICK", "animal-nature", "animal-bird", "🐤"),
        EmojiItem("HATCHING CHICK", "animal-nature", "animal-bird", "🐣"),
        EmojiItem("CHICKEN", "animal-nature", "animal-bird", "🐔"),
        EmojiItem("ROOSTER", "animal-nature", "animal-bird", "🐓"),
        EmojiItem("COCKROACH", "animal-nature", "animal-bug", "🪳"),
        EmojiItem("BEETLE", "animal-nature", "animal-bug", "🪲"),
        EmojiItem("WORM", "animal-nature", "animal-bug", "🪱"),
        EmojiItem("FLY", "animal-nature", "animal-bug", "🪰"),
        EmojiItem("MICROBE", "animal-nature", "animal-bug", "🦠"),
        EmojiItem("MOSQUITO", "animal-nature", "animal-bug", "🦟"),
        EmojiItem("CRICKET", "animal-nature", "animal-bug", "🦗"),
        EmojiItem("BUTTERFLY", "animal-nature", "animal-bug", "🦋"),
        EmojiItem("SCORPION", "animal-nature", "animal-bug", "🦂"),
        EmojiItem("SPIDER WEB", "animal-nature", "animal-bug", "🕸"),
        EmojiItem("SPIDER", "animal-nature", "animal-bug", "🕷"),
        EmojiItem("LADY BEETLE", "animal-nature", "animal-bug", "🐞"),
        EmojiItem("HONEYBEE", "animal-nature", "animal-bug", "🐝"),
        EmojiItem("ANT", "animal-nature", "animal-bug", "🐜"),
        EmojiItem("BUG", "animal-nature", "animal-bug", "🐛"),
        EmojiItem("SNAIL", "animal-nature", "animal-bug", "🐌"),
        EmojiItem("GUIDE DOG", "animal-nature", "animal-mammal", "🦮"),
        EmojiItem("BISON", "animal-nature", "animal-mammal", "🦬"),
        EmojiItem("BEAVER", "animal-nature", "animal-mammal", "🦫"),
        EmojiItem("SKUNK", "animal-nature", "animal-mammal", "🦨"),
        EmojiItem("ORANGUTAN", "animal-nature", "animal-mammal", "🦧"),
        EmojiItem("OTTER", "animal-nature", "animal-mammal", "🦦"),
        EmojiItem("SLOTH", "animal-nature", "animal-mammal", "🦥"),
        EmojiItem("MAMMOTH", "animal-nature", "animal-mammal", "🦣"),
        EmojiItem("BADGER", "animal-nature", "animal-mammal", "🦡"),
        EmojiItem("RACCOON", "animal-nature", "animal-mammal", "🦝"),
        EmojiItem("HIPPOPOTAMUS", "animal-nature", "animal-mammal", "🦛"),
        EmojiItem("LLAMA", "animal-nature", "animal-mammal", "🦙"),
        EmojiItem("KANGAROO", "animal-nature", "animal-mammal", "🦘"),
        EmojiItem("HEDGEHOG", "animal-nature", "animal-mammal", "🦔"),
        EmojiItem("ZEBRA FACE", "animal-nature", "animal-mammal", "🦓"),
        EmojiItem("GIRAFFE FACE", "animal-nature", "animal-mammal", "🦒"),
        EmojiItem("RHINOCEROS", "animal-nature", "animal-mammal", "🦏"),
        EmojiItem("GORILLA", "animal-nature", "animal-mammal", "🦍"),
        EmojiItem("DEER", "animal-nature", "animal-mammal", "🦌"),
        EmojiItem("FOX FACE", "animal-nature", "animal-mammal", "🦊"),
        EmojiItem("BAT", "animal-nature", "animal-mammal", "🦇"),
        EmojiItem("UNICORN FACE", "animal-nature", "animal-mammal", "🦄"),
        EmojiItem("LION FACE", "animal-nature", "animal-mammal", "🦁"),
        EmojiItem("CHIPMUNK", "animal-nature", "animal-mammal", "🐿"),
        EmojiItem("PAW PRINTS", "animal-nature", "animal-mammal", "🐾"),
        EmojiItem("PIG NOSE", "animal-nature", "animal-mammal", "🐽"),
        EmojiItem("PANDA FACE", "animal-nature", "animal-mammal", "🐼"),
        EmojiItem("BEAR FACE", "animal-nature", "animal-mammal", "🐻"),
        EmojiItem("WOLF FACE", "animal-nature", "animal-mammal", "🐺"),
        EmojiItem("HAMSTER FACE", "animal-nature", "animal-mammal", "🐹"),
        EmojiItem("PIG FACE", "animal-nature", "animal-mammal", "🐷"),
        EmojiItem("DOG FACE", "animal-nature", "animal-mammal", "🐶"),
        EmojiItem("MONKEY FACE", "animal-nature", "animal-mammal", "🐵"),
        EmojiItem("HORSE FACE", "animal-nature", "animal-mammal", "🐴"),
        EmojiItem("CAT FACE", "animal-nature", "animal-mammal", "🐱"),
        EmojiItem("RABBIT FACE", "animal-nature", "animal-mammal", "🐰"),
        EmojiItem("TIGER FACE", "animal-nature", "animal-mammal", "🐯"),
        EmojiItem("COW FACE", "animal-nature", "animal-mammal", "🐮"),
        EmojiItem("MOUSE FACE", "animal-nature", "animal-mammal", "🐭"),
        EmojiItem("BACTRIAN CAMEL", "animal-nature", "animal-mammal", "🐫"),
        EmojiItem("DROMEDARY CAMEL", "animal-nature", "animal-mammal", "🐪"),
        EmojiItem("POODLE", "animal-nature", "animal-mammal", "🐩"),
        EmojiItem("KOALA", "animal-nature", "animal-mammal", "🐨"),
        EmojiItem("ELEPHANT", "animal-nature", "animal-mammal", "🐘"),
        EmojiItem("BOAR", "animal-nature", "animal-mammal", "🐗"),
        EmojiItem("PIG", "animal-nature", "animal-mammal", "🐖"),
        EmojiItem("DOG", "animal-nature", "animal-mammal", "🐕"),
        EmojiItem("MONKEY", "animal-nature", "animal-mammal", "🐒"),
        EmojiItem("SHEEP", "animal-nature", "animal-mammal", "🐑"),
        EmojiItem("GOAT", "animal-nature", "animal-mammal", "🐐"),
        EmojiItem("RAM", "animal-nature", "animal-mammal", "🐏"),
        EmojiItem("HORSE", "animal-nature", "animal-mammal", "🐎"),
        EmojiItem("CAT", "animal-nature", "animal-mammal", "🐈"),
        EmojiItem("RABBIT", "animal-nature", "animal-mammal", "🐇"),
        EmojiItem("LEOPARD", "animal-nature", "animal-mammal", "🐆"),
        EmojiItem("TIGER", "animal-nature", "animal-mammal", "🐅"),
        EmojiItem("COW", "animal-nature", "animal-mammal", "🐄"),
        EmojiItem("WATER BUFFALO", "animal-nature", "animal-mammal", "🐃"),
        EmojiItem("OX", "animal-nature", "animal-mammal", "🐂"),
        EmojiItem("MOUSE", "animal-nature", "animal-mammal", "🐁"),
        EmojiItem("RAT", "animal-nature", "animal-mammal", "🐀"),
        EmojiItem("SEAL", "animal-nature", "animal-marine", "🦭"),
        EmojiItem("SHARK", "animal-nature", "animal-marine", "🦈"),
        EmojiItem("SPOUTING WHALE", "animal-nature", "animal-marine", "🐳"),
        EmojiItem("DOLPHIN", "animal-nature", "animal-marine", "🐬"),
        EmojiItem("BLOWFISH", "animal-nature", "animal-marine", "🐡"),
        EmojiItem("TROPICAL FISH", "animal-nature", "animal-marine", "🐠"),
        EmojiItem("FISH", "animal-nature", "animal-marine", "🐟"),
        EmojiItem("SPIRAL SHELL", "animal-nature", "animal-marine", "🐚"),
        EmojiItem("OCTOPUS", "animal-nature", "animal-marine", "🐙"),
        EmojiItem("WHALE", "animal-nature", "animal-marine", "🐋"),
        EmojiItem("T-REX", "animal-nature", "animal-reptile", "🦖"),
        EmojiItem("SAUROPOD", "animal-nature", "animal-reptile", "🦕"),
        EmojiItem("LIZARD", "animal-nature", "animal-reptile", "🦎"),
        EmojiItem("DRAGON FACE", "animal-nature", "animal-reptile", "🐲"),
        EmojiItem("TURTLE", "animal-nature", "animal-reptile", "🐢"),
        EmojiItem("SNAKE", "animal-nature", "animal-reptile", "🐍"),
        EmojiItem("CROCODILE", "animal-nature", "animal-reptile", "🐊"),
        EmojiItem("DRAGON", "animal-nature", "animal-reptile", "🐉"),
        EmojiItem("WILTED FLOWER", "animal-nature", "plant-flower", "🥀"),
        EmojiItem("WHITE FLOWER", "animal-nature", "plant-flower", "💮"),
        EmojiItem("BOUQUET", "animal-nature", "plant-flower", "💐"),
        EmojiItem("ROSETTE", "animal-nature", "plant-flower", "🏵"),
        EmojiItem("BLOSSOM", "animal-nature", "plant-flower", "🌼"),
        EmojiItem("SUNFLOWER", "animal-nature", "plant-flower", "🌻"),
        EmojiItem("HIBISCUS", "animal-nature", "plant-flower", "🌺"),
        EmojiItem("ROSE", "animal-nature", "plant-flower", "🌹"),
        EmojiItem("CHERRY BLOSSOM", "animal-nature", "plant-flower", "🌸"),
        EmojiItem("TULIP", "animal-nature", "plant-flower", "🌷"),
        EmojiItem("SHAMROCK", "animal-nature", "plant-other", "☘"),
        EmojiItem("POTTED PLANT", "animal-nature", "plant-other", "🪴"),
        EmojiItem(
            "LEAF FLUTTERING IN WIND", "animal-nature", "plant-other", "🍃"
        ),
        EmojiItem("FALLEN LEAF", "animal-nature", "plant-other", "🍂"),
        EmojiItem("MAPLE LEAF", "animal-nature", "plant-other", "🍁"),
        EmojiItem("FOUR LEAF CLOVER", "animal-nature", "plant-other", "🍀"),
        EmojiItem("HERB", "animal-nature", "plant-other", "🌿"),
        EmojiItem("EAR OF RICE", "animal-nature", "plant-other", "🌾"),
        EmojiItem("CACTUS", "animal-nature", "plant-other", "🌵"),
        EmojiItem("PALM TREE", "animal-nature", "plant-other", "🌴"),
        EmojiItem("DECIDUOUS TREE", "animal-nature", "plant-other", "🌳"),
        EmojiItem("EVERGREEN TREE", "animal-nature", "plant-other", "🌲"),
        EmojiItem("SEEDLING", "animal-nature", "plant-other", "🌱"),
        EmojiItem(
            "EMOJI COMPONENT WHITE HAIR", "component", "hair-style", "🦳"
        ),
        EmojiItem("EMOJI COMPONENT BALD", "component", "hair-style", "🦲"),
        EmojiItem(
            "EMOJI COMPONENT CURLY HAIR", "component", "hair-style", "🦱"
        ),
        EmojiItem("EMOJI COMPONENT RED HAIR", "component", "hair-style", "🦰"),
        EmojiItem(
            "EMOJI MODIFIER FITZPATRICK TYPE-6", "component", "skin-tone", "🏿"
        ),
        EmojiItem(
            "EMOJI MODIFIER FITZPATRICK TYPE-5", "component", "skin-tone", "🏾"
        ),
        EmojiItem(
            "EMOJI MODIFIER FITZPATRICK TYPE-4", "component", "skin-tone", "🏽"
        ),
        EmojiItem(
            "EMOJI MODIFIER FITZPATRICK TYPE-3", "component", "skin-tone", "🏼"
        ),
        EmojiItem(
            "EMOJI MODIFIER FITZPATRICK TYPE-1-2",
            "component",
            "skin-tone",
            "🏻",
        ),
        EmojiItem("TRIANGULAR FLAG ON POST", "flags", "flag", "🚩"),
        EmojiItem("WAVING BLACK FLAG", "flags", "flag", "🏴"),
        EmojiItem("WAVING WHITE FLAG", "flags", "flag", "🏳"),
        EmojiItem("CHEQUERED FLAG", "flags", "flag", "🏁"),
        EmojiItem("CROSSED FLAGS", "flags", "flag", "🎌"),
        EmojiItem("CHOPSTICKS", "food-drink", "dishware", "🥢"),
        EmojiItem("SPOON", "food-drink", "dishware", "🥄"),
        EmojiItem("HOCHO", "food-drink", "dishware", "🔪"),
        EmojiItem("AMPHORA", "food-drink", "dishware", "🏺"),
        EmojiItem("FORK AND KNIFE WITH PLATE", "food-drink", "dishware", "🍽"),
        EmojiItem("FORK AND KNIFE", "food-drink", "dishware", "🍴"),
        EmojiItem("HOT BEVERAGE", "food-drink", "drink", "☕"),
        EmojiItem("TEAPOT", "food-drink", "drink", "🫖"),
        EmojiItem("BUBBLE TEA", "food-drink", "drink", "🧋"),
        EmojiItem("ICE CUBE", "food-drink", "drink", "🧊"),
        EmojiItem("MATE DRINK", "food-drink", "drink", "🧉"),
        EmojiItem("BEVERAGE BOX", "food-drink", "drink", "🧃"),
        EmojiItem("CUP WITH STRAW", "food-drink", "drink", "🥤"),
        EmojiItem("GLASS OF MILK", "food-drink", "drink", "🥛"),
        EmojiItem("TUMBLER GLASS", "food-drink", "drink", "🥃"),
        EmojiItem("CLINKING GLASSES", "food-drink", "drink", "🥂"),
        EmojiItem("BOTTLE WITH POPPING CORK", "food-drink", "drink", "🍾"),
        EmojiItem("BABY BOTTLE", "food-drink", "drink", "🍼"),
        EmojiItem("CLINKING BEER MUGS", "food-drink", "drink", "🍻"),
        EmojiItem("BEER MUG", "food-drink", "drink", "🍺"),
        EmojiItem("TROPICAL DRINK", "food-drink", "drink", "🍹"),
        EmojiItem("COCKTAIL GLASS", "food-drink", "drink", "🍸"),
        EmojiItem("WINE GLASS", "food-drink", "drink", "🍷"),
        EmojiItem("SAKE BOTTLE AND CUP", "food-drink", "drink", "🍶"),
        EmojiItem("TEACUP WITHOUT HANDLE", "food-drink", "drink", "🍵"),
        EmojiItem("MOON CAKE", "food-drink", "food-asian", "🥮"),
        EmojiItem("TAKEOUT BOX", "food-drink", "food-asian", "🥡"),
        EmojiItem("FORTUNE COOKIE", "food-drink", "food-asian", "🥠"),
        EmojiItem("DUMPLING", "food-drink", "food-asian", "🥟"),
        EmojiItem("BENTO BOX", "food-drink", "food-asian", "🍱"),
        EmojiItem(
            "FISH CAKE WITH SWIRL DESIGN", "food-drink", "food-asian", "🍥"
        ),
        EmojiItem("FRIED SHRIMP", "food-drink", "food-asian", "🍤"),
        EmojiItem("SUSHI", "food-drink", "food-asian", "🍣"),
        EmojiItem("ODEN", "food-drink", "food-asian", "🍢"),
        EmojiItem("DANGO", "food-drink", "food-asian", "🍡"),
        EmojiItem("ROASTED SWEET POTATO", "food-drink", "food-asian", "🍠"),
        EmojiItem("SPAGHETTI", "food-drink", "food-asian", "🍝"),
        EmojiItem("STEAMING BOWL", "food-drink", "food-asian", "🍜"),
        EmojiItem("CURRY AND RICE", "food-drink", "food-asian", "🍛"),
        EmojiItem("COOKED RICE", "food-drink", "food-asian", "🍚"),
        EmojiItem("RICE BALL", "food-drink", "food-asian", "🍙"),
        EmojiItem("RICE CRACKER", "food-drink", "food-asian", "🍘"),
        EmojiItem("OLIVE", "food-drink", "food-fruit", "🫒"),
        EmojiItem("BLUEBERRIES", "food-drink", "food-fruit", "🫐"),
        EmojiItem("MANGO", "food-drink", "food-fruit", "🥭"),
        EmojiItem("COCONUT", "food-drink", "food-fruit", "🥥"),
        EmojiItem("KIWIFRUIT", "food-drink", "food-fruit", "🥝"),
        EmojiItem("STRAWBERRY", "food-drink", "food-fruit", "🍓"),
        EmojiItem("CHERRIES", "food-drink", "food-fruit", "🍒"),
        EmojiItem("PEACH", "food-drink", "food-fruit", "🍑"),
        EmojiItem("PEAR", "food-drink", "food-fruit", "🍐"),
        EmojiItem("GREEN APPLE", "food-drink", "food-fruit", "🍏"),
        EmojiItem("RED APPLE", "food-drink", "food-fruit", "🍎"),
        EmojiItem("PINEAPPLE", "food-drink", "food-fruit", "🍍"),
        EmojiItem("BANANA", "food-drink", "food-fruit", "🍌"),
        EmojiItem("LEMON", "food-drink", "food-fruit", "🍋"),
        EmojiItem("TANGERINE", "food-drink", "food-fruit", "🍊"),
        EmojiItem("WATERMELON", "food-drink", "food-fruit", "🍉"),
        EmojiItem("MELON", "food-drink", "food-fruit", "🍈"),
        EmojiItem("GRAPES", "food-drink", "food-fruit", "🍇"),
        EmojiItem("TOMATO", "food-drink", "food-fruit", "🍅"),
        EmojiItem("OYSTER", "food-drink", "food-marine", "🦪"),
        EmojiItem("LOBSTER", "food-drink", "food-marine", "🦞"),
        EmojiItem("SQUID", "food-drink", "food-marine", "🦑"),
        EmojiItem("SHRIMP", "food-drink", "food-marine", "🦐"),
        EmojiItem("CRAB", "food-drink", "food-marine", "🦀"),
        EmojiItem("FONDUE", "food-drink", "food-prepared", "🫕"),
        EmojiItem("TAMALE", "food-drink", "food-prepared", "🫔"),
        EmojiItem("FLATBREAD", "food-drink", "food-prepared", "🫓"),
        EmojiItem("BUTTER", "food-drink", "food-prepared", "🧈"),
        EmojiItem("WAFFLE", "food-drink", "food-prepared", "🧇"),
        EmojiItem("FALAFEL", "food-drink", "food-prepared", "🧆"),
        EmojiItem("SALT SHAKER", "food-drink", "food-prepared", "🧂"),
        EmojiItem("CHEESE WEDGE", "food-drink", "food-prepared", "🧀"),
        EmojiItem("BAGEL", "food-drink", "food-prepared", "🥯"),
        EmojiItem("CANNED FOOD", "food-drink", "food-prepared", "🥫"),
        EmojiItem("SANDWICH", "food-drink", "food-prepared", "🥪"),
        EmojiItem("CUT OF MEAT", "food-drink", "food-prepared", "🥩"),
        EmojiItem("PRETZEL", "food-drink", "food-prepared", "🥨"),
        EmojiItem("BOWL WITH SPOON", "food-drink", "food-prepared", "🥣"),
        EmojiItem("PANCAKES", "food-drink", "food-prepared", "🥞"),
        EmojiItem("EGG", "food-drink", "food-prepared", "🥚"),
        EmojiItem("STUFFED FLATBREAD", "food-drink", "food-prepared", "🥙"),
        EmojiItem("SHALLOW PAN OF FOOD", "food-drink", "food-prepared", "🥘"),
        EmojiItem("GREEN SALAD", "food-drink", "food-prepared", "🥗"),
        EmojiItem("BAGUETTE BREAD", "food-drink", "food-prepared", "🥖"),
        EmojiItem("BACON", "food-drink", "food-prepared", "🥓"),
        EmojiItem("CROISSANT", "food-drink", "food-prepared", "🥐"),
        EmojiItem("POPCORN", "food-drink", "food-prepared", "🍿"),
        EmojiItem("COOKING", "food-drink", "food-prepared", "🍳"),
        EmojiItem("POT OF FOOD", "food-drink", "food-prepared", "🍲"),
        EmojiItem("FRENCH FRIES", "food-drink", "food-prepared", "🍟"),
        EmojiItem("BREAD", "food-drink", "food-prepared", "🍞"),
        EmojiItem("POULTRY LEG", "food-drink", "food-prepared", "🍗"),
        EmojiItem("MEAT ON BONE", "food-drink", "food-prepared", "🍖"),
        EmojiItem("SLICE OF PIZZA", "food-drink", "food-prepared", "🍕"),
        EmojiItem("HAMBURGER", "food-drink", "food-prepared", "🍔"),
        EmojiItem("BURRITO", "food-drink", "food-prepared", "🌯"),
        EmojiItem("TACO", "food-drink", "food-prepared", "🌮"),
        EmojiItem("HOT DOG", "food-drink", "food-prepared", "🌭"),
        EmojiItem("CUPCAKE", "food-drink", "food-sweet", "🧁"),
        EmojiItem("PIE", "food-drink", "food-sweet", "🥧"),
        EmojiItem("BIRTHDAY CAKE", "food-drink", "food-sweet", "🎂"),
        EmojiItem("SHORTCAKE", "food-drink", "food-sweet", "🍰"),
        EmojiItem("HONEY POT", "food-drink", "food-sweet", "🍯"),
        EmojiItem("CUSTARD", "food-drink", "food-sweet", "🍮"),
        EmojiItem("LOLLIPOP", "food-drink", "food-sweet", "🍭"),
        EmojiItem("CANDY", "food-drink", "food-sweet", "🍬"),
        EmojiItem("CHOCOLATE BAR", "food-drink", "food-sweet", "🍫"),
        EmojiItem("COOKIE", "food-drink", "food-sweet", "🍪"),
        EmojiItem("DOUGHNUT", "food-drink", "food-sweet", "🍩"),
        EmojiItem("ICE CREAM", "food-drink", "food-sweet", "🍨"),
        EmojiItem("SHAVED ICE", "food-drink", "food-sweet", "🍧"),
        EmojiItem("SOFT ICE CREAM", "food-drink", "food-sweet", "🍦"),
        EmojiItem("BELL PEPPER", "food-drink", "food-vegetable", "🫑"),
        EmojiItem("ONION", "food-drink", "food-vegetable", "🧅"),
        EmojiItem("GARLIC", "food-drink", "food-vegetable", "🧄"),
        EmojiItem("LEAFY GREEN", "food-drink", "food-vegetable", "🥬"),
        EmojiItem("BROCCOLI", "food-drink", "food-vegetable", "🥦"),
        EmojiItem("PEANUTS", "food-drink", "food-vegetable", "🥜"),
        EmojiItem("CARROT", "food-drink", "food-vegetable", "🥕"),
        EmojiItem("POTATO", "food-drink", "food-vegetable", "🥔"),
        EmojiItem("CUCUMBER", "food-drink", "food-vegetable", "🥒"),
        EmojiItem("AVOCADO", "food-drink", "food-vegetable", "🥑"),
        EmojiItem("AUBERGINE", "food-drink", "food-vegetable", "🍆"),
        EmojiItem("MUSHROOM", "food-drink", "food-vegetable", "🍄"),
        EmojiItem("EAR OF MAIZE", "food-drink", "food-vegetable", "🌽"),
        EmojiItem("HOT PEPPER", "food-drink", "food-vegetable", "🌶"),
        EmojiItem("CHESTNUT", "food-drink", "food-vegetable", "🌰"),
        EmojiItem("ROLLED-UP NEWSPAPER", "objects", "book-paper", "🗞"),
        EmojiItem("BOOKMARK", "objects", "book-paper", "🔖"),
        EmojiItem("NEWSPAPER", "objects", "book-paper", "📰"),
        EmojiItem("SCROLL", "objects", "book-paper", "📜"),
        EmojiItem("BOOKS", "objects", "book-paper", "📚"),
        EmojiItem("ORANGE BOOK", "objects", "book-paper", "📙"),
        EmojiItem("BLUE BOOK", "objects", "book-paper", "📘"),
        EmojiItem("GREEN BOOK", "objects", "book-paper", "📗"),
        EmojiItem("OPEN BOOK", "objects", "book-paper", "📖"),
        EmojiItem("CLOSED BOOK", "objects", "book-paper", "📕"),
        EmojiItem(
            "NOTEBOOK WITH DECORATIVE COVER", "objects", "book-paper", "📔"
        ),
        EmojiItem("NOTEBOOK", "objects", "book-paper", "📓"),
        EmojiItem("LEDGER", "objects", "book-paper", "📒"),
        EmojiItem("BOOKMARK TABS", "objects", "book-paper", "📑"),
        EmojiItem("PAGE FACING UP", "objects", "book-paper", "📄"),
        EmojiItem("PAGE WITH CURL", "objects", "book-paper", "📃"),
        EmojiItem("LABEL", "objects", "book-paper", "🏷"),
        EmojiItem("HELMET WITH WHITE CROSS", "objects", "clothing", "⛑"),
        EmojiItem("MILITARY HELMET", "objects", "clothing", "🪖"),
        EmojiItem("THONG SANDAL", "objects", "clothing", "🩴"),
        EmojiItem("SHORTS", "objects", "clothing", "🩳"),
        EmojiItem("BRIEFS", "objects", "clothing", "🩲"),
        EmojiItem("ONE-PIECE SWIMSUIT", "objects", "clothing", "🩱"),
        EmojiItem("BALLET SHOES", "objects", "clothing", "🩰"),
        EmojiItem("SOCKS", "objects", "clothing", "🧦"),
        EmojiItem("COAT", "objects", "clothing", "🧥"),
        EmojiItem("GLOVES", "objects", "clothing", "🧤"),
        EmojiItem("SCARF", "objects", "clothing", "🧣"),
        EmojiItem("BILLED CAP", "objects", "clothing", "🧢"),
        EmojiItem("SAFETY VEST", "objects", "clothing", "🦺"),
        EmojiItem("FLAT SHOE", "objects", "clothing", "🥿"),
        EmojiItem("HIKING BOOT", "objects", "clothing", "🥾"),
        EmojiItem("GOGGLES", "objects", "clothing", "🥽"),
        EmojiItem("LAB COAT", "objects", "clothing", "🥼"),
        EmojiItem("SARI", "objects", "clothing", "🥻"),
        EmojiItem("SHOPPING BAGS", "objects", "clothing", "🛍"),
        EmojiItem("DARK SUNGLASSES", "objects", "clothing", "🕶"),
        EmojiItem("PRAYER BEADS", "objects", "clothing", "📿"),
        EmojiItem("GEM STONE", "objects", "clothing", "💎"),
        EmojiItem("RING", "objects", "clothing", "💍"),
        EmojiItem("LIPSTICK", "objects", "clothing", "💄"),
        EmojiItem("WOMANS BOOTS", "objects", "clothing", "👢"),
        EmojiItem("WOMANS SANDAL", "objects", "clothing", "👡"),
        EmojiItem("HIGH-HEELED SHOE", "objects", "clothing", "👠"),
        EmojiItem("ATHLETIC SHOE", "objects", "clothing", "👟"),
        EmojiItem("MANS SHOE", "objects", "clothing", "👞"),
        EmojiItem("POUCH", "objects", "clothing", "👝"),
        EmojiItem("HANDBAG", "objects", "clothing", "👜"),
        EmojiItem("PURSE", "objects", "clothing", "👛"),
        EmojiItem("WOMANS CLOTHES", "objects", "clothing", "👚"),
        EmojiItem("BIKINI", "objects", "clothing", "👙"),
        EmojiItem("KIMONO", "objects", "clothing", "👘"),
        EmojiItem("DRESS", "objects", "clothing", "👗"),
        EmojiItem("JEANS", "objects", "clothing", "👖"),
        EmojiItem("T-SHIRT", "objects", "clothing", "👕"),
        EmojiItem("NECKTIE", "objects", "clothing", "👔"),
        EmojiItem("EYEGLASSES", "objects", "clothing", "👓"),
        EmojiItem("WOMANS HAT", "objects", "clothing", "👒"),
        EmojiItem("CROWN", "objects", "clothing", "👑"),
        EmojiItem("TOP HAT", "objects", "clothing", "🎩"),
        EmojiItem("GRADUATION CAP", "objects", "clothing", "🎓"),
        EmojiItem("SCHOOL SATCHEL", "objects", "clothing", "🎒"),
        EmojiItem("KEYBOARD", "objects", "computer", "⌨"),
        EmojiItem("ABACUS", "objects", "computer", "🧮"),
        EmojiItem("TRACKBALL", "objects", "computer", "🖲"),
        EmojiItem("THREE BUTTON MOUSE", "objects", "computer", "🖱"),
        EmojiItem("PRINTER", "objects", "computer", "🖨"),
        EmojiItem("DESKTOP COMPUTER", "objects", "computer", "🖥"),
        EmojiItem("ELECTRIC PLUG", "objects", "computer", "🔌"),
        EmojiItem("BATTERY", "objects", "computer", "🔋"),
        EmojiItem("DVD", "objects", "computer", "📀"),
        EmojiItem("OPTICAL DISC", "objects", "computer", "💿"),
        EmojiItem("FLOPPY DISK", "objects", "computer", "💾"),
        EmojiItem("MINIDISC", "objects", "computer", "💽"),
        EmojiItem("PERSONAL COMPUTER", "objects", "computer", "💻"),
        EmojiItem("TOOTHBRUSH", "objects", "household", "🪥"),
        EmojiItem("MOUSE TRAP", "objects", "household", "🪤"),
        EmojiItem("BUCKET", "objects", "household", "🪣"),
        EmojiItem("PLUNGER", "objects", "household", "🪠"),
        EmojiItem("WINDOW", "objects", "household", "🪟"),
        EmojiItem("MIRROR", "objects", "household", "🪞"),
        EmojiItem("RAZOR", "objects", "household", "🪒"),
        EmojiItem("CHAIR", "objects", "household", "🪑"),
        EmojiItem("SPONGE", "objects", "household", "🧽"),
        EmojiItem("BAR OF SOAP", "objects", "household", "🧼"),
        EmojiItem("ROLL OF PAPER", "objects", "household", "🧻"),
        EmojiItem("BASKET", "objects", "household", "🧺"),
        EmojiItem("BROOM", "objects", "household", "🧹"),
        EmojiItem("SAFETY PIN", "objects", "household", "🧷"),
        EmojiItem("LOTION BOTTLE", "objects", "household", "🧴"),
        EmojiItem("FIRE EXTINGUISHER", "objects", "household", "🧯"),
        EmojiItem("ELEVATOR", "objects", "household", "🛗"),
        EmojiItem("SHOPPING TROLLEY", "objects", "household", "🛒"),
        EmojiItem("BED", "objects", "household", "🛏"),
        EmojiItem("COUCH AND LAMP", "objects", "household", "🛋"),
        EmojiItem("BATHTUB", "objects", "household", "🛁"),
        EmojiItem("SHOWER", "objects", "household", "🚿"),
        EmojiItem("TOILET", "objects", "household", "🚽"),
        EmojiItem("DOOR", "objects", "household", "🚪"),
        EmojiItem("DIYA LAMP", "objects", "light & video", "🪔"),
        EmojiItem("CANDLE", "objects", "light & video", "🕯"),
        EmojiItem("ELECTRIC TORCH", "objects", "light & video", "🔦"),
        EmojiItem(
            "RIGHT-POINTING MAGNIFYING GLASS", "objects", "light & video", "🔎"
        ),
        EmojiItem(
            "LEFT-POINTING MAGNIFYING GLASS", "objects", "light & video", "🔍"
        ),
        EmojiItem("FILM PROJECTOR", "objects", "light & video", "📽"),
        EmojiItem("VIDEOCASSETTE", "objects", "light & video", "📼"),
        EmojiItem("TELEVISION", "objects", "light & video", "📺"),
        EmojiItem("VIDEO CAMERA", "objects", "light & video", "📹"),
        EmojiItem("CAMERA WITH FLASH", "objects", "light & video", "📸"),
        EmojiItem("CAMERA", "objects", "light & video", "📷"),
        EmojiItem("ELECTRIC LIGHT BULB", "objects", "light & video", "💡"),
        EmojiItem("IZAKAYA LANTERN", "objects", "light & video", "🏮"),
        EmojiItem("CLAPPER BOARD", "objects", "light & video", "🎬"),
        EmojiItem("MOVIE CAMERA", "objects", "light & video", "🎥"),
        EmojiItem("FILM FRAMES", "objects", "light & video", "🎞"),
        EmojiItem("OLD KEY", "objects", "lock", "🗝"),
        EmojiItem("OPEN LOCK", "objects", "lock", "🔓"),
        EmojiItem("LOCK", "objects", "lock", "🔒"),
        EmojiItem("KEY", "objects", "lock", "🔑"),
        EmojiItem("CLOSED LOCK WITH KEY", "objects", "lock", "🔐"),
        EmojiItem("LOCK WITH INK PEN", "objects", "lock", "🔏"),
        EmojiItem("ENVELOPE", "objects", "mail", "✉"),
        EmojiItem("BALLOT BOX WITH BALLOT", "objects", "mail", "🗳"),
        EmojiItem("POSTBOX", "objects", "mail", "📮"),
        EmojiItem("OPEN MAILBOX WITH LOWERED FLAG", "objects", "mail", "📭"),
        EmojiItem("OPEN MAILBOX WITH RAISED FLAG", "objects", "mail", "📬"),
        EmojiItem("CLOSED MAILBOX WITH RAISED FLAG", "objects", "mail", "📫"),
        EmojiItem("CLOSED MAILBOX WITH LOWERED FLAG", "objects", "mail", "📪"),
        EmojiItem(
            "ENVELOPE WITH DOWNWARDS ARROW ABOVE", "objects", "mail", "📩"
        ),
        EmojiItem("INCOMING ENVELOPE", "objects", "mail", "📨"),
        EmojiItem("E-MAIL SYMBOL", "objects", "mail", "📧"),
        EmojiItem("PACKAGE", "objects", "mail", "📦"),
        EmojiItem("INBOX TRAY", "objects", "mail", "📥"),
        EmojiItem("OUTBOX TRAY", "objects", "mail", "📤"),
        EmojiItem("STETHOSCOPE", "objects", "medical", "🩺"),
        EmojiItem("ADHESIVE BANDAGE", "objects", "medical", "🩹"),
        EmojiItem("DROP OF BLOOD", "objects", "medical", "🩸"),
        EmojiItem("PILL", "objects", "medical", "💊"),
        EmojiItem("SYRINGE", "objects", "medical", "💉"),
        EmojiItem("COIN", "objects", "money", "🪙"),
        EmojiItem("RECEIPT", "objects", "money", "🧾"),
        EmojiItem(
            "CHART WITH UPWARDS TREND AND YEN SIGN", "objects", "money", "💹"
        ),
        EmojiItem("MONEY WITH WINGS", "objects", "money", "💸"),
        EmojiItem("BANKNOTE WITH POUND SIGN", "objects", "money", "💷"),
        EmojiItem("BANKNOTE WITH EURO SIGN", "objects", "money", "💶"),
        EmojiItem("BANKNOTE WITH DOLLAR SIGN", "objects", "money", "💵"),
        EmojiItem("BANKNOTE WITH YEN SIGN", "objects", "money", "💴"),
        EmojiItem("CREDIT CARD", "objects", "money", "💳"),
        EmojiItem("MONEY BAG", "objects", "money", "💰"),
        EmojiItem("RADIO", "objects", "music", "📻"),
        EmojiItem("MUSICAL SCORE", "objects", "music", "🎼"),
        EmojiItem("MULTIPLE MUSICAL NOTES", "objects", "music", "🎶"),
        EmojiItem("MUSICAL NOTE", "objects", "music", "🎵"),
        EmojiItem("HEADPHONE", "objects", "music", "🎧"),
        EmojiItem("MICROPHONE", "objects", "music", "🎤"),
        EmojiItem("CONTROL KNOBS", "objects", "music", "🎛"),
        EmojiItem("LEVEL SLIDER", "objects", "music", "🎚"),
        EmojiItem("STUDIO MICROPHONE", "objects", "music", "🎙"),
        EmojiItem("LONG DRUM", "objects", "musical-instrument", "🪘"),
        EmojiItem("ACCORDION", "objects", "musical-instrument", "🪗"),
        EmojiItem("BANJO", "objects", "musical-instrument", "🪕"),
        EmojiItem(
            "DRUM WITH DRUMSTICKS", "objects", "musical-instrument", "🥁"
        ),
        EmojiItem("VIOLIN", "objects", "musical-instrument", "🎻"),
        EmojiItem("TRUMPET", "objects", "musical-instrument", "🎺"),
        EmojiItem("MUSICAL KEYBOARD", "objects", "musical-instrument", "🎹"),
        EmojiItem("GUITAR", "objects", "musical-instrument", "🎸"),
        EmojiItem("SAXOPHONE", "objects", "musical-instrument", "🎷"),
        EmojiItem("BLACK SCISSORS", "objects", "office", "✂"),
        EmojiItem("SPIRAL CALENDAR PAD", "objects", "office", "🗓"),
        EmojiItem("SPIRAL NOTE PAD", "objects", "office", "🗒"),
        EmojiItem("WASTEBASKET", "objects", "office", "🗑"),
        EmojiItem("FILE CABINET", "objects", "office", "🗄"),
        EmojiItem("CARD FILE BOX", "objects", "office", "🗃"),
        EmojiItem("CARD INDEX DIVIDERS", "objects", "office", "🗂"),
        EmojiItem("LINKED PAPERCLIPS", "objects", "office", "🖇"),
        EmojiItem("TRIANGULAR RULER", "objects", "office", "📐"),
        EmojiItem("STRAIGHT RULER", "objects", "office", "📏"),
        EmojiItem("PAPERCLIP", "objects", "office", "📎"),
        EmojiItem("ROUND PUSHPIN", "objects", "office", "📍"),
        EmojiItem("PUSHPIN", "objects", "office", "📌"),
        EmojiItem("CLIPBOARD", "objects", "office", "📋"),
        EmojiItem("BAR CHART", "objects", "office", "📊"),
        EmojiItem("CHART WITH DOWNWARDS TREND", "objects", "office", "📉"),
        EmojiItem("CHART WITH UPWARDS TREND", "objects", "office", "📈"),
        EmojiItem("CARD INDEX", "objects", "office", "📇"),
        EmojiItem("TEAR-OFF CALENDAR", "objects", "office", "📆"),
        EmojiItem("CALENDAR", "objects", "office", "📅"),
        EmojiItem("OPEN FILE FOLDER", "objects", "office", "📂"),
        EmojiItem("FILE FOLDER", "objects", "office", "📁"),
        EmojiItem("BRIEFCASE", "objects", "office", "💼"),
        EmojiItem("FUNERAL URN", "objects", "other-object", "⚱"),
        EmojiItem("COFFIN", "objects", "other-object", "⚰"),
        EmojiItem("PLACARD", "objects", "other-object", "🪧"),
        EmojiItem("HEADSTONE", "objects", "other-object", "🪦"),
        EmojiItem("SMOKING SYMBOL", "objects", "other-object", "🚬"),
        EmojiItem("MOYAI", "objects", "other-object", "🗿"),
        EmojiItem("BLACK TELEPHONE", "objects", "phone", "☎"),
        EmojiItem(
            "MOBILE PHONE WITH RIGHTWARDS ARROW AT LEFT",
            "objects",
            "phone",
            "📲",
        ),
        EmojiItem("MOBILE PHONE", "objects", "phone", "📱"),
        EmojiItem("FAX MACHINE", "objects", "phone", "📠"),
        EmojiItem("PAGER", "objects", "phone", "📟"),
        EmojiItem("TELEPHONE RECEIVER", "objects", "phone", "📞"),
        EmojiItem("ALEMBIC", "objects", "science", "⚗"),
        EmojiItem("DNA DOUBLE HELIX", "objects", "science", "🧬"),
        EmojiItem("PETRI DISH", "objects", "science", "🧫"),
        EmojiItem("TEST TUBE", "objects", "science", "🧪"),
        EmojiItem("TELESCOPE", "objects", "science", "🔭"),
        EmojiItem("MICROSCOPE", "objects", "science", "🔬"),
        EmojiItem("SATELLITE ANTENNA", "objects", "science", "📡"),
        EmojiItem("BELL WITH CANCELLATION STROKE", "objects", "sound", "🔕"),
        EmojiItem("BELL", "objects", "sound", "🔔"),
        EmojiItem("SPEAKER WITH THREE SOUND WAVES", "objects", "sound", "🔊"),
        EmojiItem("SPEAKER WITH ONE SOUND WAVE", "objects", "sound", "🔉"),
        EmojiItem("SPEAKER", "objects", "sound", "🔈"),
        EmojiItem("SPEAKER WITH CANCELLATION STROKE", "objects", "sound", "🔇"),
        EmojiItem("POSTAL HORN", "objects", "sound", "📯"),
        EmojiItem("CHEERING MEGAPHONE", "objects", "sound", "📣"),
        EmojiItem("PUBLIC ADDRESS LOUDSPEAKER", "objects", "sound", "📢"),
        EmojiItem("CHAINS", "objects", "tool", "⛓"),
        EmojiItem("PICK", "objects", "tool", "⛏"),
        EmojiItem("GEAR", "objects", "tool", "⚙"),
        EmojiItem("SCALES", "objects", "tool", "⚖"),
        EmojiItem("CROSSED SWORDS", "objects", "tool", "⚔"),
        EmojiItem("HAMMER AND PICK", "objects", "tool", "⚒"),
        EmojiItem("HOOK", "objects", "tool", "🪝"),
        EmojiItem("LADDER", "objects", "tool", "🪜"),
        EmojiItem("SCREWDRIVER", "objects", "tool", "🪛"),
        EmojiItem("CARPENTRY SAW", "objects", "tool", "🪚"),
        EmojiItem("AXE", "objects", "tool", "🪓"),
        EmojiItem("BOOMERANG", "objects", "tool", "🪃"),
        EmojiItem("MAGNET", "objects", "tool", "🧲"),
        EmojiItem("TOOLBOX", "objects", "tool", "🧰"),
        EmojiItem("PROBING CANE", "objects", "tool", "🦯"),
        EmojiItem("SHIELD", "objects", "tool", "🛡"),
        EmojiItem("HAMMER AND WRENCH", "objects", "tool", "🛠"),
        EmojiItem("DAGGER KNIFE", "objects", "tool", "🗡"),
        EmojiItem("COMPRESSION", "objects", "tool", "🗜"),
        EmojiItem("PISTOL", "objects", "tool", "🔫"),
        EmojiItem("NUT AND BOLT", "objects", "tool", "🔩"),
        EmojiItem("HAMMER", "objects", "tool", "🔨"),
        EmojiItem("WRENCH", "objects", "tool", "🔧"),
        EmojiItem("LINK SYMBOL", "objects", "tool", "🔗"),
        EmojiItem("BOW AND ARROW", "objects", "tool", "🏹"),
        EmojiItem("PENCIL", "objects", "writing", "✏"),
        EmojiItem("BLACK NIB", "objects", "writing", "✒"),
        EmojiItem("LOWER LEFT CRAYON", "objects", "writing", "🖍"),
        EmojiItem("LOWER LEFT PAINTBRUSH", "objects", "writing", "🖌"),
        EmojiItem("LOWER LEFT FOUNTAIN PEN", "objects", "writing", "🖋"),
        EmojiItem("LOWER LEFT BALLPOINT PEN", "objects", "writing", "🖊"),
        EmojiItem("MEMO", "objects", "writing", "📝"),
        EmojiItem("LUNGS", "people-body", "body-parts", "🫁"),
        EmojiItem("ANATOMICAL HEART", "people-body", "body-parts", "🫀"),
        EmojiItem("BRAIN", "people-body", "body-parts", "🧠"),
        EmojiItem("MECHANICAL LEG", "people-body", "body-parts", "🦿"),
        EmojiItem("MECHANICAL ARM", "people-body", "body-parts", "🦾"),
        EmojiItem("EAR WITH HEARING AID", "people-body", "body-parts", "🦻"),
        EmojiItem("TOOTH", "people-body", "body-parts", "🦷"),
        EmojiItem("FOOT", "people-body", "body-parts", "🦶"),
        EmojiItem("LEG", "people-body", "body-parts", "🦵"),
        EmojiItem("BONE", "people-body", "body-parts", "🦴"),
        EmojiItem("FLEXED BICEPS", "people-body", "body-parts", "💪"),
        EmojiItem("TONGUE", "people-body", "body-parts", "👅"),
        EmojiItem("MOUTH", "people-body", "body-parts", "👄"),
        EmojiItem("NOSE", "people-body", "body-parts", "👃"),
        EmojiItem("EAR", "people-body", "body-parts", "👂"),
        EmojiItem("EYE", "people-body", "body-parts", "👁"),
        EmojiItem("EYES", "people-body", "body-parts", "👀"),
        EmojiItem("COUPLE WITH HEART", "people-body", "family", "💑"),
        EmojiItem("KISS", "people-body", "family", "💏"),
        EmojiItem("TWO WOMEN HOLDING HANDS", "people-body", "family", "👭"),
        EmojiItem("TWO MEN HOLDING HANDS", "people-body", "family", "👬"),
        EmojiItem("MAN AND WOMAN HOLDING HANDS", "people-body", "family", "👫"),
        EmojiItem("FAMILY", "people-body", "family", "👪"),
        EmojiItem("RAISED FIST", "people-body", "hand-fingers-closed", "✊"),
        EmojiItem(
            "RIGHT-FACING FIST", "people-body", "hand-fingers-closed", "🤜"
        ),
        EmojiItem(
            "LEFT-FACING FIST", "people-body", "hand-fingers-closed", "🤛"
        ),
        EmojiItem(
            "THUMBS DOWN SIGN", "people-body", "hand-fingers-closed", "👎"
        ),
        EmojiItem("THUMBS UP SIGN", "people-body", "hand-fingers-closed", "👍"),
        EmojiItem(
            "FISTED HAND SIGN", "people-body", "hand-fingers-closed", "👊"
        ),
        EmojiItem("RAISED HAND", "people-body", "hand-fingers-open", "✋"),
        EmojiItem(
            "RAISED BACK OF HAND", "people-body", "hand-fingers-open", "🤚"
        ),
        EmojiItem(
            "RAISED HAND WITH PART BETWEEN MIDDLE AND RING FINGERS",
            "people-body",
            "hand-fingers-open",
            "🖖",
        ),
        EmojiItem(
            "RAISED HAND WITH FINGERS SPLAYED",
            "people-body",
            "hand-fingers-open",
            "🖐",
        ),
        EmojiItem("WAVING HAND SIGN", "people-body", "hand-fingers-open", "👋"),
        EmojiItem("VICTORY HAND", "people-body", "hand-fingers-partial", "✌"),
        EmojiItem(
            "I LOVE YOU HAND SIGN", "people-body", "hand-fingers-partial", "🤟"
        ),
        EmojiItem(
            "HAND WITH INDEX AND MIDDLE FINGERS CROSSED",
            "people-body",
            "hand-fingers-partial",
            "🤞",
        ),
        EmojiItem("CALL ME HAND", "people-body", "hand-fingers-partial", "🤙"),
        EmojiItem(
            "SIGN OF THE HORNS", "people-body", "hand-fingers-partial", "🤘"
        ),
        EmojiItem("PINCHING HAND", "people-body", "hand-fingers-partial", "🤏"),
        EmojiItem(
            "PINCHED FINGERS", "people-body", "hand-fingers-partial", "🤌"
        ),
        EmojiItem("OK HAND SIGN", "people-body", "hand-fingers-partial", "👌"),
        EmojiItem("WRITING HAND", "people-body", "hand-prop", "✍"),
        EmojiItem("SELFIE", "people-body", "hand-prop", "🤳"),
        EmojiItem("NAIL POLISH", "people-body", "hand-prop", "💅"),
        EmojiItem("PALMS UP TOGETHER", "people-body", "hands", "🤲"),
        EmojiItem("HANDSHAKE", "people-body", "hands", "🤝"),
        EmojiItem("PERSON WITH FOLDED HANDS", "people-body", "hands", "🙏"),
        EmojiItem(
            "PERSON RAISING BOTH HANDS IN CELEBRATION",
            "people-body",
            "hands",
            "🙌",
        ),
        EmojiItem("OPEN HANDS SIGN", "people-body", "hands", "👐"),
        EmojiItem("CLAPPING HANDS SIGN", "people-body", "hands", "👏"),
        EmojiItem(
            "WHITE UP POINTING INDEX", "people-body", "hand-single-finger", "☝"
        ),
        EmojiItem(
            "REVERSED HAND WITH MIDDLE FINGER EXTENDED",
            "people-body",
            "hand-single-finger",
            "🖕",
        ),
        EmojiItem(
            "WHITE RIGHT POINTING BACKHAND INDEX",
            "people-body",
            "hand-single-finger",
            "👉",
        ),
        EmojiItem(
            "WHITE LEFT POINTING BACKHAND INDEX",
            "people-body",
            "hand-single-finger",
            "👈",
        ),
        EmojiItem(
            "WHITE DOWN POINTING BACKHAND INDEX",
            "people-body",
            "hand-single-finger",
            "👇",
        ),
        EmojiItem(
            "WHITE UP POINTING BACKHAND INDEX",
            "people-body",
            "hand-single-finger",
            "👆",
        ),
        EmojiItem("BEARDED PERSON", "people-body", "person", "🧔"),
        EmojiItem("OLDER ADULT", "people-body", "person", "🧓"),
        EmojiItem("CHILD", "people-body", "person", "🧒"),
        EmojiItem("ADULT", "people-body", "person", "🧑"),
        EmojiItem("BABY", "people-body", "person", "👶"),
        EmojiItem("OLDER WOMAN", "people-body", "person", "👵"),
        EmojiItem("OLDER MAN", "people-body", "person", "👴"),
        EmojiItem("PERSON WITH BLOND HAIR", "people-body", "person", "👱"),
        EmojiItem("WOMAN", "people-body", "person", "👩"),
        EmojiItem("MAN", "people-body", "person", "👨"),
        EmojiItem("GIRL", "people-body", "person", "👧"),
        EmojiItem("BOY", "people-body", "person", "👦"),
        EmojiItem("PERSON CLIMBING", "people-body", "person-activity", "🧗"),
        EmojiItem(
            "PERSON IN STEAMY ROOM", "people-body", "person-activity", "🧖"
        ),
        EmojiItem("KNEELING PERSON", "people-body", "person-activity", "🧎"),
        EmojiItem("STANDING PERSON", "people-body", "person-activity", "🧍"),
        EmojiItem("PEDESTRIAN", "people-body", "person-activity", "🚶"),
        EmojiItem("MAN DANCING", "people-body", "person-activity", "🕺"),
        EmojiItem(
            "MAN IN BUSINESS SUIT LEVITATING",
            "people-body",
            "person-activity",
            "🕴",
        ),
        EmojiItem("HAIRCUT", "people-body", "person-activity", "💇"),
        EmojiItem("FACE MASSAGE", "people-body", "person-activity", "💆"),
        EmojiItem("DANCER", "people-body", "person-activity", "💃"),
        EmojiItem(
            "WOMAN WITH BUNNY EARS", "people-body", "person-activity", "👯"
        ),
        EmojiItem("RUNNER", "people-body", "person-activity", "🏃"),
        EmojiItem("ZOMBIE", "people-body", "person-fantasy", "🧟"),
        EmojiItem("GENIE", "people-body", "person-fantasy", "🧞"),
        EmojiItem("ELF", "people-body", "person-fantasy", "🧝"),
        EmojiItem("MERPERSON", "people-body", "person-fantasy", "🧜"),
        EmojiItem("VAMPIRE", "people-body", "person-fantasy", "🧛"),
        EmojiItem("FAIRY", "people-body", "person-fantasy", "🧚"),
        EmojiItem("MAGE", "people-body", "person-fantasy", "🧙"),
        EmojiItem("SUPERVILLAIN", "people-body", "person-fantasy", "🦹"),
        EmojiItem("SUPERHERO", "people-body", "person-fantasy", "🦸"),
        EmojiItem("MOTHER CHRISTMAS", "people-body", "person-fantasy", "🤶"),
        EmojiItem("BABY ANGEL", "people-body", "person-fantasy", "👼"),
        EmojiItem("FATHER CHRISTMAS", "people-body", "person-fantasy", "🎅"),
        EmojiItem("DEAF PERSON", "people-body", "person-gesture", "🧏"),
        EmojiItem("SHRUG", "people-body", "person-gesture", "🤷"),
        EmojiItem("FACE PALM", "people-body", "person-gesture", "🤦"),
        EmojiItem(
            "PERSON WITH POUTING FACE", "people-body", "person-gesture", "🙎"
        ),
        EmojiItem("PERSON FROWNING", "people-body", "person-gesture", "🙍"),
        EmojiItem(
            "HAPPY PERSON RAISING ONE HAND",
            "people-body",
            "person-gesture",
            "🙋",
        ),
        EmojiItem(
            "PERSON BOWING DEEPLY", "people-body", "person-gesture", "🙇"
        ),
        EmojiItem(
            "FACE WITH OK GESTURE", "people-body", "person-gesture", "🙆"
        ),
        EmojiItem(
            "FACE WITH NO GOOD GESTURE", "people-body", "person-gesture", "🙅"
        ),
        EmojiItem(
            "INFORMATION DESK PERSON", "people-body", "person-gesture", "💁"
        ),
        EmojiItem(
            "PERSON IN LOTUS POSITION", "people-body", "person-resting", "🧘"
        ),
        EmojiItem(
            "SLEEPING ACCOMMODATION", "people-body", "person-resting", "🛌"
        ),
        EmojiItem("BATH", "people-body", "person-resting", "🛀"),
        EmojiItem("PERSON WITH HEADSCARF", "people-body", "person-role", "🧕"),
        EmojiItem("NINJA", "people-body", "person-role", "🥷"),
        EmojiItem("MAN IN TUXEDO", "people-body", "person-role", "🤵"),
        EmojiItem("PRINCE", "people-body", "person-role", "🤴"),
        EmojiItem("BREAST-FEEDING", "people-body", "person-role", "🤱"),
        EmojiItem("PREGNANT WOMAN", "people-body", "person-role", "🤰"),
        EmojiItem("SLEUTH OR SPY", "people-body", "person-role", "🕵"),
        EmojiItem("GUARDSMAN", "people-body", "person-role", "💂"),
        EmojiItem("PRINCESS", "people-body", "person-role", "👸"),
        EmojiItem("CONSTRUCTION WORKER", "people-body", "person-role", "👷"),
        EmojiItem("MAN WITH TURBAN", "people-body", "person-role", "👳"),
        EmojiItem("MAN WITH GUA PI MAO", "people-body", "person-role", "👲"),
        EmojiItem("BRIDE WITH VEIL", "people-body", "person-role", "👰"),
        EmojiItem("POLICE OFFICER", "people-body", "person-role", "👮"),
        EmojiItem("PERSON WITH BALL", "people-body", "person-sport", "⛹"),
        EmojiItem("SKIER", "people-body", "person-sport", "⛷"),
        EmojiItem("HANDBALL", "people-body", "person-sport", "🤾"),
        EmojiItem("WATER POLO", "people-body", "person-sport", "🤽"),
        EmojiItem("WRESTLERS", "people-body", "person-sport", "🤼"),
        EmojiItem("FENCER", "people-body", "person-sport", "🤺"),
        EmojiItem("JUGGLING", "people-body", "person-sport", "🤹"),
        EmojiItem(
            "PERSON DOING CARTWHEEL", "people-body", "person-sport", "🤸"
        ),
        EmojiItem("MOUNTAIN BICYCLIST", "people-body", "person-sport", "🚵"),
        EmojiItem("BICYCLIST", "people-body", "person-sport", "🚴"),
        EmojiItem("ROWBOAT", "people-body", "person-sport", "🚣"),
        EmojiItem("GOLFER", "people-body", "person-sport", "🏌"),
        EmojiItem("WEIGHT LIFTER", "people-body", "person-sport", "🏋"),
        EmojiItem("SWIMMER", "people-body", "person-sport", "🏊"),
        EmojiItem("HORSE RACING", "people-body", "person-sport", "🏇"),
        EmojiItem("SURFER", "people-body", "person-sport", "🏄"),
        EmojiItem("SNOWBOARDER", "people-body", "person-sport", "🏂"),
        EmojiItem("PEOPLE HUGGING", "people-body", "person-symbol", "🫂"),
        EmojiItem(
            "SPEAKING HEAD IN SILHOUETTE", "people-body", "person-symbol", "🗣"
        ),
        EmojiItem("BUSTS IN SILHOUETTE", "people-body", "person-symbol", "👥"),
        EmojiItem("BUST IN SILHOUETTE", "people-body", "person-symbol", "👤"),
        EmojiItem("FOOTPRINTS", "people-body", "person-symbol", "👣"),
        EmojiItem(
            "CIRCLED LATIN CAPITAL LETTER M", "symbols", "alphanum", "Ⓜ"
        ),
        EmojiItem("CIRCLED IDEOGRAPH SECRET", "symbols", "alphanum", "㊙"),
        EmojiItem(
            "CIRCLED IDEOGRAPH CONGRATULATION", "symbols", "alphanum", "㊗"
        ),
        EmojiItem("INFORMATION SOURCE", "symbols", "alphanum", "ℹ"),
        EmojiItem(
            "INPUT SYMBOL FOR LATIN LETTERS", "symbols", "alphanum", "🔤"
        ),
        EmojiItem("INPUT SYMBOL FOR SYMBOLS", "symbols", "alphanum", "🔣"),
        EmojiItem("INPUT SYMBOL FOR NUMBERS", "symbols", "alphanum", "🔢"),
        EmojiItem(
            "INPUT SYMBOL FOR LATIN SMALL LETTERS", "symbols", "alphanum", "🔡"
        ),
        EmojiItem(
            "INPUT SYMBOL FOR LATIN CAPITAL LETTERS",
            "symbols",
            "alphanum",
            "🔠",
        ),
        EmojiItem("CIRCLED IDEOGRAPH ACCEPT", "symbols", "alphanum", "🉑"),
        EmojiItem("CIRCLED IDEOGRAPH ADVANTAGE", "symbols", "alphanum", "🉐"),
        EmojiItem(
            "SQUARED CJK UNIFIED IDEOGRAPH-55B6", "symbols", "alphanum", "🈺"
        ),
        EmojiItem(
            "SQUARED CJK UNIFIED IDEOGRAPH-5272", "symbols", "alphanum", "🈹"
        ),
        EmojiItem(
            "SQUARED CJK UNIFIED IDEOGRAPH-7533", "symbols", "alphanum", "🈸"
        ),
        EmojiItem(
            "SQUARED CJK UNIFIED IDEOGRAPH-6708", "symbols", "alphanum", "🈷"
        ),
        EmojiItem(
            "SQUARED CJK UNIFIED IDEOGRAPH-6709", "symbols", "alphanum", "🈶"
        ),
        EmojiItem(
            "SQUARED CJK UNIFIED IDEOGRAPH-6E80", "symbols", "alphanum", "🈵"
        ),
        EmojiItem(
            "SQUARED CJK UNIFIED IDEOGRAPH-5408", "symbols", "alphanum", "🈴"
        ),
        EmojiItem(
            "SQUARED CJK UNIFIED IDEOGRAPH-7A7A", "symbols", "alphanum", "🈳"
        ),
        EmojiItem(
            "SQUARED CJK UNIFIED IDEOGRAPH-7981", "symbols", "alphanum", "🈲"
        ),
        EmojiItem(
            "SQUARED CJK UNIFIED IDEOGRAPH-6307", "symbols", "alphanum", "🈯"
        ),
        EmojiItem(
            "SQUARED CJK UNIFIED IDEOGRAPH-7121", "symbols", "alphanum", "🈚"
        ),
        EmojiItem("SQUARED KATAKANA SA", "symbols", "alphanum", "🈂"),
        EmojiItem("SQUARED KATAKANA KOKO", "symbols", "alphanum", "🈁"),
        EmojiItem("SQUARED VS", "symbols", "alphanum", "🆚"),
        EmojiItem(
            "SQUARED UP WITH EXCLAMATION MARK", "symbols", "alphanum", "🆙"
        ),
        EmojiItem("SQUARED SOS", "symbols", "alphanum", "🆘"),
        EmojiItem("SQUARED OK", "symbols", "alphanum", "🆗"),
        EmojiItem("SQUARED NG", "symbols", "alphanum", "🆖"),
        EmojiItem("SQUARED NEW", "symbols", "alphanum", "🆕"),
        EmojiItem("SQUARED ID", "symbols", "alphanum", "🆔"),
        EmojiItem("SQUARED FREE", "symbols", "alphanum", "🆓"),
        EmojiItem("SQUARED COOL", "symbols", "alphanum", "🆒"),
        EmojiItem("SQUARED CL", "symbols", "alphanum", "🆑"),
        EmojiItem("NEGATIVE SQUARED AB", "symbols", "alphanum", "🆎"),
        EmojiItem(
            "NEGATIVE SQUARED LATIN CAPITAL LETTER P",
            "symbols",
            "alphanum",
            "🅿",
        ),
        EmojiItem(
            "NEGATIVE SQUARED LATIN CAPITAL LETTER O",
            "symbols",
            "alphanum",
            "🅾",
        ),
        EmojiItem(
            "NEGATIVE SQUARED LATIN CAPITAL LETTER B",
            "symbols",
            "alphanum",
            "🅱",
        ),
        EmojiItem(
            "NEGATIVE SQUARED LATIN CAPITAL LETTER A",
            "symbols",
            "alphanum",
            "🅰",
        ),
        EmojiItem("DOWNWARDS BLACK ARROW", "symbols", "arrow", "⬇"),
        EmojiItem("UPWARDS BLACK ARROW", "symbols", "arrow", "⬆"),
        EmojiItem("LEFTWARDS BLACK ARROW", "symbols", "arrow", "⬅"),
        EmojiItem("BLACK RIGHTWARDS ARROW", "symbols", "arrow", "➡"),
        EmojiItem("RIGHTWARDS ARROW WITH HOOK", "symbols", "arrow", "↪"),
        EmojiItem("LEFTWARDS ARROW WITH HOOK", "symbols", "arrow", "↩"),
        EmojiItem(
            "ARROW POINTING RIGHTWARDS THEN CURVING DOWNWARDS",
            "symbols",
            "arrow",
            "⤵",
        ),
        EmojiItem(
            "ARROW POINTING RIGHTWARDS THEN CURVING UPWARDS",
            "symbols",
            "arrow",
            "⤴",
        ),
        EmojiItem("SOUTH WEST ARROW", "symbols", "arrow", "↙"),
        EmojiItem("SOUTH EAST ARROW", "symbols", "arrow", "↘"),
        EmojiItem("NORTH EAST ARROW", "symbols", "arrow", "↗"),
        EmojiItem("NORTH WEST ARROW", "symbols", "arrow", "↖"),
        EmojiItem("UP DOWN ARROW", "symbols", "arrow", "↕"),
        EmojiItem("LEFT RIGHT ARROW", "symbols", "arrow", "↔"),
        EmojiItem("TOP WITH UPWARDS ARROW ABOVE", "symbols", "arrow", "🔝"),
        EmojiItem("SOON WITH RIGHTWARDS ARROW ABOVE", "symbols", "arrow", "🔜"),
        EmojiItem(
            "ON WITH EXCLAMATION MARK WITH LEFT RIGHT ARROW ABOVE",
            "symbols",
            "arrow",
            "🔛",
        ),
        EmojiItem("END WITH LEFTWARDS ARROW ABOVE", "symbols", "arrow", "🔚"),
        EmojiItem("BACK WITH LEFTWARDS ARROW ABOVE", "symbols", "arrow", "🔙"),
        EmojiItem(
            "ANTICLOCKWISE DOWNWARDS AND UPWARDS OPEN CIRCLE ARROWS",
            "symbols",
            "arrow",
            "🔄",
        ),
        EmojiItem(
            "CLOCKWISE DOWNWARDS AND UPWARDS OPEN CIRCLE ARROWS",
            "symbols",
            "arrow",
            "🔃",
        ),
        EmojiItem("BLACK LEFT-POINTING TRIANGLE", "symbols", "av-symbol", "◀"),
        EmojiItem(
            "BLACK RIGHT-POINTING TRIANGLE", "symbols", "av-symbol", "▶"
        ),
        EmojiItem("BLACK CIRCLE FOR RECORD", "symbols", "av-symbol", "⏺"),
        EmojiItem("BLACK SQUARE FOR STOP", "symbols", "av-symbol", "⏹"),
        EmojiItem("DOUBLE VERTICAL BAR", "symbols", "av-symbol", "⏸"),
        EmojiItem(
            "BLACK RIGHT-POINTING TRIANGLE WITH DOUBLE VERTICAL BAR",
            "symbols",
            "av-symbol",
            "⏯",
        ),
        EmojiItem(
            "BLACK LEFT-POINTING DOUBLE TRIANGLE WITH VERTICAL BAR",
            "symbols",
            "av-symbol",
            "⏮",
        ),
        EmojiItem(
            "BLACK RIGHT-POINTING DOUBLE TRIANGLE WITH VERTICAL BAR",
            "symbols",
            "av-symbol",
            "⏭",
        ),
        EmojiItem(
            "BLACK DOWN-POINTING DOUBLE TRIANGLE", "symbols", "av-symbol", "⏬"
        ),
        EmojiItem(
            "BLACK UP-POINTING DOUBLE TRIANGLE", "symbols", "av-symbol", "⏫"
        ),
        EmojiItem(
            "BLACK LEFT-POINTING DOUBLE TRIANGLE", "symbols", "av-symbol", "⏪"
        ),
        EmojiItem("EJECT SYMBOL", "symbols", "av-symbol", "⏏"),
        EmojiItem(
            "DOWN-POINTING SMALL RED TRIANGLE", "symbols", "av-symbol", "🔽"
        ),
        EmojiItem(
            "UP-POINTING SMALL RED TRIANGLE", "symbols", "av-symbol", "🔼"
        ),
        EmojiItem("HIGH BRIGHTNESS SYMBOL", "symbols", "av-symbol", "🔆"),
        EmojiItem("LOW BRIGHTNESS SYMBOL", "symbols", "av-symbol", "🔅"),
        EmojiItem(
            "CLOCKWISE RIGHTWARDS AND LEFTWARDS OPEN CIRCLE ARROWS WITH CIRCLED ONE OVERLAY",
            "symbols",
            "av-symbol",
            "🔂",
        ),
        EmojiItem(
            "CLOCKWISE RIGHTWARDS AND LEFTWARDS OPEN CIRCLE ARROWS",
            "symbols",
            "av-symbol",
            "🔁",
        ),
        EmojiItem("TWISTED RIGHTWARDS ARROWS", "symbols", "av-symbol", "🔀"),
        EmojiItem("ANTENNA WITH BARS", "symbols", "av-symbol", "📶"),
        EmojiItem("MOBILE PHONE OFF", "symbols", "av-symbol", "📴"),
        EmojiItem("VIBRATION MODE", "symbols", "av-symbol", "📳"),
        EmojiItem("CINEMA", "symbols", "av-symbol", "🎦"),
        EmojiItem("HEAVY DOLLAR SIGN", "symbols", "currency", "💲"),
        EmojiItem("CURRENCY EXCHANGE", "symbols", "currency", "💱"),
        EmojiItem(
            "MALE WITH STROKE AND MALE AND FEMALE SIGN",
            "symbols",
            "gender",
            "⚧",
        ),
        EmojiItem("MALE SIGN", "symbols", "gender", "♂"),
        EmojiItem("FEMALE SIGN", "symbols", "gender", "♀"),
        EmojiItem("WHITE LARGE SQUARE", "symbols", "geometric", "⬜"),
        EmojiItem("BLACK LARGE SQUARE", "symbols", "geometric", "⬛"),
        EmojiItem("MEDIUM BLACK CIRCLE", "symbols", "geometric", "⚫"),
        EmojiItem("MEDIUM WHITE CIRCLE", "symbols", "geometric", "⚪"),
        EmojiItem("BLACK MEDIUM SMALL SQUARE", "symbols", "geometric", "◾"),
        EmojiItem("WHITE MEDIUM SMALL SQUARE", "symbols", "geometric", "◽"),
        EmojiItem("BLACK MEDIUM SQUARE", "symbols", "geometric", "◼"),
        EmojiItem("WHITE MEDIUM SQUARE", "symbols", "geometric", "◻"),
        EmojiItem("WHITE SMALL SQUARE", "symbols", "geometric", "▫"),
        EmojiItem("BLACK SMALL SQUARE", "symbols", "geometric", "▪"),
        EmojiItem("LARGE BROWN SQUARE", "symbols", "geometric", "🟫"),
        EmojiItem("LARGE PURPLE SQUARE", "symbols", "geometric", "🟪"),
        EmojiItem("LARGE GREEN SQUARE", "symbols", "geometric", "🟩"),
        EmojiItem("LARGE YELLOW SQUARE", "symbols", "geometric", "🟨"),
        EmojiItem("LARGE ORANGE SQUARE", "symbols", "geometric", "🟧"),
        EmojiItem("LARGE BLUE SQUARE", "symbols", "geometric", "🟦"),
        EmojiItem("LARGE RED SQUARE", "symbols", "geometric", "🟥"),
        EmojiItem("LARGE BROWN CIRCLE", "symbols", "geometric", "🟤"),
        EmojiItem("LARGE PURPLE CIRCLE", "symbols", "geometric", "🟣"),
        EmojiItem("LARGE GREEN CIRCLE", "symbols", "geometric", "🟢"),
        EmojiItem("LARGE YELLOW CIRCLE", "symbols", "geometric", "🟡"),
        EmojiItem("LARGE ORANGE CIRCLE", "symbols", "geometric", "🟠"),
        EmojiItem("DOWN-POINTING RED TRIANGLE", "symbols", "geometric", "🔻"),
        EmojiItem("UP-POINTING RED TRIANGLE", "symbols", "geometric", "🔺"),
        EmojiItem("SMALL BLUE DIAMOND", "symbols", "geometric", "🔹"),
        EmojiItem("SMALL ORANGE DIAMOND", "symbols", "geometric", "🔸"),
        EmojiItem("LARGE BLUE DIAMOND", "symbols", "geometric", "🔷"),
        EmojiItem("LARGE ORANGE DIAMOND", "symbols", "geometric", "🔶"),
        EmojiItem("LARGE BLUE CIRCLE", "symbols", "geometric", "🔵"),
        EmojiItem("LARGE RED CIRCLE", "symbols", "geometric", "🔴"),
        EmojiItem("WHITE SQUARE BUTTON", "symbols", "geometric", "🔳"),
        EmojiItem("BLACK SQUARE BUTTON", "symbols", "geometric", "🔲"),
        EmojiItem("RADIO BUTTON", "symbols", "geometric", "🔘"),
        EmojiItem(
            "DIAMOND SHAPE WITH A DOT INSIDE", "symbols", "geometric", "💠"
        ),
        EmojiItem("KEYCAP TEN", "symbols", "keycap", "🔟"),
        EmojiItem("PERMANENT PAPER SIGN", "symbols", "math", "♾"),
        EmojiItem("HEAVY DIVISION SIGN", "symbols", "math", "➗"),
        EmojiItem("HEAVY MINUS SIGN", "symbols", "math", "➖"),
        EmojiItem("HEAVY PLUS SIGN", "symbols", "math", "➕"),
        EmojiItem("HEAVY MULTIPLICATION X", "symbols", "math", "✖"),
        EmojiItem("PART ALTERNATION MARK", "symbols", "other-symbol", "〽"),
        EmojiItem("HEAVY LARGE CIRCLE", "symbols", "other-symbol", "⭕"),
        EmojiItem("DOUBLE CURLY LOOP", "symbols", "other-symbol", "➿"),
        EmojiItem("CURLY LOOP", "symbols", "other-symbol", "➰"),
        EmojiItem(
            "NEGATIVE SQUARED CROSS MARK", "symbols", "other-symbol", "❎"
        ),
        EmojiItem("CROSS MARK", "symbols", "other-symbol", "❌"),
        EmojiItem("FLEUR-DE-LIS", "symbols", "other-symbol", "⚜"),
        EmojiItem(
            "BLACK UNIVERSAL RECYCLING SYMBOL", "symbols", "other-symbol", "♻"
        ),
        EmojiItem("REGISTERED SIGN", "symbols", "other-symbol", "®"),
        EmojiItem("COPYRIGHT SIGN", "symbols", "other-symbol", "©"),
        EmojiItem("SPARKLE", "symbols", "other-symbol", "❇"),
        EmojiItem("EIGHT POINTED BLACK STAR", "symbols", "other-symbol", "✴"),
        EmojiItem("EIGHT SPOKED ASTERISK", "symbols", "other-symbol", "✳"),
        EmojiItem("HEAVY CHECK MARK", "symbols", "other-symbol", "✔"),
        EmojiItem("WHITE HEAVY CHECK MARK", "symbols", "other-symbol", "✅"),
        EmojiItem("STAFF OF AESCULAPIUS", "symbols", "other-symbol", "⚕"),
        EmojiItem("BALLOT BOX WITH CHECK", "symbols", "other-symbol", "☑"),
        EmojiItem("TRADE MARK SIGN", "symbols", "other-symbol", "™"),
        EmojiItem("TRIDENT EMBLEM", "symbols", "other-symbol", "🔱"),
        EmojiItem(
            "JAPANESE SYMBOL FOR BEGINNER", "symbols", "other-symbol", "🔰"
        ),
        EmojiItem("NAME BADGE", "symbols", "other-symbol", "📛"),
        EmojiItem("DOUBLE EXCLAMATION MARK", "symbols", "punctuation", "‼"),
        EmojiItem("WAVY DASH", "symbols", "punctuation", "〰"),
        EmojiItem(
            "HEAVY EXCLAMATION MARK SYMBOL", "symbols", "punctuation", "❗"
        ),
        EmojiItem(
            "WHITE EXCLAMATION MARK ORNAMENT", "symbols", "punctuation", "❕"
        ),
        EmojiItem(
            "WHITE QUESTION MARK ORNAMENT", "symbols", "punctuation", "❔"
        ),
        EmojiItem(
            "BLACK QUESTION MARK ORNAMENT", "symbols", "punctuation", "❓"
        ),
        EmojiItem("EXCLAMATION QUESTION MARK", "symbols", "punctuation", "⁉"),
        EmojiItem("LATIN CROSS", "symbols", "religion", "✝"),
        EmojiItem("ATOM SYMBOL", "symbols", "religion", "⚛"),
        EmojiItem("YIN YANG", "symbols", "religion", "☯"),
        EmojiItem("PEACE SYMBOL", "symbols", "religion", "☮"),
        EmojiItem("STAR AND CRESCENT", "symbols", "religion", "☪"),
        EmojiItem("STAR OF DAVID", "symbols", "religion", "✡"),
        EmojiItem("WHEEL OF DHARMA", "symbols", "religion", "☸"),
        EmojiItem("ORTHODOX CROSS", "symbols", "religion", "☦"),
        EmojiItem("PLACE OF WORSHIP", "symbols", "religion", "🛐"),
        EmojiItem("MENORAH WITH NINE BRANCHES", "symbols", "religion", "🕎"),
        EmojiItem("OM SYMBOL", "symbols", "religion", "🕉"),
        EmojiItem(
            "SIX POINTED STAR WITH MIDDLE DOT", "symbols", "religion", "🔯"
        ),
        EmojiItem("WHEELCHAIR SYMBOL", "symbols", "transport-sign", "♿"),
        EmojiItem("LEFT LUGGAGE", "symbols", "transport-sign", "🛅"),
        EmojiItem("BAGGAGE CLAIM", "symbols", "transport-sign", "🛄"),
        EmojiItem("CUSTOMS", "symbols", "transport-sign", "🛃"),
        EmojiItem("PASSPORT CONTROL", "symbols", "transport-sign", "🛂"),
        EmojiItem("WATER CLOSET", "symbols", "transport-sign", "🚾"),
        EmojiItem("BABY SYMBOL", "symbols", "transport-sign", "🚼"),
        EmojiItem("RESTROOM", "symbols", "transport-sign", "🚻"),
        EmojiItem("WOMENS SYMBOL", "symbols", "transport-sign", "🚺"),
        EmojiItem("MENS SYMBOL", "symbols", "transport-sign", "🚹"),
        EmojiItem("POTABLE WATER SYMBOL", "symbols", "transport-sign", "🚰"),
        EmojiItem(
            "PUT LITTER IN ITS PLACE SYMBOL", "symbols", "transport-sign", "🚮"
        ),
        EmojiItem(
            "AUTOMATED TELLER MACHINE", "symbols", "transport-sign", "🏧"
        ),
        EmojiItem("NO ENTRY", "symbols", "warning", "⛔"),
        EmojiItem("WARNING SIGN", "symbols", "warning", "⚠"),
        EmojiItem("BIOHAZARD SIGN", "symbols", "warning", "☣"),
        EmojiItem("RADIOACTIVE SIGN", "symbols", "warning", "☢"),
        EmojiItem("CHILDREN CROSSING", "symbols", "warning", "🚸"),
        EmojiItem("NO PEDESTRIANS", "symbols", "warning", "🚷"),
        EmojiItem("NO BICYCLES", "symbols", "warning", "🚳"),
        EmojiItem("NON-POTABLE WATER SYMBOL", "symbols", "warning", "🚱"),
        EmojiItem("DO NOT LITTER SYMBOL", "symbols", "warning", "🚯"),
        EmojiItem("NO SMOKING SYMBOL", "symbols", "warning", "🚭"),
        EmojiItem("NO ENTRY SIGN", "symbols", "warning", "🚫"),
        EmojiItem("NO ONE UNDER EIGHTEEN SYMBOL", "symbols", "warning", "🔞"),
        EmojiItem("NO MOBILE PHONES", "symbols", "warning", "📵"),
        EmojiItem("OPHIUCHUS", "symbols", "zodiac", "⛎"),
        EmojiItem("SCORPIUS", "symbols", "zodiac", "♏"),
        EmojiItem("LIBRA", "symbols", "zodiac", "♎"),
        EmojiItem("VIRGO", "symbols", "zodiac", "♍"),
        EmojiItem("LEO", "symbols", "zodiac", "♌"),
        EmojiItem("CANCER", "symbols", "zodiac", "♋"),
        EmojiItem("GEMINI", "symbols", "zodiac", "♊"),
        EmojiItem("PISCES", "symbols", "zodiac", "♓"),
        EmojiItem("AQUARIUS", "symbols", "zodiac", "♒"),
        EmojiItem("CAPRICORN", "symbols", "zodiac", "♑"),
        EmojiItem("SAGITTARIUS", "symbols", "zodiac", "♐"),
        EmojiItem("TAURUS", "symbols", "zodiac", "♉"),
        EmojiItem("ARIES", "symbols", "zodiac", "♈"),
        EmojiItem("LUGGAGE", "travel-places", "hotel", "🧳"),
        EmojiItem("BELLHOP BELL", "travel-places", "hotel", "🛎"),
        EmojiItem("WOOD", "travel-places", "place-building", "🪵"),
        EmojiItem("ROCK", "travel-places", "place-building", "🪨"),
        EmojiItem("BRICK", "travel-places", "place-building", "🧱"),
        EmojiItem("HUT", "travel-places", "place-building", "🛖"),
        EmojiItem("STATUE OF LIBERTY", "travel-places", "place-building", "🗽"),
        EmojiItem("TOKYO TOWER", "travel-places", "place-building", "🗼"),
        EmojiItem("WEDDING", "travel-places", "place-building", "💒"),
        EmojiItem("EUROPEAN CASTLE", "travel-places", "place-building", "🏰"),
        EmojiItem("JAPANESE CASTLE", "travel-places", "place-building", "🏯"),
        EmojiItem("FACTORY", "travel-places", "place-building", "🏭"),
        EmojiItem("DEPARTMENT STORE", "travel-places", "place-building", "🏬"),
        EmojiItem("SCHOOL", "travel-places", "place-building", "🏫"),
        EmojiItem("CONVENIENCE STORE", "travel-places", "place-building", "🏪"),
        EmojiItem("LOVE HOTEL", "travel-places", "place-building", "🏩"),
        EmojiItem("HOTEL", "travel-places", "place-building", "🏨"),
        EmojiItem("BANK", "travel-places", "place-building", "🏦"),
        EmojiItem("HOSPITAL", "travel-places", "place-building", "🏥"),
        EmojiItem(
            "EUROPEAN POST OFFICE", "travel-places", "place-building", "🏤"
        ),
        EmojiItem(
            "JAPANESE POST OFFICE", "travel-places", "place-building", "🏣"
        ),
        EmojiItem("OFFICE BUILDING", "travel-places", "place-building", "🏢"),
        EmojiItem("HOUSE WITH GARDEN", "travel-places", "place-building", "🏡"),
        EmojiItem("HOUSE BUILDING", "travel-places", "place-building", "🏠"),
        EmojiItem("STADIUM", "travel-places", "place-building", "🏟"),
        EmojiItem(
            "CLASSICAL BUILDING", "travel-places", "place-building", "🏛"
        ),
        EmojiItem(
            "DERELICT HOUSE BUILDING", "travel-places", "place-building", "🏚"
        ),
        EmojiItem("HOUSE BUILDINGS", "travel-places", "place-building", "🏘"),
        EmojiItem(
            "BUILDING CONSTRUCTION", "travel-places", "place-building", "🏗"
        ),
        EmojiItem("MOUNTAIN", "travel-places", "place-geographic", "⛰"),
        EmojiItem("MOUNT FUJI", "travel-places", "place-geographic", "🗻"),
        EmojiItem("NATIONAL PARK", "travel-places", "place-geographic", "🏞"),
        EmojiItem("DESERT ISLAND", "travel-places", "place-geographic", "🏝"),
        EmojiItem("DESERT", "travel-places", "place-geographic", "🏜"),
        EmojiItem(
            "BEACH WITH UMBRELLA", "travel-places", "place-geographic", "🏖"
        ),
        EmojiItem("CAMPING", "travel-places", "place-geographic", "🏕"),
        EmojiItem(
            "SNOW CAPPED MOUNTAIN", "travel-places", "place-geographic", "🏔"
        ),
        EmojiItem("VOLCANO", "travel-places", "place-geographic", "🌋"),
        EmojiItem("COMPASS", "travel-places", "place-map", "🧭"),
        EmojiItem("SILHOUETTE OF JAPAN", "travel-places", "place-map", "🗾"),
        EmojiItem("WORLD MAP", "travel-places", "place-map", "🗺"),
        EmojiItem("GLOBE WITH MERIDIANS", "travel-places", "place-map", "🌐"),
        EmojiItem(
            "EARTH GLOBE ASIA-AUSTRALIA", "travel-places", "place-map", "🌏"
        ),
        EmojiItem("EARTH GLOBE AMERICAS", "travel-places", "place-map", "🌎"),
        EmojiItem(
            "EARTH GLOBE EUROPE-AFRICA", "travel-places", "place-map", "🌍"
        ),
        EmojiItem("TENT", "travel-places", "place-other", "⛺"),
        EmojiItem("FOUNTAIN", "travel-places", "place-other", "⛲"),
        EmojiItem("HOT SPRINGS", "travel-places", "place-other", "♨"),
        EmojiItem("BARBER POLE", "travel-places", "place-other", "💈"),
        EmojiItem("CITYSCAPE", "travel-places", "place-other", "🏙"),
        EmojiItem("CIRCUS TENT", "travel-places", "place-other", "🎪"),
        EmojiItem("ROLLER COASTER", "travel-places", "place-other", "🎢"),
        EmojiItem("FERRIS WHEEL", "travel-places", "place-other", "🎡"),
        EmojiItem("CAROUSEL HORSE", "travel-places", "place-other", "🎠"),
        EmojiItem("BRIDGE AT NIGHT", "travel-places", "place-other", "🌉"),
        EmojiItem(
            "SUNSET OVER BUILDINGS", "travel-places", "place-other", "🌇"
        ),
        EmojiItem("CITYSCAPE AT DUSK", "travel-places", "place-other", "🌆"),
        EmojiItem("SUNRISE", "travel-places", "place-other", "🌅"),
        EmojiItem(
            "SUNRISE OVER MOUNTAINS", "travel-places", "place-other", "🌄"
        ),
        EmojiItem("NIGHT WITH STARS", "travel-places", "place-other", "🌃"),
        EmojiItem("FOGGY", "travel-places", "place-other", "🌁"),
        EmojiItem("CHURCH", "travel-places", "place-religious", "⛪"),
        EmojiItem("HINDU TEMPLE", "travel-places", "place-religious", "🛕"),
        EmojiItem("SYNAGOGUE", "travel-places", "place-religious", "🕍"),
        EmojiItem("MOSQUE", "travel-places", "place-religious", "🕌"),
        EmojiItem("KAABA", "travel-places", "place-religious", "🕋"),
        EmojiItem("WHITE MEDIUM STAR", "travel-places", "sky & weather", "⭐"),
        EmojiItem("UMBRELLA ON GROUND", "travel-places", "sky & weather", "⛱"),
        EmojiItem(
            "THUNDER CLOUD AND RAIN", "travel-places", "sky & weather", "⛈"
        ),
        EmojiItem("SUN BEHIND CLOUD", "travel-places", "sky & weather", "⛅"),
        EmojiItem(
            "SNOWMAN WITHOUT SNOW", "travel-places", "sky & weather", "⛄"
        ),
        EmojiItem("HIGH VOLTAGE SIGN", "travel-places", "sky & weather", "⚡"),
        EmojiItem("SNOWFLAKE", "travel-places", "sky & weather", "❄"),
        EmojiItem(
            "UMBRELLA WITH RAIN DROPS", "travel-places", "sky & weather", "☔"
        ),
        EmojiItem("COMET", "travel-places", "sky & weather", "☄"),
        EmojiItem("SNOWMAN", "travel-places", "sky & weather", "☃"),
        EmojiItem("UMBRELLA", "travel-places", "sky & weather", "☂"),
        EmojiItem("CLOUD", "travel-places", "sky & weather", "☁"),
        EmojiItem(
            "BLACK SUN WITH RAYS", "travel-places", "sky & weather", "☀"
        ),
        EmojiItem("RINGED PLANET", "travel-places", "sky & weather", "🪐"),
        EmojiItem("FIRE", "travel-places", "sky & weather", "🔥"),
        EmojiItem("DROPLET", "travel-places", "sky & weather", "💧"),
        EmojiItem("WIND BLOWING FACE", "travel-places", "sky & weather", "🌬"),
        EmojiItem("FOG", "travel-places", "sky & weather", "🌫"),
        EmojiItem("CLOUD WITH TORNADO", "travel-places", "sky & weather", "🌪"),
        EmojiItem(
            "CLOUD WITH LIGHTNING", "travel-places", "sky & weather", "🌩"
        ),
        EmojiItem("CLOUD WITH SNOW", "travel-places", "sky & weather", "🌨"),
        EmojiItem("CLOUD WITH RAIN", "travel-places", "sky & weather", "🌧"),
        EmojiItem(
            "WHITE SUN BEHIND CLOUD WITH RAIN",
            "travel-places",
            "sky & weather",
            "🌦",
        ),
        EmojiItem(
            "WHITE SUN BEHIND CLOUD", "travel-places", "sky & weather", "🌥"
        ),
        EmojiItem(
            "WHITE SUN WITH SMALL CLOUD", "travel-places", "sky & weather", "🌤"
        ),
        EmojiItem("THERMOMETER", "travel-places", "sky & weather", "🌡"),
        EmojiItem("SHOOTING STAR", "travel-places", "sky & weather", "🌠"),
        EmojiItem("GLOWING STAR", "travel-places", "sky & weather", "🌟"),
        EmojiItem("SUN WITH FACE", "travel-places", "sky & weather", "🌞"),
        EmojiItem(
            "FULL MOON WITH FACE", "travel-places", "sky & weather", "🌝"
        ),
        EmojiItem(
            "LAST QUARTER MOON WITH FACE",
            "travel-places",
            "sky & weather",
            "🌜",
        ),
        EmojiItem(
            "FIRST QUARTER MOON WITH FACE",
            "travel-places",
            "sky & weather",
            "🌛",
        ),
        EmojiItem("NEW MOON WITH FACE", "travel-places", "sky & weather", "🌚"),
        EmojiItem("CRESCENT MOON", "travel-places", "sky & weather", "🌙"),
        EmojiItem(
            "WANING CRESCENT MOON SYMBOL",
            "travel-places",
            "sky & weather",
            "🌘",
        ),
        EmojiItem(
            "LAST QUARTER MOON SYMBOL", "travel-places", "sky & weather", "🌗"
        ),
        EmojiItem(
            "WANING GIBBOUS MOON SYMBOL", "travel-places", "sky & weather", "🌖"
        ),
        EmojiItem("FULL MOON SYMBOL", "travel-places", "sky & weather", "🌕"),
        EmojiItem(
            "WAXING GIBBOUS MOON SYMBOL", "travel-places", "sky & weather", "🌔"
        ),
        EmojiItem(
            "FIRST QUARTER MOON SYMBOL", "travel-places", "sky & weather", "🌓"
        ),
        EmojiItem(
            "WAXING CRESCENT MOON SYMBOL",
            "travel-places",
            "sky & weather",
            "🌒",
        ),
        EmojiItem("NEW MOON SYMBOL", "travel-places", "sky & weather", "🌑"),
        EmojiItem("MILKY WAY", "travel-places", "sky & weather", "🌌"),
        EmojiItem("WATER WAVE", "travel-places", "sky & weather", "🌊"),
        EmojiItem("RAINBOW", "travel-places", "sky & weather", "🌈"),
        EmojiItem("CLOSED UMBRELLA", "travel-places", "sky & weather", "🌂"),
        EmojiItem("CYCLONE", "travel-places", "sky & weather", "🌀"),
        EmojiItem("HOURGLASS WITH FLOWING SAND", "travel-places", "time", "⏳"),
        EmojiItem("TIMER CLOCK", "travel-places", "time", "⏲"),
        EmojiItem("STOPWATCH", "travel-places", "time", "⏱"),
        EmojiItem("ALARM CLOCK", "travel-places", "time", "⏰"),
        EmojiItem("HOURGLASS", "travel-places", "time", "⌛"),
        EmojiItem("WATCH", "travel-places", "time", "⌚"),
        EmojiItem("MANTELPIECE CLOCK", "travel-places", "time", "🕰"),
        EmojiItem("CLOCK FACE TWELVE-THIRTY", "travel-places", "time", "🕧"),
        EmojiItem("CLOCK FACE ELEVEN-THIRTY", "travel-places", "time", "🕦"),
        EmojiItem("CLOCK FACE TEN-THIRTY", "travel-places", "time", "🕥"),
        EmojiItem("CLOCK FACE NINE-THIRTY", "travel-places", "time", "🕤"),
        EmojiItem("CLOCK FACE EIGHT-THIRTY", "travel-places", "time", "🕣"),
        EmojiItem("CLOCK FACE SEVEN-THIRTY", "travel-places", "time", "🕢"),
        EmojiItem("CLOCK FACE SIX-THIRTY", "travel-places", "time", "🕡"),
        EmojiItem("CLOCK FACE FIVE-THIRTY", "travel-places", "time", "🕠"),
        EmojiItem("CLOCK FACE FOUR-THIRTY", "travel-places", "time", "🕟"),
        EmojiItem("CLOCK FACE THREE-THIRTY", "travel-places", "time", "🕞"),
        EmojiItem("CLOCK FACE TWO-THIRTY", "travel-places", "time", "🕝"),
        EmojiItem("CLOCK FACE ONE-THIRTY", "travel-places", "time", "🕜"),
        EmojiItem("CLOCK FACE TWELVE OCLOCK", "travel-places", "time", "🕛"),
        EmojiItem("CLOCK FACE ELEVEN OCLOCK", "travel-places", "time", "🕚"),
        EmojiItem("CLOCK FACE TEN OCLOCK", "travel-places", "time", "🕙"),
        EmojiItem("CLOCK FACE NINE OCLOCK", "travel-places", "time", "🕘"),
        EmojiItem("CLOCK FACE EIGHT OCLOCK", "travel-places", "time", "🕗"),
        EmojiItem("CLOCK FACE SEVEN OCLOCK", "travel-places", "time", "🕖"),
        EmojiItem("CLOCK FACE SIX OCLOCK", "travel-places", "time", "🕕"),
        EmojiItem("CLOCK FACE FIVE OCLOCK", "travel-places", "time", "🕔"),
        EmojiItem("CLOCK FACE FOUR OCLOCK", "travel-places", "time", "🕓"),
        EmojiItem("CLOCK FACE THREE OCLOCK", "travel-places", "time", "🕒"),
        EmojiItem("CLOCK FACE TWO OCLOCK", "travel-places", "time", "🕑"),
        EmojiItem("CLOCK FACE ONE OCLOCK", "travel-places", "time", "🕐"),
        EmojiItem("AIRPLANE", "travel-places", "transport-air", "✈"),
        EmojiItem("PARACHUTE", "travel-places", "transport-air", "🪂"),
        EmojiItem("FLYING SAUCER", "travel-places", "transport-air", "🛸"),
        EmojiItem("SATELLITE", "travel-places", "transport-air", "🛰"),
        EmojiItem("AIRPLANE ARRIVING", "travel-places", "transport-air", "🛬"),
        EmojiItem("AIRPLANE DEPARTURE", "travel-places", "transport-air", "🛫"),
        EmojiItem("SMALL AIRPLANE", "travel-places", "transport-air", "🛩"),
        EmojiItem("AERIAL TRAMWAY", "travel-places", "transport-air", "🚡"),
        EmojiItem("MOUNTAIN CABLEWAY", "travel-places", "transport-air", "🚠"),
        EmojiItem("SUSPENSION RAILWAY", "travel-places", "transport-air", "🚟"),
        EmojiItem("HELICOPTER", "travel-places", "transport-air", "🚁"),
        EmojiItem("ROCKET", "travel-places", "transport-air", "🚀"),
        EmojiItem("SEAT", "travel-places", "transport-air", "💺"),
        EmojiItem("FUEL PUMP", "travel-places", "transport-ground", "⛽"),
        EmojiItem(
            "MANUAL WHEELCHAIR", "travel-places", "transport-ground", "🦽"
        ),
        EmojiItem(
            "MOTORIZED WHEELCHAIR", "travel-places", "transport-ground", "🦼"
        ),
        EmojiItem("ROLLER SKATE", "travel-places", "transport-ground", "🛼"),
        EmojiItem("PICKUP TRUCK", "travel-places", "transport-ground", "🛻"),
        EmojiItem("AUTO RICKSHAW", "travel-places", "transport-ground", "🛺"),
        EmojiItem("SKATEBOARD", "travel-places", "transport-ground", "🛹"),
        EmojiItem("MOTOR SCOOTER", "travel-places", "transport-ground", "🛵"),
        EmojiItem("SCOOTER", "travel-places", "transport-ground", "🛴"),
        EmojiItem("RAILWAY TRACK", "travel-places", "transport-ground", "🛤"),
        EmojiItem("MOTORWAY", "travel-places", "transport-ground", "🛣"),
        EmojiItem("OIL DRUM", "travel-places", "transport-ground", "🛢"),
        EmojiItem("OCTAGONAL SIGN", "travel-places", "transport-ground", "🛑"),
        EmojiItem("BICYCLE", "travel-places", "transport-ground", "🚲"),
        EmojiItem(
            "POLICE CARS REVOLVING LIGHT",
            "travel-places",
            "transport-ground",
            "🚨",
        ),
        EmojiItem(
            "CONSTRUCTION SIGN", "travel-places", "transport-ground", "🚧"
        ),
        EmojiItem(
            "VERTICAL TRAFFIC LIGHT", "travel-places", "transport-ground", "🚦"
        ),
        EmojiItem(
            "HORIZONTAL TRAFFIC LIGHT",
            "travel-places",
            "transport-ground",
            "🚥",
        ),
        EmojiItem(
            "MOUNTAIN RAILWAY", "travel-places", "transport-ground", "🚞"
        ),
        EmojiItem("MONORAIL", "travel-places", "transport-ground", "🚝"),
        EmojiItem("TRACTOR", "travel-places", "transport-ground", "🚜"),
        EmojiItem(
            "ARTICULATED LORRY", "travel-places", "transport-ground", "🚛"
        ),
        EmojiItem("DELIVERY TRUCK", "travel-places", "transport-ground", "🚚"),
        EmojiItem(
            "RECREATIONAL VEHICLE", "travel-places", "transport-ground", "🚙"
        ),
        EmojiItem(
            "ONCOMING AUTOMOBILE", "travel-places", "transport-ground", "🚘"
        ),
        EmojiItem("AUTOMOBILE", "travel-places", "transport-ground", "🚗"),
        EmojiItem("ONCOMING TAXI", "travel-places", "transport-ground", "🚖"),
        EmojiItem("TAXI", "travel-places", "transport-ground", "🚕"),
        EmojiItem(
            "ONCOMING POLICE CAR", "travel-places", "transport-ground", "🚔"
        ),
        EmojiItem("POLICE CAR", "travel-places", "transport-ground", "🚓"),
        EmojiItem("FIRE ENGINE", "travel-places", "transport-ground", "🚒"),
        EmojiItem("AMBULANCE", "travel-places", "transport-ground", "🚑"),
        EmojiItem("MINIBUS", "travel-places", "transport-ground", "🚐"),
        EmojiItem("BUS STOP", "travel-places", "transport-ground", "🚏"),
        EmojiItem("TROLLEYBUS", "travel-places", "transport-ground", "🚎"),
        EmojiItem("ONCOMING BUS", "travel-places", "transport-ground", "🚍"),
        EmojiItem("BUS", "travel-places", "transport-ground", "🚌"),
        EmojiItem("TRAM CAR", "travel-places", "transport-ground", "🚋"),
        EmojiItem("TRAM", "travel-places", "transport-ground", "🚊"),
        EmojiItem("STATION", "travel-places", "transport-ground", "🚉"),
        EmojiItem("LIGHT RAIL", "travel-places", "transport-ground", "🚈"),
        EmojiItem("METRO", "travel-places", "transport-ground", "🚇"),
        EmojiItem("TRAIN", "travel-places", "transport-ground", "🚆"),
        EmojiItem(
            "HIGH-SPEED TRAIN WITH BULLET NOSE",
            "travel-places",
            "transport-ground",
            "🚅",
        ),
        EmojiItem(
            "HIGH-SPEED TRAIN", "travel-places", "transport-ground", "🚄"
        ),
        EmojiItem("RAILWAY CAR", "travel-places", "transport-ground", "🚃"),
        EmojiItem(
            "STEAM LOCOMOTIVE", "travel-places", "transport-ground", "🚂"
        ),
        EmojiItem("RACING CAR", "travel-places", "transport-ground", "🏎"),
        EmojiItem(
            "RACING MOTORCYCLE", "travel-places", "transport-ground", "🏍"
        ),
        EmojiItem("SAILBOAT", "travel-places", "transport-water", "⛵"),
        EmojiItem("FERRY", "travel-places", "transport-water", "⛴"),
        EmojiItem("ANCHOR", "travel-places", "transport-water", "⚓"),
        EmojiItem("CANOE", "travel-places", "transport-water", "🛶"),
        EmojiItem("PASSENGER SHIP", "travel-places", "transport-water", "🛳"),
        EmojiItem("MOTOR BOAT", "travel-places", "transport-water", "🛥"),
        EmojiItem("SPEEDBOAT", "travel-places", "transport-water", "🚤"),
        EmojiItem("SHIP", "travel-places", "transport-water", "🚢"),
        EmojiItem("WEARY CAT FACE", "smiley-emotion", "cat-face", "🙀"),
        EmojiItem("CRYING CAT FACE", "smiley-emotion", "cat-face", "😿"),
        EmojiItem("POUTING CAT FACE", "smiley-emotion", "cat-face", "😾"),
        EmojiItem(
            "KISSING CAT FACE WITH CLOSED EYES",
            "smiley-emotion",
            "cat-face",
            "😽",
        ),
        EmojiItem(
            "CAT FACE WITH WRY SMILE", "smiley-emotion", "cat-face", "😼"
        ),
        EmojiItem(
            "SMILING CAT FACE WITH HEART-SHAPED EYES",
            "smiley-emotion",
            "cat-face",
            "😻",
        ),
        EmojiItem(
            "SMILING CAT FACE WITH OPEN MOUTH",
            "smiley-emotion",
            "cat-face",
            "😺",
        ),
        EmojiItem(
            "CAT FACE WITH TEARS OF JOY", "smiley-emotion", "cat-face", "😹"
        ),
        EmojiItem(
            "GRINNING CAT FACE WITH SMILING EYES",
            "smiley-emotion",
            "cat-face",
            "😸",
        ),
        EmojiItem("HEAVY BLACK HEART", "smiley-emotion", "emotion", "❤"),
        EmojiItem(
            "HEAVY HEART EXCLAMATION MARK ORNAMENT",
            "smiley-emotion",
            "emotion",
            "❣",
        ),
        EmojiItem("ORANGE HEART", "smiley-emotion", "emotion", "🧡"),
        EmojiItem("BROWN HEART", "smiley-emotion", "emotion", "🤎"),
        EmojiItem("WHITE HEART", "smiley-emotion", "emotion", "🤍"),
        EmojiItem("RIGHT ANGER BUBBLE", "smiley-emotion", "emotion", "🗯"),
        EmojiItem("LEFT SPEECH BUBBLE", "smiley-emotion", "emotion", "🗨"),
        EmojiItem("BLACK HEART", "smiley-emotion", "emotion", "🖤"),
        EmojiItem("HOLE", "smiley-emotion", "emotion", "🕳"),
        EmojiItem("HUNDRED POINTS SYMBOL", "smiley-emotion", "emotion", "💯"),
        EmojiItem("THOUGHT BALLOON", "smiley-emotion", "emotion", "💭"),
        EmojiItem("SPEECH BALLOON", "smiley-emotion", "emotion", "💬"),
        EmojiItem("DIZZY SYMBOL", "smiley-emotion", "emotion", "💫"),
        EmojiItem("DASH SYMBOL", "smiley-emotion", "emotion", "💨"),
        EmojiItem("SPLASHING SWEAT SYMBOL", "smiley-emotion", "emotion", "💦"),
        EmojiItem("COLLISION SYMBOL", "smiley-emotion", "emotion", "💥"),
        EmojiItem("SLEEPING SYMBOL", "smiley-emotion", "emotion", "💤"),
        EmojiItem("BOMB", "smiley-emotion", "emotion", "💣"),
        EmojiItem("ANGER SYMBOL", "smiley-emotion", "emotion", "💢"),
        EmojiItem("HEART DECORATION", "smiley-emotion", "emotion", "💟"),
        EmojiItem("REVOLVING HEARTS", "smiley-emotion", "emotion", "💞"),
        EmojiItem("HEART WITH RIBBON", "smiley-emotion", "emotion", "💝"),
        EmojiItem("PURPLE HEART", "smiley-emotion", "emotion", "💜"),
        EmojiItem("YELLOW HEART", "smiley-emotion", "emotion", "💛"),
        EmojiItem("GREEN HEART", "smiley-emotion", "emotion", "💚"),
        EmojiItem("BLUE HEART", "smiley-emotion", "emotion", "💙"),
        EmojiItem("HEART WITH ARROW", "smiley-emotion", "emotion", "💘"),
        EmojiItem("GROWING HEART", "smiley-emotion", "emotion", "💗"),
        EmojiItem("SPARKLING HEART", "smiley-emotion", "emotion", "💖"),
        EmojiItem("TWO HEARTS", "smiley-emotion", "emotion", "💕"),
        EmojiItem("BROKEN HEART", "smiley-emotion", "emotion", "💔"),
        EmojiItem("BEATING HEART", "smiley-emotion", "emotion", "💓"),
        EmojiItem("LOVE LETTER", "smiley-emotion", "emotion", "💌"),
        EmojiItem("KISS MARK", "smiley-emotion", "emotion", "💋"),
        EmojiItem(
            "WHITE SMILING FACE", "smiley-emotion", "face-affection", "☺"
        ),
        EmojiItem(
            "SMILING FACE WITH TEAR", "smiley-emotion", "face-affection", "🥲"
        ),
        EmojiItem(
            "SMILING FACE WITH SMILING EYES AND THREE HEARTS",
            "smiley-emotion",
            "face-affection",
            "🥰",
        ),
        EmojiItem(
            "GRINNING FACE WITH STAR EYES",
            "smiley-emotion",
            "face-affection",
            "🤩",
        ),
        EmojiItem(
            "KISSING FACE WITH CLOSED EYES",
            "smiley-emotion",
            "face-affection",
            "😚",
        ),
        EmojiItem(
            "KISSING FACE WITH SMILING EYES",
            "smiley-emotion",
            "face-affection",
            "😙",
        ),
        EmojiItem(
            "FACE THROWING A KISS", "smiley-emotion", "face-affection", "😘"
        ),
        EmojiItem("KISSING FACE", "smiley-emotion", "face-affection", "😗"),
        EmojiItem(
            "SMILING FACE WITH HEART-SHAPED EYES",
            "smiley-emotion",
            "face-affection",
            "😍",
        ),
        EmojiItem(
            "WHITE FROWNING FACE", "smiley-emotion", "face-concerned", "☹"
        ),
        EmojiItem(
            "FACE WITH PLEADING EYES", "smiley-emotion", "face-concerned", "🥺"
        ),
        EmojiItem("YAWNING FACE", "smiley-emotion", "face-concerned", "🥱"),
        EmojiItem(
            "SLIGHTLY FROWNING FACE", "smiley-emotion", "face-concerned", "🙁"
        ),
        EmojiItem("FLUSHED FACE", "smiley-emotion", "face-concerned", "😳"),
        EmojiItem("ASTONISHED FACE", "smiley-emotion", "face-concerned", "😲"),
        EmojiItem(
            "FACE SCREAMING IN FEAR", "smiley-emotion", "face-concerned", "😱"
        ),
        EmojiItem(
            "FACE WITH OPEN MOUTH AND COLD SWEAT",
            "smiley-emotion",
            "face-concerned",
            "😰",
        ),
        EmojiItem("HUSHED FACE", "smiley-emotion", "face-concerned", "😯"),
        EmojiItem(
            "FACE WITH OPEN MOUTH", "smiley-emotion", "face-concerned", "😮"
        ),
        EmojiItem(
            "LOUDLY CRYING FACE", "smiley-emotion", "face-concerned", "😭"
        ),
        EmojiItem("TIRED FACE", "smiley-emotion", "face-concerned", "😫"),
        EmojiItem("WEARY FACE", "smiley-emotion", "face-concerned", "😩"),
        EmojiItem("FEARFUL FACE", "smiley-emotion", "face-concerned", "😨"),
        EmojiItem("ANGUISHED FACE", "smiley-emotion", "face-concerned", "😧"),
        EmojiItem(
            "FROWNING FACE WITH OPEN MOUTH",
            "smiley-emotion",
            "face-concerned",
            "😦",
        ),
        EmojiItem(
            "DISAPPOINTED BUT RELIEVED FACE",
            "smiley-emotion",
            "face-concerned",
            "😥",
        ),
        EmojiItem("PERSEVERING FACE", "smiley-emotion", "face-concerned", "😣"),
        EmojiItem("CRYING FACE", "smiley-emotion", "face-concerned", "😢"),
        EmojiItem("WORRIED FACE", "smiley-emotion", "face-concerned", "😟"),
        EmojiItem(
            "DISAPPOINTED FACE", "smiley-emotion", "face-concerned", "😞"
        ),
        EmojiItem("CONFOUNDED FACE", "smiley-emotion", "face-concerned", "😖"),
        EmojiItem("CONFUSED FACE", "smiley-emotion", "face-concerned", "😕"),
        EmojiItem(
            "FACE WITH COLD SWEAT", "smiley-emotion", "face-concerned", "😓"
        ),
        EmojiItem("CLOWN FACE", "smiley-emotion", "face-costume", "🤡"),
        EmojiItem("ROBOT FACE", "smiley-emotion", "face-costume", "🤖"),
        EmojiItem("PILE OF POO", "smiley-emotion", "face-costume", "💩"),
        EmojiItem("ALIEN MONSTER", "smiley-emotion", "face-costume", "👾"),
        EmojiItem(
            "EXTRATERRESTRIAL ALIEN", "smiley-emotion", "face-costume", "👽"
        ),
        EmojiItem("GHOST", "smiley-emotion", "face-costume", "👻"),
        EmojiItem("JAPANESE GOBLIN", "smiley-emotion", "face-costume", "👺"),
        EmojiItem("JAPANESE OGRE", "smiley-emotion", "face-costume", "👹"),
        EmojiItem("FACE WITH MONOCLE", "smiley-emotion", "face-glasses", "🧐"),
        EmojiItem("NERD FACE", "smiley-emotion", "face-glasses", "🤓"),
        EmojiItem(
            "SMILING FACE WITH SUNGLASSES",
            "smiley-emotion",
            "face-glasses",
            "😎",
        ),
        EmojiItem(
            "SMILING FACE WITH SMILING EYES AND HAND COVERING MOUTH",
            "smiley-emotion",
            "face-hand",
            "🤭",
        ),
        EmojiItem(
            "FACE WITH FINGER COVERING CLOSED LIPS",
            "smiley-emotion",
            "face-hand",
            "🤫",
        ),
        EmojiItem("HUGGING FACE", "smiley-emotion", "face-hand", "🤗"),
        EmojiItem("THINKING FACE", "smiley-emotion", "face-hand", "🤔"),
        EmojiItem("DISGUISED FACE", "smiley-emotion", "face-hat", "🥸"),
        EmojiItem(
            "FACE WITH PARTY HORN AND PARTY HAT",
            "smiley-emotion",
            "face-hat",
            "🥳",
        ),
        EmojiItem("FACE WITH COWBOY HAT", "smiley-emotion", "face-hat", "🤠"),
        EmojiItem(
            "SKULL AND CROSSBONES", "smiley-emotion", "face-negative", "☠"
        ),
        EmojiItem(
            "SERIOUS FACE WITH SYMBOLS COVERING MOUTH",
            "smiley-emotion",
            "face-negative",
            "🤬",
        ),
        EmojiItem(
            "FACE WITH LOOK OF TRIUMPH", "smiley-emotion", "face-negative", "😤"
        ),
        EmojiItem("POUTING FACE", "smiley-emotion", "face-negative", "😡"),
        EmojiItem("ANGRY FACE", "smiley-emotion", "face-negative", "😠"),
        EmojiItem(
            "SMILING FACE WITH HORNS", "smiley-emotion", "face-negative", "😈"
        ),
        EmojiItem("SKULL", "smiley-emotion", "face-negative", "💀"),
        EmojiItem("IMP", "smiley-emotion", "face-negative", "👿"),
        EmojiItem(
            "FACE WITH ONE EYEBROW RAISED",
            "smiley-emotion",
            "face-neutral-skeptical",
            "🤨",
        ),
        EmojiItem(
            "LYING FACE", "smiley-emotion", "face-neutral-skeptical", "🤥"
        ),
        EmojiItem(
            "ZIPPER-MOUTH FACE",
            "smiley-emotion",
            "face-neutral-skeptical",
            "🤐",
        ),
        EmojiItem(
            "FACE WITH ROLLING EYES",
            "smiley-emotion",
            "face-neutral-skeptical",
            "🙄",
        ),
        EmojiItem(
            "FACE WITHOUT MOUTH",
            "smiley-emotion",
            "face-neutral-skeptical",
            "😶",
        ),
        EmojiItem(
            "GRIMACING FACE", "smiley-emotion", "face-neutral-skeptical", "😬"
        ),
        EmojiItem(
            "UNAMUSED FACE", "smiley-emotion", "face-neutral-skeptical", "😒"
        ),
        EmojiItem(
            "EXPRESSIONLESS FACE",
            "smiley-emotion",
            "face-neutral-skeptical",
            "😑",
        ),
        EmojiItem(
            "NEUTRAL FACE", "smiley-emotion", "face-neutral-skeptical", "😐"
        ),
        EmojiItem(
            "SMIRKING FACE", "smiley-emotion", "face-neutral-skeptical", "😏"
        ),
        EmojiItem("DROOLING FACE", "smiley-emotion", "face-sleepy", "🤤"),
        EmojiItem("SLEEPING FACE", "smiley-emotion", "face-sleepy", "😴"),
        EmojiItem("SLEEPY FACE", "smiley-emotion", "face-sleepy", "😪"),
        EmojiItem("PENSIVE FACE", "smiley-emotion", "face-sleepy", "😔"),
        EmojiItem("RELIEVED FACE", "smiley-emotion", "face-sleepy", "😌"),
        EmojiItem(
            "ROLLING ON THE FLOOR LAUGHING",
            "smiley-emotion",
            "face-smiling",
            "🤣",
        ),
        EmojiItem("UPSIDE-DOWN FACE", "smiley-emotion", "face-smiling", "🙃"),
        EmojiItem(
            "SLIGHTLY SMILING FACE", "smiley-emotion", "face-smiling", "🙂"
        ),
        EmojiItem(
            "SMILING FACE WITH SMILING EYES",
            "smiley-emotion",
            "face-smiling",
            "😊",
        ),
        EmojiItem("WINKING FACE", "smiley-emotion", "face-smiling", "😉"),
        EmojiItem(
            "SMILING FACE WITH HALO", "smiley-emotion", "face-smiling", "😇"
        ),
        EmojiItem(
            "SMILING FACE WITH OPEN MOUTH AND TIGHTLY-CLOSED EYES",
            "smiley-emotion",
            "face-smiling",
            "😆",
        ),
        EmojiItem(
            "SMILING FACE WITH OPEN MOUTH AND COLD SWEAT",
            "smiley-emotion",
            "face-smiling",
            "😅",
        ),
        EmojiItem(
            "SMILING FACE WITH OPEN MOUTH AND SMILING EYES",
            "smiley-emotion",
            "face-smiling",
            "😄",
        ),
        EmojiItem(
            "SMILING FACE WITH OPEN MOUTH",
            "smiley-emotion",
            "face-smiling",
            "😃",
        ),
        EmojiItem(
            "FACE WITH TEARS OF JOY", "smiley-emotion", "face-smiling", "😂"
        ),
        EmojiItem(
            "GRINNING FACE WITH SMILING EYES",
            "smiley-emotion",
            "face-smiling",
            "😁",
        ),
        EmojiItem("GRINNING FACE", "smiley-emotion", "face-smiling", "😀"),
        EmojiItem(
            "GRINNING FACE WITH ONE LARGE AND ONE SMALL EYE",
            "smiley-emotion",
            "face-tongue",
            "🤪",
        ),
        EmojiItem("MONEY-MOUTH FACE", "smiley-emotion", "face-tongue", "🤑"),
        EmojiItem(
            "FACE WITH STUCK-OUT TONGUE AND TIGHTLY-CLOSED EYES",
            "smiley-emotion",
            "face-tongue",
            "😝",
        ),
        EmojiItem(
            "FACE WITH STUCK-OUT TONGUE AND WINKING EYE",
            "smiley-emotion",
            "face-tongue",
            "😜",
        ),
        EmojiItem(
            "FACE WITH STUCK-OUT TONGUE", "smiley-emotion", "face-tongue", "😛"
        ),
        EmojiItem(
            "FACE SAVOURING DELICIOUS FOOD",
            "smiley-emotion",
            "face-tongue",
            "😋",
        ),
        EmojiItem("FREEZING FACE", "smiley-emotion", "face-unwell", "🥶"),
        EmojiItem("OVERHEATED FACE", "smiley-emotion", "face-unwell", "🥵"),
        EmojiItem(
            "FACE WITH UNEVEN EYES AND WAVY MOUTH",
            "smiley-emotion",
            "face-unwell",
            "🥴",
        ),
        EmojiItem(
            "SHOCKED FACE WITH EXPLODING HEAD",
            "smiley-emotion",
            "face-unwell",
            "🤯",
        ),
        EmojiItem(
            "FACE WITH OPEN MOUTH VOMITING",
            "smiley-emotion",
            "face-unwell",
            "🤮",
        ),
        EmojiItem("SNEEZING FACE", "smiley-emotion", "face-unwell", "🤧"),
        EmojiItem("NAUSEATED FACE", "smiley-emotion", "face-unwell", "🤢"),
        EmojiItem(
            "FACE WITH HEAD-BANDAGE", "smiley-emotion", "face-unwell", "🤕"
        ),
        EmojiItem(
            "FACE WITH THERMOMETER", "smiley-emotion", "face-unwell", "🤒"
        ),
        EmojiItem(
            "FACE WITH MEDICAL MASK", "smiley-emotion", "face-unwell", "😷"
        ),
        EmojiItem("DIZZY FACE", "smiley-emotion", "face-unwell", "😵"),
        EmojiItem(
            "SPEAK-NO-EVIL MONKEY", "smiley-emotion", "monkey-face", "🙊"
        ),
        EmojiItem("HEAR-NO-EVIL MONKEY", "smiley-emotion", "monkey-face", "🙉"),
        EmojiItem("SEE-NO-EVIL MONKEY", "smiley-emotion", "monkey-face", "🙈"),
    ]

    @staticmethod
    def categories():
        """Get a set of categories.

        Returns:

            set:
                Emoji categories.

        Examples:

            ```python
            >>> Emoji.categories()
            {'component', 'animal-nature', 'objects', 'symbols', 'flags',
             'people-body', 'smiley-emotion', 'activities', 'food-drink',
             'travel-places'}
            ```
        """
        cat = set()
        for e in Emoji._ITEMS:
            cat.add(e.category)
        return cat

    @staticmethod
    def subcategories(category: str = None):
        """Get a set of all subcategories or for a specific category.

        Parameters:

            category (str):
                The name of the category to query.

        Returns:

            set:
                All subcategories or categories for a specific category.

        Examples:

            ```python
            >>> Emoji.subcategories('activities')
            {'award-medal', 'arts & crafts', 'event', 'game', 'sport'}
            ```
        """
        subcat = set()
        for e in Emoji._ITEMS:
            if not category:
                subcat.add(e.subcategory)
            else:
                if e.category == category:
                    subcat.add(e.subcategory)
        return subcat

    @staticmethod
    def get(name: str):
        """Lookup an emoji by name.

        Parameters:

            name (str):
                The name of the emoji to lookup.

        Returns:

            Union[EmojiItem, None]:
                The selected emoji or None if not found.

        Examples:

            ```python
            >>> Emoji.get('winking face')
            😉

            >>> face = Emoji.get('winking face')
            >>> face.name
            WINKING FACE

            >>> face.category
            smiley-emotion

            >>> face.subcategory
            face.smiling

            >>> face.char
            😉
            ```
        """
        for e in Emoji._ITEMS:
            if e.name.lower() == name.lower():
                return e


if __name__ == "__main__":
    print(Emoji.get("winking face"))
    print(Emoji.categories())
    print(Emoji.subcategories())
