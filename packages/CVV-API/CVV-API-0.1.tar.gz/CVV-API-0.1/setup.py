from setuptools import setup, find_packages

with open("README.md", 'r') as f:
    long_desc = f.read()

setup(
    name="CVV-API",
    version="0.1",
    author="Fabrizio Gasparini",
    author_email="gasparini.fabrizio@einaudicorreggio.it",
    description="ClasseViva-API è una libreria Python che permette di utlizzare l'API di Classeviva - GruppoSpaggiariParma per ottenere informazioni come Voti, Note e Documenti, relative ad un account ClasseViva.",
    long_description=long_desc,
    long_description_content_type="text/markdown",
    url="https://github.com/MakerFaffa/ClasseVivaAPI",
    packages=find_packages(),
    keywords=[
        "classeviva",
        "api",
        "ClasseViva-API"
    ],
    install_requires=["requests"],
    python_requires=">=3.10",
    classifiers=[
        "Programming Language :: Python :: 3"
    ]
)