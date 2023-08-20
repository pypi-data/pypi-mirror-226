import os

try:
    from Cython.Build import cythonize
except ImportError:
    def build(setup_kwargs):
        pass

else:
        from setuptools import Extension
        from setuptools.dist import Distribution
        from distutils.command.build_ext import build_ext


        def build(setup_kwags):
            extensions = [
                 "alcheonengine/game_runner.py",
                 "alcheonengine/engine_core.py"
            ]

            os.environ['CFLAGS'] = '-O3'


            setup_kwags.update(
                {
                    'ext_modules': cythonize(
                        extensions,
                        language_level=3,
                        compiler_directives={'linetrace': True},
                    ),
                    'cmdclass': {'build_ext': build_ext}
                }
            )