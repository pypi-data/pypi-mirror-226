from setuptools import setup
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='whatsapp_onprem',
    version='0.0.1',
    description='WhatsAppPrem is a powerful Python module that empowers you to seamlessly integrate WhatsApp messaging within your on-premises environment.',
    author= 'Shlok Sawant',
    url = 'https://github.com/Shlok221B/whatsapp-onprem',
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    keywords=['whatsapp', 'whatsapp on premises', 'whatsapp business api'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    py_modules=['PyMusic_Player'],
    package_dir={'':'src'},
    install_requires = [
        'requests',
        'pybase64'
    ]
)