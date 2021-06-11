import shutil
import operator
import os
from PIL import Image, ImageChops
from operator import itemgetter

def process(file_name):
	im = Image.open(file_name,"r")
	# Get the size of the picture
	width, height = im.size

	#convert to RGB
	pixels = im.load()

	d = {}

	for x in range(width):
		for y in range(height):
			if pixels[x,y] not in d:
				d[pixels[x,y]]=1
			else:
				d[pixels[x,y]]+=1
	print(d) 
	sorted_d = sorted(d.items(), key=operator.itemgetter(0))
	background = sorted_d[0][0]
	captcha = sorted_d[1][0]
	print (background, captcha) 

	for x in range(width):
		for y in range(height):
			if pixels[x,y] != captcha:
				pixels[x,y]=0
			else:
				pixels[x,y]=1
	im.putpalette([0, 0, 0,255,255,255])
	#pattern fix
	for x in range(1,width-1,1):
		for y in range(1,height-1,1):
			if (pixels[x,y] != pixels[x-1,y-1]) and (pixels[x,y] != pixels[x+1,y-1]) and (pixels[x,y] != pixels[x-1,y+1]) and (pixels[x,y] != pixels[x+1,y+1]):
				pixels[x,y]=1

	im.save("tmp.png")

def main(file_name):
	print ("[?] Input file:", file_name) 
	process(file_name)
	captcha_filtered = Image.open('tmp.png')
	captcha_filtered = captcha_filtered.convert("P")
	inletter = False
	foundletter = False
	start = 0
	end = 0

	letters = []

	for y in range(captcha_filtered.size[0]): # slice across
		for x in range(captcha_filtered.size[1]): # slice down
			pix = captcha_filtered.getpixel((y,x))
			if pix != 0:
				inletter = True

		if foundletter == False and inletter == True:
			foundletter = True
			start = y

		if foundletter == True and inletter == False:
			foundletter = False
			end = y
			letters.append((start,end))

		inletter = False

	print ("[+] Horizontal positions:", letters) 

	captcha = ""

	if len(letters) == 4:
		file_names = ["d-0.png", "d-3.png", "d-6.png", "d-9.png", "l-c.png", "l-f.png", "l-i.png", "l-m.png", "l-p.png", "l-s.png", "l-v.png", "l-y.png", "u-b.png", "u-E.png", "u-H.png", "u-k.png", "u-N.png", "u-q.png", "u-t.png", "u-w.png", "u-z.png", "d-1.png", "d-4.png", "d-7.png", "l-a.png", "l-d.png", "l-g.png", "l-j.png", "l-n.png", "l-q.png", "l-t.png", "l-w.png", "l-z.png", "u-c.png", "u-f.png", "u-i.png", "u-l.png", "u-o.png", "u-r.png", "u-u.png", "u-x.png", "d-2.png", "d-5.png", "d-8.png", "l-b.png", "l-e.png", "l-h.png", "l-k.png", "l-o.png", "l-r.png", "l-u.png", "l-x.png", "u-A.png", "u-d.png", "u-G.png", "u-J.png", "u-m.png", "u-p.png", "u-s.png", "u-V.png", "u-y.png"]
		for letter in letters:
			im3 = captcha_filtered.crop(( letter[0], 0, letter[1],captcha_filtered.size[1] ))
			im3 = im3.crop((0, 92, im3.size[0], 220))
			base = im3.convert('L')

			class Fit:
				letter = None
				difference = 0

			best = Fit()

			for letter in file_names:
				#print letter
				current = Fit(p) 
				current.letter = letter

				sample_path = "samples/" + letter
				#print sample_path
				sample = Image.open(sample_path).convert('L').resize(base.size)
				difference = ImageChops.difference(base, sample)

				for x in range(difference.size[0]):
					for y in range(difference.size[1]):
						current.difference += difference.getpixel((x, y))

				if not best.letter or best.difference > current.difference:
					best = current

			#final captcha decoded
			tmp = ''
			tp, letter = best.letter.split('-')
			letter = letter.split('.')[0]
			if tp == 'u':
				tmp = letter.upper()
			else:
				tmp = letter
			print ("[+] New leter:", tmp) 
			captcha = captcha + tmp
		print ("[+] Correct captcha:", captcha) 
	else:
		print ("[!] Missing characters in captcha !") 

if __name__ == '__main__':
	main("captcha.png")