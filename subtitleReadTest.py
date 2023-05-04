import pysrt
subs = pysrt.open('subs.srt')
for i in subs:
    print(i.text)
    print(i.start)
    print(i.end)
        