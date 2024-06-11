from distutils.core import setup
setup(
   name='fhircraft',
   version='0.1',
   license='MIT',
   long_description=open('README.md').read(),
   entry_points = {
      'console_scripts': ['fhircraft=fhircraft.command_line:app'],
   },
)
