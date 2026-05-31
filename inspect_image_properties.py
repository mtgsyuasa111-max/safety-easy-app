import openpyxl

excel_path = r"C:\Users\db2b2\Downloads\Safety Patrol By Sakon.1.xlsx"
wb = openpyxl.load_workbook(excel_path)
ws = wb['FirePump']
img = ws._images[0]
print("Image class:", img.__class__.__name__)
print("Attributes of image:", dir(img))
if hasattr(img, 'ref'):
    print("img.ref type:", type(img.ref))
    # Is img.ref a BytesIO or PIL image?
    try:
        from PIL import Image as PILImage
        # In some openpyxl versions, img.ref is a PIL image or we can use open(img.ref)
        print("img.ref is PIL Image?", isinstance(img.ref, PILImage.Image))
    except Exception as e:
        print("Error checking img.ref:", e)
