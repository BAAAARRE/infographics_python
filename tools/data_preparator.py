class GameParticipationPreparator:
    def __init__(self, raw_data_dict):
        self.raw_data_dict = raw_data_dict
        self.prepared_data_dict = {}

    def header(self):
        """

        :return:
        """
        df_game = self.raw_data_dict['df_game']
        name = df_game['name'][0]
        start_date = df_game['start_date'][0]
        end_date = df_game['end_date'][0]
        full_date = start_date + ' - ' + end_date
        self.prepared_data_dict['header'] = {'name': name, 'full_date': full_date}

    def participation(self):
        """

        :return:
        """
        df_game = self.raw_data_dict['df_game']
        df_player = self.raw_data_dict['df_player']

        n_subscribed = df_player.shape[0]
        n_participants = df_player[df_player['has_participated'] == 1].shape[0]
        participation_rate = int(round(n_participants / n_subscribed, 2) * 100)
        n_teams = df_game['n_teams'][0]

        self.prepared_data_dict['game_participation'] = {'n_subscribed': n_subscribed, 'n_participants': n_participants,
                                                         'participation_rate': participation_rate, 'n_teams': n_teams}

    def gender(self):
        """

        @param df_player_activity_agg:
        @return:
        """
        df_player = self.raw_data_dict['df_player']
        df_gender_agg = df_player.groupby('gender').agg(n_players=('player_uid', 'count'))
        df_gender_agg['percent_player'] = (df_gender_agg / df_player.shape[0]).round(2)
        self.prepared_data_dict['game_participation'].update({'df_gender_agg': df_gender_agg})

    def age(self):
        df_player = self.raw_data_dict['df_player']
        df_age_agg = df_player.groupby('classe_age', as_index=False).agg(n_players=('player_uid', 'count'))
        df_age_agg['percent_player'] = (df_age_agg['n_players'] / df_player.shape[0] * 100).round(0)
        self.prepared_data_dict['game_participation'].update({'df_age_agg': df_age_agg})
