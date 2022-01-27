import tkinter as tk
import ttkbootstrap as ttk

root = tk.Tk()
style = ttk.Style()
colors = style.theme.colors

# setup meter
m = ttk.Meter(
    master=root,
    metersize=180,
    amountused=25,
    padding=20,
    metertype='semi',
    subtext='miles per hour',
    interactive=True
)
m.pack()

# test meter configuration

m.configure(subtext='residual')
assert m.subtext.cget('text') == 'residual'

m.configure(arcrange=180)
assert m._arcrange == 180
assert m.configure('arcrange') == 180

m.configure(arcoffset=10)
assert m._arcoffset == 10
assert m.configure('arcoffset') == 10

m.configure(amounttotal=200)
assert m.amounttotalvar.get() == 200
assert m['amounttotal'] == 200
assert m.configure('amounttotal') == 200

m['amountused'] = 50
assert m['amountused'] == 50
assert m.configure('amountused') == 50
assert m.amountusedvar.get() == 50

m['interactive'] = False
assert m['interactive'] == False
assert m.configure('interactive') == False

m.configure(subtextfont='ariel 8 bold')
assert m.configure('subtextfont') == 'ariel 8 bold'
assert m['subtextfont'] == 'ariel 8 bold'

m['subtextstyle'] = 'danger'
assert m['subtextstyle'] == 'danger'
assert m.configure('subtextstyle') == 'danger'

m.configure(subtext='Water Pressure')
assert m['subtext'] == 'Water Pressure'
assert m.configure('subtext')

m['bootstyle'] = 'info'
assert m['bootstyle'] == 'info'
assert m.configure('bootstyle') == 'info'

m.configure(metertype='full')
assert m.configure('metertype') == 'full'
assert m['metertype'] == 'full'

m['meterthickness'] = 5
assert m.configure('meterthickness') == 5
assert m['meterthickness'] == 5

m.configure(stripethickness=5)
assert m.configure('stripethickness') == 5
assert m['stripethickness'] == 5

m.configure(textright='>>')
assert m['textright'] == '>>'

m.configure(textleft="<<")
assert m.configure('textleft') == "<<"
assert m['textleft'] == '<<'

m['showtext'] = False
assert m.configure('showtext') == False
assert m['showtext'] == False

m['wedgesize'] = 15
assert m.configure('wedgesize') == 15
assert m['wedgesize'] == 15
