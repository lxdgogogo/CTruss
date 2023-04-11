from distutils.core import setup
from distutils.extension import Extension
from shutil import copyfile
from Cython.Build import cythonize
print('test')
if __name__ == '__main__':
    # files to be included in the extensions
    print('test')
    paths = [
        '../test/test_cython',
        # '../DTruss/DTruss',
        # '../experiment/experiment',
        # '../experiment/bottom_up_experiment',
        # '../methods/bottom_up',
        # '../methods/d_truss_baseline',
        # '../methods/top_down',
        # '../Tools/tools',
        # '../Tools/memory_measure',
        # '../MLGraph/multilayer_graph',
    ]

    # if Cython is available
    # set the .pyx extension
    ext = '.pyx'
    # create the new .pyx files
    for path in paths:
        print(path + '.py', path + ext)
        copyfile(path + '.py', path + ext)
    # build the extensions list
    extensions = [Extension(path.replace('/', '.'), [path + ext]) for path in paths]

    extensions = cythonize(extensions, compiler_directives={'language_level': 3})

    # run the setup
    setup(
         ext_modules=extensions
    )
