from setuptools import setup, find_packages

with open(r'statmanager\README.md', encoding='utf-8') as f:
    description_markdown = f.read()

setup(
    name='statmanager-kr',
    version='1.0.1',
    long_description=description_markdown,
    long_description_content_type='text/markdown',
    description='사회과학의 맥락에서 통계를 손쉽게 사용할 수 있는 패키지 by Changseok Lee',
    author='ckdckd145',
    author_email='ckdckd145@gmail.com',
    url='',
    install_requires=['pandas', 'scipy', 'statsmodels', 'numpy', 'json'],
    packages=find_packages(),
    keywords=['statistic', 'socialscience', 'stats',],
    python_requires='>=3.6',
    package_data={},
    zip_safe=False,
    classifiers=[
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)