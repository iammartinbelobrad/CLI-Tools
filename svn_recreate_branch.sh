#!/bin/bash

# ----------------------------------------------------------------------------
# SVN skript slouzi pro znovuvytvoreni vetve po zmergovani do trunku
# ----------------------------------------------------------------------------

echo -n 'Path to project: '
read PROJECT

echo -n 'Branch name: '
read BRANCH_NAME

echo -n 'Username: '
read USERNAME

echo -n 'Password: '
read PASS


BRANCH_PATH=$PROJECT/branches/$BRANCH_NAME

echo ''
echo $BRANCH_PATH
echo -n 'Are you sure you want to delete this branch? (Y/N): '
read CONFIRM

if [ $CONFIRM == 'Y' ]
	then
		echo '-- Deleting branch'
		svn del $BRANCH_PATH --username $USERNAME --password $PASS -m ' - Smazana vetev $BRANCH_NAME'

		echo '-- Copying trunk to branch'
		svn copy $PROJECT/trunk $BRANCH_PATH --username $USERNAME --password $PASS -m ' - Znovuvytvorena vetev $BRANCH_NAME'
		echo '-- COMPLETE'
	else
		echo '-- Script terminated'
		exit
fi

