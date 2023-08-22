from setuptools import setup, find_packages

setup(
    name='EqFlow',
    version='0.0.1',
    description='Introducing EqFlow: Your all-in-one solution for efficient web scraping, AI development, and more. Streamline your projects with its intuitive API, eliminating the need for multiple libraries like requests and bs4. EqFlow\'s lightning-fast performance and simplified syntax redefine coding, making tasks that once required extensive code a breeze. Elevate your coding experience, embrace efficiency, and unlock your true creative potential with EqFlow.',
    author='Stutya Patwal',
    author_email='stutyapatwal@gmail.com',
    packages=find_packages(),
    install_requires=[
        'requests',
        'bs4',
        'nltk',
        'scikit-learn',
        'numpy',
        'pandas',
        'textblob',
    ],
    package_data={
        'eqflow': ['usage.py', 'Eqai.py', 'Eqre.py'],
    },
    classifiers=[
        'Development Status :: 3 - Alpha', 
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
)
