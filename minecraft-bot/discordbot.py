import discord
import subprocess
import paramiko
import time

# 自分のBotのアクセストークンに置き換えてください
TOKEN = ''
# game-serverのインスタンスidを指定してください
INSTANCEID = ''
# regionを指定
REGION = ""

# 接続に必要なオブジェクトを生成
#client = discord.Client()
intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)
# ***************************
# ***    処理関数
# ***************************


class DiscordBOT:
    def __init__(self, client):
        self.SSHClient = None

    async def main(self, discord_event):
        get_text = discord_event.content
        send_text = ""

        if "$start minecraft" in get_text:
            await discord_event.channel.send("サーバーを起動します。(起動には1分ほど時間がかかります。)")
            # インスタンスの起動
            subprocess.call(
                "aws ec2 start-instances --instance-ids {} --region {}".format(INSTANCEID, REGION), shell=True)
            time.sleep(1)

            # インスタンスが起動するまで待機
            subprocess.call(
                "aws ec2 wait instance-running --instance-ids {}  --region {}".format(INSTANCEID, REGION), shell=True)
            time.sleep(1)

            # インスタンスのIPアドレスを取得
            proc = subprocess.run(["aws ec2 describe-instances --instance-ids {} --region {} --query 'Reservations[*].Instances[*].PublicIpAddress' --output text".format(
                INSTANCEID, REGION)], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            ip_add = proc.stdout.decode("utf-8")
            ip_add = ip_add.replace("\n", "")
            self.server_ip = ip_add
            print(f"server_ip=", self.server_ip)

            time.sleep(15)

            # SSH接続クライアント作成
            self.SSHClient = paramiko.SSHClient()
            self.SSHClient.set_missing_host_key_policy(
                paramiko.WarningPolicy())
            self.SSHClient.connect(
                self.server_ip, username="ubuntu", timeout=1.0)
            time.sleep(2)

            # SSHでminecraftサーバー起動
            stdin, stdout, stderr = self.SSHClient.exec_command(
                "cd /home/ubuntu/minecraft ; source startminecraft.sh")
            for x in stdout:
                print(x)
            for x in stderr:
                print("error:", x)
            time.sleep(10)

            # 接続用のIPアドレスをdiscordに送信
            send_text = "インスタンスの起動とminecraftサーバーへの接続に成功しました。\n サーバー起動後は {} で接続できます".format(
                ip_add.replace("-", "."))

        elif "$stop minecraft" in get_text:
            await discord_event.channel.send("サーバーを停止します。（この処理は1分ほど時間がかかります。）")
            # サーバーの停止
            self.SSHClient.connect(
                self.server_ip, username="ubuntu", timeout=1.0)
            time.sleep(2)

            stdin, stdout, stderr = self.SSHClient.exec_command(
                "cd /home/ubuntu/minecraft ; source stopminecraft.sh")
            self.SSHClient.close()
            time.sleep(60)

            # インスタンスの停止
            subprocess.call(
                "aws ec2 stop-instances --instance-ids {} --region {}".format(INSTANCEID, REGION), shell=True)
            send_text = "サーバーの停止が完了しました。"

        if send_text:
            await discord_event.channel.send(send_text)


discordbot = DiscordBOT(client)


@client.event
async def on_ready():
    print('ログインしました')

# on get message


@client.event
async def on_message(message):
    if message.author.bot:
        return

    await discordbot.main(message)

# Botの起動とDiscordサーバーへの接続
client.run(TOKEN)
