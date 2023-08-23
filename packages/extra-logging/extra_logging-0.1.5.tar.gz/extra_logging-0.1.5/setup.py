from setuptools import setup

setup(name='extra_logging',
      version='0.1.5',
      url="https://github.com/Kapysta38/extra_logging",
      author="Lev Mihalev",
      description='Library complementing the `logging` library for quick customization of logging in the project',
      long_description_content_type='text/markdown',
      long_description="""# Quick start

```python
import extra_logging as ex_log

log = ex_log.Logging('app', 'log.log', max_bytes=ex_log.kb * 10).get_log

for i in range(100):
    log.info(i)

```""",
      packages=['extra_logging'],
      license='MIT',
      author_email='vinnipyx38@gmail.com',
      zip_safe=False)
