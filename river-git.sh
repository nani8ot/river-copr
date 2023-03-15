#!/bin/sh

git clone https://github.com/riverwm/river
wget https://raw.githubusercontent.com/nani8ot/river-copr/main/river-git.spec -O river.spec
cd river
git submodule update --init
cd ..

mv river river-git
tar -czf river-git.tar.gz river-git
