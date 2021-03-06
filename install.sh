#!/bin/bash
SUDO=sudo

# root ユーザーの場合 sudo コマンドを抜かす
if [ $EUID -eq 0 ]; then
        SUDO=""
fi

# OSの判別
if [ `uname` = "Darwin" ]; then
	# mac用のコード
	# ==get mac os name==
	dist_name=`uname`
	deploy_script="./dist/${dist_name}.sh"

	echo $dist_name

	# ディストリビューションのデプロイスクリプトの存在確認
	if [ -f $deploy_script ]
	then
		# get source
		source $deploy_script
	else
		# error message
		echo "Deploy script($deploy_script) not found!!"
		exit
	fi
elif [ `uname` = "Linux" ]; then
	# =Linux用のコード=
	# ==get linux distribution name==
	read dist_hint < /etc/issue
	dist_name=`echo $dist_hint | awk '{print $1}'`
	deploy_script="./dist/${dist_name,,}.sh"

	# ディストリビューションのデプロイスクリプトの存在確認
	if [ -f $deploy_script ]
	then
		# get source
		source $deploy_script
	else
		# error message
		echo "Deploy script($deploy_script) not found!!"
		exit
	fi
fi

# confirm root directory
if [ ! -d "root" ]
then
	# add mkdir root
	mkdir "root"
	mkdir "mnt"
fi

