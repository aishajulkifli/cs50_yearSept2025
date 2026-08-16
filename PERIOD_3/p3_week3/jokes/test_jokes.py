import sys
import jokes as tob

def test_args_no():
	sys.argv = ["",]
	l = tob.read_arg()
	assert l == "en"


def test_args_more():
	sys.argv = ["", "-de", "-fr"]
	l = tob.read_arg()
	assert l == "de"
	sys.argv = ["", "de", "-fr"]
	l = tob.read_arg()
	assert l == "en"

def test_args_upper():
	sys.argv = ["", "-FR"]
	l = tob.read_arg()
	assert l == "fr"
	sys.argv = ["", "-Fr"]
	l = tob.read_arg()
	assert l == "fr"

def test_args_minus():
	sys.argv = ["", "de"]
	l = tob.read_arg()
	assert l == "en"
	sys.argv = ["", "-fr"]
	l = tob.read_arg()
	assert l == "fr"

def test_args_list():
	sys.argv = ["", "-kl"]
	l = tob.read_arg()
	assert l == "en"
	sys.argv = ["", "-nl"]
	l = tob.read_arg()
	assert l == "en"

def test_joke_ok():
	j = tob.get_single_joke("de")
	assert type(j) == str

def test_joke_wrong():
	j = tob.get_single_joke("kl")
	assert j.lower() == "Bad joke".lower()
