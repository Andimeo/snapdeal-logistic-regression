d = {}
with open('search_keys', 'r') as f:
	for line in f:
		if len(line.strip()) == 0:
			continue
		key, value = line.strip().split('=', 1)
		value = value.strip()
		if value != '':
			d[value] = d[value] + 1 if d.has_key(value) else 1

l = sorted(d.items(), key=lambda x : x[1], reverse=True)
with open('queries', 'w') as f:
	f.write('\n'.join([str(x[1]) + ' ' + x[0] for x in l]))

