# 1) Get the latest from remote
git fetch --all --prune

# 2) Switch to main and fast-forward it
git switch main
git pull --rebase origin main

# 3) (Optional) bring your feature branch up to date OR delete it
# Option A: keep branch and rebase onto updated main
git switch chore/pages-rebuild
git rebase main
# push the rebased branch if you’ll keep using it
git push --force-with-lease

# Option B: if PR is merged and you’re done with the branch
git switch main
git branch -d chore/pages-rebuild              # delete local
git push origin --delete chore/pages-rebuild   # delete remote


