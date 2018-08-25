from setuptools import setup

def readme():
    with open('README.md') as f:
        return f.read()

setup(name='pympw',
      version='0.2',
      description=' An implementation of the Master Password algorithm v3 with a nice CLI',
      url='http://github.com/roguh/pympw',
      author='Hugo Rivera',
      author_email='flyingcircus@example.com',
      long_description=readme(),
      classifiers=[
          'Topic :: Security',
          'Topic :: Security :: Cryptography',
          'Topic :: Utilities',
          'Environment :: Console',
          'Operating System :: Unix',
          'Operating System :: POSIX :: Linux',
          'Topic :: Internet',
      ],
      # TODO license=None,
      packages=['pympw'],
      install_requires=[
          'scrypt', 'pyperclip'
      ],
      scripts=['bin/pympw'],
      setup_requires=["pytest-runner"],
      tests_require=["pytest"],
      zip_safe=False)

