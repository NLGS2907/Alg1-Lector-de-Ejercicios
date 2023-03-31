"""
Módulo para checks auxiliares.
"""

from discord import Interaction, Thread
from discord.app_commands import check as appcheck

from ..db.atajos import get_rol_diego_id, get_rol_docente_id, get_sv_algo1_id


def verificar_rol(interaccion: Interaction) -> bool:
    """
    Verifica si efectivamente existe los roles adecuados.
    """

    return not all((interaccion.guild.id == get_sv_algo1_id(),
                    all([role.id not in (get_rol_diego_id(), get_rol_docente_id())
                         for role in (interaccion.user.roles
                                      if hasattr(interaccion.user, "roles")
                                      else [])]
                        )
                    ))


def es_rol_valido():
    """
    Verifica si está en el servidor del curso, y si es así,
    si se tienen los roles correspondientes.
    """

    return appcheck(verificar_rol)


def es_hilo():
    """
    Verifica si la interacción ocurrió en un hilo.
    """

    def predicado(interaccion: Interaction) -> bool:
        """
        Crea el check correspondiente.
        """

        return isinstance(interaccion.channel, Thread)

    return appcheck(predicado)