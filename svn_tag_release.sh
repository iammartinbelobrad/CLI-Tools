#!/bin/bash

# ----------------------------------------------------------------------------
# SVN skript slouzi pro releasovani nove verze
# ----------------------------------------------------------------------------

BIN='/usr/bin'
REPOSITORY_PATH=''
TAGS_PATH=$REPOSITORY_PATH/tags

echo -n 'Username: '
read USERNAME

echo -n 'Password: '
read PASS

echo -n '-- last release is: '
$BIN/svn list $TAGS_PATH --username $USERNAME --password $PASS | $BIN/tail -n 1 | $BIN/awk 'BEGIN { FS = "-" } ; { print $2 }' | $BIN/awk 'BEGIN { FS = "/" } ; { print $1 }'

echo -n 'Enter the new release version: '
read VERSION

if [ $VERSION != '' ]
	then
		echo '-- Taging trunk'
		$BIN/svn cp $REPOSITORY_PATH/trunk $REPOSITORY_PATH/tags/release-$VERSION --username $USERNAME --password $PASS -m ' - tag $VERSION released'
		echo '-- COMPLETE'
	else
		echo '-- Script terminated'
		exit
fi

