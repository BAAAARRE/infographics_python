import os
import shutil
import plotly.io as pio

from tools.load_data import load_data

from config.plotly_styling import custom_template
from tools import data_preparator as dp, graph_maker as gm, pdf


def main():
    # Set and create save dir for temp graphs
    temp_dir = f'{os.getcwd()}/temp'
    os.makedirs(temp_dir, exist_ok=True)

    # Plotly styling
    pio.templates["custom_pg"] = custom_template
    pio.templates.default = 'plotly_white+custom_pg'
    engine_plotly = 'auto'

    # Load Data
    data_raw_dict = load_data()

    # Prepare data
    dp_gp = dp.GameParticipationPreparator(data_raw_dict)
    dp_gp.header()
    dp_gp.participation()
    dp_gp.gender()
    dp_gp.age()
    prepared_data_dict = dp_gp.prepared_data_dict

    # Graphs
    gm_gp = gm.GameParticipationGraphMaker(prepared_data_dict, temp_dir, engine_plotly)
    gm_gp.gauge_participation_rate()
    gm_gp.plot_gender_donuts()
    gm_gp.plot_bar_age()

    # Generate PDF
    pdf_gp = pdf.CustomPDF(prepared_data_dict, temp_dir)
    pdf_gp.initiate_pdf()
    pdf_gp.background()
    pdf_gp.game_name()
    pdf_gp.game_dates()
    pdf_gp.logo()
    pdf_gp.n_participants_and_registered()
    pdf_gp.participation_rate()
    pdf_gp.gender()
    pdf_gp.teams()
    pdf_gp.age()
    pdf_gp.save_pdf()

    # Remove temp directory
    shutil.rmtree(path=temp_dir, ignore_errors=True)


if __name__ == '__main__':
    main()
