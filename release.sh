#!/bin/bash
# 
# Author: Mathew Robinson <chasinglogic@gmail.com>
# 
# This script builds praelatus with the frontend and deploys it to Github
# Requires go, npm, node, and curl be installed.
#

function parse_git_branch {
    ref=$(git symbolic-ref HEAD 2> /dev/null) || return
    echo "${ref#refs/heads/} "
}

function check_if_success() {
    if [ $? -ne 0 ]; then
        echo "error running last command"
        exit $?
    fi
}

function print_help() {
    echo "Usage: 
    ./release.sh tag_name name_of_release prelease_bool:optional

Examples:
    This would deploy to tag v0.0.1 naming the release MVP and specify it is a 
    prerelease

    ./release.sh v0.0.1 MVP true

    If the 3rd argument is omitted we assume it is a normal release

    ./release.sh v1.0.0 \"Aces High\""
}

BRANCH=$(parse_git_branch)

if [ $BRANCH != "master" ] && [ $BRANCH != "develop" ]; then
    echo "you aren't on master or develop, refusing to package a release"
    exit 1
fi

if [ "$1" == "--help" ] || [ "-h" == "$1" ]; then
    print_help
    exit 0
fi

if [ "$#" -ne 3 ] && [ "$#" -ne 2 ]; then
    echo "wrong number of arguments $#"
    print_help
    exit 1
fi

TAG_NAME=$1
RELEASE_NAME=$2
PRERELEASE=$3
STARTING_DIR=$(pwd)
PROGRAM="praelatus"
ARCHES=("amd64")

if [ -z "$OWNER" ]; then
    OWNER=$USER
fi

if [ -z "$PLATFORMS" ]; then
    PLATFORMS=("linux" "darwin" "windows")
fi

echo "Tag Name: $TAG_NAME"
echo "Release Name: $RELEASE_NAME"
echo "Prelease: $PRERELEASE"
echo "Program: $PROGRAM"
echo "Building for Arches: ${ARCHES[@]}"
echo "Building for Platforms: ${PLATFORMS[@]}"
echo "Repo Owner: $OWNER"

echo "Checking for dependencies..."
if ! [ -x "$(command -v go)" ]; then
    echo "You need to install the go tool. https://golang.org/download"
    exit 1
fi

if ! [ -x "$(command -v npm)" ]; then
    echo "You need to install npm. https://nodejs.org/en/download/"
    exit 1
fi

if ! [ -x "$(command -v node)" ]; then
    echo "You need to install node. https://nodejs.org/en/download/"
    exit 1
fi

if ! [ -x "$(command -v curl)" ]; then
    echo "You need to install curl"
    exit 1
fi

if ! [ -x "$(command -v yarn)" ]; then
    echo "yarn not detected attempting to install..."
    sudo npm install -g yarn
fi

if ! [ -x "$(command -v webpack)" ]; then
    echo "webpack not detected attempting to install..."
    sudo npm install -g webpack
fi

if ! [ -x "$(command -v glide)" ]; then
    echo "glide not detected attempting to install..."
    go get github.com/Masterminds/glide
    if ! [ -x "$(command -v glide)" ]; then
        echo "installed glide but \$GOBIN isn't in \$PATH"
        exit 1
    fi
fi

if [ -d "build" ]; then
    echo "cleaning build directory..."
    rm -rf build
fi

# create the final build directories
mkdir build/
mkdir build/client

# get the frontend
echo "downloading the frontend"
git clone https://github.com/praelatus/frontend $STARTING_DIR/build/frontend

# change to frontend git repo
cd $STARTING_DIR/build/frontend

echo "installing dependencies for frontend"
yarn install

echo "compiling the frontend"
webpack -p
mv $STARTING_DIR/build/frontend/build/debug/static $STARTING_DIR/build/client/
cp $STARTING_DIR/build/frontend/index.html $STARTING_DIR/build/client/index.html

echo "installing dependencies for backend"
glide install

echo "cleaning up"
cd $STARTING_DIR
rm -rf build/frontend


PACKAGES=()

for platform in "${PLATFORMS[@]}"
do
    for arch in "${ARCHES[@]}"
    do
        echo "adding miscellaneous files to release"
        mkdir build/$platform-$arch
        cp $STARTING_DIR/envfile.example $STARTING_DIR/build/$platform-$arch/

        echo "compiling the backend for $platform-$arch"

        GOOS=$platform
        GOARCH=$arch 
        if [ "$platform" == "windows" ]; then
            go build -o build/$platform-$arch/$PROGRAM.exe >/dev/null
        else
            go build -o build/$platform-$arch/$PROGRAM >/dev/null
        fi

        # make sure builds worked
        check_if_success

        echo "building release tar"
        cd build/$platform-$arch

        PACKAGE_NAME="$PROGRAM-$TAG_NAME-$platform-$arch.tar.gz"
        if [ "$platform" == "windows" ]; then
            PACKAGE_NAME="$PROGRAM-$TAG_NAME-$platform-$arch.zip"
        fi

        echo $PACKAGE_NAME
        PACKAGES+=("$PACKAGE_NAME")

        if [ -f "$STARTING_DIR/$PACKAGE_NAME" ]; then
            echo "old package detected removing..."
            rm $STARTING_DIR/$PACKAGE_NAME
        fi

        if [ "$platform" == "windows" ]; then
	    ls
	    exit 0
            zip $STARTING_DIR/$PACKAGE_NAME *
        else
	    ls
	    exit 0
            tar -czvf $STARTING_DIR/$PACKAGE_NAME *
        fi

        cd $STARTING_DIR
    done
done

# create the tag
echo "tagging release..."
# git tag -fa $TAG_NAME -m "$RELEASE_NAME"

# push the tag
echo "Pushing tags..."
git push --follow-tags

if [ -z "$GITHUB_API_TOKEN" ]; then
    echo "no github token detected all done."
    exit 0
fi

GITHUB_URL="https://api.github.com/repos/$OWNER/$PROGRAM/releases?access_token=$GITHUB_API_TOKEN"
echo $GITHUB_URL
JSON="{ \"tag_name\": \"$TAG_NAME\", \"name\": \"$RELEASE_NAME\", \"body\": \"$PROGRAM release $RELEASE_NAME\", \"target_commitsh\": \"master\" }"

RESP=$(curl -X POST --data "$JSON" $GITHUB_URL)
echo $RESP
ASSETS_URL=$(echo "$RESP" | grep -oP '(?<="upload_url": ")(.*assets)')

for pkg in "${PACKAGES[@]}"
do
    echo "uploading $pkg"
    UPLOAD_URL="$ASSETS_URL?name=$pkg&access_token=$GITHUB_API_TOKEN"
    echo $UPLOAD_URL

    if [ -z "$(echo $pkg | grep -o ".zip")" ]; then
        HEADERS="Content-Type:application/zip"
    else
        HEADERS="Content-Type:application/gzip"
    fi

    curl -X POST -H $HEADERS --data-binary $STARTING_DIR/$pkg $UPLOAD_URL >/dev/null
done
