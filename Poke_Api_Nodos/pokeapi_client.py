import requests

class PokeAPIClient:
    
    @staticmethod
    def get_evolution_chain(pokemon_name):
        # Obtiene la cadena de evolución completa de un Pokémon desde la PokeAPI, retornando los datos JSON de la cadena evolutiva
        try:
            pokemon_url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name.lower()}"
            pokemon_response = requests.get(pokemon_url)
            
            if pokemon_response.status_code != 200:
                print(f"Error: Pokemon '{pokemon_name}' not found.")
                return None
            
            pokemon_data = pokemon_response.json()
            species_url = pokemon_data['species']['url']
            
            species_response = requests.get(species_url)
            species_data = species_response.json()
            evolution_url = species_data['evolution_chain']['url']
            
            evolution_response = requests.get(evolution_url)
            evolution_data = evolution_response.json()
            
            return evolution_data
        
        except requests.exceptions.RequestException as e:
            print(f"Connection error: {e}")
            return None
        except KeyError as e:
            print(f"Data processing error: {e}")
            return None