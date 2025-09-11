import pandas as pd

class GoalPredictionPipeline:
    def __init__(self, clf1, clf_cap, reg, features,
                 df_players, df_teams, df_train, df_goals_vs_team, threshold=0.3):
        self.clf1 = clf1
        self.clf_cap = clf_cap
        self.reg = reg
        self.features = features
        self.df_players = df_players
        self.df_teams = df_teams
        self.df_train = df_train
        self.df_goals_vs_team = df_goals_vs_team
        self.threshold = threshold

    def build_features(self, player_name, opponent_name, home_team):
        player_row = self.df_players[self.df_players["name"] == player_name]
        if player_row.empty:
            raise ValueError(f"Player {player_name} not found in player_features.csv")
        player_id = player_row.iloc[0]["player_id"]
        player_team = player_row.iloc[0].get("team_name", None)

        player_hist = self.df_train[self.df_train["player_id"] == player_id].sort_values("fixture_id")
        if not player_hist.empty:
            last_row = player_hist.iloc[-1]
            form_goals_lastN = last_row["form_goals_lastN"]
            form_shots_lastN = last_row["form_shots_lastN"]
            form_minutes_lastN = last_row["form_minutes_lastN"]
        else:
            form_goals_lastN = form_shots_lastN = form_minutes_lastN = 0

        row_lookup = self.df_goals_vs_team[
            (self.df_goals_vs_team["player_id"] == player_id) &
            (self.df_goals_vs_team["opposing_team"] == opponent_name)
        ]
        goals_vs_team = row_lookup.iloc[0]["goals_vs_this_team"] if not row_lookup.empty else 0

        team_row = self.df_teams[self.df_teams["team_name"] == player_team] if player_team else pd.DataFrame()
        opp_row = self.df_teams[self.df_teams["team_name"] == opponent_name]
        if opp_row.empty:
            raise ValueError(f"Opponent {opponent_name} not found in team_level_features.csv")

        is_home_match = 1 if player_team == home_team else 0

        feature_row = pd.DataFrame([{
            "position_encoded": player_row.iloc[0]["position_encoded"],
            "avg_minutes_played": player_row.iloc[0]["avg_minutes_played"],
            "shots_per_game": player_row.iloc[0]["shots_per_game"],
            "conversion_rate": player_row.iloc[0]["conversion_rate"],
            "form_goals_lastN": form_goals_lastN,
            "form_shots_lastN": form_shots_lastN,
            "form_minutes_lastN": form_minutes_lastN,
            "team_team_avg_goals_per_match": team_row["team_avg_goals_per_match"].iloc[0] if not team_row.empty else 0,
            "team_team_avg_shots": team_row["team_avg_shots"].iloc[0] if not team_row.empty else 0,
            "opp_team_avg_goals_conceded": opp_row["team_avg_goals_conceded"].iloc[0],
            "opp_team_clean_sheet_rate": opp_row["team_clean_sheet_rate"].iloc[0],
            "goals_vs_this_team": goals_vs_team,
            "is_home_match": is_home_match
        }])

        return feature_row[self.features]

    def predict(self, X):
        try:
            player_name, opponent_name, home_team = [x.strip() for x in X.split(",")]
        except ValueError:
            raise ValueError("Input must be 'player_name,opponent_name,home_team'")
        return self._predict_single(player_name, opponent_name, home_team)

    def _predict_single(self, player_name, opponent_name, home_team):
        X = self.build_features(player_name, opponent_name, home_team)

        # Stage 1
        p_scorer = self.clf1.predict_proba(X)[:, 1][0]
        if p_scorer < self.threshold:
            return 0

        # Stage 2
        cap_pred = self.clf_cap.predict(X)[0]
        if cap_pred == 0:
            return 1

        # Stage 3
        reg_pred = self.reg.predict(X)[0]
        return round(reg_pred)