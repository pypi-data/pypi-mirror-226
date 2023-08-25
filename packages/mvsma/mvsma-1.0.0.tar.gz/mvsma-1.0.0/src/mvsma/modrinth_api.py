from requests import get, post
from json import dumps, loads


class Modrinth:
    '''
    Super simple class to access [modrinth's api](https://api.modrinth.com).
    Only supports requests that does not require authorization.
    '''

    def __init__(self):
        self._apiUrl = "https://api.modrinth.com/v2"
        self.DEFAULT_UA = "mhamsterr/very-simple-modrinth-api (t.me/mhamsterr)"
        self.ua = self.DEFAULT_UA
        self.headers = {
            'Content-Type': 'application/json',
            'User-agent': self.ua
        }
        self.SEARCH_INDEXES = [
            "relevance",
            "downloads",
            "follows",
            "newest",
            "updated"
        ]

    def search(self, query: str, index: str = "", offset: int = 0, limit: int = 10):
        '''
        Search projects by given `query`

        `query` - The query to search for.
        `index` - (Optional, default="relevance") The sorting method used for sorting search results. Possible indices listed in Modrinth.SEARCH_INDEXES
        `offset` - (Optional, default=0) The offset into the search. Skips this number of results.
        `limit` - (Optional, default=10) The number of results returned by the search. Can be int in range [0 .. 100]
        '''
        self._index = index
        if self._index == "":
            self._index = self.SEARCH_INDEXES[0]

        self._searchData = f"?query={query}&index={self._index}&offset={(offset if offset >= 0 else 0)}&limit={(limit if limit >= 0 else 1)}"
        return loads(get(url=(f"{self._apiUrl}/search{self._searchData}"), headers=self.headers).text)

    def project(self, slug: str):
        '''
        Get project by it's "slug"

        `slug` - The ID or slug of the project.
        '''
        return loads(get(url=(f'{self._apiUrl}/project/{slug}'), headers=self.headers).text)

    def projects(self, ids: list[str]):
        '''
        Get multiple projects from list of slugs

        `ids` - The IDs of the projects.
        '''
        self._parsedIds = str(ids).replace(
            "'", '"')  # Because api does not accept single-quotes and returns json error
        return loads(get(url=(f'{self._apiUrl}/projects?ids={self._parsedIds}'), headers=self.headers).text)

    def random_projects(self, count: int = 10):
        '''
        Get list of completly random projects (it can be anything from mods to resourcepacks)

        `count` - (Optional, default=10) The number of random projects to return. Can be int in range [0 .. 100]
        '''
        return loads(get(url=(f'{self._apiUrl}/projects_random?count={count}'), headers=self.headers).text)

    def check_project(self, slug: str):
        '''
        Check if project id/slug is valid

        `slug` - The ID or slug of the project.
        '''
        return loads(get(url=(f'{self._apiUrl}/project/{slug}/check'), headers=self.headers).text)

    def project_dependencies(self, slug: str):
        '''
        Get all of a project's dependencies

        `slug` - The ID or slug of the project.
        '''
        return loads(get(url=(f'{self._apiUrl}/project/{slug}/dependencies'), headers=self.headers).text)

    def project_versions(self, slug: str):
        '''
        List project's versions

        `slug` - The ID or slug of the project.
        '''
        return loads(get(url=(f'{self._apiUrl}/project/{slug}/version'), headers=self.headers).text)

    def version(self, version_id: str):
        '''
        Get a version

        `version_id` - The ID of the version.
        '''
        return loads(get(url=(f'{self._apiUrl}/version/{version_id}'), headers=self.headers).text)

    def project_version(self, slug: str, version_id: str):
        '''
        Get a version given a version number or ID

        `slug` - The ID or slug of the project.
        `version_id` - The version ID or version number.
        '''
        return loads(get(url=(f'{self._apiUrl}/project/{slug}/version/{version_id}'), headers=self.headers).text)

    def versions(self, ids: list[str]):
        '''
        Get multiple versions

        `ids` - The IDs of the versions.
        '''
        self._parsedIds = str(ids).replace(
            "'", '"')  # Because api does not accept single-quotes and returns json error part two
        return loads(get(url=(f'{self._apiUrl}/projects?ids={self._parsedIds}'), headers=self.headers).text)

    def version_file(self, ver_hash: str, mode: str = ""):
        '''
        Get version from hash

        `ver_hash` - The hash of the file, considering its byte content, and encoded in hexadecimal.
        `mode` - (Optional, default="sha1") The algorithm of the hash. Can be "sha1" or "sha512".
        '''
        self._hashMode = mode
        if len(ver_hash) == 40:  # sha1 hash is 40-symbols lenght
            self._hashMode = "sha1"
        elif len(ver_hash) == 128:  # sha512 hash is 128-symbols lenght
            self._hashMode = "sha512"
        # idk what else I can do, if none of this will work then it will be  **your** fault.
        return loads(get(url=(f'{self._apiUrl}/version_file/{ver_hash}?algorithm={self._hashMode}'), headers=self.headers).text)

    def version_files(self, ver_hashes: list[str], mode: str = "sha1"):
        '''
        Get versions from hashes

        `ver_hashes` - The hashes of versions.
        `mode` - (Optional, default="sha1") The algorithm of the hashes. Can be "sha1" or "sha512".
        '''
        self._versionFilesData = {
            'hashes': ver_hashes,
            'algorithm': mode
        }
        return loads(post(f"{self._apiUrl}/version_files", headers=self.headers, data=dumps(self._versionFilesData)).text)

    def version_file_update(self, ver_hash: str, loaders: list[str], game_versions: list[str], mode: str = ""):
        '''
        Latest version of a project from a hash, loader(s), and game version(s)

        `ver_hash` - The hash of the file, considering its byte content, and encoded in hexadecimal. 
        `loaders` - List of mod loaders.
        `game_versions` - List of game versions.
        `mode` - (Optional, default="sha1") The algorithm of the hashes. Can be "sha1" or "sha512".
        '''
        self._hashMode = mode
        if len(ver_hash) == 40:  # sha1 hash is 40-symbols lenght
            self._hashMode = "sha1"
        elif len(ver_hash) == 128:  # sha512 hash is 128-symbols lenght
            self._hashMode = "sha512"
        # the same goes here, if it fails then it's your fault :)
        self._versionFileUpdateData = {
            'loaders': loaders,
            'game_versions': game_versions
        }
        return loads(post(f"{self._apiUrl}/version_file/{ver_hash}/update?algorithm={self._hashMode}", headers=self.headers, data=dumps(self._versionFileUpdateData)).text)

    def version_files_update(self, ver_hashes: list[str], mode: str, loaders: list[str], game_versions: list[str]):
        '''
        Latest versions of multiple project from hashes, loader(s), and game version(s)

        `ver_hashes` - The hashes of versions.
        `mode` - The algorithm of the hashes. Can be "sha1" or "sha512".
        `loaders` - List of mod loaders.
        `game_versions` - List of game versions.
        '''
        # alright, i wont even try to check if your hashe mod is correct for ALL HASHES IN LIST, so just make sure that they are, okay?
        self._versionFilesUpdateData = {
            'hashes': ver_hashes,
            'algorithm': mode,
            'loaders': loaders,
            'game_versions': game_versions
        }
        return loads(post(f"{self._apiUrl}/version_files/update", headers=self.headers, data=dumps(self._versionFilesUpdateData)).text)
