alias gh-clean='env -u GITHUB_TOKEN gh'
# usage:
gh-clean auth login
gh-clean release create "$VERSION" --title "Release $VERSION" --notes-file CHANGELOG.md --target main


