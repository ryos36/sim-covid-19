FILE0=$1
FILE1=$2
TMP_FILE0=tmp0.$$
TMP_FILE1=tmp1.$$
head -1 $FILE0 | xargs -n 1 echo > $TMP_FILE0
head -1 $FILE1 | xargs -n 1 echo > $TMP_FILE1
diff -u $TMP_FILE0 $TMP_FILE1
rm $TMP_FILE0 $TMP_FILE1
