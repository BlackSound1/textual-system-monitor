# Contributing

To develop the app:

1. Please fork it, not just clone it.

2. Install the dependencies (including dev dependencies), with:

   ```sh
   make install-dev
   ```

   or use `requirements.txt` and `requirements_dev.txt`.

3. Check that all tests pass with:

   ```sh
   make test
   ```

   **Note**: If you see Pytest failing with errors like
   "NoMatches: No nodes match...", this is a known race condition problem. When
   testing, occasionally the app will render too slowly and the asserts may fail.
   This app is naturally vulnerable to these race conditions because much of its
   functionality involves UI rendering. If you see these errors, just run the tests
   again. I know this is not a real solution, but I'm looking into it.

4. Generate code coverage with:
   ```sh
   make cov
   ```

   We're not necessarily aiming for 100%, but aim for a high percentage that covers
   everything reasonable. This might also take quite a while.

5. Lint the Python files with:

   ```sh
   make lint
   ```

   All checks should pass. If you are contributing, make sure all linter checks
   pass before making a pull request, even though I have a CI/CD step to lint
   upon PR.

After those steps are done, have 2 terminals open. I use 2 instances of Bash in
Windows Terminal.

- In one instance, navigate to the repo, and run `make console`. This will cause the terminal to create a debug console waiting for an
instance of the app to hook into. [Read more here](https://textual.textualize.io/guide/devtools/).
- In the other instance, from the repo directory, run the dev version of the app
with `make run-dev` to run the app in development mode. The console in the first
instance should activate with logs from the running app.

More info on the Textual console [here](https://textual.textualize.io/guide/devtools/#console).

When contributing, **always** work from a branch other than `main`. Name your branch
something meaningful. Push to your 
own remote branch (because you forked it). Create a pull request from your forked
branch into my `main` branch.
