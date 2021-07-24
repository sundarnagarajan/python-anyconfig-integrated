#! /bin/bash
#set -ex

curdir=${0%/*}
output=${curdir}/../AUTHORS.txt

contributors=$(git log --pretty=format:"# %an%n%B" --perl-regexp --author='^((?!.*satoru.satoh.*).*)$')

cat << EOF > "${output}"
# Generated by ${0}, $(date "+%F %T")

Author
--------

Satoru SATOH <ssato@redhat.com>

Contributors (order in the commit logs)
-----------------------------------------

${contributors:?}
EOF

# vim:sw=2:ts=2:et:
