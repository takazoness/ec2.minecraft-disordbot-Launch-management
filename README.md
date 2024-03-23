このBOTはAWS,EC2インスタンス上のUbuntuで動作することを前提としています。
インスタンス(鯖)間での、SSHのノンパス設定をやってください！

*********************************
スペック

マイクラ鯖起動用
インスタンスタイプ : t2.micro
OS : Ubuntu 22.04

マイクラ鯖本体
インスタンスタイプ : t3a.medium(動けばなんでもヨシ！)
OS : Ubuntu 22.04
*********************************

=================================================================================
インストールしなきゃいけないもの(マイクラ鯖起動用)

Python3
sudo apt update
↓
sudo apt install -y python3-pip

paramiko
pip install paramiko

AWS CLI
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
↓
unzip awscliv2.zip
↓
sudo ./aws/install
↓
aws --version
=================================================================================
