
<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->
<a name="readme-top"></a>

<div>
    <h1 align="center">WiseSpot Python package build-up documentation <h1>
    </br>
    </br>
        <p align="center">
            This is an easy python Package tutorial for WiseSpot staff to build their own Python packages.
        </p>
</div>
</br>
</br>
</br>


<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#introduction">Introduction</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li>
        <a href="#step1-build-python-package">Step1: Build python package</a>
    </li>
    <li>
      <a href="#step2-upload-package-to-wisespot-sonatype-nexus">Step2: Upload source code to WiseSpot Sonatype Nexus</a>
      <ul>
        <li><a href="#make-sure-the-environment-install-twine-package">2.1 make sure the environment install `twine` package</a></li>
      </ul>
    </li>
    <li>
      <a href="#step3-build-a-ci-cd-python-package-in-gitlab">Step3: Build a Ci & Cd python package in Gitlab</a>
      <ul>
        <li><a href="#set-up-gitlab">3.1  Set up Gitlab</a></li>
        <li><a href="#set-up-gitlab-ci-and-cd">3.2  Set up Gitlab CI/CD</a></li>
      </ul>
    </li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#credits">Credits</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



 <!-- Introduction -->
# Introduction
Here is tutorial about how to creat a Python Package for WiseSpot staff. 

## Why build Python package to develop Python software?
Python packages are the fundamental units of shareable code in Python. Packages make it easy to organize, reuse, and maintain your code, as well as share it between projects, with your colleagues, and with the wider Python community. 

In this project, we will demonstrate methods and tools you can use to develop and maintain packages quickly, reproducibly, and with as much automation as possible — so you can focus on writing and sharing code!

## Not only package
This tutorial also concludes with how to build an HTML document at the same time. `Sphinx` is a popular tool for creating documentation for Python and other computer languages. It is intended to generate high-quality documentation from source code and other textual sources. `Sphinx`'s markup language is reStructuredText, which allows you to write documentation in a simple and readable way.

 `Sphinx` is widely used in the Python community and is the preferred documentation tool for many well-known Python applications and packages. It makes it easier for developers to produce comprehensive and up-to-date documentation for their projects by simplifying the process of developing and managing documentation.

## Tutorial Schedule
We have 3 major part in this project: 
* `Build python package`
* `Gitlab CiCd`
* `Upload package to Nexus or Pypi`

## At last
Thanks a lot to WiseSpot for giving this project the opportunity. Ming, and Michael, would like to express their gratitude! Special thanks to Jason and Brian for their great help! Enjoy!



<!-- Built With -->
# Built With
* [![Python][Python]][Python-url]
* [Cookiecutter](https://github.com/cookiecutter/cookiecutter)
* [Sphinx](https://github.com/sphinx-doc/sphinx)
* [Sonatype Nexus](https://www.sonatype.com/products/sonatype-nexus-repository)


<!-- Getting Started -->
# Getting Started
This is an example of how you may give instructions on setting up your project locally. To get a local copy up and running follow these simple example steps.

## Prerequisites
This is an example of how to list things you need to use the software and how to install them.

### Python
* You may directly access the `Python` official website for installation:
https://www.python.org/downloads/


### Anaconda

* `Anaconda`'s feature enables you to have multiple independent environments with different package versions, avoiding conflicts between different projects or dependencies.
https://www.anaconda.com/download/

### Poetry

* `Poetry` is a dependency management and packaging tool for Python. It is designed to simplify the process of managing project dependencies and creating distributable packages.
https://python-poetry.org/

## Installation
### Anaconda installation
After installation check and make sure the environment configuration is correct. Before start check the conda version or update.
```zsh
conda update conda
```

Check the created virtual environment
```zsh
conda env list
```

Create virtual environment
```zsh
conda create -n {your_env_name} python={version}
```

Start Virtual Environment
```zsh
conda activate {your_env_name}
```

### Poetry installation
* After `Poetry` install you will see the package folder have `pyproject.toml`file. the pyproject.toml file stores all the metadata and install instructions for the package.
  
```zsh
$ poetry install
Installing dependencies from lock file

No dependencies to install or update

Installing the current project: yuenpycounts (0.1.13)
```


<!-- Usage -->
## Usage
<div>
Here have a sample of our created package function usage sample.
<div> 

- pip install the package, import `yuenpycounts` package and then call `count_words()` function or `plot_words()` function.

Step1: Open the Mac terminal enter the command to get `PIP`

```bash
python3 get-pip.py
```

Step2: install `yuenpycounts` package

```bash
pip install yuenpycounts
```

Demo yuenpycounts's `count_words()`
```zsh
$ python3
>>> from yuenpycounts.yuenpycounts import count_words 
>>> count_words("zen.txt")
Counter({'is': 10, 'better': 8, 'than': 8, 'the': 6, 'to': 5, 'of': 3, 'although': 3, 'never': 3, 'be': 3, 'one': 3, 'idea': 3, 'complex': 2, 'special': 2, 'should': 2, 'unless': 2, 'obvious': 2, 'way': 2, 'do': 2, 'it': 2, 'may': 2, 'now': 2, 'if': 2, 'implementation': 2, 'explain': 2, 'a': 2, 'zen': 1, 'python': 1, 'by': 1, 'tim': 1, 'peters': 1, 'beautiful': 1, 'ugly': 1, 'explicit': 1, 'implicit': 1, 'simple': 1, 'complicated': 1, 'flat': 1, 'nested': 1, 'sparse': 1, 'dense': 1, 'readability': 1, 'counts': 1, 'cases': 1, 'arent': 1, 'enough': 1, 'break': 1, 'rules': 1, 'practicality': 1, 'beats': 1, 'purity': 1, 'errors': 1, 'pass': 1, 'silently': 1, 'explicitly': 1, 'silenced': 1, 'in': 1, 'face': 1, 'ambiguity': 1, 'refuse': 1, 'temptation': 1, 'guess': 1, 'there': 1, 'and': 1, 'preferably': 1, 'only': 1, 'that': 1, 'not': 1, 'at': 1, 'first': 1, 'youre': 1, 'dutch': 1, 'often': 1, 'right': 1, 'hard': 1, 'its': 1, 'bad': 1, 'easy': 1, 'good': 1, 'namespaces': 1, 'are': 1, 'honking': 1, 'great': 1, 'lets': 1, 'more': 1, 'those': 1})
```


<p align="right">(<a href="#readme-top">back to top</a>)</p>

</br>
<br>
<br>



# Step1 Build Python Package
Run cookiecutter command to build package structure
```bash
cookiecutter https://github.com/py-pkgs/py-pkgs-cookiecutter.git
```

Enter package name
```bash
author_name [Monty Python]: 'Your name'
package_name [mypkg]: 'Your package name'
package_short_description []: Calculate word counts in a text file!
package_version [0.1.0]: 
python_version [3.9]: 
Select open_source_license:
1 - MIT
2 - Apache License 2.0
3 - GNU General Public License v3.0
4 - Creative Commons Attribution 4.0
5 - BSD 3-Clause
6 - Proprietary
7 - None
Choose from 1, 2, 3, 4, 5, 6 [1]: 
Select include_github_actions:
1 - no
2 - ci
3 - ci+cd
Choose from 1, 2, 3 [1]: 3
```

* After creating the package, run the cmd `poetry build`.
```zsh
$ poetry build
Building yuenpycounts (0.1.13)
  - Building sdist
  - Built yuenpycounts-0.1.13.tar.gz
  - Building wheel
  - Built yuenpycounts-0.1.13-py3-none-any.whl
```
In `Python`, both `sdist` and `wheel` are packaging formats used to distribute Python projects and libraries. They serve as standardized formats that package your code and its dependencies, making it easier to distribute and install Python packages.

## Create Auto Documentation With `Sphinx`
Sphinx is a popular documentation generation tool used primarily for documenting Python projects.
```zsh
conda install sphinx
```
* If you want to add some function make sure add extensions to 	`conf.py` in `docs` folder.
```zsh
poetry add --dev myst-nb --python "^3.9"
poetry add --dev sphinx-autoapi sphinx-rtd-theme
```
* If you have some change, please use `make clean html`
```zsh
cd docs
make html
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>
</br>
<br>
<br>


# Step2 Upload Package To Wisespot Sonatype Nexus

<div align="center">
    <a href="">
        <img src="images/index.jpg">
</div>

`Sonatype Nexus` is a well-known repository manager in the software development industry. Nexus is a centralized storage and management system for software artifacts like as libraries, frameworks, and other dependencies.

`Nexus repository` managers are popular in organizations that use build automation technologies such as Apache Maven, Python Package, Gradle, or npm. Nexus is used by these tools to retrieve dependencies from a trusted and controlled source, ensuring consistent and reproducible builds. 

<div>
If you want to login to WiseSpot Nexus repository, you may ask for IT support team a avliable account for access repository. 
</div>
</br>
<br>
<br>

* Notice:
If you want to log in to the WiseSpot Nexus repository, you may ask for IT support team for an available account to access the repository. Of course, using the `twine upload` python package function the username and password is necessary. As an aside, if username, password, and token are directly run in `ci-cd. yml`, it may cause security issues. In the `. yml` file, you can use `${secrets. YOUR_PASSWORD_OR_TOKEN}}` to replace insert the password or token in the `. yml` file
<p align="right">(<a href="#readme-top">back to top</a>)</p>
</br>
<br>
<br>



## Make Sure The Environment Install Twine Package

If you not confirme that whether the package installed. You can use `pip show PACKAGE_NAME` to check.

```zsh
$ pip show twine
Name: twine
Version: 4.0.2
Summary: Collection of utilities for publishing packages on PyPI
Home-page: https://twine.readthedocs.io/
Author: Donald Stufft and individual contributors
Author-email: donald@stufft.io
License: 
Location: /Users/username/opt/anaconda3/envs/package/lib/python3.9/site-packages
Requires: importlib-metadata, keyring, pkginfo, readme-renderer, requests, requests-toolbelt, rfc3986, rich, urllib3
Required-by: 
```
<p align="right">(<a href="#readme-top">back to top</a>)</p>
</br>
<br>
<br>



# Step3 Build A Ci Cd Python Package In Gitlab
## Set Up Gitlab
First, set up local version control and initialize a Git repository:
```bash
git init
```
Next, set up git remote to our Gitlab repository:
```bash
git remote add origin https://git.wisespotgroup.com.hk/wisespot/example/jetdemo.git
git branch -M main
```
Check remote localtion:
```bash
git remote -v
```
When you `git clone` or `git push` project at Gitlab, Gitlab requires you to provide `Personal Access Tokens` for authentication of your identity.

Now, we will generate the personal access token:

Click your name -> `Edit Profile` -> `Access Tokens` ->  enter token name -> select all scopes -> `Create personal access token` -> copy your new personal access token.

We will use this token in next step

Now, you can enter `git clone origin main` command access to GitLab:
```bash
git clone origin main
```
Gitlab will requires you enter `Username` and `Password` in VsCode:
```bash
`Username` = `Your login Gitlab account name`
`Password` = `Your personal access token`
```  
Now, you can git `pull` `push` `clone`!
<p align="right">(<a href="#readme-top">back to top</a>)</p>
</br>
<br>
<br>



## Set Up Gitlab CI And CD 
Create a file call `.gitlab-ci.yml` in the root of your repository, which contains the CI/CD configuration.
This file will control Gitlab CI/CD workflow. For example:

```bash
stages:
  - install
  - test
  - deploy

install:
  rules:
    - if: '$CI_COMMIT_BRANCH == "main"'

  image: python:3.9-slim-buster
  before_script:
    - apt-get update && apt-get install make
  stage: install
  script:
    - echo "this is install stage"
    - pip install poetry
    - poetry install

test:
  rules:
      - if: '$CI_COMMIT_BRANCH == "main"'
  image: python:3.9-slim-buster
  stage: test
  script:
    - echo "this is test stage"
    - pip install poetry
    - pip install pytest
    - poetry install
    - poetry run pytest tests/  --cov=yuenpycounts

deploy:
  rules:
    - if: '$CI_COMMIT_BRANCH == "main"'
  image: python:3.9-slim-buster
  stage: deploy
  script:
    - echo "this is deploy stage!"
    - pip install poetry
    - pip install twine
    - poetry install
    - poetry build
    - python -m build

    - echo "start time"

    - twine upload -u __token__ -p pypi-AgENdGVzdC5weXBpLm9yZwIkYzQwMzIwYmQtMDU2ZS00YjNiLWEyNjYtNTdlNWFjMzg0ZDRlAAIUWzEsWyJ5dWVucHljb3VudHMiXV0AAixbMixbImNiNjIyMmQ4LWQ1ODctNDE2OC04ZDI0LTY0NWYwZTIzNTA2ZCJdXQAABiB0URGZP_BhY_GqAXQOf8xsOWrNIBfGBov7sHbxjRHzqg --repository-url https://test.pypi.org/legacy/ dist/*

    - twine upload -u __token__ -p pypi-AgEIcHlwaS5vcmcCJGVhN2UxOWU4LTk2NTUtNDVlZi1iNmI1LTk5NDcxZDRhNDIxOQACKlszLCI2OTQ5MjNjYi1iZGIwLTRkMDctYjdjZS1lZDg3NmQ2N2NmMDYiXQAABiAWYsh-c-1Z7e2o803cuq1M3_rczfFxprNB5BEtFWrcLA --repository-url https://upload.pypi.org/legacy/ dist/*

    - echo "end time"

    - echo "start Nexus"

    - twine upload --repository-url https://repo.wisespotgroup.com.hk/repository/PiPy-release/ -u student -p student@Sep dist/*
```

First, `stages` this part you should define how many `jobs` in your project. In this case, you can see 3 jobs `install`,`test`,`deploy`. Also, `stages` has `priority`. Ci/Cd must pass first stage to enter next stage. In this case, Ci/Cd must pass `install` stage to enter `test` stage. If `install` stage was fail, Ci/Cd return fail message skip `test` and `deploy` stage.

```bash
stages:
  - install
  - test
  - deploy
```

Next, we will dicuss `install` this job structure.

`install` is the job name, `rules` define with constraints stating under what conditions they should be executed. In this case, `rules` defined this job will execute when your repository main branch was changed in GitLab.

`image` is the name of the Docker image the Docker executor uses to run CI/CD jobs. In this case, we will use python3.9 environment to execute our script

`stage` define which job you doing now.

`script` will execute all commands included in the script. In this case, we will install `poetry` tool after we will use it. Also, we execute `poetry install` to install our package.

```bash
install:
  rules:
    - if: '$CI_COMMIT_BRANCH == "main"'

  image: python:3.9-slim-buster
  before_script:
    - apt-get update && apt-get install make
  stage: install
  script:
    - echo "this is install stage"
    - pip install poetry
    - poetry install
```

In `test` stage, we use `pytest` tool to execute our test case which we prepare in the `tests` folder.
We execute `pip install poetry` and `pip install pytest` to install `poetry` and `pytest`. And then install our package use `poetry install`.

Now, we can execute `poetry run pytest tests/  --cov=yuenpycounts` command to test our package. `pytest test/` command mean `pytest` will execute all name `test_xxxxxx.py` file in `tests` folder. `--cov=yuenpycounts` command display coverage of our package. In this case, `pytest` will execute `test_Yuen_pycount.py` file in `tests` folder.

```bash
test:
  rules:
      - if: '$CI_COMMIT_BRANCH == "main"'
  image: python:3.9-slim-buster
  stage: test
  script:
    - echo "this is test stage"
    - pip install poetry
    - pip install pytest
    - poetry install
    - poetry run pytest tests/  --cov=yuenpycounts
```

In `deploy` stage, we will distribute packages for our project. And then we upload our package to `Nexus` and `Pypi`.

First, we execute command `pip install poetry` and `pip install twine` to install `poetry` and `twine` these two tools. We can use `poetry install` to install our package. Now, we can use `poetry build` command to create distribution packages for our project.

`twine` can upload our package to `Nexus` and `Pypi` through `Username` , `Password` or `Token`. In this case, we use `twine upload --repository-url https://repo.wisespotgroup.com.hk/repository/PiPy-release/ -u student -p student@Sep dist/*` command upload our package to our `Nexus` repository. 

Command `twine upload --repository-url https://repo.wisespotgroup.com.hk/repository/PiPy-release/` mean `twine` upload our package to repository url. `-u` mean username, `-p` mean password, `dist/*` is folder contant your distribution package.
If you want upload package to `Pypi` repository, the command syntax is same to`Nexus`,`-u` change to `__token__`, `-p` change to your Pypi account API token.

```bash
deploy:
  rules:
    - if: '$CI_COMMIT_BRANCH == "main"'
  image: python:3.9-slim-buster
  stage: deploy
  script:
    - echo "this is deploy stage!"
    - pip install poetry
    - pip install twine
    - poetry install
    - poetry build
    - python -m build

    - echo "start time"

    - twine upload -u __token__ -p pypi-AgENdGVzdC5weXBpLm9yZwIkYzQwMzIwYmQtMDU2ZS00YjNiLWEyNjYtNTdlNWFjMzg0ZDRlAAIUWzEsWyJ5dWVucHljb3VudHMiXV0AAixbMixbImNiNjIyMmQ4LWQ1ODctNDE2OC04ZDI0LTY0NWYwZTIzNTA2ZCJdXQAABiB0URGZP_BhY_GqAXQOf8xsOWrNIBfGBov7sHbxjRHzqg --repository-url https://test.pypi.org/legacy/ dist/*

    - twine upload -u __token__ -p pypi-AgEIcHlwaS5vcmcCJGVhN2UxOWU4LTk2NTUtNDVlZi1iNmI1LTk5NDcxZDRhNDIxOQACKlszLCI2OTQ5MjNjYi1iZGIwLTRkMDctYjdjZS1lZDg3NmQ2N2NmMDYiXQAABiAWYsh-c-1Z7e2o803cuq1M3_rczfFxprNB5BEtFWrcLA --repository-url https://upload.pypi.org/legacy/ dist/*

    - echo "end time"

    - echo "start Nexus"

    - twine upload --repository-url https://repo.wisespotgroup.com.hk/repository/PiPy-release/ -u student -p student@Sep dist/*
```
<p align="right">(<a href="#readme-top">back to top</a>)</p>
</br>
<br>
<br>



# Version Control
`pyproject.toml` this file will control our package version. When you updata your package, you need to config your `pyproject.toml`:

```bash
[tool.poetry]
name = "yuenpycounts"
version = "0.1.13"
description = "Calculate word counts in a text file!"
authors = ["Micheal","Ming"]
license = "MIT"
readme = "README.md"

[tool.poetry.dependencies]
python = "^3.9"
matplotlib = "^3.7.2"
```

In this case, we updata our package `yuenpycounts` patch, we should config `version= "0.1.13"` to `version= "0.1.14"`.

if you don't want to hand config `pyproject.toml` file, you can use following the command to automatically config your `pyproject.toml` file:

A <type> of fix triggers a patch version bump, e.g.:
```bash
git commit -m "fix(mod_plotting): fix confusing error message in \
                 plot_words"
```
A <type> of feat triggers a minor version bump, e.g.:
```bash
git commit -m "feat(package): add example data and new module to \
                 package"
```

The text BREAKING CHANGE: in the footer will trigger a major release, e.g.:
```bash
git commit -m "feat(mod_plotting): move code from plotting module \
                 to pycounts module 
BREAKING CHANGE: plotting module wont exist after this release."
```
<p align="right">(<a href="#readme-top">back to top</a>)</p>
</br>
<br>
<br>



# Contributing

Interested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.

</br>
<br>
<br>

# License

`yuenpycounts` was created by Micheal and Ming. It is licensed under the terms of the MIT license.
<p align="right">(<a href="#readme-top">back to top</a>)</p>
</br>
<br>
<br>

# Credits

`yuenpycounts` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).
<p align="right">(<a href="#readme-top">back to top</a>)</p>
</br>
<br>
<br>

<!-- Acknowledgments -->
# Acknowledgments

Use this space to list resources you find helpful and would like to give credit to. I've included a few of my favorites to kick things off!

* [Python Package Reference Document](https://py-pkgs.org/welcome)

* [Twine Reference Document](https://twine.readthedocs.io/en/stable/changelog.html)


<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- Markdown Links & Images -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->

[Python]: https://img.shields.io/pypi/pyversions/yuenpycounts
[Python-url]: https://www.python.org/