# hmcl-rpm

Unofficial RPM packages for [HMCL](https://github.com/HMCL-dev/HMCL) (Hello Minecraft! Launcher), built in [COPR](https://copr.fedorainfracloud.org/coprs/orzmiku/hmcl/).

## Packages

| Package | Tracks | Version format |
| --- | --- | --- |
| `hmcl-stable` | Latest stable HMCL release | `3.x.y` |
| `hmcl-beta` | Latest beta (prerelease) HMCL release | `3.x.y.NNN` |

The two packages conflict — install exactly one. Both provide a virtual `hmcl` capability.

## Installation

```sh
dnf copr enable orzmiku/hmcl
dnf install hmcl-stable        # or: hmcl-beta
```

Requirements:

- A Java 17+ runtime (the `java-headless` capability); HMCL's launcher itself refuses to start on older Javas.
- On first launch, HMCL downloads its JavaFX dependencies from Maven Central into `~/.local/share/hmcl/dependencies` (`HMCL_DEPENDENCIES_DIR`).

Stable and beta keep separate runtime data (`~/.local/share/hmcl/local-stable` vs `~/.local/share/hmcl/local-beta`), so switching packages does not clobber existing installations.

## How updates work

[.github/workflows/update.yml](.github/workflows/update.yml) runs every 6 hours:

1. Fetches all HMCL GitHub releases and picks the newest matching version for each channel (stable: non-prerelease `3.x.y`; beta: `3.x.y.NNN`).
2. Bumps `Version:` in the spec files and adds a `%changelog` entry.
3. Builds in COPR and waits for the result.
4. Commits the bump only if the build succeeded — a broken update never lands silently.

You can also trigger a manual rebuild (no version change) via *Actions → Update HMCL packages → Run workflow* with the `force-build` option.

## Development

- `rpmspec -P hmcl-stable.spec` — preprocess/validate a spec locally.
- `copr-cli build hmcl hmcl-stable.spec hmcl-beta.spec` — build via COPR.
- Repository conventions for agents/contributors: [agents.md](agents.md).
