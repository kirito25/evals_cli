
# Evaluation report generator
This repo provides the tools needed to generate an evaluation report from
a giving filled out evaluation sheet.

### How to use
$ python evaluation.py -h
usage: evaluations.py [-h] [--dest DEST] project_name eval_scan instructor course term

positional arguments:
  project_name  Name of the project
  eval_scan     Path to scanned pdf
  instructor    Name of instructor
  course        Couse name
  term          The eval term

optional arguments:
  -h, --help    show this help message and exit
  --dest DEST   Directory to create project in (default is '.')

### Python Dependencies (available on pip)
- numpy
- shutil
- cv2
- pdf2image 
- pylab
- subprocess
- imutils 

