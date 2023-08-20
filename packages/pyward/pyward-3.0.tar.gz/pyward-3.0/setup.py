from setuptools import setup, find_packages

setup(
    name='pyward',                     # Replace with your package name
    version='3.0',                     # Update the version number
    description='Stabilizes Code and Makes It Secure',  # Add a description
    author='Rachel Anthony',           # Replace with the author's name
    author_email='dev@pyward.com',     # Replace with the author's email
    url='https://github.com/pyward/pyward',  # Replace with the project URL
    packages=find_packages(),          # Automatically find and include all packages
    package_data={'': ['*.py']},       # Include all Python files
    scripts=['pyward/__init__.py'],    # Specify the path to the init.py file
    install_requires=[
        'requests',                    # Add your dependencies here
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
