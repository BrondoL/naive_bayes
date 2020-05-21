import base64
import os

def verif_ext_data():
	namafile = input("Masukkan nama file yang berisi data fakta: ")
	cek = namafile.split(".")
	if(base64.b64encode(cek[len(cek)-1].encode("utf-8")).decode("utf-8") != "bmFmaQ=="):
		print("Ekstensi File Salah!")
		exit()
	return namafile

def verif_ext_soal():
	namafile = input("Masukkan nama file yang berisi data testing: ")
	cek = namafile.split(".")
	if(cek[len(cek)-1] != "test"):
		print("Ekstensi File Salah!")
		exit()
	return namafile

def det_attributes(data):
	attributes = data[0]
	attributes = attributes.split(", ")
	return attributes

def det_value(data, n):
	tmp = data[1]
	tmp = tmp.split(", ")
	banyak_data = len(tmp)

	value = []
	for i in range(banyak_data):
		value.append([])
		for j in range(1, n):
			tmp2 = data[j]
			tmp2 = tmp2.split(", ")
			value[i].append(tmp2[i].lower())
	return value

def det_dict_value(attributes,value):
	att = []
	banyak_attibutes = len(attributes)
	for i in range(banyak_attibutes):
		att.append([])
		att[i] = list(dict.fromkeys(value[i]))
	return att

def det_py_pn(attributes, value, att):
	py = []
	pn = []
	banyak_attibutes = len(attributes)
	for x in range(2):
		for i in range(banyak_attibutes-1):
			if(x==0):
				py.append([])
			else:
				pn.append([])
			total = 0
			yes = []
			for j in range(len(att[i])):
				jumlah_yes = 0
				for k in range(len(value[i])):
					if(value[i][k] == att[i][j] and value[banyak_attibutes-1][k] == att[banyak_attibutes-1][x]):
						jumlah_yes = jumlah_yes + 1
				yes.append(jumlah_yes)
			total = 0
			for k in range(len(yes)):
				total = total + yes[k]
			for l in range(len(yes)):
				y = yes[l] / total
				if(x==0):
					py[i].append(y)
				else:
					pn[i].append(y)
		jumlah_yes = 0
		if(x==0):
			n = len(py)
			py.append([])
		else:
			n = len(pn)
			pn.append([])
		for j in range(len(value[banyak_attibutes-1])):
			if(value[banyak_attibutes-1][j] == att[banyak_attibutes-1][x]):
				jumlah_yes = jumlah_yes + 1
		if(x==0):
			py[n].append(jumlah_yes/len(value[banyak_attibutes-1]))
		else:
			pn[n].append(jumlah_yes/len(value[banyak_attibutes-1]))
	return py,pn

def det_indeks_soal(n, soal, att):
	indeks = []
	for i in range(n):
		for j in range(len(att[i])):
			if(soal[i]==att[i][j]):
				indeks.append(j)
	return indeks

def det_pyes_pno(attributes, py, pn, indeks):
	p_yes = 1
	p_no = 1
	banyak_attibutes = len(attributes)
	for i in range(2):
		for j in range(banyak_attibutes-1):
			if(i == 0):
				p_yes = p_yes * py[j][indeks[j]]
			else:
				p_no = p_no * pn[j][indeks[j]]
		if(i == 0):
			p_yes = p_yes * py[len(py)-1][0]
		else:
			p_no = p_no * pn[len(pn)-1][0]
	p_yes_fix = p_yes / (p_yes + p_no)
	p_no = p_no / (p_yes + p_no)
	return p_yes_fix

def decision_maker(p_yes_fix, att):
	if(p_yes_fix == 1):
		print("Keputusan berdasarkan data di atas adalah:", att[len(att)-1][0].capitalize())
	else:
		print("Keputusan berdasarkan data di atas adalah:", att[len(att)-1][1].capitalize())

def print_data(data):
	os.system('clear')
	print("\t\t[ Data ]")
	print()
	for i in range(len(data)):
		print(data[i])
	print()
	print("\t    [ Data Testing ]")
	print()

def print_soal(i, n, data_testing):
	print(i+1, ". ", end='', sep='')
	for j in range(n):
		if(j != n-1):
			print(data_testing[j].capitalize(), ", ", end='', sep='')
		else:
			print(data_testing[j].capitalize())

def banner():
	print("\t\t  https://github.com/BrondoL/naive_bayes")
	print("\t||=====================================================||")
	print("\t||                                                     ||")
	print("\t||      DEVELOPED BY BrondoL aka Aulia Ahmad Nabil     ||")
	print("\t||                                                     ||")
	print("\t||=====================================================||")
	print()
	print("\t\t\t        Naive Bayes")
	print()

def main():
	f = open(verif_ext_data(),"r")
	data = f.read().splitlines()
	f.close()
	n = len(data)

	attributes = det_attributes(data)
	value = det_value(data, n)
	att = det_dict_value(attributes, value)
	py, pn = det_py_pn(attributes, value, att)

	f = open(verif_ext_soal(),"r")
	soal = f.read().splitlines()
	f.close()
	banyak_soal = len(soal)

	print_data(data)

	for i in range(banyak_soal):
		data_testing = soal[i].lower().split(", ")
		n = len(data_testing)
		print_soal(i, n, data_testing)
		indeks = det_indeks_soal(n, data_testing, att)
		p_yes_fix = det_pyes_pno(attributes, py, pn, indeks)
		decision_maker(p_yes_fix, att)
		print()

banner()
main()