from kivymd.app import MDApp
from kivy.app import App
from kivy.config import Config
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.animation import Animation
from App_database import App_database
from kivy. uix. button import Button
from kivy. uix. label import Label
from kivymd.uix.button import MDRectangleFlatButton
from kivymd.uix.list import OneLineListItem
from kivymd.uix.list import TwoLineListItem
from kivymd.uix.list import ThreeLineListItem
from kivy.uix.boxlayout import BoxLayout
from Vocabulary_machine import Vocabulary_machine
from kivymd.uix.button import MDRectangleFlatButton
from kivy.core.window import Window
from kivy.graphics import Line
from kivy.graphics import Color
from kivy.graphics import Rectangle
import random

from kivy.lang import Builder

database = None

vocabulary_machine = None



class StartWindow(Screen):

    def Open_animation(self):

        print("The window is open!")




class ModulesViewWindow(Screen):


    def on_open_window(self):

        self.modules = database.Get_all_modules()

        for i in range(len(self.modules)):

            item = Module_Button(text = str(self.modules[i][1]),
                                 on_press = self.choose_module,
                                 font_name = "AverageMono.otf",
                                 color = (0.549, 0.941, 0.627, 1),
                                 background_color = (0, 0, 0, 0),
                                 font_size = 28,
                                 height = 50,
                                 halign = 'left',
                                 )
            item.Button_index = str(i)

            self.modules_list.add_widget(item)


    def choose_module(self, module):

        database.current_module_id = self.modules[int(module.Button_index)][0]
        self.manager.current = 'edit_module'


    def on_close_window(self):

        self.modules_list.clear_widgets()



class Module_Button(Button):

    def __init__(self, **kwargs):
        super(Module_Button, self).__init__(**kwargs)

        self.__button_index = 0


    @property
    def Button_index(self):

        return self.__button_index


    @Button_index.setter
    def Button_index(self, value: int):

        self.__button_index = value





class EditModuleWindow(Screen):

    def on_open_window(self):

        self.is_module_edited = False

        self.module = database.Get_module(database.current_module_id)
        self.words = database.Get_all_words_of_module(database.current_module_id)

        self.name_display.text = self.module[0][1]
        self.description_display.text = self.module[0][2]
        self.author_display.text = self.module[0][3]
        self.total_words.text = "WORDS=" + str(len(self.words))

        for i in range(0, len(self.words)):

            item = ThreeLineListItem(text = str(self.words[i][1]),
                                     secondary_text = str(self.words[i][2]),
                                     tertiary_text = str(self.words[i][3]),
                                     id = str(i),
                                     on_press = self.choose_word)

            self.words_list.add_widget(item)


    def choose_word(self, word):

        database.current_word_id = self.words[int(word.id)][0]
        self.manager.current = 'edit_word'


    def on_edit_button_clicked(self):

        self.name_display.readonly = False
        self.description_display.readonly = False
        self.author_display.readonly = False
        self.is_module_edited = True


    def on_back_button_clicked(self):

        if self.is_module_edited:

            id = database.current_module_id
            new_name = self.name_display.text
            new_description = self.description_display.text
            new_author = self.author_display.text

            database.Edit_module(id, new_name, new_description, new_author)

    def on_close_window(self):

        self.words_list.clear_widgets()


class EditWordWindow(Screen):

    def on_open_window(self):

        self.word = database.Get_word(database.current_word_id)

        self.edit_cyrilic.text = str(self.word[0][1])
        self.edit_latin.text = str(self.word[0][2])
        self.edit_translation.text = str(self.word[0][3])


    def on_delete_button_clicked(self):

        id = database.current_word_id
        database.Delete_word(id)


    def on_close_window(self):

        id = database.current_word_id
        new_cyrilic = self.edit_cyrilic.text
        new_latin = self.edit_latin.text
        new_translation = self.edit_translation.text

        database.Edit_word(id, new_cyrilic, new_latin, new_translation)



class AddModuleWindow(Screen):

    def on_add_module_clicked(self):

        database.Add_module(self.enter_name.text, self.enter_description.text, self.enter_author.text)



class ModuleDeleteWindow(Screen):

    def on_open_window(self):

        id = database.current_module_id
        module = database.Get_module(id)
        self.module_name.text = "ARE YOU SURE YOU WANT TO DELETE MODULE " + str(module[0][1]) + "?"


    def on_Yes_button_clicked(self):

        id = database.current_module_id
        database.Delete_module(id)



class AddWordWindow(Screen):

    def on_open_window(self):

        self.enter_cyrilic.text = ''
        self.enter_latin.text = ''
        self.enter_translation.text = ''

    def on_add_word_clicked(self):

        id = database.current_module_id
        database.Add_word(self.enter_cyrilic.text, self.enter_latin.text, self.enter_translation.text, id)



class ModulesListWindow(Screen):

    def on_open_window(self):

        self.modules = database.Get_all_modules()

        for i in range(0, len(self.modules)):

            left_column = Module_Button(text = str(self.modules[i][1]),
                                 height = 60,
                                 width = self.width - 80,
                                 halign = "left",
                                 background_color = (0, 0, 0, 0),
                                 color = (0.549, 0.941, 0.627, 1),
                                 font_size = 20,
                                 font_name = 'AverageMono.otf',
                                 size_hint_y = None,
                                 on_press = self.open_module)

            left_column.Button_index = i

            module_progress = str(vocabulary_machine.Progress_rate(database.Get_all_words_of_module(self.modules[i][0]))) + "%"

            right_column = Label(text = module_progress,
                                 background_color = (0, 0, 0, 0),
                                 color = (0.549, 0.941, 0.627, 1),
                                 height = 60,
                                 width = 60,
                                 font_size = 20,
                                 font_name = 'AverageMono.otf',
                                 size_hint_y = None)

            self.modules_list.add_widget(left_column)
            self.modules_list.add_widget(right_column)


    def open_module(self, module):

        database.current_module_id = self.modules[int(module.Button_index)][0]
        self.modules_list.clear_widgets()
        self.manager.current = 'introduction_module'


    def on_close_window(self):

        self.modules_list.clear_widgets()



class IntroductionModuleWindow(Screen):

    def on_open_window(self):

        module_id = database.current_module_id
        module = database.Get_module(module_id)
        words_list = database.Get_all_words_of_module(module_id)
        vocabulary_machine.Load_words(words_list)
        progress = vocabulary_machine.Progress_rate(words_list)

        self.name_display.text = module[0][1]
        self.author_display.text = "by " + module[0][3]
        self.description_display.text = module[0][2]
        self.total_words.text = "WORDS = " + str(len(words_list))
        self.progress_label.text = "PROGRESS = " + str(progress) + "%"
        self.alphabet_label.text = str(vocabulary_machine.Alphabet.name)
        self.__name_alpchabet_label()

        if vocabulary_machine.Is_module_learnt():

            self.learn_button.text = "LEARN AGAIN"

        else:

            self.learn_button.text = "LEARN"


    def on_changing_alphabet(self):

        current_alphabet = vocabulary_machine.Alphabet.name

        if current_alphabet == "CYRILIC":

            vocabulary_machine.Alphabet = "LATIN"
            self.__name_alpchabet_label()

        else:

            vocabulary_machine.Alphabet = "CYRILIC"
            self.__name_alpchabet_label()


    def __name_alpchabet_label(self):

        self.alphabet_label.text = str(vocabulary_machine.Alphabet.name)


    def on_learn_button_clicked(self):

        if vocabulary_machine.Is_module_learnt():
            vocabulary_machine.Reset_learning_progress()

        next_page = vocabulary_machine.Next_page()


        if next_page == "U":

            self.manager.current = 'choose_word'

        else:

            self.manager.current = 'typing_answer'



class TypingAnswerWindow(Screen):

    def on_open_window(self):

        self.__is_first_time = True

        self.__clear_window()

        words_states = vocabulary_machine.Calculate_words_states()
        self.__update_progress_bar(words_states)
        self.__display_words_states(words_states)

        self.__current_word = vocabulary_machine.Get_choosed_word()
        self.translation_label.text = self.__current_word[2]


    def on_next_button_clicked(self):

        answer = self.answer_text_input.text

        if self.__is_first_time:
            is_correct = vocabulary_machine.Check_answer(answer)

            if vocabulary_machine.Is_module_learnt():

                words_list = vocabulary_machine.Unload_words()
                database.Save_learning_progress_of_module(words_list)
                self.manager.current = "congratulations"

            elif is_correct:

                self.__go_to_next_page()

            else:

                self.__light_correct_answer()
                self.__is_first_time = False

        elif answer.lower() == self.__current_word[0].lower() or answer.lower() == self.__current_word[1].lower():

            self.__is_first_time = True
            self.__go_to_next_page()


    def on_back_button_clicked(self):

        module_words = vocabulary_machine.Unload_words()
        database.Save_learning_progress_of_module(module_words)


    def __go_to_next_page(self):

        page_type = vocabulary_machine.Next_page()

        if page_type == "U":
            self.manager.current = 'choose_word'

        else:
            self.on_open_window()


    def __clear_window(self):

        self.answer_text_input.text = ""
        self.translation_label.text = ""
        self.translation_label.color = (0.549, 0.941, 0.627, 1)
        self.translation_label.background_color = (0, 0, 0, 0)


    def __update_progress_bar(self, words_states: tuple):

        coef = words_states[2] / (words_states[0] + words_states[1] + words_states[2])
        self.progress_bar.width = self.scale.width * coef


    def __light_correct_answer(self):

        self.translation_label.text = self.__current_word[0] if vocabulary_machine.Alphabet.name == "CYRILIC" else \
        self.__current_word[1]
        self.translation_label.background_color = (0.549, 0.941, 0.627, 1)
        self.translation_label.color = (0, 0, 0, 1)
        self.answer_text_input.text = ""


    def __display_words_states(self, words_states: tuple):

        self.sum_unknown.text = str(words_states[0])
        self.sum_known.text = str(words_states[1])
        self.sum_learned.text = str(words_states[2])



class IncorrectAnswerWindow(Screen):
    pass


class ChooseWordWindow(Screen):

    def on_open_window(self):

        self.__enable_all_buttons()
        self.__blow_out_buttons()

        words_states = vocabulary_machine.Calculate_words_states()
        self.__update_progress_bar(words_states)
        self.__display_words_states(words_states)

        correct_word = vocabulary_machine.Get_choosed_word()
        self.translation_label.text = correct_word[2]

        answer_variants = vocabulary_machine.Get_3_random_words()
        answer_variants.append([correct_word[0], correct_word[1]])

        random.shuffle(answer_variants)


        if vocabulary_machine.Alphabet.name == "CYRILIC":

            self.variant_1.text = answer_variants[0][0]
            self.variant_2.text = answer_variants[1][0]
            self.variant_3.text = answer_variants[2][0]
            self.variant_4.text = answer_variants[3][0]

        else:

            self.variant_1.text = answer_variants[0][1]
            self.variant_2.text = answer_variants[1][1]
            self.variant_3.text = answer_variants[2][1]
            self.variant_4.text = answer_variants[3][1]


    def on_variant_word_clicked(self, button, variant: str):

        is_correct = vocabulary_machine.Check_answer(variant)

        if is_correct:

            self.translation_label.text = "CORRECT!"
            button.background_color = (0.549, 0.941, 0.627, 1)
            button.color = (0, 0, 0, 1)
            button.disabled_color = (0, 0, 0, 1)

        else:

            self.translation_label.text = "INCORRECT!"
            self.__Light_correct_answer()

        self.__disable_all_buttons()
        self.__active_next_button()


    def __Light_correct_answer(self):

        current_word = vocabulary_machine.Get_choosed_word()
        correct_answer = current_word[0] if vocabulary_machine.Alphabet.name == "CYRILIC" else current_word[1]
        variants = list()

        variants.append(self.variant_1)
        variants.append(self.variant_2)
        variants.append(self.variant_3)
        variants.append(self.variant_4)

        for i in range(len(variants)):

            if correct_answer == variants[i].text:

                variants[i].background_color = (0.549, 0.941, 0.627, 1)
                variants[i].color = (0, 0, 0, 1)
                variants[i].disabled_color = (0, 0, 0, 1)


    def __disable_all_buttons(self):

        self.variant_1.disabled = True
        self.variant_2.disabled = True
        self.variant_3.disabled = True
        self.variant_4.disabled = True


    def __enable_all_buttons(self):

        self.variant_1.disabled = False
        self.variant_2.disabled = False
        self.variant_3.disabled = False
        self.variant_4.disabled = False


    def __active_next_button(self):

        self.next_button.disabled = False
        self.color = (0.549, 0.941, 0.627, 1)
        self.disabled_color = (0.549, 0.941, 0.627, 1)


    def __update_progress_bar(self, words_states: tuple):

        coef = words_states[2] / (words_states[0] + words_states[1] + words_states[2])
        self.progress_bar.width = self.scale.width * coef


    def __display_words_states(self, words_states: tuple):

        self.sum_unknown.text = str(words_states[0])
        self.sum_known.text = str(words_states[1])
        self.sum_learned.text = str(words_states[2])


    def __blow_out_buttons(self):

        self.variant_1.background_color = (0, 0, 0, 0)
        self.variant_2.background_color = (0, 0, 0, 0)
        self.variant_3.background_color = (0, 0, 0, 0)
        self.variant_4.background_color = (0, 0, 0, 0)
        self.variant_1.color = (0.549, 0.941, 0.627, 1)
        self.variant_2.color = (0.549, 0.941, 0.627, 1)
        self.variant_3.color = (0.549, 0.941, 0.627, 1)
        self.variant_4.color = (0.549, 0.941, 0.627, 1)
        self.variant_1.disabled_color = (0.549, 0.941, 0.627, 1)
        self.variant_2.disabled_color = (0.549, 0.941, 0.627, 1)
        self.variant_3.disabled_color = (0.549, 0.941, 0.627, 1)
        self.variant_4.disabled_color = (0.549, 0.941, 0.627, 1)


    def on_back_button_clicked(self):

        module_words = vocabulary_machine.Unload_words()
        database.Save_learning_progress_of_module(module_words)


    def go_to_next_page(self):

        page_type = vocabulary_machine.Next_page()

        if page_type == "U":

            self.on_open_window()

        else:
            self.manager.current = 'typing_answer'



class CongratulationsWindow(Screen):

    pass



class WindowManager(ScreenManager):

    def on_open_window(self):

        pass



class SrpskiApp(MDApp):
    def build(self):

        Builder.load_file("srpski.kv")




if __name__ == '__main__':

    database = App_database()

    vocabulary_machine = Vocabulary_machine()

    SrpskiApp().run()

