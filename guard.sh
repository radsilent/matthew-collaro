#!/usr/bin/env bash
# Keeps the personal site published.
#
# Both radsilent/matthew-collaro and radsilent/radsilent have reverted from
# public to private at least once, which disables GitHub Pages and 404s the
# site. This re-asserts the desired state and re-enables Pages if needed.
#
# Install:  */15 * * * * /home/vectorstream/matthew-collaro-site/guard.sh

set -uo pipefail

export PATH="/usr/bin:/usr/local/bin:/bin:$PATH"
LOG="/home/vectorstream/matthew-collaro-site/guard.log"
SITE="https://radsilent.github.io/matthew-collaro/"
REPOS=("radsilent/matthew-collaro" "radsilent/radsilent")

log() { printf '%s  %s\n' "$(date -u '+%Y-%m-%dT%H:%M:%SZ')" "$*" >> "$LOG"; }

for repo in "${REPOS[@]}"; do
  vis=$(gh api "/repos/$repo" --jq '.visibility' 2>/dev/null)
  if [[ "$vis" != "public" ]]; then
    log "WARN $repo visibility=$vis -> restoring public"
    if gh api -X PATCH "/repos/$repo" -f visibility=public >/dev/null 2>&1; then
      log "OK   $repo restored to public"
    else
      log "FAIL $repo could not be restored"
    fi
  fi
done

# Pages must be enabled on the site repo, sourced from main:/docs.
if ! gh api /repos/radsilent/matthew-collaro/pages >/dev/null 2>&1; then
  log "WARN Pages disabled -> re-enabling from main:/docs"
  if gh api -X POST /repos/radsilent/matthew-collaro/pages \
       -f "source[branch]=main" -f "source[path]=/docs" >/dev/null 2>&1; then
    log "OK   Pages re-enabled"
  else
    log "FAIL Pages could not be re-enabled"
  fi
fi

code=$(curl -s -o /dev/null -w '%{http_code}' --max-time 30 "$SITE")
if [[ "$code" == "200" ]]; then
  log "OK   site $code"
else
  log "WARN site $code"
fi
