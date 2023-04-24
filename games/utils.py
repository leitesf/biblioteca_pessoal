from games.models import Genero


def get_genero_equivalente(genero_steam):
    if genero_steam=='Action':
        return Genero.objects.get_or_create(descricao='Ação')[0]
    elif genero_steam=='Indie':
        return Genero.objects.get_or_create(descricao='Indie')[0]
    elif genero_steam=='Adventure':
        return Genero.objects.get_or_create(descricao='Aventura')[0]
    elif genero_steam=='RPG':
        return Genero.objects.get_or_create(descricao='RPG')[0]
    elif genero_steam=='Strategy':
        return Genero.objects.get_or_create(descricao='Estratégia')[0]
    elif genero_steam=='Simulation':
        return Genero.objects.get_or_create(descricao='Simulação')[0]
    elif genero_steam=='Casual':
        return Genero.objects.get_or_create(descricao='Casual')[0]
    elif genero_steam=='Sports':
        return Genero.objects.get_or_create(descricao='Esportes')[0]
    elif genero_steam=='Racing':
        return Genero.objects.get_or_create(descricao='Corrida')[0]
    else:
        return None