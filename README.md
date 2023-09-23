# boilerplatePYweb
Starting point of your python web project with Flask and REST API.

This repo provides an empty python project template of a RESTful web app with `Flask`. It is concise and only contains the basic configurations of a mimimum python web application.

To use this template, you can simplt follow the steps below:

- clone this repo
- copy the content to your target repo
- replace package name `boilerplatepy` with your desired package name
(don not forget to update the credentials in `pyproject.toml`, e.g. author's information, etc.)

## Content
The following aspects of creating a new python project is addressed by this boilerplate:
- Package manager: `hatch`
- Web app framework: `Flask`
- API: `REST`
- Testing framework: `pytest`
- Linter: `ruff`
- Formatter: `black`
- CD/CI: `github action`
- Documentation: `mkdocs`

### Setup

To start the server in the development mode, navigate to the repo and run:

```py
python pyweb/main.py
```
