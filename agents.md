# agents.md

This file provides guidance for AI agents and contributors working in this repository.

## Repository purpose

This repository packages [HMCL](https://github.com/HMCL-dev/HMCL) (Hello Minecraft! Launcher) as RPM packages:

- `hmcl-stable.spec` — the stable HMCL release package.
- `hmcl-beta.spec` — the beta HMCL release package.
- `.github/workflows/update.yml` — scheduled GitHub Actions workflow that checks upstream releases, updates the spec files, triggers a COPR build, and commits changes only after the build succeeds.

## Repository layout

| Path | Purpose |
| --- | --- |
| `hmcl-stable.spec` | RPM spec for the stable package. |
| `hmcl-beta.spec` | RPM spec for the beta package. |
| `.github/workflows/update.yml` | Automation that updates versions from upstream HMCL releases. |
| `README.md` | User-facing overview and install instructions. |
| `LICENSE` | GPL-3.0-only, matching the packaged upstream project. |
| `agents.md` | Guidance for agents and contributors (this file). |

## Spec file conventions

- Both packages are `noarch` Java JAR packages; the actual `.jar` is downloaded from the upstream release URL at RPM build time via `Source0`.
- Package names are `hmcl-stable` and `hmcl-beta`; each package provides `hmcl` and conflicts with the other package.
- Both packages require `java-headless`, not a specific JDK: HMCL's bytecode targets Java 17 and its boot loader (`HMCLBoot/src/main/java/org/jackhuang/hmcl/Main.java`, `MINIMUM_JAVA_VERSION = 17`) refuses to start on older Javas. Pinning a specific JDK major (e.g. `java-25-openjdk`) breaks builds on older distros and forces a full JDK on users.
- The desktop file is validated with `desktop-file-validate` in `%check` (`BuildRequires: desktop-file-utils`).
- `%_licensedir` is only defined on Fedora >= 35 / RHEL >= 9.2; the specs define a fallback for older distros.
- Runtime data is isolated so stable and beta can coexist conceptually:
  - stable uses `HMCL_LOCAL_HOME="$HMCL_USER_HOME/local-stable"`.
  - beta uses `HMCL_LOCAL_HOME="$HMCL_USER_HOME/local-beta"`.
  - both share `HMCL_DEPENDENCIES_DIR="$HMCL_USER_HOME/dependencies"` (HMCL downloads its JavaFX dependencies there on first launch).
- Version numbering:
  - Stable versions look like `3.x.y` (e.g. `3.16.3`).
  - Beta versions look like `3.x.y.NNN` (e.g. `3.17.0.354`).
- Bump `Release:` (e.g. `2%{?dist}`) for packaging-only changes; the automation always uses `1%{?dist}` for version bumps.
- Always add a `%changelog` entry when changing a spec file, using the format:
  `* <Day Mon DD YYYY> OrzMiku <miku@ecy.pink> - <version>-<release>`

## Update automation behavior

- The workflow runs every 6 hours (cron `17 */6 * * *`) and on `workflow_dispatch`.
- `workflow_dispatch` has a `force-build` input that rebuilds the current specs in COPR even when upstream did not change.
- It fetches the GitHub releases API with `gh api --paginate` (merging all pages — HMCL has 300+ releases, so a single page of 100 would silently miss an old stable).
- Stable updates come from the newest tag matching `^v[0-9]+\.[0-9]+\.[0-9]+$` that is **not** marked as a prerelease (upstream marks RCs as prereleases).
- Beta updates come from the newest tag matching `^v[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+$` (all beta tags are prereleases upstream).
- It refuses to downgrade a package and validates that upstream versions look like numeric dotted versions; a missing match is logged and skipped instead of failing the run.
- When versions change, it:
  1. Updates `Version:` in the matching spec.
  2. Adds a `%changelog` entry.
  3. Builds in COPR (`copr-cli build hmcl <spec>...`), which waits for the result; the version bump is committed **only if the build succeeds** (a 25-minute timeout fails the run so the next scheduled run retries).
  4. Commits with a message like `update hmcl: hmcl-beta-3.17.0.354`, rebasing onto the latest `main` before pushing.

## COPR project

- Project: `orzmiku/hmcl` (https://copr.fedorainfracloud.org/coprs/orzmiku/hmcl/), currently fedora-44/45/rawhide x86_64 chroots.
- Adding chroots (e.g. `fedora-45-aarch64`, or EPEL 9/10 now that the Java requirement is portable) is a project-level change:
  `copr-cli edit hmcl --chroot fedora-45-aarch64` (or the web UI), then adjust `Requires`/sources as needed.

## Contribution guidelines

- Keep both spec files consistent with each other unless a change is intentionally package-specific.
- Do not manually bump versions to values not present upstream; let the automation or a deliberate release update do it.
- Run `git diff --check` before committing to avoid whitespace errors.
- Test spec syntax locally: `rpmspec -P hmcl-stable.spec`; validate the desktop file with `desktop-file-validate`.
- Update this `agents.md` when repository layout or workflows change significantly.
