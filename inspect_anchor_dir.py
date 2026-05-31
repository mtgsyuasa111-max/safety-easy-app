import openpyxl

excel_path = r"C:\Users\db2b2\Downloads\Safety Patrol By Sakon.1.xlsx"
wb = openpyxl.load_workbook(excel_path, data_only=True)
ws = wb['FirePump']
img = ws._images[0]
anchor = img.anchor
print("Anchor class:", anchor.__class__.__name__)
print("Attributes of anchor:", dir(anchor))
if hasattr(anchor, '_from'):
    print("_from class:", anchor._from.__class__.__name__)
    print("_from attrs:", dir(anchor._from))
    print("Col:", anchor._from.col)
    print("Row:", anchor._from.row)
if hasattr(anchor, 'from_'):
    print("from_ class:", anchor.from_.__class__.__name__)
    print("from_ attrs:", dir(anchor.from_))
