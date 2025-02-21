#!/usr/bin/env bash

set -ex
set -o pipefail

SCRIPT_DIR="$(realpath $(dirname $0))"
REPO_ROOT="$(dirname "${SCRIPT_DIR}")"

BASE_URL='https://blog.quantumghost.dev/'
if [ -n "${VERCEL_URL}" ]; then
    BASE_URL="https://${VERCEL_URL}"
fi

hugo build --gc --baseURL "${BASE_URL}"
cp "${REPO_ROOT}/public/index.xml" "${REPO_ROOT}/public/all.atom.xml"
