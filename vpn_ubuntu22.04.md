# ubuntu 22.04LTSで研究室のVPNに接続する

1. https://qiita.com/maromaro0013/items/86f129a953dbe7419e56 を参考にkl2tpdをインストールする.  
libnm-gtk-dev libnm-util-dev libnm-glib-vpn-dev は不要なので無視する.
2. 画像のように設定する.

![Screenshot from 2022-07-15 15-20-45](https://user-images.githubusercontent.com/80142550/179235920-1f975cbc-7f20-4517-9a11-5d437a94b096.png)
![Screenshot from 2022-07-15 15-23-52](https://user-images.githubusercontent.com/80142550/179235983-071b75d8-7f9b-4495-95bd-7e99dbcee6cf.png)
![Screenshot from 2022-07-15 15-24-13](https://user-images.githubusercontent.com/80142550/179164438-d84af211-4990-4538-8516-72d92f13610a.png)
![Screenshot from 2022-07-15 15-24-22](https://user-images.githubusercontent.com/80142550/179164441-08144bd2-01cf-4ab2-8dab-b028cdcffc6e.png)
![Screenshot from 2022-07-15 15-24-29](https://user-images.githubusercontent.com/80142550/179164443-a3304eef-a047-4c2c-88b1-b23468fd5d22.png)


論文誌のウェブサイトなどにアクセスすると，東大経由で接続していることは検知してくれるけど，なぜか論文のダウロードができないサイトがある(IEEEなど)．
VirtualBoxにwindowsを入れてそこからVPN接続して対処できるが，根本的な対処は詳しい人にお願いする．


![image](https://github.com/magnetizedCell/lab_notes/assets/80142550/d7dcdc20-da0f-4761-a23f-e5d1fa1a7344)

添付画像のようにすると，192.168.1.14や192.168.1.171のサーバーにのみVPN経由でアクセスし，別のipには自宅の環境から直接アクセスする．
大学当局に見られたくない通信をするときなど
