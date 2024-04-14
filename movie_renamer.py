import requests
import shutil
from requests.models import Response
import os

def parse_env(filename: str = '.env') -> dict:
    env: dict = {
        'lang': 'fr-FR',
    }
    with open(filename, 'r') as file:
        while line := file.readline().strip():
            pair = line.split('=')
            env.update({pair[0]: pair[1]})
    return env

class MovieRenamer:
    def __init__(self, env: dict = parse_env(), dl_dir: str = './downloads', out_dir: str = '/data/Movies'):
        self.env: dict = env
        self.out_dir: str = out_dir
        self.headers: dict = {
                'accept': 'application/json',
                'Authorization': f'Bearer {self.env["THE_MOVIE_DB_API"]}'
        }
        self.tokens: list = []
        self.dl_dir: str = dl_dir
        self.movie_name: str = ''
        self.movie_year: int = 0

    def get_tokens(self, filename: str):
        separators: str = '._-[]{}\'"|'
        for separator in separators:
            filename = filename.replace(separator, ' ')
        self.tokens = filename.split(' ')
        i: int = 0
        while self.tokens[i].isalpha():
            self.movie_name += (self.tokens[i] + ' ')
            i += 1
        if self.tokens[i].isdigit() and int(self.tokens[i]) >= 1930:
            self.movie_year = int(self.tokens[i])
        
    def search(self, movie_name: str, year: int = 0, page: int = 1,
               include_adult: bool = True) -> dict:
        url: str = f'https://api.themoviedb.org/3/search/movie?query={movie_name}&include_adult={include_adult}&language={self.env["lang"]}&page={page}'
        if year:
            url += '&year={year}'
        response: Response = requests.get(url, headers=self.headers)
        response_json: dict = response.json()
        response_json['results'][0]['release_date'] = int(response_json['results'][0]['release_date'].split('-')[0])
        return response_json

    def rename(self, filename: str, ):
        self.get_tokens(filename)
        response = self.search(self.movie_name, self.movie_year)
        new_name: str = ''
        filepath: str = os.path.join(self.dl_dir, filename)
        if self.movie_year:
            new_name = f'{response["results"][0]["title"]} ({self.movie_year})'
        else:
            new_name = f'{response["results"][0]["title"]} ({response["results"][0]["release_date"]})'
        new_name = new_name + '/' + (new_name + f'.{self.tokens[-1]}')
        new_name = os.path.join(self.out_dir, new_name)
        if not os.path.exists(os.path.dirname(new_name)):
            os.makedirs(os.path.dirname(new_name))
        print(f'{filepath} -> {new_name}')
        shutil.move(filepath, new_name)

def main():
    renamer = MovieRenamer()
    renamer.rename("Debarquement Immediat 2016 1080p FR X264 AC3-mHDgz.mkv")

if __name__ == '__main__':
    main()
