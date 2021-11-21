"""
Módulo dedicado a contener al cliente que procesa solicitudes
a Imgur.
"""

from imgur_python import Imgur, Album
from os.path import splitext

from constantes import CLIENT_CONFIG, MEMES_ALBUM_NAME


class AlbumNoEncontrado(Exception):
    """
    Clase de una excepcion que salta cuando no se encuentra
    un album.
    """

    pass


class MemeImgur(Imgur):
    """
    Clase personalizada para sobrecargar 'Imgur'.
    """

    def __init__(self, config: dict[str, str]=CLIENT_CONFIG):

        super().__init__(config)


    def _get_response_data(self, solicitud: dict) -> dict:
        """
        Atajo para devolver los datos de la respuesta a una solicitud.
        """

        return solicitud["response"]["data"]


    def get_album_por_nombre(self, nombre_a_buscar: str) -> Album:
        """
        Busca y devuelve la primera aparición de un album cuyo
        titulo coincida con el pasado por parametro. De lo contrario,
        devuelve 'None'.
        """

        album_a_devolver = None

        for album in self._get_response_data(self.albums()):

            if not album:

                continue

            if album["title"] == nombre_a_buscar:

                album_a_devolver = self._get_response_data(self.album_get(album["id"]))
                break

        return album_a_devolver


    def cuantas_imagenes(self, titulo_album: str) -> int:
        """
        Devuelve cuantas imagenes hay en el album seleccionado.
        """

        return self.get_album_por_nombre(titulo_album)["images_count"]


    def get_links_imagenes(self, titulo_album: str) -> list[str]:
        """
        Devuelve una lista con los links de todas las imagenes que tiene el
        album de titulo especificado.

        Si no se encuentra el album devuelve una lista vacia.
        """

        album = self.get_album_por_nombre(titulo_album)

        if not album:

            return list()

        imagenes = self._get_response_data(self.album_images(album["id"]))

        return [imagen["link"] for imagen in imagenes]


    def repite_nombre(self, nombre_imagen: str, titulo_album: str=MEMES_ALBUM_NAME) -> bool:
        """
        Se fija si de todas las imágenes disponibles en el album de titulo especificado,
        hay una cuyo nombre de archivo es exactamente igual al pasado por parámetro.
        """

        album = self.get_album_por_nombre(titulo_album)

        if not album:

            raise AlbumNoEncontrado(f"El album '{titulo_album}' no existe o no fue encontrado.")

        for imagen in self._get(self.album_images(album["id"])):

            if splitext(imagen["name"])[0] == splitext(nombre_imagen)[0]: # La extensión del archivo es ignorada

                return True

        return False
