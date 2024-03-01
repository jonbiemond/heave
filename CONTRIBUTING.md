## 🤝 How to submit a contribution

To make a contribution, follow these steps:

1. [Fork](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/working-with-forks/fork-a-repo#forking-a-repository) and clone this repository.
2. Make changes in a new branch including the issue number. e.g. `git checkout -b 42-new-feature`.
3. If you modified the code (new feature or bug-fix), please add tests for it.
4. Check the linting. [see below](https://github.com/jonbiemond/heave/blob/main/CONTRIBUTING.md#-linting)
6. Ensure that all tests pass. [see below](https://github.com/jonbiemond/heave/blob/main/CONTRIBUTING.md#-testing)
7. Submit a pull request.

For more details about pull requests, please read [GitHub's guides](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request).


### 📦 Package manager

We use `poetry` as our package manager. You can install poetry by following the instructions [here](https://python-poetry.org/docs/#installation).

Please DO NOT use pip or conda to install the dependencies. Instead, use poetry:

```bash
poetry install
```

### 📌 Pre-commit

To ensure code standards, make sure to install pre-commit before your first commit.

```bash
pre-commit install
```

### 🧹 Linting

Use `ruff` to lint your code. You can run the linter by running the following command:

```bash
ruff .
```

Make sure that the linter does not report any errors or warnings before submitting a pull request.

### 📎 Code Format with `ruff`

Use `ruff` to reformat the code by running the following command:

```bash
ruff format . 
```

### 🧪 Testing

Use `pytest` to test your code. You can run the tests by running the following command:

```bash
pytest .
```

Make sure that all tests pass before submitting a pull request.


## FAQ

Contributing frequently asked questions.


### Changes made to a clone instead of a fork.

If you've already made changes to a clone of the base repo you should still create a fork:

1. Create the [fork in GitHub](https://docs.github.com/en/get-started/quickstart/fork-a-repo).
2. From the local repo rename `origin` remote (original clone) to `upstream`.
```bash
git remote rename origin upstream
```
3. Set the forked repo as the new origin.
```bash
git remote add origin <git@github.com:username/heave.git>
```
4. Fetch and push to fork.
```bash
git fetch origin
git push origin
```
