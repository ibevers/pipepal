## ```senselab``` pull request guidelines
Pull requests are always welcome, and we appreciate any help you give. Note that a code of conduct applies to all spaces managed by the ```senselab``` project, including issues and pull requests. Please see the [Code of Conduct](CODE_OF_CONDUCT.md) for details.

### Workflow
Please use the following workflow when contributing:
1. If you have access, add a task to the [Project board](https://github.com/orgs/sensein/projects/45)
2. Create an issue (with the same name as the task, if applicable),
3. Use GitHub's "Create a branch" button from the issue page to generate a branch associated with the issue
4. Fork the issue branch
5. Work locally on the forked issue branch
6. Add the following repository secrets: ```CODECOV_TOKEN``` (CodeCov), ```HF_TOKEN``` (HuggingFace), ```PYPI_TOKEN``` (Pypi).
7. Submit a pull request to merge the forked issue branch into the upstream issue branch
8. After the pull request from 6 is merged, submit a pull request to merge the upstream issue branch into the upstream main

This approach ensures that tasks, issues, and branches all have names that clearly correspond. It also facilitates incremental neatly scoped changes since it tends to keep the scope of individual changes narrow.

If you would like to change this workflow, please use the current workflow process to suggest a change to this document.

When submitting a pull request, we ask you to check the following:

1. **Unit tests**, **code style**, **docstring** are in order.
   - Execute all unit tests to verify functionality through the following command:
     ```poetry run pytest```
      This command uses ```pytest``` to run tests, helping to identify any issues early.
   - Check your code for style guidelines and common errors by running:
     ```poetry run ruff check```
      This command utilizes ```ruff```, a code style checker, to ensure your code adheres to the project's style guidelines.

   See the Continuous Integration for up-to-date information on the current tests, code style, and any other requirements.

   It is also OK to submit work in progress if you're unsure of what this exactly means, in which case you'll likely be asked to make some further changes.

3. The contributed code will be **licensed under the same [license](LICENSE) as the rest of the repository**, If you did not write the code yourself, you must ensure the existing license is compatible and include the license information in the contributed files, or obtain permission from the original author to relicense the contributed code.
