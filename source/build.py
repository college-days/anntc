from distutils.core import setup  
from distutils.extension import Extension  
from Cython.Distutils import build_ext  
  
ext_modules = [Extension("calcUtil", ["calcUtil.py"])]  

setup(  
  name = 'Hello world app',  
  cmdclass = {'build_ext': build_ext},  
  ext_modules = ext_modules  
)  

ext_modules = [Extension("tianchiann", ["tianchiann.py"])]
  
setup(  
  name = 'Hello world app',  
  cmdclass = {'build_ext': build_ext},  
  ext_modules = ext_modules  
)  
