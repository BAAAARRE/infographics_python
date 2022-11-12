from fpdf import FPDF
from PIL import Image


class CustomPDF(FPDF):
    def initiate_pdf(self):
        self.add_font('Montserrat_medium', '', 'assets/fonts/Montserrat-Medium.ttf', uni=True)
        self.add_font('CriteriaCF_bold', '', 'assets/fonts/criteria-cf-bold.ttf', uni=True)
        self.set_auto_page_break(auto=False, margin=0.0)

        self.add_page(orientation='P', format=(248, 143))

    def game_name(self, title):
        self.set_xy(0, 0)
        self.set_font("CriteriaCF_bold", size=20)
        self.cell(0, 35, title, align='C')

    def game_dates(self, full_date):
        self.set_xy(0, 0)
        self.set_font("Montserrat_medium", size=16)
        self.cell(0, 65, full_date, align='C')

    def fix_logo(self):
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

    def nb_participants_subscribes(self, nb_participants, nb_subscribes):
        self.set_font("CriteriaCF_bold", size=10)
        self.set_text_color(16, 194, 220)

        self.set_xy(x=28, y=82.9)
        str_participants = f"{str(nb_participants)} participants /"
        self.cell(w=1, txt=str_participants, align='L')

        self.set_font("Montserrat_medium", size=10)
        self.set_text_color(0, 0, 0)

        x_participants = self.get_x()
        len_str_participants = self.get_string_width(str_participants)
        self.set_xy(x=x_participants + len_str_participants + 2, y=82.9)
        self.cell(w=1, txt=f"{str(nb_subscribes)} registered", align='L')


    def picto_gender(self):
        self.image('assets/images/genders_picto.png', x=118, y=72, w=11)

    def teams(self, nb_teams):
        self.set_font("CriteriaCF_bold", size=30)
        self.set_text_color(16, 194, 220)
        self.set_xy(x=123, y=116)
        self.cell(w=1, txt=str(nb_teams), align='C')


def generate_pdf(data_dict, temp_dir):
    pdf = CustomPDF(unit='mm')
    pdf.initiate_pdf()
    pdf.image('assets/images/background.png', x=9, y=4, w=230)

    # Header
    pdf.game_name(data_dict['header']['name'])
    pdf.game_dates(data_dict['header']['full_date'])
    pdf.fix_logo()

    # Game participation
    pdf.nb_participants_subscribes(data_dict['game_participation']['n_participants'],
                                   data_dict['game_participation']['n_subscribed'])
    pdf.image('{}/participation_rate.png'.format(temp_dir), x=24.6, y=94, w=72)
    pdf.picto_gender()
    pdf.image('{}/genders_picto.png'.format(temp_dir), x=91.3, y=55, w=64)
    pdf.teams(data_dict['game_participation']['n_teams'])
    pdf.image('{}/age.png'.format(temp_dir), x=150, y=76, w=72)

    # Export PDF
    pdf.output('infographic_example.pdf')
