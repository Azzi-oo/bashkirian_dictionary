import sqlite3 as sq


def replace_bashkir_letters(word):
    # Заменить башкирские буквы на соответствующие русские фонемы
    replacements = {'ә': 'э', 'ғ': 'г', 'ҡ': 'к', 'ң': 'н', 'һ': 'х', 'ү': 'у', 'ҙ': 'з', 'ҫ': 'c', 'ө': 'о'}
    for bashkir_letter, russian_phoneme in replacements.items():
        word = word.replace(bashkir_letter, russian_phoneme)
    return word


def remove_special_characters(word):
    special_characters = ['I', 'II', '|']
    for char in special_characters:
        word = word.replace(char, '')
    return word


# def remove_non_letters(word):
#     return ''.join(char for char in word if char.isalpha())


# Подключение к исходной базе данных
with sq.connect('bashkort_test.db') as db_test:
    # source_cursor = db_source.cursor()

    # Получение данных из исходной таблицы
    # source_cursor.execute('SELECT * FROM bash_rus')
    # data = source_cursor.fetchall()

    # Подключение к тестовой базе данных

    test_cursor = db_test.cursor()

    test_cursor.execute('SELECT * FROM bashkort')
    data = test_cursor.fetchall()

        # Добавление новых колонок в тестовую базу данных (если их еще нет)
        # test_cursor.execute('''
        #     CREATE TABLE IF NOT EXISTS bashkort (
        #         id INTEGER PRIMARY KEY,
        #         word_raw TEXT,
        #         word_markup TEXT,
        #         translation_raw TEXT,
        #         translation_markup TEXT
        #     );
        # ''')

        # Перенос данных из исходной таблицы в тестовую
    for row in data:
        word_raw_updated = replace_bashkir_letters(row[1])
        word_markup_updated = replace_bashkir_letters(row[2])

        # word_raw_updated = remove_non_letters(word_raw_updated)
        # word_markup_updated = remove_non_letters(word_markup_updated)

        word_raw_updated = remove_special_characters(word_raw_updated)
        word_markup_updated = remove_special_characters(word_markup_updated)

        test_cursor.execute('''
            UPDATE bashkort
            SET word_raw = ?,
                word_markup = ?
            WHERE id = ?;
        ''', (word_raw_updated, word_markup_updated, row[0]))

            # test_cursor.execute('''
            #     INSERT INTO bashkort (word_raw, word_markup, translation_raw, translation_markup)
            #     VALUES (?, ?, ?, ?);
            # ''', (row[1], row[1], row[2], row[2]))

        # Commit изменений в тестовой базе данных
    db_test.commit()

print("Данные успешно перенесены в тестовую базу данных.")
