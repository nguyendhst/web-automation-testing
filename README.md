<h3 align="center">
  Repository for the Web Automation Testing Project
</h3>

## Table of Contents

- [Setup](#setup)
- [Project Structure](#project-structure)
- [Workflow](#workflow)


## Setup

1. Fork the repository & clone locally

```bash
git clone github.com/<uname>/web-automation-testing
```

2. Add the main repository as a remote `upstream`:

```bash
git remote add upstream https://github.com/nguyendhst/web-automation-testing.git
```

3. Install dependencies

>**Note:** Run `checks.sh` for a quick check of dependencies and installation

```bash
pip3 install -r requirements.txt
```

- Install [ChromeDriver](https://chromedriver.chromium.org/downloads)
	- MacOS: `brew install --cask chromedriver` and `brew upgrade chromedriver`
	- Linux: `sudo apt-get install chromium-chromedriver`
	- Windows: Download the latest version from [here](https://chromedriver.chromium.org/downloads) and add it to your PATH

>**Note** If you are using a different browser, you can find the corresponding driver [here](https://www.selenium.dev/documentation/en/webdriver/driver_requirements/)

>**Note** The chrome driver version should match the version of your chrome browser. You can check the version of your chrome browser by going to `chrome://version/`


## Project Structure



## Workflow

1. Pull the latest changes from `upstream`:

```bash
git pull upstream master
```

2. Create a new branch for your feature:

```bash
git checkout -b <feature-name>
```

3. Make your changes and commit them:

```bash
git add .

git commit -m "Add some feature"
```

4. Push your changes to your fork:

```bash
git push origin <feature-name>
```

5. Create a pull request from your fork to the `upstream` repository