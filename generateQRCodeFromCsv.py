import csv
import qrcode
from PIL import Image, ImageFont, ImageDraw, ImageOps

# SOURCE: https://stackoverflow.com/questions/8868564/draw-underline-text-with-pil
def draw_underlined_text(draw, pos, text, font, **options):    
    twidth, theight = draw.textsize(text, font=font)
    lx, ly = pos[0], pos[1] + theight
    draw.text(pos, text, font=font, **options)
    draw.line((lx, ly+3, lx + twidth, ly+3), **options, width=3)
    return draw.textsize(text, font=font)

with open('userdata.csv', newline='') as userdata:
    parsed_userdata = csv.DictReader(userdata)
    for row in parsed_userdata:
        # format data for qr code generation
        # BARCODE NUMBER
        BARCODE = row['BARCODE']
        NAME = row['FIRST NAME'] + " " + row['MIDDLE INITIAL'] + " "  + row['SURNAME']
        ROLE = row['ROLE']
        print("GENERATING QR CODE IMAGE FOR " + NAME + " - " + ROLE)

        # CREATES QR CODE
        qr = qrcode.QRCode(
            version=None,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=0,
        )
        qr.add_data(BARCODE + '\n' + NAME)
        qr.make(fit=True)

        # generates the qr code image
        qr_code_img = qr.make_image(fill_color="black", back_color="white")
        
        # sets up the padding size
        qr_code_img_newsize = (qr_code_img.size[0], qr_code_img.size[1]+40)
        
        # create the padding image
        padding = Image.new("RGB", qr_code_img_newsize, (255,255,255))

        padding.paste(qr_code_img)

        draw = ImageDraw.Draw(padding)
        FONT = ImageFont.truetype('C:\Windows\Fonts\Calibrib.ttf', 24)
        FONT2 = ImageFont.truetype('C:\Windows\Fonts\Calibrib.ttf', 16)

        text_size = draw_underlined_text(draw, (0,qr_code_img.size[1]), ROLE, FONT, fill=0)

        print(text_size[1]+qr_code_img.size[1])

        draw.text((0,text_size[1]+qr_code_img.size[1]+5), NAME, font=FONT2, fill=(0,0,0))

        padding.save(".\\generated_qr_codes\\" + NAME + ' - ' + BARCODE + '.png')
        








