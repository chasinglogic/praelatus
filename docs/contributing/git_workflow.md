# Praelatus Git Workflow

Praelatus uses a "master is develop" branching model as this forces us to keep
our tests up to date and comprehensive.

## Branches

Praelatus uses release branches to handle of back porting of bug fixes /
features to older versions. Almost all development happens on master.

For managing your own changes we recommend [forking](https://github.com/praelatus/praelatus/fork) 
the project and either developing on your own master or using feature branching.

## Merging and Rebasing

We use Pull Requests and merges to bring these changes back into the main
repo's `master` branch however, we try to keep the pull requests to as few
commits as possible. Generally 1 to 2 commits for a branch. We do this
through `git rebase` and
[squashing](https://git-scm.com/book/en/v2/Git-Tools-Rewriting-History). This
allows us to keep the project mangeable from a history perspective as well as
encouraging high quality commit messages. 

For those unfamiliar with git, however this can be a daunting task the first
time so below we have written a tutorial on how to perform these steps. If
you're already familiar with rebasing and squashing then move on to 
[Commit Messages](#commit-messages)

Let's say that you've done some updates to the deployment documentation,
written some new documentation, and while you were at it you noticed the
settings module had old configuration information so you updated it. 
Your branch is called more-docs and your `git log` looks something like this:

```
commit 54bac418947a0f6882aac528dbca9747a8e76b52 (HEAD -> more-docs)
Author: Mathew Robinson <chasinglogic@gmail.com>
Date:   Thu Jul 27 13:55:16 2017 -0400

    WIP: Fix settings module so it matches new settings

commit 745353784c549299465ce1910738ea848248c18c
Author: Mathew Robinson <chasinglogic@gmail.com>
Date:   Thu Jul 27 13:54:23 2017 -0400

    WIP: update deployment docs

commit 61626d856b8d6caa4d4251beff34149c36fdc567 (origin/more-docs)
Author: Mathew Robinson <chasinglogic@gmail.com>
Date:   Wed Jul 26 16:18:17 2017 -0400

    write apache and nginx docs
```

You originally set out to just write some more documentation but made a few
minor fixes along the way. This is totally fine but what we're going to do is
"squash" all of these commits into one big commit with a descriptive commit
message. First, we need to make sure we have the latest updates for our local
copies of remote branches. Use git fetch to accomplish this:

```bash
git fetch -a
```

Now we need to interactively rebase onto origin/master. To do this we need to run:

```
git rebase -i origin/master
```

You'll then be prompted with the following in your git editor:

```
pick 61626d8 write apache and nginx docs
pick 7453537 WIP: update deployment docs
pick 54bac41 WIP: Fix tox config so it matches new settings

# Rebase 5c5add7..54bac41 onto 5c5add7 (3 commands)
#
# Commands:
# p, pick = use commit
# r, reword = use commit, but edit the commit message
# e, edit = use commit, but stop for amending
# s, squash = use commit, but meld into previous commit
# f, fixup = like "squash", but discard this commit's log message
# x, exec = run command (the rest of the line) using shell
# d, drop = remove commit
#
# These lines can be re-ordered; they are executed from top to bottom.
#
# If you remove a line here THAT COMMIT WILL BE LOST.
#
# However, if you remove everything, the rebase will be aborted.
#
# Note that empty commits are commented out
```

If you read the documentation below you'll see that we can use squash to meld
everything into the commit before it. So update this text file accordingly:

```
pick 61626d8 write apache and nginx docs
squash 7453537 WIP: update deployment docs
squash 54bac41 WIP: Fix tox config so it matches new settings

# Rebase 5c5add7..54bac41 onto 5c5add7 (3 commands)
#
# Commands:
# p, pick = use commit
# r, reword = use commit, but edit the commit message
# e, edit = use commit, but stop for amending
# s, squash = use commit, but meld into previous commit
# f, fixup = like "squash", but discard this commit's log message
# x, exec = run command (the rest of the line) using shell
# d, drop = remove commit
#
# These lines can be re-ordered; they are executed from top to bottom.
#
# If you remove a line here THAT COMMIT WILL BE LOST.
#
# However, if you remove everything, the rebase will be aborted.
#
# Note that empty commits are commented out
```

Then save and exit the file, if all goes well git will prompt you to write a
new commit message and so you can view [Commit Messages](#commit-messages)
below to see how we want the commit messages formatted.

## Dealing with broken rebases

Sometimes all of your commits won't play nice when squashed. In this instance
you'll get something that is kind of like a merge conflict except you have to
"play through" each commit. The workflow for getting through this is:

```bash
# Run git status to find "unmergable" files
git status

# Find broken chunks of files by looking for the <<<<<<< HEAD and making the
# appropriate edits then:
git rebase --continue
# Update the commit message if necessary
```

View the [rebasing docs](https://help.github.com/articles/using-git-rebase-on-the-command-line/)
for more information.

# Commit Messages

We follow a specific format for our commit messages. Our template commit looks like this:

```
Summary of Bug or Title of Feature

Short description of problem followed by a detailed description of the
solution.

# Omit if none
Addiitional Bugs Fixed:
- Bug1 short description
- Bug2 short description

# Omit if none, this is for things like "made code follow pep8"
Additional Changes or Minor Fixes:
- Minor change short description
- Minor change 2 short description
```

A real world example of what you will see after a rebase following the above
example would be this:

```
# This is a combination of 3 commits.
# This is the 1st commit message:

write apache and nginx docs

# This is the commit message #2:

WIP: update deployment docs

# This is the commit message #3:

WIP: Fix tox config so it matches new settings

# Please enter the commit message for your changes. Lines starting
# with '#' will be ignored, and an empty message aborts the commit.
#
# Date:      Wed Jul 26 16:18:17 2017 -0400
#
# interactive rebase in progress; onto 5c5add7
# Last commands done (3 commands done):
#    squash 7453537 WIP: update deployment docs
#    squash 54bac41 WIP: Fix tox config so it matches new settings
# No commands remaining.
# You are currently rebasing branch 'more-docs' on '5c5add7'.
#
# Changes to be committed:
#       modified:   README.md
#       modified:   docs/README.md
#       modified:   docs/_sidebar.md
#       new file:   docs/contributing/code_of_conduct.md
#       new file:   docs/contributing/git_workflow.md
#       renamed:    docs/contributing/README.md -> docs/contributing/guidelines.md
#       new file:   docs/contributing/hacking.md
#       deleted:    docs/deployment/README.md
#       deleted:    docs/deployment/_sidebar.md
#       deleted:    docs/deployment/advanced/README.md
#       modified:   docs/deployment/advanced/apache.md
#       modified:   docs/deployment/advanced/nginx.md
#       deleted:    docs/hacking/README.md
#       modified:   docs/index.html
#       modified:   praelatus/settings/__init__.py
#
```

We would change this to the following commit message:

```
Update Documentation

This updates the deployment documentation for Linux. Reorganizes the sidebar so
that it's more clear and managed inside a single file. Additionally this
includes "advanced" topics like configuring a reverse proxy for Praelatus, How
to set up and develop on Praelatus, and how to use git on this project.

Bug Fixes:
- The settings module was using an old environment variable to configure the
  database this commit updates it to the new environment variables to use
  Sqlite.

# Please enter the commit message for your changes. Lines starting
# with '#' will be ignored, and an empty message aborts the commit.
#
# Date:      Wed Jul 26 16:18:17 2017 -0400
#
# interactive rebase in progress; onto 5c5add7
# Last commands done (3 commands done):
#    squash 7453537 WIP: update deployment docs
#    squash 54bac41 WIP: Fix tox config so it matches new settings
# No commands remaining.
# You are currently rebasing branch 'more-docs' on '5c5add7'.
#
# Changes to be committed:
#       modified:   README.md
#       modified:   docs/README.md
#       modified:   docs/_sidebar.md
#       new file:   docs/contributing/code_of_conduct.md
#       new file:   docs/contributing/git_workflow.md
#       renamed:    docs/contributing/README.md -> docs/contributing/guidelines.md
#       new file:   docs/contributing/hacking.md
#       deleted:    docs/deployment/README.md
#       deleted:    docs/deployment/_sidebar.md
#       deleted:    docs/deployment/advanced/README.md
#       modified:   docs/deployment/advanced/apache.md
#       modified:   docs/deployment/advanced/nginx.md
#       deleted:    docs/hacking/README.md
#       modified:   docs/index.html
#       modified:   praelatus/settings/__init__.py
#
```

From that point you can push to your fork with:

```bash
git push --force fork more-docs
```

Finally you will [open a pull request](https://help.github.com/articles/creating-a-pull-request/) on Github
and it will automatically populate the PR with the well written commit message.
From there a member of the core team will perform a code review and any
additional changes as a result of that code review should not be squashed and
instead should be separate commits for each review rejection.


# Further Questions?

If you feel this document was insufficient in explaining the use of git for
Praelatus then please feel free to [submit an issue](https://github.com/praelatus/praelatus/issue). 
If you have questions or unclear in understanding then please contact the team via
email at [praelatus-devel@googlegroups.com](mailto:praelatus-devel@googlegroups.com)
