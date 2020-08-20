import random
import time
import keyboard
import click
import db as db
from utility import flush_input

@click.command()
@click.option('--category', prompt='Виберіть категорію слів', help='Категорія відокремлює окремі мовні пакети.')


def select_category(category):
	"""Select words category."""
	click.clear()
	click.echo('Вибрана категорія мовного пакету %s!' % click.style(category, fg='green', bold=True))
	click.echo(click.style('Виберіть дію:', bold=True) + ' \n * 1. Ввести нове слово. \n * 2. Пройти бігло тестування. \n * 3. Пройти детальне тестуваня (виправлення помилок).')
	while True:
		if keyboard.is_pressed('1'):
			add_word(category)
			break
		elif keyboard.is_pressed('2'):
			start_simple_test(category)
			break
		elif keyboard.is_pressed('3'):
			pass


def add_word(category):
	"""Add words to storage."""
	click.clear()
	flush_input()
	click.echo('Введіть нове слово по формі: ' + click.style('WORD - TRANSLATE', fg="green", bold=True))
	while True:
		word = input()
		try:
			word = word.split(' - ')
			original = word[0]
			translate = word[1]

			if (not db.add_word_to_storage(original, translate, category=category)):
				click.secho('Слово вже існує в рамках категорії!', fg="red")
		except:
			click.secho('Некорректно введено слово!', fg="red")

def start_simple_test(category):
	"""Start simple user test (with passing mistakes)"""
	words = db.get_all_category_words(category)

	if (words.count() < 5):
		click.secho('\nНедостатня кількість слів, потрібно хочаб 5 слова для початку!', fg="red")
		exit()

	#random.shuffle(words)
	mistakes = 0

	for word in words:
		click.clear()
		flush_input()

		user_choice = [word.original]
		click.secho('Виберіть правильний переклад до слова "%s":' % click.style(word.translate, fg='green'), bold=True)
		
		for i in range(random.randint(1, 4)):
			original = random.choice(words).original
			if not original in user_choice:
				user_choice.append(original)

		random.shuffle(user_choice)

		for element in user_choice:
			click.echo('[' + str(user_choice.index(element)) + '] %s' % element.upper())

		answer = input()

		if int(answer) >= len(user_choice):
			mistakes +=1
			continue

		if (user_choice[int(answer)] == word.original): continue
		else:
			click.clear()
			mistakes += 1
			click.secho('Невірна відповідь, повинно бути %s!' % click.style(word.original, fg='green', bold=True), fg='red')
			time.sleep(3) # Затримка після відображення помилки.

	click.clear()
	click.secho('Пройдено, кількість помилок: ' + str(mistakes) + '/' + str(len(words)), fg='red', bold=True)
	

if __name__ == '__main__':
	select_category()