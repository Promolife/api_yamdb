# Проект «API YaMDb»

## Описание проекта:

- #### Проект YaMDb собирает **отзывы** пользователей на **произведения**.  Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку.

- #### Произведения делятся на Категории , например:
 - - #### «*Книги*»
 - - - #### «*Винни-Пух и все-все-все*» и «*Марсианские хроники*»
 - -  #### «*Фильмы*»
 - - - #### «*Омерзительная Восьмёрка*»
 - - #### «*Музыка*»
 - - - #### «*KISS - I Was Made For Lovin' You*»
 ### Список категорий может быть расширен (например, можно добавить категорию «Изобразительное искусство» или «Ювелирка»).
 ### Произведению может быть так же присвоен **жанр** из списка предустановленных (например, «Сказка», «Рок» или «Артхаус»).
---
### Добавлять произведения, категории и жанры может только администратор.
---

### Благодарные или возмущённые пользователи оставляют к произведениям текстовые **отзывы** и ставят произведению оценку в диапазоне от одного до десяти (целое число); из пользовательских оценок формируется усреднённая оценка произведения — **рейтинг** (целое число). На одно произведение пользователь может оставить только один отзыв.
---

### Пользователи могут оставлять **комментарии** к отзывам. Добавлять отзывы, комментарии и ставить оценки могут только аутентифицированные пользователи.

---
 ## Как запустить проект:
 - #### Клонировать репозиторий и перейти в него в командной строке: ` git@github.com:Promolife/api_yamdb.git`
- #### Cоздать и активировать виртуальное окружение: 
-  - ##### На Mac & Linux: `python3 -m venv env`/ `source env/bin/activate`
-  - ##### На Windows: `python -m venv venv` / `source venv/Scripts/activate`

- #### Установить зависимости из файла requirements.txt:
-  - ##### На Mac & Linux: `python3 -m pip install --upgrade pip` / `pip install -r requirements.txt`
-  - ##### На Windows: `python -m pip install --upgrade pip` / `pip install -r requirements.txt`
- #### Выполнить миграции: 
-  - ##### На Mac & Linux: `python3 manage.py migrate`
- - ##### На Windows: `python manage.py makemigrations` / `python manage.py migrate`
-  #### Запустить проект: 
-  - ##### На Mac & Linux: `python3 manage.py runserver`
-  - ##### На Windows: `python manage.py runserver`
 ---
 ### Над проектом работали:
 <div id="header" align="center">  <img src="https://media.giphy.com/media/TFPdmm3rdzeZ0kP3zG/giphy.gif" width="50"/>  </div>
 
 * [Alpha (Python - Developer) TeamLead .](https://github.com/Promolife)
* [Efesov (Python - Developer)](https://github.com/Efesov)
* [Dmitrij Gribkov(Python - Developer)](https://github.com/we5h)
--- 
<div id="header" align="center">  <img src="https://media.giphy.com/media/LMt9638dO8dftAjtco/giphy.gif" width="300"/>  </div>
