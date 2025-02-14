import pygame
import requests
import json
import os
import random
from datetime import datetime

# Initialisation de Pygame
pygame.init()
pygame.font.init()

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
FPS = 60

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Fonts
FONT = pygame.font.SysFont('Arial', 32)
SMALL_FONT = pygame.font.SysFont('Arial', 24)

class Player:
    def __init__(self):
        self.name = ""
        self.deck_name = ""
        self.pokemon_team = []
        self.current_pokemon = None
        self.score = 0

class Pokemon:
    def __init__(self, x, y, pokemon_id, pokemon_data, is_player=True):
        self.x = x
        self.y = y
        self.is_player = is_player
        self.width = 100
        self.height = 100
        self.health = 100
        self.max_health = 100
        self.projectiles = []
        self.id = pokemon_id
        self.name = pokemon_data['name']
        
        if self.is_player:
            sprite_url = pokemon_data['sprites']['back_default']
        else:
            sprite_url = pokemon_data['sprites']['front_default']
            
        sprite_response = requests.get(sprite_url)
        sprite_filename = f"pokemon_{pokemon_id}_{'player' if is_player else 'enemy'}.png"
        
        with open(sprite_filename, 'wb') as f:
            f.write(sprite_response.content)
            
        self.sprite = pygame.image.load(sprite_filename)
        self.sprite = pygame.transform.scale(self.sprite, (self.width, self.height))
        
        os.remove(sprite_filename)

    def shoot(self):
        projectile = Projectile(
            self.x + (self.width if not self.is_player else 0),
            self.y + self.height // 2,
            10 if self.is_player else -10
        )
        self.projectiles.append(projectile)

    def update_projectiles(self):
        for projectile in self.projectiles[:]:
            projectile.update()
            if projectile.x < 0 or projectile.x > WINDOW_WIDTH:
                self.projectiles.remove(projectile)

    def draw(self, screen):
        screen.blit(self.sprite, (self.x, self.y))
        # Barre de vie
        pygame.draw.rect(screen, RED, (self.x, self.y - 20, self.width, 10))
        pygame.draw.rect(screen, GREEN, (self.x, self.y - 20, self.width * (self.health / self.max_health), 10))
        for projectile in self.projectiles:
            projectile.draw(screen)

class Projectile:
    def __init__(self, x, y, speed):
        self.x = x
        self.y = y
        self.speed = speed
        self.radius = 5

    def update(self):
        self.x += self.speed

    def draw(self, screen):
        pygame.draw.circle(screen, BLACK, (int(self.x), int(self.y)), self.radius)

    def check_collision(self, pokemon):
        pokemon_rect = pygame.Rect(pokemon.x, pokemon.y, pokemon.width, pokemon.height)
        projectile_rect = pygame.Rect(self.x - self.radius, self.y - self.radius, 
                                    self.radius * 2, self.radius * 2)
        return pokemon_rect.colliderect(projectile_rect)

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Combat Pokémon")
        self.clock = pygame.time.Clock()
        self.state = "WELCOME"
        self.player = Player()
        self.ai_pokemon_team = []
        self.available_pokemon = []
        self.input_text = ""
        self.input_active = "name"
        self.load_available_pokemon()
        self.running = True

    def load_available_pokemon(self):
        # Chargement de 6 Pokémon différents pour la sélection
        pokemon_ids = [1, 4, 7, 25, 6, 9]  # IDs des Pokémon disponibles
        for pokemon_id in pokemon_ids:
            response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{pokemon_id}")
            self.available_pokemon.append(response.json())

    def handle_welcome_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                if self.input_active == "name":
                    self.input_active = "deck"
                elif self.input_active == "deck":
                    self.state = "SELECTION"
            elif event.key == pygame.K_BACKSPACE:
                if self.input_active == "name":
                    self.player.name = self.player.name[:-1]
                else:
                    self.player.deck_name = self.player.deck_name[:-1]
            else:
                if self.input_active == "name":
                    self.player.name += event.unicode
                else:
                    self.player.deck_name += event.unicode

    def handle_selection_input(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            for i, pokemon in enumerate(self.available_pokemon[:6]):
                pokemon_rect = pygame.Rect(100 + i * 120, 200, 100, 100)
                if pokemon_rect.collidepoint(mouse_pos) and len(self.player.pokemon_team) < 3:
                    self.player.pokemon_team.append(pokemon)
                    if len(self.player.pokemon_team) == 3:
                        # L'IA choisit ses Pokémon
                        remaining_pokemon = [p for p in self.available_pokemon if p not in self.player.pokemon_team]
                        self.ai_pokemon_team = random.sample(remaining_pokemon, 3)
                        self.state = "BATTLE"
                        self.setup_battle()

    def setup_battle(self):
        self.player_pokemon = None
        self.ai_pokemon = Pokemon(600, 300, 
                                self.ai_pokemon_team[0]['id'],
                                self.ai_pokemon_team[0], 
                                False)

    def save_game_data(self):
        with open("pokemon.txt", "a") as f:
            f.write(f"Date: {datetime.now()}\n")
            f.write(f"Player: {self.player.name}\n")
            f.write(f"Deck: {self.player.deck_name}\n")
            f.write(f"Pokemon utilisés: {[p['name'] for p in self.player.pokemon_team]}\n")
            f.write(f"Score: {self.player.score}\n")
            f.write("-" * 50 + "\n")

    def handle_battle_input(self, event):
        if self.player_pokemon is None:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for i, pokemon in enumerate(self.player.pokemon_team):
                    pokemon_rect = pygame.Rect(50 + i * 120, 450, 100, 100)
                    if pokemon_rect.collidepoint(mouse_pos):
                        self.player_pokemon = Pokemon(100, 300, 
                                                    pokemon['id'],
                                                    pokemon, 
                                                    True)
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_x:
                self.player_pokemon.shoot()

    def update_battle(self):
        if self.player_pokemon and self.ai_pokemon:
            # Mise à jour des projectiles
            self.player_pokemon.update_projectiles()
            self.ai_pokemon.update_projectiles()

            # IA tire aléatoirement
            if random.random() < 0.02:  # 2% de chance de tirer à chaque frame
                self.ai_pokemon.shoot()

            # Vérification des collisions
            for projectile in self.player_pokemon.projectiles[:]:
                if projectile.check_collision(self.ai_pokemon):
                    self.ai_pokemon.health -= 10
                    self.player_pokemon.projectiles.remove(projectile)

            for projectile in self.ai_pokemon.projectiles[:]:
                if projectile.check_collision(self.player_pokemon):
                    self.player_pokemon.health -= 10
                    self.ai_pokemon.projectiles.remove(projectile)

            # Vérification de la fin du combat
            if self.player_pokemon.health <= 0 or self.ai_pokemon.health <= 0:
                if self.ai_pokemon.health <= 0:
                    self.player.score += 1
                self.save_game_data()
                self.running = False

    def draw_welcome(self):
        self.screen.fill(WHITE)
        name_text = FONT.render(f"Nom: {self.player.name}", True, BLACK)
        deck_text = FONT.render(f"Nom du deck: {self.player.deck_name}", True, BLACK)
        self.screen.blit(name_text, (200, 200))
        self.screen.blit(deck_text, (200, 300))

    def draw_selection(self):
        self.screen.fill(WHITE)
        title = FONT.render("Sélectionnez 3 Pokémon", True, BLACK)
        self.screen.blit(title, (250, 100))
        
        for i, pokemon in enumerate(self.available_pokemon[:6]):
            response = requests.get(pokemon['sprites']['front_default'])
            temp_file = f"temp_pokemon_{i}.png"
            with open(temp_file, 'wb') as f:
                f.write(response.content)
            sprite = pygame.image.load(temp_file)
            sprite = pygame.transform.scale(sprite, (100, 100))
            self.screen.blit(sprite, (100 + i * 120, 200))
            os.remove(temp_file)

        # Affichage de l'équipe sélectionnée
        selected_text = FONT.render("Équipe sélectionnée:", True, BLACK)
        self.screen.blit(selected_text, (250, 350))
        for i, pokemon in enumerate(self.player.pokemon_team):
            name_text = SMALL_FONT.render(pokemon['name'], True, BLACK)
            self.screen.blit(name_text, (100 + i * 120, 400))

    def draw_battle(self):
        self.screen.fill(WHITE)
        if self.player_pokemon is None:
            # Affichage de la sélection du Pokémon pour le combat
            text = FONT.render("Choisissez votre Pokémon", True, BLACK)
            self.screen.blit(text, (250, 400))
            for i, pokemon in enumerate(self.player.pokemon_team):
                response = requests.get(pokemon['sprites']['front_default'])
                temp_file = f"temp_battle_{i}.png"
                with open(temp_file, 'wb') as f:
                    f.write(response.content)
                sprite = pygame.image.load(temp_file)
                sprite = pygame.transform.scale(sprite, (100, 100))
                self.screen.blit(sprite, (50 + i * 120, 450))
                os.remove(temp_file)
        else:
            # Affichage du combat
            self.player_pokemon.draw(self.screen)
            self.ai_pokemon.draw(self.screen)

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif self.state == "WELCOME":
                    self.handle_welcome_input(event)
                elif self.state == "SELECTION":
                    self.handle_selection_input(event)
                elif self.state == "BATTLE":
                    self.handle_battle_input(event)

            if self.state == "WELCOME":
                self.draw_welcome()
            elif self.state == "SELECTION":
                self.draw_selection()
            elif self.state == "BATTLE":
                self.update_battle()
                self.draw_battle()

            pygame.display.flip()
            self.clock.tick(FPS)

if __name__ == "__main__":
    game = Game()
    game.run()
    pygame.quit()