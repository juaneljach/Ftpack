import urllib
import re

print "\t\t-------------Vextract------------"
print "\t\t-\tBy: @juan_eljach\t-"
print "\t\t-\tFor fun and profit\t-"
print "\t\t---------------------------------\n\n"
regexp = "<version>(.+?)</version>"
pattern = re.compile(regexp)

sensible_file = "language/en-GB/en-GB.xml"
url=str(raw_input("Url: "))
joomla_directory = str(raw_input("Joomla Directory[Default /]:"))

if not joomla_directory:
	joomla_directory = "/"
else:
	pass

try:
	conection = urllib.urlopen(url+joomla_directory+sensible_file)
	code = conection.read()
	version = re.findall(pattern,code)
	print "Joomla Version: " + version[0]
except:
	print "Can't detect version. sorry :("
