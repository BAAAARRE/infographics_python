from fpdf import FPDF
from PIL import Image


class CustomPDF(FPDF):
    def __init__(self, data_dict, temp_dir):
        super().__init__()
        self.data_dict = data_dict
        self.temp_dir = temp_dir

    def initiate_pdf(self):
        self.add_font('Montserrat_medium', '', 'assets/fonts/Montserrat-Medium.ttf', uni=True)
        self.add_font('CriteriaCF_bold', '', 'assets/fonts/criteria-cf-bold.ttf', uni=True)
        self.set_auto_page_break(auto=False, margin=0.0)

        self.add_page(orientation='P', format=(248, 143))

    def background(self):
        self.image('assets/images/background.png', x=9, y=4, w=230)

    def game_name(self):
        name = self.data_dict['header']['name']
        self.set_xy(0, 0)
        self.set_font("CriteriaCF_bold", size=20)
        self.cell(0, 35, name, align='C')

    def game_dates(self):
        full_date = self.data_dict['header']['full_date']
        self.set_xy(0, 0)
        self.set_font("Montserrat_medium", size=16)
        self.cell(0, 65, full_date, align='C')

    def logo(self):
        image_url = 'assets/images/python_logo.png'
        im = Image.open(image_url)
        x, y = im.size
        max_place = 39
        if x > y:
            ratio = y / x
            width = max_place
            height = width * ratio
            y_axis = (max_place - height) / 2
            self.image(x=182, y=y_axis, name=image_url, w=max_place, h=height)

        else:
            ratio = x / y
            margin = 9
            max_place = max_place - margin
            height = max_place
            width = height * ratio
            y_axis = margin / 2
            self.image(x=182, y=y_axis, name=image_url, w=width, h=max_place)

    def n_participants_and_registered(self):
        n_participants = self.data_dict['game_participation']['n_participants']
        n_registered = self.data_dict['game_participation']['n_registered']

        self.set_font("CriteriaCF_bold", size=10)
        self.set_text_color(16, 194, 220)

        self.set_xy(x=28, y=82.9)
        str_participants = f"{str(n_participants)} participants /"
        self.cell(w=1, txt=str_participants, align='L')

        self.set_font("Montserrat_medium", size=10)
        self.set_text_color(0, 0, 0)

        x_participants = self.get_x()
        len_str_participants = self.get_string_width(str_participants)
        self.set_xy(x=x_participants + len_str_participants + 2, y=82.9)
        self.cell(w=1, txt=f"{str(n_registered)} registered", align='L')

    def participation_rate(self):
        self.image(f'{self.temp_dir}/participation_rate.png', x=24.6, y=94, w=72)

    def gender(self):
        self.image('assets/images/genders_picto.png', x=118, y=72, w=11)
        self.image(f'{self.temp_dir}/gender.png', x=91.3, y=55, w=64)

    def teams(self):
        n_teams = self.data_dict['game_participation']['n_teams']
        self.set_font("CriteriaCF_bold", size=30)
        self.set_text_color(16, 194, 220)
        self.set_xy(x=123, y=116)
        self.cell(w=1, txt=str(n_teams), align='C')

    def age(self):
        self.image(f'{self.temp_dir}/age.png', x=150, y=76, w=72)

    def save_pdf(self):
        self.output('infographic_you_made.pdf')
