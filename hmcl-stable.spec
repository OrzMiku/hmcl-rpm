Name:           hmcl-stable
Version:        3.15.1
Release:        4%{?dist}
Summary:        A Minecraft Launcher which is multi-functional, cross-platform and popular.

License:        GPL-3.0-only
URL:            https://github.com/HMCL-dev/HMCL
Source0:        https://github.com/HMCL-dev/HMCL/releases/download/v%{version}/HMCL-%{version}.jar
Source1:        https://raw.githubusercontent.com/HMCL-dev/HMCL/v%{version}/LICENSE
Source2:        https://raw.githubusercontent.com/HMCL-dev/HMCL/v%{version}/HMCL/src/main/resources/assets/img/icon.png
Source3:        https://raw.githubusercontent.com/HMCL-dev/HMCL/v%{version}/HMCL/src/main/resources/assets/img/icon@2x.png
Source4:        https://raw.githubusercontent.com/HMCL-dev/HMCL/v%{version}/HMCL/src/main/resources/assets/img/icon@4x.png
Source5:        https://raw.githubusercontent.com/HMCL-dev/HMCL/v%{version}/HMCL/src/main/resources/assets/img/icon@8x.png

Requires:       java-25-openjdk

BuildArch:      noarch

%description
HMCL is an open-source, cross-platform Minecraft launcher that supports Mod Management, Game Customizing, ModLoader Installing (Forge, NeoForge, Cleanroom, Fabric, Legacy Fabric, Quilt, LiteLoader, and OptiFine), Modpack Creating, UI Customization, and more.

HMCL has amazing cross-platform capabilities. Not only does it run on different operating systems like Windows, Linux, macOS, and FreeBSD, but it also supports various CPU architectures such as x86, ARM, RISC-V, MIPS, and LoongArch. You can easily enjoy Minecraft across different platforms through HMCL.

%prep


%build


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
    HMCL_LOCAL_HOME="$HMCL_USER_HOME/local-stable"
    export HMCL_LOCAL_HOME
fi

if [ -z "${HMCL_DEPENDENCIES_DIR:-}" ]; then
    HMCL_DEPENDENCIES_DIR="$HMCL_USER_HOME/dependencies"
    export HMCL_DEPENDENCIES_DIR
fi

exec java -jar %{_datadir}/%{name}/%{name}.jar "$@"
EOF

install -Dm0644 /dev/stdin %{buildroot}%{_datadir}/applications/%{name}.desktop <<'EOF'
[Desktop Entry]
Type=Application
Name=HMCL
Comment=Hello Minecraft! Launcher
Exec=%{name}
Icon=%{name}
Terminal=false
StartupNotify=false
Categories=Game;
Keywords=mc;minecraft;
EOF


%files
%license %{_licensedir}/%{name}/LICENSE
%{_bindir}/%{name}
%{_datadir}/%{name}/%{name}.jar
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}.png


%changelog
* Fri Jun 19 2026 OrzMiku <miku@ecy.pink> - 3.15.1-3
- Initial package
