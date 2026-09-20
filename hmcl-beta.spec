Name:           hmcl-beta
Version:        3.17.0.357
Release:        2%{?dist}
Summary:        A Minecraft Launcher which is multi-functional, cross-platform and popular.

Conflicts:      hmcl-stable
Provides:       hmcl = %{version}-%{release}

License:        GPL-3.0-only
URL:            https://github.com/HMCL-dev/HMCL
Source0:        https://github.com/HMCL-dev/HMCL/releases/download/v%{version}/HMCL-%{version}.jar
Source1:        https://raw.githubusercontent.com/HMCL-dev/HMCL/v%{version}/LICENSE
Source2:        https://raw.githubusercontent.com/HMCL-dev/HMCL/v%{version}/HMCL/src/main/resources/assets/img/icon.png
Source3:        https://raw.githubusercontent.com/HMCL-dev/HMCL/v%{version}/HMCL/src/main/resources/assets/img/icon@2x.png
Source4:        https://raw.githubusercontent.com/HMCL-dev/HMCL/v%{version}/HMCL/src/main/resources/assets/img/icon@4x.png
Source5:        https://raw.githubusercontent.com/HMCL-dev/HMCL/v%{version}/HMCL/src/main/resources/assets/img/icon@8x.png

# HMCL needs Java 17+ at runtime (its boot loader refuses to start on older
# Javas), so depend on the virtual java-headless capability instead of pinning
# a specific JDK major version; this also keeps builds working on older distros.
Requires:       java-headless
BuildRequires:  desktop-file-utils
BuildArch:      noarch

# %%_licensedir is defined on Fedora >= 35 / RHEL >= 9.2; provide a fallback.
%{!?_licensedir:%global _licensedir %{_datadir}/licenses}

%description
HMCL is an open-source, cross-platform Minecraft launcher that supports Mod Management, Game Customizing, ModLoader Installing (Forge, NeoForge, Cleanroom, Fabric, Legacy Fabric, Quilt, LiteLoader, and OptiFine), Modpack Creating, UI Customization, and more.

HMCL has amazing cross-platform capabilities. Not only does it run on different operating systems like Windows, Linux, macOS, and FreeBSD, but it also supports various CPU architectures such as x86, ARM, RISC-V, MIPS, and LoongArch. You can easily enjoy Minecraft across different platforms through HMCL.

%prep
# Sources are installed directly in %%install.

%build
# Nothing to build.

%install
install -Dm0644 %{SOURCE0} %{buildroot}%{_datadir}/%{name}/%{name}.jar
install -Dm0644 %{SOURCE1} %{buildroot}%{_licensedir}/%{name}/LICENSE
install -Dm0644 %{SOURCE2} %{buildroot}%{_datadir}/icons/hicolor/32x32/apps/%{name}.png
install -Dm0644 %{SOURCE3} %{buildroot}%{_datadir}/icons/hicolor/64x64/apps/%{name}.png
install -Dm0644 %{SOURCE4} %{buildroot}%{_datadir}/icons/hicolor/128x128/apps/%{name}.png
install -Dm0644 %{SOURCE5} %{buildroot}%{_datadir}/icons/hicolor/256x256/apps/%{name}.png

install -Dm0755 /dev/stdin %{buildroot}%{_bindir}/%{name} <<"EOF"
#!/bin/sh
cd "$HOME" || exit 1

if [ -z "${HMCL_USER_HOME:-}" ]; then
    HMCL_USER_HOME="${XDG_DATA_HOME:-$HOME/.local/share}/hmcl"
    export HMCL_USER_HOME
fi

if [ -z "${HMCL_LOCAL_HOME:-}" ]; then
    HMCL_LOCAL_HOME="$HMCL_USER_HOME/local-beta"
    export HMCL_LOCAL_HOME
fi

if [ -z "${HMCL_DEPENDENCIES_DIR:-}" ]; then
    HMCL_DEPENDENCIES_DIR="$HMCL_USER_HOME/dependencies"
    export HMCL_DEPENDENCIES_DIR
fi

if ! command -v java >/dev/null 2>&1; then
    echo "%{name}: no java runtime found (Java 17+ required)" >&2
    exit 1
fi

exec java -jar %{_datadir}/%{name}/%{name}.jar "$@"
EOF

install -Dm0644 /dev/stdin %{buildroot}%{_datadir}/applications/%{name}.desktop <<'EOF'
[Desktop Entry]
Type=Application
Name=HMCL Beta
GenericName=Minecraft Launcher
Comment=Hello Minecraft! Launcher
Exec=%{name}
Icon=%{name}
Terminal=false
StartupNotify=false
Categories=Game;
Keywords=HMCL;Minecraft;Game;
EOF


%check
desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop


%files
%license %{_licensedir}/%{name}/LICENSE
%{_bindir}/%{name}
%{_datadir}/%{name}/%{name}.jar
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}.png


%changelog
* Sun Sep 20 2026 OrzMiku <miku@ecy.pink> - 3.17.0.357-1
* Sat Sep 12 2026 OrzMiku <miku@ecy.pink> - 3.17.0.356-1
* Sat Sep 05 2026 OrzMiku <miku@ecy.pink> - 3.17.0.355-1
* Sat Aug 15 2026 OrzMiku <miku@ecy.pink> - 3.17.0.354-2
- Require java-headless instead of a pinned JDK (HMCL needs Java 17+).
- Validate the desktop file with desktop-file-validate.
- Fall back for %_licensedir and check for java in the launcher script.
* Tue Aug 11 2026 OrzMiku <miku@ecy.pink> - 3.17.0.354-1
* Fri Aug 07 2026 OrzMiku <miku@ecy.pink> - 3.17.0.353-1
* Sun Jul 26 2026 OrzMiku <miku@ecy.pink> - 3.17.0.351-1
* Thu Jul 16 2026 OrzMiku <miku@ecy.pink> - 3.17.0.350-1
* Wed Jul 01 2026 OrzMiku <miku@ecy.pink> - 3.16.0.348-1
* Wed Jul 01 2026 OrzMiku <miku@ecy.pink> - 3.16.0.347-1
- Initial beta package.
