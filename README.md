<p align="start">
  <a href="#"><img alt="" src="https://img.shields.io/badge/Release%20Date-Jan.%2031%2C%202023-aqua" /></a>
  <a href=""><img alt="" src="" /></a>
  <a href=""><img alt="" src="" /></a>
</p>


# Python Selenium - all-senmonka.jp

The purpose of this project is to create a list of contact email addresses of the offices listed on [https://all-senmonka.jp/](https://all-senmonka.jp/)

## Description

The script first scrapes [https://all-senmonka.jp/](https://all-senmonka.jp/) for a list of all office names. Then, for each office it will search google with the office name as the query, open the first result page, search each page for email addresses and saves it as a csv file.

## Getting Started

### Prerequisites

Python enviroment with the following dependencies installed.

### Dependencies

-   Selenium
-   ChromeDriver
-   Pandas
-   Requests
-   BeautifulSoup

## Usage

-   run `main.py`

```
python3 main.py
```

## Authors

Masa Yamanaka - [yamanaka@lcom-group.jp](yamanaka@lcom-group.jp)

## Version History

-   1.0
    -   Initial Release

## License


## References
