
![名称未設定ファイル drawio](https://user-images.githubusercontent.com/80142550/181688361-11fa1c27-da69-4386-8e63-0510372acaab.png)

クラスターはControllerNodeとWorkerNodeからなり,[slurm](https://slurm.schedmd.com/documentation.html)によって操作される.
ControllerNodeはローカルip 192.168.1.100を持つ.
WorkerNodesはローカルip 192.168.1.101~を持つ.

1. 各ユーザーはControllerNodeの自分のアカウントにログインし、[slurmコマンド](https://slurm.schedmd.com/pdfs/summary.pdf)を実行することでジョブを投入する.ControllerNodeの```/archive```, ```/projects```はNSFによってWorkerNodesと共有される。実行プログラムを```/projects```に置き、実行結果を```/archive```に入れるようにする。ControllerNodeはWorkerNodeの秘密鍵を持つ。
2. WorkerNodeはslurmに渡されたジョブを実行する。すべてのWorkerNodeはssh公開鍵を共有し、```worker``` アカウントで作業をおこなう.
3. p100, epyc1はクラスタ以外のユーザーも使う. クラスタから一時的に外す方法は後に記述する.

   

The cluster is composed of one ControllerNode and multiple WorkerNodes. Batch job is queued and executed by [slurm](https://slurm.schedmd.com/documentation.html).
ControllerNode has its local ip address 192.168.1.100. WorkerNodes have their local ip addresses 192.168.1.101-

1. Each user logs in to his/her account of ControllerNode. And throw jobs using [slurm commands](https://slurm.schedmd.com/pdfs/summary.pdf). ControllerNode's Directories ```/archive``` and ```/projects``` are shared with NSF protocol among WorkerNodes. Put executable programs in ```/projects``` and let calculation results be in ```/archive```. ControllerNode has WorkerNodes' private key.
2. Each WorkerNode executes jobs those are given by slurm. WorkerNodes share the same ssh public key for account ```worker``` .
4. WorkerNodes p100 and epyc1 are used not only by the cluster. Temporal removal of these servers from the cluster will be described.




### 現在わかっている問題点
- Controllerの持つ```/archive```ディレクトリとworkreの通信が遅い  
  現在はControllerとスイッチを10GBase, workerとスイッチを1GBaseでつないでいる.  
  Controllerとworkerが1対1で通信するときは100Mbpsくらい出るが，15台のworkerが同時に通信したり，特に```/archive```への書き込みがあるときはかなり遅くなることが予想される．
  
  
### 解決策
1. 必要なデータをworkerのローカルディスクで読み書きし，最終的な計算結果を```/archive```に書き込む
2. 高速ネットワークを用いる.
    - スイッチ: https://nttxstore.jp/_II_QN16322602
    - NIC: https://www.fs.com/jp/products/119649.html
  こんなので25GBps環境を整えたり．なぜかスイッチはこの25GBpsが他の10GBpsより安い(2022/9/6時点)

  スイッチは25GbpsだけどSFP28接続の10GbpsのNICでもつながるはずなのでNICはもっと安いのがあるはず  
    - https://www.oliospec.com/shopdetail/000000008576/ こんなのとか  
    ```/archive``` はHDDなので10Gbpsあれば十分か．マルチノード計算するときは10Gbpsは遅いかも．
  自前で構築するにせよ業者に頼むにせよ，年々機器は安くなるのでいまは1.の方法をとっておく.
  
3. 分散ファイルシステム
  2.ができていることが前提. GlusterFSとかlustreとか試したい
  
4. セキュリティ
　ちゃんとしないとね
