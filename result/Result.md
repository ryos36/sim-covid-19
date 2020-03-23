### 00_Serious
初期のシミュレーション結果。
病床数を限った結果、ピークで 29602 人の重症者が出てしまった。

125日目に重症者数が 2073 を超え、病床のキャパを超える。
```
125 [2065098, 2467, 2149, 123, 2, 45, 3179, 527] 12
```
実際の現場では病床のキャパを超える前に人的キャパを超えるかもしれない。
この時点でまだ大半の人は感染していない

214 日目に感染者数のピークを迎える。 
```
214 [1177868, 139996, 107900, 20780, 388, 202, 598642, 19082] 9130
```
240 日目に重症者のピーク。重症者のピークは感染者のピークの後。
```
240 [794728, 93449, 67532, 29602, 540, 46, 1057002, 9481] 21760
```

319 日目にやっと重症者の数が 2073 を切る。
```
319 [640861, 518, 346, 2026, 60, 2954, 1370113, 46] 56736
```

このシミューレションはあまりに数値を劇的にしてしまったかもしれない。
重症者数が増えたときの致死率が高すぎて、最終的な犠牲者は 56775。
全体の感染率は 66% で収束する。

### 01_ok_bed
前の結果があまりに悲観的過ぎたので比較のためにベッド数が足りた場合
シミュレーションする。

この場合は 194 日目に重症者数のピークを迎えるがベッド数が
足りているという仮定であれば急速に収束する
(そのようにシミュレーションが設計されているともいえる)
```
194, 1215202, 114323, 73753, 9314, 78, 8090, 632831, 17726, 2361
```

感染者のピークもほぼ同時期で 190 日目。
```
190, 1286902, 115652, 75120, 9154, 71, 7528, 558833, 18336, 2075
```

最終的には 5060 の犠牲者となり数値的には落ち着いた感じになる。
感染率は 63% 。結局 r0 に応じた感染率まで広がり続ける可能性がある
ということ。

### 02_Karaburi
day1 を少し短くしてみた。その場合
r0 = 2.0 の設定だとまったく拡散せずに収束する場合がある。
4回続けて早期収束してしまった。
rate=r0/(day1 * around) だったのを
以後、rate = r0/(day2 * around) に変更する

### 03_Serious
day2 で割るようにしたので rate があがった。
そのため急速に感染し最終的におちつくのに 235 日かかっている。
最終的な感染率も 0.87 となる。病床数は足りないと設定したので
82476 の犠牲者をつくってしまった。

たしかにピークをなだらかにすることで重症者の最大値は抑えられる。

### 04_Serious
03_Serious ではいくらなんでも犠牲者を出し過ぎだろう(感情の問題)。
ちょっと明るいシミュレーションをするために serious_rate と dead_rate を
それぞれ半分にしてみた。そうすれば結果として 1/4 となるだろう。

しかし結果は 34548。最終感染率は 90%。
このシミュレーション結果の問題は重症者数がいったん増えるとなかなか
減らないで犠牲者を積み上げてしまう事。これは何を意味するかというと
世の中的には落ち着いても現場では混乱が長く続くことを意味する。

### 05_Serious
04_Serious での最終感染率は 90% と高めなので r0 を調整する。
r0=1.8。ここでいう r0 は医学的な用語ではない。

32744 で 86%。若干、改善された。本来 r0 は人間がコントロールできる
数字ではないのであくまでシミュレーション上の改善だ。

### 06_Serious
spreader_rate を 0.7 にした。
いままで 0.5 。
このレートは無症状の人の割合。結果として重症の人は減るだろう。
これも人間がコントロールできる数字ではない。

最終的には 13915 で 84%。05_Serious の 6割になるかと思ったら
それを下回った。急速に安全に広まったのでそれによりブロックされたか？

なお、プログラム上 if then else を修正した。
いままで 0.5 だったので影響なかった。文字の意味を反映するように
プログラムを修正した。

### 07_ok_bed
06_Serious との比較のために潤沢な病床数に設定。
結果は 1070 で 85%。感染率の1%はシミュレーション上のブレだろう。
ほぼイコールと考えてよい。13905 - 1070 が病床数のパラメタによる差。
10000 を越しているので感情的には受け入れがたい。

この数字はあくまでシミュレーション上の値であり
医学的根拠はまったくないことに注意されたい。

### 08_distance
病床数を元に戻し(06_Serious と比較するため)、
jump_distance_rate = 1.0 にする。
これにより長距離移動をする人がいなくなる。
長距離移動をすると感染空白地帯に感染者が紛れ込む可能性があり
それにより拡散が早くなることが、以前のシミュレーションでわかっている。

結果は 10896 で 84%。2割ほど救える。
やまがなだらかになったからだろう。06_Serious は収束まで 230 日を
要しているが、273 日で 40 日ほどシミュレーションに時間がかかっている。

なおここからプログラム上の表示を少し変えた。
```
sed -e 's/^.//' -e 's/.$//' result.txt 
```
で CSV に変えることが出来る。

### 09_sim_bug
120 目で jump_distance_rate を 0.9 に変えてみた。
82% で 8182。予想に反して 08_distance より値が数は減った。
これはシミュレーション的な課題。
初期段階で治癒した人が拡散していきそれがブロッカーになって
全体の拡散を押さえたものと思われる。
実際の動きとは違うと予測されるので修正の必要がある。

３度シミュレーションしたがばらつきがあることも分かった。

### 10_fix_bug
移動に関してバグがあった(重症者も動いていた)。
修正した。ピークは若干なだらかになったか？