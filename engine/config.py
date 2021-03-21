dict={
  "_comment": "use the config file to store constants, narrative, and-or other fixed variables like dictionaries with feature names, urls, or dates",
  "init_date": "01-01-2020",
  "dictionary": {
    "feature_1": "ID",
    "feature_2": "target"
  },
  "en": {
        "header_1": "Heard-A-Bird: Birdcall Identifier App",
        "intro_1": "Upload your audio (or use pre-loaded mp3's) to get a prediction and sound-alikes. Currently recognizing over 200 most common European species",
        "lang": "Language",
        "Geo": "Source Geo",
        "filename_help": "Model has never seen these",
        "fileupload_help": "Best if length of audiotrack is less than 10min",
        "success_msg": "AI guessed - ",
        "not_guessed_msg": "AI missed the bird: ",
        "uploaded_msg": "Ground Truth of uploaded files unknown",
        "low_certainty_msg": "* - predictions with certainty <5 % considered unreliable",
        "select_mp3": "Select mp3 from validation batch",
        "upload_mp3": "Upload a pre-recorded mp3",
        "top_guess": "Top guess: ",
        "top_5": "Top 5 guesses: "
  },
    "ru": {
        "header_1": "Пернатоугадайка - Сервис аудиоидентификации птиц",
        "intro_1": "Загрузи свою запись или выбери одну из тестовых мп3.",
        "lang": "Язык",
        "Geo": "Локализация",
        "filename_help": "Эти записи модели неизвестны",
        "fileupload_help": "Оптимальная длина аудиозаписи не больше 10 мин",
        "success_msg": "AI угадал - ",
        "not_guessed_msg": "AI не угадал :(  ",
        "uploaded_msg": "Не знаю правильный ответ",
        "low_certainty_msg": "* - Птицы с показателем вероятности <5% считаются неопознаными",
        "select_mp3": "Выбери мп3",
        "upload_mp3": "Загрузи свой мп3",
        "top_guess": "Это :",
        "top_5": "Топ 5 :"
  },
    "uk": {
        "header_1": "Птахоздогадайка - сервіс аудіорозпізнавання пернатих",
        "intro_1": "Загрузи свій запис або вибери один з тестових мп3. Модель розпізнає більше 200 найрозповсюдженіших птахів Європи",
        "lang": "Мова",
        "Geo": "Локація",
        "filename_help": "Ці записи моделі не відомі",
        "fileupload_help": "Найкраще якщо аудіозапис не довший 10хв",
        "success_msg": "AI вгадав - ",
        "not_guessed_msg": "AI не вгадав :(  ",
        "uploaded_msg": "Не знаю правильну відповідь",
        "low_certainty_msg": "* - Зазначені птахи, що мають імовірність <5%, вважаються нерозпізнаними",
        "select_mp3": "Вибери мп3",
        "upload_mp3": "Загрузи свій мп3",
        "top_guess": "Це :",
        "top_5": "Топ 5 :"
    },
  "de": {
        "header_1": "Guess Your Bird - Demo",
        "intro_1": "Select from a set of test mp3's, or use widgets to upload or record your own birb - AI will attempt to guess it!",
        "success_msg": "AI guessed - ",
        "not_guessed_msg": "AI missed the bird: ",
        "low_certainty_msg": "* - predictions with certainty <5 % considered unreliable",
        "uploaded_msg": "Ground Truth of uploaded files unknown",
        "select_mp3": "Select mp3 from validation batch",
        "upload_mp3": "Upload a pre-recorded mp3"
  },
   "fr": {
      "header_1": "Devinez votre oiseau - Demo",
      "intro_1": "Faites votre choix parmi un ensemble de mp3 de test ou utilisez des widgets pour telecharger ou enregistrer votre propre oiseau - l'IA tentera de le deviner!",
      "success_msg": "AI guessed - ",
      "not_guessed_msg": "AI missed the bird: ",
      "low_certainty_msg": "* - predictions with certainty <5 % considered unreliable",
      "uploaded_msg": "Ground Truth of uploaded files unknown",
       "select_mp3": "Select mp3 from validation batch",
      "upload_mp3": "Upload pre-recorded mp3"
    },
    "pl": {
        "header_1": "Co to za ptak?",
        "intro_1": "Wybierz z zestawu testowych plikow MP3 lub uzyj widzetow, aby przeslac wlasnego MP3 - AI sprobuje go odgadnac!",
        "success_msg": "AI guessed - ",
        "lang": "Język",
        "Geo": "Lokalizacja",
        "filename_help": "Model has never seen these",
        "fileupload_help": "Best if length of audiotrack is less than 10min",
        "not_guessed_msg": "AI missed the birb: ",
        "uploaded_msg": "Ground Truth of uploaded files unknown",
        "low_certainty_msg": "* - predictions with certainty <5 % considered unreliable",
        "select_mp3": "Select mp3 from validation batch",
        "upload_mp3": "Upload pre-recorded mp3",
          "top_guess": "Top guess: ",
          "top_5": "Top 5 guesses: "
  }
}

def config_json(dict=dict):
    return dict
