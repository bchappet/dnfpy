dnfpy
=====

dnfpy will be a python library for manipulation and visualization of Dynamic Neural Fields (http://www.scholarpedia.org/article/Neural_fields)

This is mainly a tool for my PhD
It is more than unstable for now


DEPENDENCIES:
    numpy
    PyQt4
    opencv
    line_profiler
    qimage2ndarray (thanks to http://kogs-www.informatik.uni-hamburg.de/~meine/software/qimage2ndarray/doc/#converting-ndarrays-into-qimages)

INSTALLATION:
    For now you have to source install_tmp.sh which will add the dnfpy module to your PYTHONPATH.

EXECUTION:
    cd src
    kernprof -l -v main.py ModelDNF context/params.dnfs 100



