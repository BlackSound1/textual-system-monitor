# Contributing

## Prerequisites

- Make (or Just, but Make is assumed here)
- UV (or a standalone Python version >= 3.12)

## Local Development

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
   testing, occasionally the app will render too slowly for certain tests that
   rely on rendered elements, so the asserts may fail.
   This app is naturally vulnerable to these race conditions because much of its
   functionality involves UI rendering, which can take arbitrary time.
   If you see these errors, just run the tests again. I know this is not a real
   solution, but I'm looking into it.

4. Generate code coverage with:
   ```sh
   make cov
   ```

   I'm not necessarily aiming for 100%, but aim for a high percentage that covers
   everything reasonable. This might also take quite a while.

   If using an IDE or something like VS Code, there might be a Pytest extension
   you could get that shows code coverage inline with the code itself
   (very nice).

5. Lint the Python files with:

   ```sh
   make lint
   ```

   All checks should pass. If you are contributing, make sure all linter checks
   pass before making a pull request, even though I have a CI/CD step to lint
   upon PR.

6. Format the Python files with:

   ```sh
   make format
   ```

After those steps are done, have 2 terminals open.

- In one terminal, navigate to the repo, and run `make console`. This will cause the terminal to create a debug console waiting for an
instance of the app to hook into. [Read more here](https://textual.textualize.io/guide/devtools/).
- In the other terminal, from the repo directory, run the dev version of the app
with `make run-dev` to run the app in development mode. The console in the first
instance should activate with logs from the running app.

More info on the Textual console [here](https://textual.textualize.io/guide/devtools/#console).

When contributing, **always** work from a branch other than `main`. Name your branch
something meaningful. Push to your 
own remote branch (because you forked it). Create a pull request from your forked
branch into my `main` branch.

Once your branch is reasonably complete, go to `pyproject.toml` and increase the `version` field
according to typical SemVer rules. Make sure to use `uv lock` to update the
lockfile upon doing so.

# Make

To see a list of available `make` commands and their uses, use:

```sh
make help
```

# Just

As I briefly mentioned earlier, Make is a build tool, not really a command runner. The fact that
Make can be used as a command runner is a useful byproduct of its other abilities.
For a true command runner, I use Just. It's a newer tool that I think is kind of neat.
It's not a requirement for this project because I only have it doing things Make does.

Check it out here: https://just.systems/man/en/introduction.html.

Similar to Make, instead of using `make run`, you would use `just run`, etc.

One of the advantages of Just is that its commands can accept arguments, so I was able to simplify
and condense several of the Make targets into single Just commands. I'm sure there's a way to
simplify my `Makefile` to better resemble the `Justfile`, but Just makes the process quite easy.

For a list of commands, use `just` or `just --list`. For usage instructions,
use `just --usage <COMMAND>`. To choose a command in an interactive picker while 
seeing its implementation, use `just --choose`.
