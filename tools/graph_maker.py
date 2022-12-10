import os
import plotly.graph_objects as go


class GameParticipationGraphMaker:
    def __init__(self, prepared_data_dict, temp_dir, engine_plotly):
        """
        Init variables
        :param prepared_data_dict: dict. Prepared data
        :param temp_dir: str. Path of temporary directory
        :param engine_plotly: str. Name of engine plotly
        """
        self.prepared_data_dict = prepared_data_dict
        self.temp_dir = temp_dir
        self.engine_plotly = engine_plotly

    def gauge_participation_rate(self):
        """
        Create a gauge chart of participation rate and save it to temporary directory
        :return: go.Figure.
        """
        rate = self.prepared_data_dict['game_participation']['participation_rate']
        fig = go.Figure(
            go.Indicator(
                mode="gauge+number",
                value=rate,
                number={
                    'font': {'size': 120, 'color': "#000000"},
                    'prefix': "<b>",
                    'suffix': " %"
                },
                gauge={
                    'axis': {
                        'range': [0, 100],
                        'visible': False
                    },
                    'bar': {'color': '#10C2DC'},
                    'borderwidth': 0,
                    'steps': [
                        {'range': [0, rate], 'color': '#10C2DC'},
                        {'range': [rate, 100], 'color': '#f3f2f1'},
                    ]
                }
            )
        )

        fig.update_layout(width=800, height=400, paper_bgcolor='rgba(255, 255, 255, 100)',
                          margin=dict(l=0, r=0, t=0, b=0))

        fig.write_image(os.path.join(self.temp_dir, "participation_rate.png"), scale=4, engine=self.engine_plotly)

    def plot_gender_donuts(self):
        """
        Create a donuts chart of gender distribution and save it to temporary directory
        """
        df_gender_agg = self.prepared_data_dict['game_participation']['df_gender_agg']
        fig = go.Figure(
            data=[
                go.Pie(
                    labels=df_gender_agg.index,
                    values=df_gender_agg['percent_player'],
                    marker_colors=['#8280ff', '#10c2dc'],
                    hole=.7,
                    direction='clockwise',
                    sort=False
                )
            ]
        )

        fig.update_traces(
            textposition='outside',
            textfont=dict(size=50, color='black'), automargin=False
        )
        fig.update_layout(showlegend=False, paper_bgcolor='rgba(0, 0, 0, 0)')
        fig.write_image(os.path.join(self.temp_dir, "gender.png"), scale=4, engine=self.engine_plotly)

    def plot_bar_age(self):
        """
        Create a bar chart of age distribution and save it to temporary directory
        """
        df_age_agg = self.prepared_data_dict['game_participation']['df_age_agg']
        fig = go.Figure(
            [
                go.Bar(
                    x=df_age_agg['classe_age'],
                    y=df_age_agg['percent_player'],
                    marker={
                        'color': ['#e7f8fe', '#10c2dc', '#8280ff', '#fe9f51', '#ffe150']
                    }
                )
            ]
        )

        fig.update_yaxes(visible=False, range=[0, max(df_age_agg['percent_player']) * 1.4])
        fig.update_xaxes(tickfont=dict(size=30), tickangle=0)
        fig.update_traces(texttemplate='%{y} %', textposition='outside')
        fig.update_layout(width=700, height=540, plot_bgcolor='rgba(255, 255, 255)', font=dict(size=42, color='black'),
                          uniformtext_mode='hide', margin=dict(l=0, r=0, t=0, b=0))
        fig.write_image(os.path.join(self.temp_dir, "age.png"), scale=4, engine=self.engine_plotly)
