import os
from camera import PolasciiCamera
from thermal import PolasciiPrinter
from console import PolasciiConsole
from export import PolasciiExport
from uploader import PolasciiUploader, contents_from_file
from PIL import Image
from datetime import datetime

console = PolasciiConsole()
camera = PolasciiCamera()
printer = PolasciiPrinter()
uploader = PolasciiUploader()

printer.contrast = console.contrast = 70

output_path = '../temp/szmakerfaire2014'
url_prefix = 'http://polascii.szdiy.org/gallery/szmakerfaire2014/'

def console_display(image):
    console.display_image(image)    

def template_print(image, url):
    if not printer.tp:
        print('printer not ready')
        #return
    printer.text('--------------------------------')
    printer.ascii_image(image)
    printer.newline()
    printer.newline()
    printer.align('C')
    printer.text('--- Project Polascii ---')
    printer.text('by terryoy, 2014')
    printer.newline()
    printer.qrcode(url)
    printer.newline()
    printer.align('L')
    printer.text('Welcome to join SZDIY!')
    printer.text('http://szdiy.org/')
    printer.text('--------------------------------')
    printer.cut()

def upload_file(fullpath):
    name = os.path.basename(fullpath)
    content = contents_from_file(fullpath)
    print 'uploading:', name, '...'

    code,reason,uri = uploader.upload_file(name, content)
    print code, reason, uploader.get_full_url(uri)

    return code, uploader.get_full_url(uri)

    
def save_image(image):
    filename = datetime.now().strftime('%Y%m%d%H%M%S')
    # save image to disk
    image.save(os.path.join(output_path, filename + '.jpg'))

    export_path = os.path.join(output_path, filename + '.html')
    export = PolasciiExport(image.convert('L').resize((400, 180)))
    export.export_nhtml(export_path, contrast=console.contrast, brightness=console.brightness)
    
    return export_path # return the export html name        

def main():
    global camera

    camera.open()
    image = camera.capture()
    while image:
        console_display(image)
        # template_print(image)
        image = camera.capture()
        
        key = console.get_key()
        if key == '\x20':
            fullpath = save_image(image)
            #template_print(image, url_prefix + os.path.basename(fullpath))
            # do we upload html here?
            code, url = upload_file(fullpath)
            if code == 200:
                template_print(image, url) # print url if network available
            else:
                print('image upload failed! cannot print ticket')

        elif key == '\x1b':
            break
        elif key == '=':
            if console.contrast < 127:
                console.contrast += 2
                printer.contrast = console.contrast
                print('contrast =', console.contrast)
        elif key == '-':
            if console.contrast > 0:
                console.contrast -= 2
                printer.contrast = console.contrast
                print('contrast =', console.contrast)
        elif key == '[':
            if console.brightness > 0:
                console.brightness -= 4
                printer.brightness = console.brightness
                print('brightness =', console.brightness)
        elif key == ']':
            if console.brightness < 255:
                console.brightness += 4
                printer.brightness = console.brightness
                print('brightness =', console.brightness)

if __name__ == '__main__':
    main()

