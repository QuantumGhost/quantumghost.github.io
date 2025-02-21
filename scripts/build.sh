#!/usr/bin/env bash

set -ex
set -o pipefail

SCRIPT_DIR="$(realpath $(dirname $0))"
REPO_ROOT="$(dirname "${SCRIPT_DIR}")"

hugo build --gc
cp "${REPO_ROOT}/public/index.xml" "${REPO_ROOT}/public/all.atom.xml"
