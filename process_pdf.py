from pdf2image import convert_from_path
import os

def convert_pdf_to_image(path_to_file):
    pages = convert_from_path(path_to_file, 100)
    path = '/'.join(path_to_file.split('/')[:-1])
    os.mkdir(path + '/bubbles')
    os.mkdir(path + '/long_forms')
    for i, page in enumerate(pages):
        if i % 2 == 0:
            destination = "%s/bubbles/%05d.jpg" % (path, i)
            page.save(destination, 'JPEG')
        else:
            destination = "%s/long_forms/%05d.jpg" % (path, i)
            page.save(destination, 'JPEG')

if __name__ == '__main__':
    import sys
    convert_pdf_to_image(sys.argv[1])
