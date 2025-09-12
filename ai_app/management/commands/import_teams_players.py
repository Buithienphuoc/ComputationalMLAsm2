import pandas as pd
from django.core.management.base import BaseCommand
from ai_app.models import Team, Player


class Command(BaseCommand):
    help = "Import Teams and Players data from CSV files into the database"

    def add_arguments(self, parser):
        parser.add_argument(
            "--teams_csv",
            type=str,
            default="table_teams_data.csv",
            help="Path to teams CSV file",
        )
        parser.add_argument(
            "--players_csv",
            type=str,
            default="table_players_data.csv",
            help="Path to players CSV file",
        )

    def handle(self, *args, **options):
        teams_csv = options["teams_csv"]
        players_csv = options["players_csv"]

        added_teams = updated_teams = 0
        added_players = updated_players = 0

        # === Import Teams ===
        teams_df = pd.read_csv(teams_csv)
        for _, row in teams_df.iterrows():
            team, created = Team.objects.update_or_create(
                name=row["team_name"],
                defaults={
                    "team_avg_goals_per_match": row["team_avg_goals_per_match"],
                    "team_avg_goals_conceded": row["team_avg_goals_conceded"],
                    "team_clean_sheet_rate": row["team_clean_sheet_rate"],
                    "matches_played": row["matches_played"],
                    "goals_scored_total": row["goals_scored_total"],
                    "goals_conceded_total": row["goals_conceded_total"],
                    "clean_sheets": row["clean_sheets"],
                    "team_avg_shots": row["team_avg_shots"],
                },
            )
            if created:
                added_teams += 1
            else:
                updated_teams += 1

        # === Import Players ===
        players_df = pd.read_csv(players_csv)
        for _, row in players_df.iterrows():
            try:
                team = Team.objects.get(name=row["team_name"])
            except Team.DoesNotExist:
                self.stdout.write(
                    self.style.ERROR(f"Skipping player {row['name']} (team {row['team_name']} not found)")
                )
                continue

            player, created = Player.objects.update_or_create(
                player_id=row["player_id"],
                defaults={
                    "name": row["name"],
                    "nationality": row["nationality"],
                    "position": row["position"],
                    "position_encoded": row["position_encoded"],
                    "team": team,
                    "minutes": row["minutes"],
                    "appearances": row["appearances"],
                    "goals": row["goals"],
                    "assists": row["assists"],
                    "shots_total": row["shots_total"],
                    "shots_on": row["shots_on"],
                    "passes_total": row["passes_total"],
                    "passes_key": row["passes_key"],
                    "avg_minutes_played": row["avg_minutes_played"],
                    "shots_per_game": row["shots_per_game"],
                    "conversion_rate": row["conversion_rate"],
                },
            )
            if created:
                added_players += 1
            else:
                updated_players += 1

        # === Summary ===
        self.stdout.write(self.style.SUCCESS("✅ Import completed!"))
        self.stdout.write(self.style.SUCCESS(
            f"Teams → Added: {added_teams}, Updated: {updated_teams}"
        ))
        self.stdout.write(self.style.SUCCESS(
            f"Players → Added: {added_players}, Updated: {updated_players}"
        ))
