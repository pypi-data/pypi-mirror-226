from setuptools import setup, find_packages

with open(r'statmanager\README.md', encoding='utf-8') as f:
    description_markdown = f.read()

setup(
    name='statmanager-kr',
    version='1.1.0',
    license='MIT',
    long_description=description_markdown,
    long_description_content_type='text/markdown',
    description='python에서도 사회과학 통계를 손쉽게 진행해보자',
    author='ckdckd145',
    author_email='ckdckd145@gmail.com',
    url='https://cslee145.notion.site/statmanager-kr-Manual-c277749fe94b4e08a836236b409642b3?pvs=4',
    install_requires=['pandas', 'scipy', 'statsmodels', 'tabulate', 'matplotlib', 'seaborn'],
    packages=find_packages(),
    keywords=['statistic', 'socialscience', 'stats',],
    python_requires='>=3.6',
    package_data={},
    zip_safe=False,
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
)