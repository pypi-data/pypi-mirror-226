from setuptools import setup
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='whatsappez',
    version='0.0.1',
    description='Whatsappez is a powerful Python module that empowers you to seamlessly integrate WhatsApp messaging within your on-premises environment',
    author= 'Shlok Sawant',
    url = 'https://github.com/Shlok221B/whatsapp-onprem',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    keywords=['Whatsapp Business API', 'Whatsapp', 'Whatsapp on premises'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.10',
    py_modules=['whatsappez'],
    package_dir={'':'src'},
    install_requires = [
        'requests',
        'pybase64'
    ]
)