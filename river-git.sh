#!/bin/sh

git clone https://github.com/riverwm/river
wget https://raw.githubusercontent.com/nani8ot/river-copr/main/river-git.spec -O river.spec
cd river
git submodule update --init
cd ..

tar -czf river.tar.gz river-git
