# Contributing

## Commit Message Format

This project uses **Conventional Commits** to automate versioning and changelog generation.
Please use the following format for your commit messages:

```
<type>(<scope>): <subject>
```

### Types
- **feat**: A new feature (triggers `MINOR` version bump).
- **fix**: A bug fix (triggers `PATCH` version bump).
- **docs**: Documentation only changes.
- **style**: Changes that do not affect the meaning of the code (white-space, formatting, etc).
- **refactor**: A code change that neither fixes a bug nor adds a feature.
- **perf**: A code change that improves performance.
- **test**: Adding missing tests or correcting existing tests.
- **chore**: Changes to the build process or auxiliary tools and libraries.

**Breaking Changes:**
If a commit includes a breaking change, add `!` after the type/scope, or include `BREAKING CHANGE:` in the footer. This triggers a `MAJOR` version bump.

### Example
```bash
feat(curl): add windows escaping support
fix: handle connection timeout in simulate_client
docs: update readme with installation steps
```

## Release Process
Releases are automated via GitHub Actions.
1. Push changes to `main`.
2. The Action analyzes commits since the last tag.
3. If valid changes are found (`feat`, `fix`, `BREAKING CHANGE`), a new release is created.
