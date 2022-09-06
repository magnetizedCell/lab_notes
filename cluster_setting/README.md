
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
