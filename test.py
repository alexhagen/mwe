import mwe

test = mwe.mwe('Hi! \lipsum[2-5]', preamble="\usepackage{lipsum}\n")
test.export()
