from mongoengine import *

connect('eng', host='localhost', port=27017)

class Word(Document):
    category = StringField(required=True)
    original = StringField(required=True)
    translate = StringField(required=True)

def add_word_to_storage(original, translate, category="standart"):
	if (Word.objects(original=original, category=category).count() == 0):
		word = Word(category=category, original=original, translate=translate)
		word.save()
		return True
	else: return False

def get_all_category_words(category):
	return Word.objects(category=category)