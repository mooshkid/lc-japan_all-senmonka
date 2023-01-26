# Python Selenium - all-senmonka.jp

The purpose of this project is to create a list of contact email addresses of the offices listed on [https://all-senmonka.jp/](https://all-senmonka.jp/)

## Description

The script first scrapes [https://all-senmonka.jp/](https://all-senmonka.jp/) for a list of all office names. Then, it will search google with the office name as the query and opens the first result page. Finally, it will search each page for email addresses and saves it as a csv file.

## Getting Started

### Prerequisites

Python enviroment with the following dependencies installed.

### Dependencies

-   Selenium
-   ChromeDriver
-   Pandas

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
