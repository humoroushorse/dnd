#!/usr/bin/env bash
LC_ALL=C

LOCAL_BRANCH_NAME="$(git rev-parse --abbrev-ref HEAD)"

# feature/DND-1234-branch-name/allowed_characters

BRANCH_TYPE="(feature|refactor|bugfix|hotfix|release|docs|wip)"
BRANCH_TICKET="(DND)-[0-9]+"
BRANCH_DESCRIPTION="[a-zA-Z0-9\/_-]*"
VALID_BRANCH_REGEX=^$BRANCH_TYPE/$BRANCH_TICKET$BRANCH_DESCRIPTION$

center() {
    termwidth="$(tput cols)"
    padding="$(printf '%0.1s' $2{1..500})"
    printf '%*.*s %s %*.*s\n' 0 "$(((termwidth-2-${#1})/2))" "$padding" "$1" 0 "$(((termwidth-1-${#1})/2))" "$padding"
}

fill_screen() {
    printf '%*s\n' "${COLUMNS:-$(tput cols)}" '' | tr ' ' $1
}

if [[ ! $LOCAL_BRANCH_NAME =~ $VALID_BRANCH_REGEX ]]
then
    center "scripts/hooks/prepare-commit-msg.sh" =
    echo "Invalid Branch Name:"
    echo "\t$LOCAL_BRANCH_NAME"
    echo "Legal Branch Name Format:"
    echo "\t$VALID_BRANCH_REGEX"
    fill_screen =
    exit 1
else
    echo "Branch name is valid: $LOCAL_BRANCH_NAME"
fi

exit 0
