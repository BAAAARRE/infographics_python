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
    dp_gpp = dp.GameParticipationPreparator(data_raw_dict)
    dp_gpp.header()
    dp_gpp.participation()
    dp_gpp.gender()
    dp_gpp.age()
    prepared_data_dict = dp_gpp.prepared_data_dict

    # Graphs
    gm_gpgm = gm.GameParticipationGraphMaker(prepared_data_dict, temp_dir, engine_plotly)
    gm_gpgm.gauge_participation_rate()
    gm_gpgm.plot_gender_donuts()
    gm_gpgm.plot_bar_age()

    # Generate PDF
    pdf.generate_pdf(prepared_data_dict, temp_dir)

    # Remove temp directory
    shutil.rmtree(path=temp_dir, ignore_errors=True)


if __name__ == '__main__':
    main()
