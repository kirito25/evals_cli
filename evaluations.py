import sys
import argparse
import os
import pprint
import shutil
import process_pdf
import analyze
import plots
import numpy
import network2
import gen_report
import subprocess
import header

def run(command):
    process = subprocess.Popen(command,
            stdin  = None, 
            stdout = subprocess.PIPE,
            stderr = subprocess.STDOUT)
    output = process.stdout.read()
    return output

def make_dir(path):
    path = shutil.abspath(path)
    if os.path.exists(path):
        pprint.pprint("Path \"%s\" already exist\n EXITING" % (path))
        sys.exit(-1)
    os.mkdir(path)

def make_project(dest, project_name, scan_path):
   dest = shutil.abspath(dest)
   scan_path = shutil.abspath(scan_path)
   project_path = dest + "/" + project_name
   make_dir(project_path)
   shutil.copy(scan_path, project_path)
   scan_path = project_path + "/" + os.path.basename(scan_path)
   process_pdf.convert_pdf_to_image(scan_path)
   return project_path

def process_project(project_path, net):
    project_path = shutil.abspath(project_path)
    make_dir(project_path + "/analyzed_bubbles")
    make_dir(project_path + "/analyzed_longforms")
    longforms = analyze.longforms(project_path + "/long_forms", project_path + "/analyzed_longforms")
    matrix = analyze.bubbles(project_path + "/bubbles/", net, \
                            align=True, \
                            debug_path=project_path + "/analyzed_bubbles")
    histograms = []
    for i, row in enumerate(matrix):
        histograms.append(plots.histogram(numpy.asarray(row).reshape(-1), i + 1, project_path))
    return (histograms, longforms)

def create_report(project_path, instructor, course, term, histogram, forms):
    latexstr = gen_report.generate_latex(args.instructor, args.course, args.term, histogram, forms)
    current_path = os.getcwd()
    os.chdir(project_path)
    outfile = open("report.tex", 'w')
    outfile.write(latexstr)
    outfile.close()
    run(["pdflatex", "report.tex"])
    run(["pdflatex", "report.tex"])
    os.chdir(current_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("project_name", help="Name of the project")
    parser.add_argument("eval_scan", help="Path to scanned pdf")
    parser.add_argument("instructor", help="Name of instructor")
    parser.add_argument("course", help="Course name")
    parser.add_argument("term", help="The eval term")
    parser.add_argument("--dest", help="Directory to create project in (default is \'.\')", default=".")
    args = parser.parse_args()
    path = make_project(args.dest, args.project_name, args.eval_scan)
    net = network2.load(header.network)
    histogram, forms = process_project(path, net)
    create_report(path, args.instructor, args.course, args.term, histogram, forms)
    print "Report is located at %s/report.pdf" % (path)




