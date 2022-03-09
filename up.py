from filestack import Client
client = Client('AqEIZLLuXSIKyNar09wzjz')

new_filelink = client.upload(filepath='/sdcard/Download/hellminer_cpu_win64_avx/mining.zip')
print(new_filelink.url)

import bitlyshortener

link = [new_filelink.url]
token = ['4e1d5ddf367814209be466e6ab24566fe34895fe']
shortener = bitlyshortener.Shortener(tokens=token, max_cache_size=256)
result = shortener.shorten_urls(link)
print(result)
