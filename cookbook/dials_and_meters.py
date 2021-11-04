"""
    Author: Israel Dryer
    Modified: 2021-05-09
"""

from ttkbootstrap import Style
from ttkbootstrap.widgets import Meter

style = Style('cosmo')
root = style.master
root.title('ttkbootstrap')

m1 = Meter(metersize=180, padding=20, amountused=25, metertype='semi', labeltext='miles per hour', interactive=True)
m1.grid(row=0, column=0)

m2 = Meter(metersize=180, padding=20, amountused=1800, amounttotal=2600, labeltext='storage used', textappend='gb',
           meterstyle='info.TMeter', stripethickness=10, interactive=True)
m2.grid(row=0, column=1)

m3 = Meter(metersize=180, padding=20, stripethickness=2, amountused=40, labeltext='project capacity', textappend='%',
           meterstyle='success.TMeter', interactive=True)
m3.grid(row=1, column=0)

m4 = Meter(metersize=180, padding=20, amounttotal=280, arcrange=180, arcoffset=-180, amountused=75, textappend='°',
           labeltext='heat temperature', wedgesize=5, meterstyle='danger.TMeter', interactive=True)
m4.grid(row=1, column=1)

root.mainloop()