#!/usr/bin/env bash
set -euo pipefail

BASE_BRANCH="${1:-main}"
CURRENT_BRANCH="$(git rev-parse --abbrev-ref HEAD)"

if [[ -z "${CURRENT_BRANCH}" ]]; then
  echo "Unable to detect current branch" >&2
  exit 1
fi

if [[ "${CURRENT_BRANCH}" == "${BASE_BRANCH}" ]]; then
  echo "You are on '${BASE_BRANCH}'. Checkout your feature branch first." >&2
  exit 1
fi

if ! git remote get-url origin >/dev/null 2>&1; then
  echo "Remote 'origin' is not configured. Add remote first:" >&2
  echo "  git remote add origin <repo-url>" >&2
  exit 1
fi

echo "Fetching origin/${BASE_BRANCH}..."
git fetch origin "${BASE_BRANCH}"

echo "Merging origin/${BASE_BRANCH} into ${CURRENT_BRANCH}..."
if ! git merge "origin/${BASE_BRANCH}"; then
  echo
  echo "Merge reported conflicts. Resolve them, then run:" >&2
  echo "  git add ." >&2
  echo "  git commit" >&2
  echo "  git push origin ${CURRENT_BRANCH}" >&2
  exit 2
fi

echo "Checking for unresolved conflict markers..."
if grep -R "^<{7}\|^={7}\|^>{7}" . --exclude-dir=node_modules --exclude-dir=.git >/dev/null; then
  echo "Conflict markers were found in files. Resolve them before push." >&2
  exit 3
fi

echo "Done. Now run checks and push:"
echo "  npm run lint && npm run build && npm run test"
echo "  git push origin ${CURRENT_BRANCH}"
