# data-repeatability-in-web-science
This repository contains code that is associated with our journal paper *Measuring and Facilitating Data Repeatability in Web Science*.
[preprint](https://hpi.de/fileadmin/user_upload/fachgebiete/naumann/publications/2019/risch2019measuring.pdf), [final publication](https://link.springer.com/article/10.1007/s13222-019-00316-9)

Requirements:
- python3.6
- pip3

Usage:
1. Run ./setup.sh to create a pipenv virtual enviroment. If there is an error in line "pipenv install --three --venv" you might try to replace "--three" with the path to your python installation ("which python")
2. Run "python -m crawler.main comments -o ./comments.csv -i ./articles.csv" to scrape comments from all articles listed in the provided "articles.csv"
3. Run "python -m crawler.main fingerprints -i ./comments.csv -o ./fingerprints.csv" to calculate fingerprints for the scraped sequences of comments.

If you use our data or code, please cite our journal paper as follows: 
```
@Article{Risch2019,
author="Risch, Julian and Krestel, Ralf",
title="Measuring and Facilitating Data Repeatability in Web Science",
journal="Datenbank-Spektrum",
year="2019",
month="Jul",
day="01",
volume="19",
number="2",
pages="117--126",
issn="1610-1995",
doi="10.1007/s13222-019-00316-9",
url="https://doi.org/10.1007/s13222-019-00316-9"
}
```
