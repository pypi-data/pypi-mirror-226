# WatchPage

[![Travis CI Build Status](https://img.shields.io/travis/com/muflone/watchpage/master.svg)](https://www.travis-ci.com/github/muflone/watchpage)
[![CircleCI Build Status](https://img.shields.io/circleci/project/github/muflone/watchpage/master.svg)](https://circleci.com/gh/muflone/watchpage)
[![PyPI - Version](https://img.shields.io/pypi/v/WatchPage.svg)](https://pypi.org/project/WatchPage/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/WatchPage.svg)](https://pypi.org/project/WatchPage/)

**Description:** Watch webpages for changes

**Copyright:** 2022-2023 Fabio Castelli (Muflone) <muflone@muflone.com>

**License:** GPL-3+

**Source code:** https://github.com/muflone/watchpage

**Documentation:** http://www.muflone.com/watchpage/

# Description

WatchPage is a simple tool to watch multiple web pages for changes.

It aims to ease the software maintainers to check for changes to the project
sites and get any news based on patterns.

# System Requirements

* Python 3.x
* PyYAML 6.0 (https://pypi.org/project/PyYAML/)
* BeautifulSoup4 4.x (https://pypi.org/project/beautifulsoup4/)
* lxml 4.9 (https://pypi.org/project/lxml/)
* html5lib 1.1 (https://pypi.org/project/html5lib/)

# Usage

WatchPage is a command line utility and it requires some arguments to be passed:

`watchpage --config <CONFIGURATION> --results <RESULTS> [--dump] [--agent <USER AGENT>]`

The argument `--config` refers to a valid YAML configuration file
(see below for some examples).

The argument `--results` must be the path to a directory where to save the
results files.

The argument `--dump` will show the results but it will discard the changes, so
they will not be saved in the directory specified in the `--results` argument.

The argument `--agent` will be used as default User-Agent for the HTTP/HTTPS 
requests. If not specified it will use the default WatchPage user agent.
You can also pass `""` to omit the default user agent.

An example to execute WatchPage will be the following:

`watchpage --config docs/muflone_apps.yaml --results output`

All the targets specified in the configuration file `muflone_apps.yaml` will be
processed, results will be saved in the `output` directory and the differences
will be printed in the stdout.

Launching again the previous command you **will not** get any results as there
will not be further changes after the previous run.
The saved items will be stored in the directory specified in the `results`
argument.

Adding `--dump` you can observe the returned values but the changes will not be
saved.

# Configuration file

A configuration file is a YAML specification file with the following values:

- `NAME`: a unique string to identify the target to process
- `URL`: the page URL to monitor for changes

  You can also specify `github:name/repository` to point to a GitHub repository
- `PARSER`: the parser to use to process the URL. This can be either:
  - `html.parser`: this will use the default Python HTML parser
  - `html5lib`: this will use [html5lib](https://pypi.org/project/html5lib/) to
    process the page
  - `lxml`: this will use [lxml](https://lxml.de/) HTML parser
  - `xml`: this will use [lxml](https://lxml.de/) XML parser
- `TYPE`: specify the type of items to process from the page. This value can be:
  - `links`: will get all the anchors from a HTML page
  - `rss`: will get all the link items from a RSS feed
  - `text`: will process the page as a simple text file
  - `github-tags`: will get all the tag anchors from a GitHub repository
  - `github-tags-zip`: will get all the tag anchors from a GitHub repository,
    filtering only those in `.zip` format
  - `github-tags-tgz`: will get all the tag anchors from a GitHub repository,
    filtering only those in `.tar.gz` format
- `ABSOLUTE_URLS`: a boolean value (true/false) to make the processed URLs as
  absolute by appending the website from the URL page
- `FILTERS`: a list of filters to apply to find the matched items. This can be
  any of the following:
  - `STARTS`: the item must begin with the specified string
  - `NOT STARTS`: the item must not begin with the specified string
  - `ENDS`: the item must end with the specified string
  - `NOT ENDS`: the item must not end with the specified string
  - `CONTAINS`: the item must contain the specified string
  - `NOT CONTAINS`: the item must not contain the specified string
  - `REGEX`: the item must match the specified regular expression string
  - `NOT REGEX`: the item must not match the specified regular expression string
  - `TRIM`: removes spaces or the specified characters from both left and right
  - `LTRIM`: removes spaces or the specified characters from the left
  - `RTRIM`: removes spaces or the specified characters from the right
  - `PREPEND`: prepend (insert at the start) the specified text
  - `APPEND`: append (insert at the end) the specified text
  - `REMOVE`: remove from the item the specified text
  - `REPLACE`: replace from the item the specified text with a new pattern
    (specified using `WITH:`)
  - `REVERSE`: reverse the item text
  - `UPPER`: makes the text uppercase
  - `LOWER`: makes the text lowercase
  - `LEFT`: return the first leftmost characters
  - `RIGHT`: return the first rightmost characters
  - `REGEX REPLACE`: replace from the item a pattern using a regular expression
    with a new pattern (specified using `WITH:`)
  - `REGEX SEARCH`: return the first regular expression match
  - `JSON DICT`: return the value from a JSON dict with the specified key
  - `JSON LIST`: return the value from a JSON list with the specified index
- `HEADERS`: a dictionary with the headers to set for the request
- `STATUS`: a boolean value (true/false) to enable or disable the target

# Configuration example files

Some configuration example files can be found in the `docs` directory.

```yaml
NAME: watchpage
URL: https://github.com/muflone/watchpage/tags
PARSER: html5lib
TYPE: links
ABSOLUTE_URLS: true
FILTERS:
  - STARTS: 'https://github.com/muflone/'
  - ENDS: '.tar.gz'
STATUS: true
```

This configuration file will use the html5lib parser to scan all the links in
the page that begin with https://github.com/muflone/ and ending with .tar.gz

---
```yaml
NAME: watchpage
URL: github:muflone/watchpage
PARSER: html5lib
TYPE: github-tags-tgz
ABSOLUTE_URLS: true
STATUS: true
```

This configuration file will use the html5lib parser to scan all the tags links
for the GitHub repository only extracting the tags ending with .tar.gz

---
```yaml
NAME: watchpage
URL: github:muflone/watchpage
PARSER: html5lib
TYPE: github-tags
ABSOLUTE_URLS: true
FILTERS:
  - ENDS: '.tar.gz'
  - REMOVE RIGHT: '.tar.gz'
  - APPEND: '.something'
  - REPLACE: '.something'
    WITH: '.different'
STATUS: true
```

This configuration file will use the html5lib parser to scan all the tags links
for the GitHub repository only extracting the tags ending with .tar.gz and
applies some text replacements.

---
```yaml
NAME: watchpage
URL: https://github.com/muflone/watchpage/tags
PARSER: html5lib
TYPE: links
ABSOLUTE_URLS: true
FILTERS:
  - STARTS: 'https://github.com/muflone/'
  - ENDS: '.tar.gz'
HEADERS:
  User-Agent: 'WatchPage'
  Foo: 'Bar'
STATUS: true
```

Custom headers can be specified for each request.

---
```yaml
NAME: dbeaver_plugins
URL: https://dbeaver.io/update/ce/latest/plugins/
PARSER: html.parser
TYPE: text
FILTERS:
  - CONTAINS: '.jar'
STATUS: false
```

This configuration file will use the html parser to scan all the lines in the
page containing the text .jar

---
```yaml
NAME: gmtp
URL: https://sourceforge.net/projects/gmtp/rss
PARSER: xml
TYPE: rss
FILTERS:
  - ENDS: '.tar.gz/download'
STATUS: true
```

This configuration file will use the xml parser to scan all the links in the
RSS feed ending with .tar.gz/download
