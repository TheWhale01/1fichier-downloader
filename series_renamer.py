import os
import shutil
import requests
from requests.models import Response

def parse_env(filename: str = '.env') -> dict:
	env: dict = {
		'lang': 'fr-FR',
	}
	with open(filename, 'r') as file:
		while line := file.readline().strip():
			pair = line.split('=')
			env.update({pair[0]: pair[1]})
	return env

class SeriesRenamer:
	def __init__(self, out_dir: str, env: dict = parse_env(), dl_dir: str = './downloads'):
		self.env: dict = env
		self.out_dir: str = out_dir
		self.headers: dict = {
			'accept': 'application/json',
			'Authorization': f'Bearer {self.env["THE_MOVIE_DB_API"]}'
		}
		self.dl_dir: str = dl_dir
		self.tokens: list = []
		self.serie_name: str = ''
		self.season_nb: int = -1
		self.episode_nb: int = 0
		self.serie_year: int = 0

	def check_year(self) -> int:
		i: int = 0
		while i < len(self.tokens):
			if self.tokens[i].isdigit() and int(self.tokens[i]) >= 1939:
				return i
			i += 1
		return -1	

	def check_season_episode(self) -> int:
		i: int = 0
		while i < len(self.tokens):
			if self.tokens[i].find('S') >= 0 and self.tokens[i].find('E') >= 0:
				return i
			i += 1
		return -1

	def get_season_episode(self, token: str):
		season_nb: str = ''
		episode_nb: str = ''
		try:
			i: int = token.find('S') + 1
			if i < 0:
				raise Exception('Season number not found')
			while i < len(token) and token[i].isdigit():
				season_nb += token[i]
				i += 1
			self.season_nb = int(season_nb)
		except:
			self.season_nb = 0
		try:
			i: int = token.find('E') + 1
			if i < 0:
				raise Exception('Episode number not found')
			while i < len(token) and token[i].isdigit():
				episode_nb += token[i]
				i += 1
			self.episode_nb = int(episode_nb)
		except:
			self.episode_nb = 0

	def get_tokens(self, filename: str):
		separators: str = '._-[]{}\'"|'
		for separator in separators:
			filename = filename.replace(separator, ' ')
		self.tokens = filename.split(' ')
		i: int = 0
		while self.tokens[i].isalpha():
			self.serie_name += (self.tokens[i] + ' ')
			i += 1
		season_episode_index: int = self.check_season_episode()
		serie_year_index: int = self.check_year()
		if season_episode_index > 0:
			self.get_season_episode(self.tokens[season_episode_index])
		if serie_year_index > 0:
			self.serie_year = int(self.tokens[serie_year_index])

	def search(self, serie_name: str, year: int = 0, page: int = 1, include_adult: bool = True) -> dict:
		url: str = f'https://api.themoviedb.org/3/search/tv?query={serie_name}&include_adult={include_adult}&language={self.env["lang"]}&page={page}'
		if year:
			url += f'&first_air_date={year}'
		response: Response = requests.get(url, headers=self.headers)
		response_json: dict = response.json()
		self.serie_year = int(response_json['results'][0]['first_air_date'].split('-')[0])
		self.serie_name = response_json['results'][0]['name']
		return response_json
			
	def rename(self, filename: str):
		self.get_tokens(filename)
		self.search(self.serie_name, self.serie_year)
		filepath: str = os.path.join(self.dl_dir, filename)
		serie_dir: str = f'{self.serie_name} ({self.serie_year})'
		new_name: str = serie_dir
		serie_dir = os.path.join(self.out_dir, serie_dir)
		serie_dir = os.path.join(serie_dir, f'Saison {self.season_nb}')
		if not os.path.exists(serie_dir):
			os.makedirs(serie_dir)
		if self.season_nb and self.episode_nb:
			new_name = new_name + f" S{self.season_nb}E{self.episode_nb}.{self.tokens[-1]}"
		else:
			new_name = os.path.join(serie_dir, filename)
			print('The following file will have to be renamed:')
		new_name = os.path.join(serie_dir, new_name)
		print(f'{filepath} -> {new_name}')
		shutil.move(filepath, new_name)

def main():
		renamer = SeriesRenamer('./')
		renamer.rename('Fallout.S01E01.MULTi.4KLight.DV.HDR10+.WEBRip.DDP5.1.Atmos.HEVC.mkv')

if __name__ == '__main__':
		main()
