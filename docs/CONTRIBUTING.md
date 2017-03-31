# Contribution Guidelines

## There are multiple ways to contribute to the project

- Submitting bugs or feature requests! For now, you can drop us a line on Github issues [here](https://github.com/praelatus/praelatus/issues).

- Write documentation. We always need contributions in the form of localization, spell check, or net new documentation. For more information, you can check out our [wiki](https://github.com/praelatus/praelatus/wiki).

- Code submissions. We always need more code written in the form of new features or bugs.

## General Contribution Guidelines

If you're planning on working on something, make sure you open an issue or claim an existing one. This practice helps everyone on the project. It helps us know what everyone is working on (avoiding double work) and also helps us prevent you from working on something that maybe isn't a good fit for Praelatus, saving everyone time.

If you'd like to tackle an existing issue, just add a comment claiming the ticket for yourself and we will leave it alone. If you comment on an issue but do not update the issue again within 7 days, we will assume you've abandoned work.

**NOTE:** This does not mean you need to resolve the issue in 7 days, only that you need to update it so we know you have not abandoned working on the issue.

## Code Contribution Guidelines

1. All code must be passed through `go fmt` before submission.
2. All code must have tests. Unit tests are preferred, integration tests are allowed where appropriate.
3. All tests must be passing on the CI system before a PR will be accepted.
4. If your code breaks some other package, feel free to adjust the other package.

Documentation for building Praelatus can be found [here](https://github.com/praelatus/praelatus/wiki/Building-Praelatus-from-Source)

## Bug Report Guidelines

Bug reports are welcome. If you're not sure if the issue you're experiencing is a bug or not, report it anyway.

All good bug reports consist of a few things and we greatly appreciate if you can include as many of these items as possible:

1. A detailed description of the problem.
    - "Opening a ticket does not work" is not a great description. "Opening a ticket from any screen fails" is much better because it tells us that you are unable to open a ticket in any available method.
2. How to repeat the issue.
    - If we are unable to reproduce the issue, it becomes impossible to solve. Any configs or environment specific items you include give us much needed information in solving your problem.
3. Any error messages you encounter.
    - Sending us the error messages you get, whether from the app itself or in your logs, goes a long way to telling us what's going wrong.

## Feature Request Guidelines

Feature requests are always welcome as we want to make Praelatus the best it can be. In keeping with that theme, we have a few guidelines for creating Feature requests:

1. All feature requests should clearly define a scope with a clear "done" state. Meaning that the sentence "When Praelatus does X then Y feature will be considered complete." can be applied to it.
2. All feature requests will go through a comment period (minimum of 7 days) before being worked and at least two project maintainers will sign off as having approved the feature for work.
