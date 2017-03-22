kmeans
======
k-means 是一個聚類 (Cluster) 的方式，依照著物以類聚去分群  
流程如下：  
1. 隨機選取data中的k筆資料當作初始群中心c1~ck  
2. 計算每個資料xi 對應到最短距離的群中心 (固定 ci 求解所屬群 Si)  
3. 利用目前得到的分類重新計算群中心 (固定 Si 求解群中心 ci)  
4. 重複step 2,3直到收斂 (達到最大疊代次數 or 群心中移動距離很小)  

###advance k-means
--------------
為解決k-means不穩定問題(初始中心沒選好)而利用重覆多次尋找其sse最小  
(sum of square error每個資料xi 對應到最短距離的群中心的平方總和)  
找到較好的初始點時在帶入k-means做分群。  

### how to choose better k
--------------
根據elbow theorem找到凸出的點為較好的k值，其原理是比較其斜率，ssei-sse/ki-k，k越多，sse則  一定越小，但是尋找sse下降幅度最多的k值就可能是更好的k值。  

### bisecting K means
--------------
二元k-means，其中心思想為從原本一群分成兩群，再從其中一群在分成兩群，直到指定的k群時  
由sse來判斷哪一群誤差有點大該被分群，其效率會比原本的k-means好，原因為只要運算被分到的群  
不用全部去運算。  

### ppt
--------------
[k-means](http://www.slideshare.net/ssuserf88631/k-means-42435149)  
