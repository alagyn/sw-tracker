import csv
import json

POSTERS = {
    "Ahsoka": "Ahsoka.jpg",
    "Andor": "Andor.jpg",
    "Clone Wars": "Clone_Wars.jpg",
    "Star Wars: Episode 1 - The Phantom Menace": "Episode1.jpg",
    "Star Wars: Episode 2 - Attack of the Clones": "Episode2.jpg",
    "Star Wars: Episode 3 - Revenge of the Sith": "Episode3.jpg",
    "Star Wars: Episode 4 - A New Hope": "Episode4.jpg",
    "Star Wars: Episode 5 - The Empire Strikes Back": "Episode5.jpg",
    "Star Wars: Episode 6 - Return of the Jedi": "Episode6.jpg",
    "Star Wars: Episode 7 - The Force Awakens": "Episode7.jpg",
    "Star Wars: Episode 8 - The Last Jedi": "Episode8.jpg",
    "Star Wars: Episode 9 - The Rise of Skywalker": "Episode9.jpg",
    "Maul: Shadow Lord": "Maul_Shadow_Lord.jpg",
    "Obi-Wan Kenobi": "Obi_Wan_Kenobi.jpg",
    "Rebels": "Rebels.jpg",
    "Rogue One: A Star Wars Story": "Rogue_One.jpg",
    "Skeleton Crew": "Skeleton_Crew.jpg",
    "Solo: A Star Wars Story": "Solo.jpg",
    "Tales of the Empire": "Tales_of_the_Empire.jpg",
    "Tales of the Jedi": "Tales_of_the_Jedi.jpg",
    "Tales of the Underworld": "Tales_of_the_Underworld.jpg",
    "The Acolyte": "The_Acolyte.jpg",
    "The Bad Batch": "The_Bad_Batch.jpg",
    "The Book of Boba Fett": "The_Book_of_Boba_Fett.jpg",
    "The Clone Wars Theatrical Release": "The_Clone_Wars_Movie.jpg",
    "The Mandalorian": "The_Mandalorian.jpg",
    "The Mandalorian and Grogu": "The_Mandalorian_and_Grogu.jpg",
}


class Entry:

    def __init__(self, series_id: int, title: str, season: int, episode: int,
                 poster: str) -> None:
        self.series_id: int = series_id
        self.title: str = title
        self.season: int = season
        self.episode: int = episode
        # Only used for movies
        self.poster: str = poster

    def to_dict(self) -> dict[str, str | int]:
        out: dict[str, str | int] = {"title": self.title}
        if self.series_id != 0:
            out['series'] = self.series_id
            out['season'] = self.season
            out['episode'] = self.episode
        else:
            out['poster'] = self.poster

        return out


def main():
    with open("timeline-data.csv") as f:
        reader = csv.DictReader(f, delimiter=',', quotechar='"')

        series_list: list[str] = []
        series_ids: dict[str, int] = {}

        title_order: list[Entry] = []

        for row in reader:
            series = str(row["Series"]).strip()
            title = str(row['Title']).strip()
            if len(series) == 0:
                # movie
                entry = Entry(series_id=0,
                              title=title,
                              season=0,
                              episode=0,
                              poster=POSTERS[title])
            else:
                # show
                try:
                    season = int(row['Season'])
                    episode = int(row['Episode'])
                except ValueError:
                    raise RuntimeError(
                        f"Invalid season or episode for '{series}' : '{title}'"
                    )
                try:
                    series_id = series_ids[series]
                except KeyError:
                    series_list.append(series)
                    # set this to the len after append so IDs start at 1
                    series_id = len(series_list)
                    series_ids[series] = series_id

                entry = Entry(series_id=series_id,
                              title=title,
                              season=season,
                              episode=episode,
                              poster='')

            title_order.append(entry)

        # End for row
    # End with open

    out = {
        "series": [{
            "name": x,
            "poster": POSTERS[x]
        } for x in series_list],
        "entries": [x.to_dict() for x in title_order]
    }

    data = json.dumps(out)

    with open("tracker/src/compiled_titles.tsx", mode='w') as f:
        f.write('export const TIMELINE = ')
        f.write(data)


if __name__ == '__main__':
    main()
