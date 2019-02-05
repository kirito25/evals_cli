import matplotlib
matplotlib.use('Agg')
import numpy, pylab

def histogram(scores, question, path):
    """
    Given the raw scores (frequencies) on a 5-point scale as a numpy array 
    and the question number xxx (1-16), generates a histogram Qxxx.png.
    """
    
    colors1 = ('#CCFF00', '#AAD400', '#88AA00',  '#668000', '#445500')
    colors2 = ('#CCFF00', '#AAD400', '#445500',  '#AAD400', '#CCFF00')
    choices = {1 : (('very little', 'something', 'enough', 'a good amount',
                     'a great deal'), colors1), 
               2 : (('very slow', 'slow', 'about right', 'fast',
                     'very fast'), colors2), 
               3 : (('poor', 'below average', 'average', 'good',
                     'excellent'), colors1), 
               4 : (('much too weak', 'weak', 'about right', 'too strong',
                     'much too strong'), colors2), 
               5 : (('very little', 'a little', 'somewhat', 'quite a bit',
                     'a great deal'), colors1), 
               6 : (('much too easy', 'easy', 'about right', 'hard',
                     'much too hard'), colors2), 
               7 : (('strong disagree', 'disagree', 'partially agree',
                     'agree', 'strongly agree'), colors1), 
               8 : (('strong disagree', 'disagree', 'partially agree',
                     'agree', 'strongly agree'), colors1), 
               9 : (('much too easy', 'easy', 'about right', 'hard',
                     'much too hard'), colors2), 
               10 : (('strong disagree', 'disagree', 'partially agree',
                      'agree', 'strongly agree'), colors1), 
               11 : (('poor', 'unclear', 'clear', 'very clear',
                      'extremely clear'), colors1), 
               12 : (('strong disagree', 'disagree', 'partially agree',
                      'agree', 'strongly agree'), colors1), 
               13 : (('poor', 'below average', 'average', 'good',
                      'excellent'), colors1), 
               14 : (('poor', 'below average', 'average', 'good',
                     'excellent'), colors1), 
               15 : (('poor', 'below average', 'average', 'good',
                      'excellent'), colors1), 
               16 : (('poor', 'below average', 'average', 'good',
                      'excellent'), colors1)
    }
    N = float(numpy.sum(scores))
    weights = numpy.array([1, 2, 3, 4, 5])
    probs = scores / N
    mean = numpy.sum(probs * weights)
    probs = scores / (N - 1)
    stddev = numpy.sum(probs * (weights - mean) ** 2) ** 0.5
    pylab.figure(1, figsize = (8, 6), dpi = 500)
    xticks = choices[question][0]
    colors = choices[question][1]
    bar = pylab.bar(numpy.arange(1, 6), scores, color = colors, alpha = 0.8)
    pylab.xticks(numpy.arange(1, 6), xticks)
    pylab.xlabel('choice')
    pylab.ylabel('frequency')
    for rect in bar:
        height = rect.get_height()
        pylab.text(rect.get_x() + rect.get_width() / 2.0, height,
                   '%d' % int(height), ha = 'center', va = 'bottom')
    
    props = dict(boxstyle='round', facecolor='white', alpha=0.5)
    pylab.text(0.5, numpy.max(scores), r'$\mu=%.3f, \sigma=%.3f, N = %d$' % (mean, stddev, N), verticalalignment='top', bbox=props)
    pylab.savefig("%s/q%02d.png" % (path, question), format = 'png', bbox_inches = 'tight')
    pylab.clf()
    return "%s/q%02d.png" % (path, question)


