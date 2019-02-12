# data-repeatability-in-web-science

Requirements:
- python3.6
- pip3

Usage:
1. Run ./setup.sh to create a pipenv virtual enviroment. If there is an error in line "pipenv install --three --venv" you might try to replace "--three" with the path to your python installation ("which python")
2. Run "python -m crawler.main comments -o ./comments.csv -i ./articles.csv" to scrape comments from all articles listed in the provided "articles.csv"
3. Run "python -m crawler.main fingerprints -i ./comments.csv -o ./fingerprints.csv" to calculate fingerprints for the scraped sequences of comments.