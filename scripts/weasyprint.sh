#!/usr/bin/env bash

set -euo pipefail

if [[ "$(uname -s)" == "Darwin" ]] && command -v brew >/dev/null 2>&1; then
    brew_prefix="$(brew --prefix)"
    if [[ -d "${brew_prefix}/lib" ]]; then
        export DYLD_FALLBACK_LIBRARY_PATH="${brew_prefix}/lib${DYLD_FALLBACK_LIBRARY_PATH:+:${DYLD_FALLBACK_LIBRARY_PATH}}"
    fi
fi

# Fontconfig needs a writable cache directory in sandboxed environments.
mkdir -p build/.cache
export XDG_CACHE_HOME="${XDG_CACHE_HOME:-$PWD/build/.cache}"

if [[ -x "$PWD/ENV/bin/weasyprint" ]]; then
    weasyprint_bin="$PWD/ENV/bin/weasyprint"
elif command -v weasyprint >/dev/null 2>&1; then
    weasyprint_bin="$(command -v weasyprint)"
else
    echo "WeasyPrint not found. Install dependencies or activate the virtualenv first." >&2
    exit 1
fi

exec "${weasyprint_bin}" "$@"
