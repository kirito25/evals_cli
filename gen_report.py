import numpy, os, pylab, subprocess, sys

def generate_latex(instructor, course, term, histograms, longforms):
    """
    Args:
        instructor  -- str
        course      -- str
        term        -- str
        histograms  -- list of str of path to images or pdf
        longforms   -- dictionary where the key is a number and the value is a list
                        of string of paths
    """
    latexstr = """\documentclass[a4paper]{article}

\\usepackage{fancyhdr}
\\usepackage{framed}
\\usepackage[top=1in, bottom=1in, left=0.5in, right=0.5in]{geometry}
\\usepackage[many]{tcolorbox}
\\usepackage{lastpage}
\\usepackage{tabularx}
\\usepackage[hidelinks]{hyperref}

\\newcommand{\TL}[1]{\def \TL {#1}}
\\newcommand{\TM}[1]{\def \TM {#1}}
\\newcommand{\TR}[1]{\def \TR {#1}}
\\newcommand{\BL}[1]{\def \BL {#1}}
\\newcommand{\BM}[1]{\def \BM {#1}}

\pagestyle{fancy}
\lhead{\\textbf{\TL}}
\chead{\\textbf{\TM}}
\\rhead{\\textbf{\TR}}
\lfoot{\\textbf{\BL}}
\cfoot{\\textbf{\BM}}
\\rfoot{\\textbf{\\thepage\ of \pageref{LastPage}}}
\\renewcommand{\headrulewidth}{0.4pt}
\\renewcommand{\\footrulewidth}{0.4pt}

\\newcommand*\circled[1]{\\tikz[baseline=(char.base)]{
            \\node[shape=circle,draw,inner sep=2pt] (char) {#1};}}
           
\\newcommand{\solbox}[1]{
\\begin{tcolorbox}[height={#1},colback=white,sharp corners]
\end{tcolorbox}
}

\TM{Computer Science Department Course Evaluation Report \\\\ University of Massachusetts at Boston \\\\ %s $\\bullet$ %s}
\BL{%s}

\\begin{document}

\\text{ }

\\tableofcontents

\section{Multiple-choice Responses}

\subsection{From this course I learned}

\\begin{center}
\includegraphics[width=\\textwidth]{%s}
\end{center}

\\newpage

\subsection{The pace was}

\\begin{center}
\includegraphics[width=\\textwidth]{%s}
\end{center}

\\newpage

\subsection{The text(s) was (were)}

\\begin{center}
\includegraphics[width=\\textwidth]{%s}
\end{center}

\\newpage

\subsection{The prerequisites were}

\\begin{center}
\includegraphics[width=\\textwidth]{%s}
\end{center}

\\newpage

\subsection{The homework/projects helped me understand the course materials}

\\begin{center}
\includegraphics[width=\\textwidth]{%s}
\end{center}

\\newpage

\subsection{The homework/projects were}

\\begin{center}
\includegraphics[width=\\textwidth]{%s}
\end{center}

\\newpage

\subsection{Grading and comments on homework/projects were useful and timely}

\\begin{center}
\includegraphics[width=\\textwidth]{%s}
\end{center}

\\newpage

\\newpage

\subsection{Exams accurately reflected the lectures and homework/projects}

\\begin{center}
\includegraphics[width=\\textwidth]{%s}
\end{center}

\\newpage

\subsection{Exams were}

\\begin{center}
\includegraphics[width=\\textwidth]{%s}
\end{center}

\\newpage

\subsection{Grading and comments on exams were useful and timely}

\\begin{center}
\includegraphics[width=\\textwidth]{%s}
\end{center}

\\newpage

\subsection{The instructor's presentation in class was}

\\begin{center}
\includegraphics[width=\\textwidth]{%s}
\end{center}

\\newpage

\subsection{Students felt free to ask questions and express ideas}

\\begin{center}
\includegraphics[width=\\textwidth]{%s}
\end{center}

\\newpage

\subsection{The instructor's response to questions was}

\\begin{center}
\includegraphics[width=\\textwidth]{%s}
\end{center}

\\newpage

\subsection{The instructor's availability for help outside class was}

\\begin{center}
\includegraphics[width=\\textwidth]{%s}
\end{center}

\\newpage

\subsection{Taking everything into account, the instructor was}

\\begin{center}
\includegraphics[width=\\textwidth]{%s}
\end{center}

\\newpage

\subsection{Taking everything into account, the course was}

\\begin{center}
\includegraphics[width=\\textwidth]{%s}
\end{center}

\\newpage

\section{Free-form Responses}

\subsection{Any particular strong points of the instructor?}

%%s

\\newpage

\subsection{Any particular weak points of the instructor?}

%%s

\\newpage

\subsection{What are the strong points of this course?}

%%s

\\newpage

\subsection{Are there any changes you wish to recommend in the course?}

%%s

\\newpage

\subsection{Other comments?}

%%s

\\newpage

\end{document} """ % tuple ([instructor, course, term] + histograms)
    template = "\n\\begin{center} \n\includegraphics[width=\\textwidth]{%s} \n\end{center}\n"
    list_of_strings = {}
    for key, value in longforms.items():
        tmp = ""
        for path in value:
            tmp += template % (path)
        list_of_strings[key] = tmp
    latexstr = latexstr % (list_of_strings[0], list_of_strings[1], list_of_strings[2], list_of_strings[3], list_of_strings[4])
    return latexstr
    
if __name__ == '__main__':
    histograms = [i for i in range(16)]
    forms = {}
    for i in range(5):
        forms[i] = ["fewr", "fwer"]
    print generate_latex("fvrefger", "fdsf", "fwedr", histograms, forms)
