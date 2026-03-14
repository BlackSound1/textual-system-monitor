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

   **Note**: Since a recent update, these tests may take quite a while depending on
   your computer. I have taken some pains to avoid threading issues, but performance
   issues may persist.

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

   The output should be:

   ```sh
   0
   0
   ```

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
