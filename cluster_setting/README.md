![名称未設定ファイル drawio(1)](https://user-images.githubusercontent.com/80142550/230250566-6d388fb5-fc54-4642-8f3e-0982e89a18e6.png)

クラスターはControllerとWorkerからなり,[slurm](https://slurm.schedmd.com/documentation.html)によって操作される.

ControllerNodeはslurmのコントローラーであるとともに,Workerのルーターでもある.  
ControllerNodeはローカルip 192.168.1.200を持ち,WorkerNodesはローカルip 200.0.0.0/16を持つ.  
WorkerNodeはその構成によってipアドレスの第3オクテットが異なり,また第4オクテットは1から追加順に振り分ける.  
CPUのみのノードは200.0.0.1,200.0.0.2, ...  
GPU1つのノードは200.0.1.1, 200.0.1.2, ...  
GPU2つのノードは200.0.2.1, 200.0.2.2, ...  
特殊なサーバーは200.0.3.1, 200.0.3.2, ...  
といったふうである.ノードのホスト名も,CPUのみのノードはcpu-1, cpu-2, GPU1つのノードはgpu1-1, gpu1-2, ....などと名付ける. サーバーには固有の名前をつける.

1. 各ユーザーはControllerNodeの自分のアカウントにログインし、[slurmコマンド](https://slurm.schedmd.com/pdfs/summary.pdf)を実行することでジョブを投入する.ControllerNodeの```/archive```, ```/projects```はNSFによってWorkerNodesと共有される。実行プログラムを```/projects```に置き、実行結果を```/archive```に入れるようにする。ControllerNodeはWorkerNodeの秘密鍵を持つ。
2. WorkerNodeはslurmに渡されたジョブを実行する。すべてのWorkerNodeはおなじssh公開鍵を持っており、```worker``` アカウントで作業をおこなう.
3. p100, epyc1はクラスタ以外のユーザーも使う. クラスタから一時的に外す方法は後に記述する.


### 現在わかっている問題点
- Controllerの持つ```/archive```ディレクトリとworkreの通信が遅い  
  現在はControllerとスイッチを10GBase, workerとスイッチを1GBaseでつないでいる.  
  Controllerとworkerが1対1で通信するときは100MBpsくらい出るが，15台のworkerが同時に通信したり，特に```/archive```への書き込みがあるときはかなり遅くなることが予想される．
  
  
### 解決策
1. 必要なデータをworkerのローカルディスクで読み書きし，最終的な計算結果を```/archive```に書き込む
2. 高速ネットワークを用いる.
    - スイッチ: https://nttxstore.jp/_II_QN16322602
    - NIC: https://www.fs.com/jp/products/119649.html
  こんなので25GBps環境を整えたり．なぜかスイッチはこの25GBpsが他の10GBpsより安い(2022/9/6時点)

  スイッチは25GbpsだけどSFP28接続の10GbpsのNICでもつながるはずなのでNICはもっと安いのがあるはず  
    - https://www.oliospec.com/shopdetail/000000008576/ こんなのとか. 流石にこれだけ古いのは爆熱で別途冷却機構を追加することになるので注意
    ```/archive``` はHDDなので10Gbpsあれば十分か．マルチノード計算するときは10Gbpsは遅いかも．
  
  自前で構築するにせよ業者に頼むにせよ，年々機器は安くなるのでいまは1.の方法をとっておく.
  
3. 分散ファイルシステム  
  2.ができていることが前提. GlusterFSとかlustreとか試したい
4. Burst Buffer
5. セキュリティ  
　別に非公開な文書を用意するのでよしなに



### 新ノードを追加したくなったときに注意すること
1. 現在はwake on lanによって遠隔起動を実現しているが,信頼性があまりないし動かなくても保証がなかったりする.  
IPMIやAMD PRO,Intel vProのような遠隔マネジメント機能を持つマシンを推奨する.後者2つはCPUとマザーボードが両方対応していないと意味がないので注意.  
安いノードをたくさん使うのがこのクラスターのコンセプトだが,信頼性が低いマシンをたくさん管理するのは結構大変なのであまり安物は使わないこと.  
既成品を買うなら1台借りたり買って検証するのも良い.



