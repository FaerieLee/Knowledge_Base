# -*-coding:utf-8-*-


with open("id.csv", mode="r") as reader, open("id1.csv", mode="w", encoding="utf-8") as writer:
	for line in reader:
		id_name_tuple = line.split(',', 2)
		print(line)
		if len(id_name_tuple[1]) > 0 and id_name_tuple[1][0] == '"':
			i = 0
			while i < len(id_name_tuple[1]):
				if id_name_tuple[1][i] == '"':
					i += 1
				else:
					break
			writer.write(id_name_tuple[0]+','+id_name_tuple[1][i-1:])
		else:
			writer.write(line)
