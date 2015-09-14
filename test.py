#
# test
# 

urllist = [
	"/controller",
	"/controller/method",
	"/controller/method/arg1",
	"/controller/method/arg1/arg2",
	"/controller/method/arg1/arg2/arg3"
	]


for url in urllist:
	paramlist =[]
	controller = ""
	method = ""
	print(url)
	controller = url.split("/")[1]
	if url.count("/") > 1:
		method = url.split("/")[2]
	if url.count("/") > 2:
		for elem in range(3, url.count("/")+1):
			paramlist.append(url.split("/")[elem])


	print("controller: " + controller)
	print("method: " + method)
	print("params: " + str(paramlist))
	print()

