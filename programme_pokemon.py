import pygame
import requests
import json
import os
import random
from datetime import datetime
import math

# On récupère les données du PokéAPI pour la Pokeball 
from io import BytesIO
from PIL import Image

# Initialisation de Pygame
pygame.init()
pygame.font.init()

# j'importe le son de la musique 
pygame.mixer.init() # Initialisation du système audio
pygame.mixer.music.load("music.mp3") # Chargement de la musique
pygame.mixer.music.play(-1) # -1 pour une lecture en boucle

# Constants
WINDOW_WIDTH = 1300
WINDOW_HEIGHT = 800
FPS = 60

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

TYPE_CHART = {
    "Normal": {"Normal": 1, "Feu": 1, "Eau": 1, "Plante": 1, "Electrik": 1, "Glace": 1, "Combat": 1, "Poison": 1, "Sol": 1, "Vol": 1, "Psy": 1, "Insecte": 1, "Roche": 0.5, "Spectre": 0, "Dragon": 1, "Ténèbres": 1, "Acier": 0.5, "Fée": 1},
    "Feu": {"Normal": 1, "Feu": 0.5, "Eau": 0.5, "Plante": 2, "Electrik": 1, "Glace": 2, "Combat": 1, "Poison": 1, "Sol": 1, "Vol": 1, "Psy": 1, "Insecte": 2, "Roche": 0.5, "Spectre": 1, "Dragon": 0.5, "Ténèbres": 1, "Acier": 2, "Fée": 1},
    "Eau": {"Normal": 1, "Feu": 2, "Eau": 0.5, "Plante": 0.5, "Electrik": 1, "Glace": 1, "Combat": 1, "Poison": 1, "Sol": 2, "Vol": 1, "Psy": 1, "Insecte": 1, "Roche": 2, "Spectre": 1, "Dragon": 0.5, "Ténèbres": 1, "Acier": 1, "Fée": 1},
    "Plante": {"Normal": 1, "Feu": 0.5, "Eau": 2, "Plante": 0.5, "Electrik": 1, "Glace": 1, "Combat": 1, "Poison": 0.5, "Sol": 2, "Vol": 0.5, "Psy": 1, "Insecte": 0.5, "Roche": 2, "Spectre": 1, "Dragon": 0.5, "Ténèbres": 1, "Acier": 0.5, "Fée": 1},
    "Electrik": {"Normal": 1, "Feu": 1, "Eau": 2, "Plante": 0.5, "Electrik": 0.5, "Glace": 1, "Combat": 1, "Poison": 1, "Sol": 0, "Vol": 2, "Psy": 1, "Insecte": 1, "Roche": 1, "Spectre": 1, "Dragon": 0.5, "Ténèbres": 1, "Acier": 1, "Fée": 1},
    "Glace": {"Normal": 1, "Feu": 0.5, "Eau": 0.5, "Plante": 2, "Electrik": 1, "Glace": 0.5, "Combat": 1, "Poison": 1, "Sol": 2, "Vol": 2, "Psy": 1, "Insecte": 1, "Roche": 1, "Spectre": 1, "Dragon": 2, "Ténèbres": 1, "Acier": 0.5, "Fée": 1},
    "Combat": {"Normal": 2, "Feu": 1, "Eau": 1, "Plante": 1, "Electrik": 1, "Glace": 2, "Combat": 1, "Poison": 0.5, "Sol": 1, "Vol": 0.5, "Psy": 0.5, "Insecte": 0.5, "Roche": 2, "Spectre": 0, "Dragon": 1, "Ténèbres": 2, "Acier": 2, "Fée": 0.5},
    "Poison": {"Normal": 1, "Feu": 1, "Eau": 1, "Plante": 2, "Electrik": 1, "Glace": 1, "Combat": 1, "Poison": 0.5, "Sol": 0.5, "Vol": 1, "Psy": 1, "Insecte": 1, "Roche": 0.5, "Spectre": 0.5, "Dragon": 1, "Ténèbres": 1, "Acier": 0, "Fée": 2},
    "Sol": {"Normal": 1, "Feu": 2, "Eau": 1, "Plante": 0.5, "Electrik": 2, "Glace": 1, "Combat": 1, "Poison": 2, "Sol": 1, "Vol": 0, "Psy": 1, "Insecte": 0.5, "Roche": 2, "Spectre": 1, "Dragon": 1, "Ténèbres": 1, "Acier": 2, "Fée": 1},
    "Vol": {"Normal": 1, "Feu": 1, "Eau": 1, "Plante": 2, "Electrik": 0.5, "Glace": 1, "Combat": 2, "Poison": 1, "Sol": 1, "Vol": 1, "Psy": 1, "Insecte": 2, "Roche": 0.5, "Spectre": 1, "Dragon": 1, "Ténèbres": 1, "Acier": 0.5, "Fée": 1},
    "Psy": {"Normal": 1, "Feu": 1, "Eau": 1, "Plante": 1, "Electrik": 1, "Glace": 1, "Combat": 2, "Poison": 2, "Sol": 1, "Vol": 1, "Psy": 0.5, "Insecte": 1, "Roche": 1, "Spectre": 1, "Dragon": 1, "Ténèbres": 0, "Acier": 0.5, "Fée": 1},
    "Insecte": {"Normal": 1, "Feu": 0.5, "Eau": 1, "Plante": 2, "Electrik": 1, "Glace": 1, "Combat": 0.5, "Poison": 0.5, "Sol": 1, "Vol": 0.5, "Psy": 2, "Insecte": 1, "Roche": 1, "Spectre": 0.5, "Dragon": 1, "Ténèbres": 2, "Acier": 0.5, "Fée": 0.5},
    "Roche": {"Normal": 1, "Feu": 2, "Eau": 1, "Plante": 1, "Electrik": 1, "Glace": 2, "Combat": 0.5, "Poison": 1, "Sol": 0.5, "Vol": 2, "Psy": 1, "Insecte": 2, "Roche": 1, "Spectre": 1, "Dragon": 1, "Ténèbres": 1, "Acier": 0.5, "Fée": 1},
    "Spectre": {"Normal": 0, "Feu": 1, "Eau": 1, "Plante": 1, "Electrik": 1, "Glace": 1, "Combat": 1, "Poison": 1, "Sol": 1, "Vol": 1, "Psy": 2, "Insecte": 1, "Roche": 1, "Spectre": 2, "Dragon": 1, "Ténèbres": 0.5, "Acier": 1, "Fée": 1},
    "Dragon": {"Normal": 1, "Feu": 1, "Eau": 1, "Plante": 1, "Electrik": 1, "Glace": 1, "Combat": 1, "Poison": 1, "Sol": 1, "Vol": 1, "Psy": 1, "Insecte": 1, "Roche": 1, "Spectre": 1, "Dragon": 2, "Ténèbres": 1, "Acier": 0.5, "Fée": 0},
    "Ténèbres": {"Normal": 1, "Feu": 1, "Eau": 1, "Plante": 1, "Electrik": 1, "Glace": 1, "Combat": 0.5, "Poison": 1, "Sol": 1, "Vol": 1, "Psy": 2, "Insecte": 1, "Roche": 1, "Spectre": 2, "Dragon": 1, "Ténèbres": 0.5, "Acier": 1, "Fée": 0.5},
    "Acier": {"Normal": 1, "Feu": 0.5, "Eau": 0.5, "Plante": 1, "Electrik": 0.5, "Glace": 2, "Combat": 1, "Poison": 1, "Sol": 1, "Vol": 1, "Psy": 1, "Insecte": 1, "Roche": 2, "Spectre": 1, "Dragon": 1, "Ténèbres": 1, "Acier": 0.5, "Fée": 2},
    "Fée": {"Normal": 1, "Feu": 0.5, "Eau": 1, "Plante": 1, "Electrik": 1, "Glace": 1, "Combat": 2, "Poison": 0.5, "Sol": 1, "Vol": 1, "Psy": 1, "Insecte": 1, "Roche": 1, "Spectre": 1, "Dragon": 2, "Ténèbres": 2, "Acier": 0.5, "Fée": 1}
}

TYPE_TRANSLATION = {
    "normal": "Normal",
    "fire": "Feu",
    "water": "Eau",
    "grass": "Plante",
    "electric": "Electrik",
    "ice": "Glace",
    "fighting": "Combat",
    "poison": "Poison",
    "ground": "Sol",
    "flying": "Vol",
    "psychic": "Psy",
    "bug": "Insecte",
    "rock": "Roche",
    "ghost": "Spectre",
    "dragon": "Dragon",
    "dark": "Ténèbres",
    "steel": "Acier",
    "fairy": "Fée"
}

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

class CaptureMinigame:
    def __init__(self, pokemon_data, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.pokemon_data = pokemon_data

        try:
        # Chargez votre image de fond (remplacez 'background.png' par votre fichier)
           self.background = pygame.image.load('background.png')
        # Redimensionnez l'image pour qu'elle corresponde à la taille de l'écran
           self.background = pygame.transform.scale(self.background, (screen_width, screen_height))
        except:
           self.background = None
           print("Erreur lors du chargement de l'image de fond")


        # Chargement du sprite du Pokémon
        sprite_url = pokemon_data['sprites']['front_default']
        response = requests.get(sprite_url)
        sprite_filename = f"temp_pokemon_minigame.png"
        with open(sprite_filename, 'wb') as f:
            f.write(response.content)
        self.pokemon_sprite = pygame.image.load(sprite_filename)
        self.pokemon_sprite = pygame.transform.scale(self.pokemon_sprite, (80, 80))
        os.remove(sprite_filename)
        
        # Chargement de l'image de la Pokéball depuis l'API
        pokeball_url = "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/items/poke-ball.png"
        response = requests.get(pokeball_url)
        if response.status_code == 200:
            pokeball_data = BytesIO(response.content)
            pokeball_image = Image.open(pokeball_data)
            pokeball_filename = "temp_pokeball.png"
            pokeball_image.save(pokeball_filename)
            self.pokeball_sprite = pygame.image.load(pokeball_filename)
            self.pokeball_sprite = pygame.transform.scale(self.pokeball_sprite, (80, 80))
            os.remove(pokeball_filename)
        else:
            self.pokeball_sprite = None
        
        # Position et mouvement du Pokémon
        self.pokemon_x = random.randint(100, screen_width - 100)
        self.pokemon_y = random.randint(100, screen_height - 100)
        self.pokemon_speed = 5
        self.pokemon_direction = random.uniform(0, 2 * math.pi)
        self.pokemon_rect = pygame.Rect(self.pokemon_x, self.pokemon_y, 80, 80)
        
        # Pokéball
        self.pokeball_x = screen_width // 2
        self.pokeball_y = screen_height - 100
        self.pokeball_thrown = False
        self.pokeball_grabbed = False
        self.pokeball_speed = 10
        self.throw_angle = 0
        self.throw_power = 0
        self.gravity = 0.5
        self.throw_velocity_x = 0
        self.throw_velocity_y = 0
        
        # Animation de capture
        self.capture_animation = 0
        self.is_capturing = False
        self.capture_successful = False
        self.pokemon_scale = 1.0
        self.shake_count = 0
        self.shake_direction = 1
        
        # Timer
        self.start_time = pygame.time.get_ticks()
        self.duration = 10000
    
    def update(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.start_time > self.duration and not self.is_capturing:
            return False

        if not self.is_capturing:
            # Mise à jour de la position du Pokémon
            self.pokemon_direction += random.uniform(-0.1, 0.1)
            self.pokemon_x += math.cos(self.pokemon_direction) * self.pokemon_speed
            self.pokemon_y += math.sin(self.pokemon_direction) * self.pokemon_speed
            
            # Maintenir le Pokémon dans l'écran
            if self.pokemon_x < 0 or self.pokemon_x > self.screen_width - 80:
                self.pokemon_direction = math.pi - self.pokemon_direction
            if self.pokemon_y < 0 or self.pokemon_y > self.screen_height - 80:
                self.pokemon_direction = -self.pokemon_direction
                
            self.pokemon_x = max(0, min(self.screen_width - 80, self.pokemon_x))
            self.pokemon_y = max(0, min(self.screen_height - 80, self.pokemon_y))
            self.pokemon_rect.x = self.pokemon_x
            self.pokemon_rect.y = self.pokemon_y

        # Mise à jour de la position de la Pokéball quand elle est lancée
        if self.pokeball_thrown and not self.is_capturing and not self.pokeball_grabbed:
            self.throw_velocity_y += self.gravity
            self.pokeball_x += self.throw_velocity_x
            self.pokeball_y += self.throw_velocity_y
            
            # Vérification de la collision
            pokeball_rect = pygame.Rect(self.pokeball_x - 20, self.pokeball_y - 20, 40, 40)
            if pokeball_rect.colliderect(self.pokemon_rect):
                self.is_capturing = True
                self.capture_animation = 0

        # Animation de capture
        if self.is_capturing:
            self.capture_animation += 1
            if self.capture_animation < 30:
                self.pokemon_scale = max(0.1, 1.0 - (self.capture_animation / 30))
            elif self.capture_animation < 90:
                if (self.capture_animation - 30) % 20 == 0:
                    self.shake_count += 1
                    self.shake_direction *= -1
            else:
                self.capture_successful = True
                return True
                
        return None

    def handle_mouse(self, mouse_pos, mouse_pressed):
        mouse_x, mouse_y = mouse_pos
        
        # Zone de collision pour la Pokéball
        pokeball_rect = pygame.Rect(self.pokeball_x - 20, self.pokeball_y - 20, 40, 40)
        
        if mouse_pressed:  # Si le bouton de la souris est enfoncé
            if not self.pokeball_thrown:
                # Si on clique sur la Pokéball, on la "attrape"
                if pokeball_rect.collidepoint(mouse_x, mouse_y):
                    self.pokeball_grabbed = True
                
                # Si la Pokéball est attrapée, elle suit la souris
                if self.pokeball_grabbed:
                    self.pokeball_x = mouse_x
                    self.pokeball_y = mouse_y
        else:  # Si le bouton de la souris est relâché
            if self.pokeball_grabbed:
                # Calculer la vitesse de lancer basée sur la position de la souris
                dx = mouse_x - self.pokeball_x
                dy = mouse_y - self.pokeball_y
                angle = math.atan2(-dy, dx)
                power = min(20, math.sqrt(dx*dx + dy*dy) / 20)
                
                self.throw_velocity_x = math.cos(angle) * power
                self.throw_velocity_y = math.sin(angle) * power * -1
                self.pokeball_thrown = True
                self.pokeball_grabbed = False

    def draw(self, screen):

        # Affichage du fond bleu
        if self.background:
           screen.blit(self.background, (0, 0))
        else:
        # Fallback : fond de couleur simple si l'image ne charge pas
          screen.fill((135, 206, 235))  # Bleu ciel par exemple


        # Affichage du temps restant
        if not self.is_capturing:
            remaining_time = max(0, (self.duration - (pygame.time.get_ticks() - self.start_time)) / 1000)
            time_text = FONT.render(f"Temps: {remaining_time:.1f}s", True, BLACK)
            screen.blit(time_text, (20, 20))
            
        # Affichage du Pokémon
        if not self.is_capturing:
            screen.blit(self.pokemon_sprite, (self.pokemon_x, self.pokemon_y))
        elif self.capture_animation < 30:
            scaled_size = int(80 * self.pokemon_scale)
            if scaled_size > 0:
                scaled_sprite = pygame.transform.scale(self.pokemon_sprite, (scaled_size, scaled_size))
                screen.blit(scaled_sprite, (self.pokemon_x + (80 - scaled_size)//2, 
                                          self.pokemon_y + (80 - scaled_size)//2))
                
        # Affichage de la Pokéball
        if self.pokeball_sprite:
            if self.is_capturing and self.capture_animation >= 30:
                shake_offset = math.sin(self.capture_animation * 0.2) * 10 * self.shake_direction
                pokeball_x = self.pokemon_x + 20 + shake_offset
            else:
                pokeball_x = self.pokeball_x - 20
                
            pokeball_y = self.pokeball_y - 20 if not self.is_capturing else self.pokemon_y + 20
            
            # Rotation de la Pokéball pendant le vol
            if self.pokeball_thrown and not self.is_capturing:
                angle = (pygame.time.get_ticks() % 360) * 2
                rotated_pokeball = pygame.transform.rotate(self.pokeball_sprite, angle)
                screen.blit(rotated_pokeball, (pokeball_x, pokeball_y))
            else:
                screen.blit(self.pokeball_sprite, (pokeball_x, pokeball_y))
        else:
            # Fallback au dessin de la Pokéball si l'image n'a pas pu être chargée
            pokeball_surface = pygame.Surface((40, 40), pygame.SRCALPHA)
            pygame.draw.circle(pokeball_surface, (203, 0, 0), (20, 20), 20)
            pygame.draw.circle(pokeball_surface, (255, 255, 255), (20, 20), 18)
            pygame.draw.rect(pokeball_surface, (0, 0, 0), (0, 18, 40, 4))
            pygame.draw.circle(pokeball_surface, (0, 0, 0), (20, 20), 6)
            pygame.draw.circle(pokeball_surface, (255, 255, 255), (20, 20), 5)
            screen.blit(pokeball_surface, (pokeball_x, pokeball_y))


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

        self.shots_fired = 0
        self.base_accuracy = 0.80  # 80% de précision initiale
        self.reduced_accuracy = 0.65  # 65% après 4 tirs
        self.accuracy_threshold = 4  # Nombre de tirs avant réduction

        # Attaques spéciales : b = 10 projectiles (à partir de l'API)
        self.special_attack_available = False

        # Stats de base (à partir de l'API)
        self.attack = pokemon_data['stats'][1]['base_stat']
        self.defense = pokemon_data['stats'][2]['base_stat']

        # Type(s) du Pokémon
        self.types = [t['type']['name'].capitalize() for t in pokemon_data['types']]
        # Modifier cette ligne pour traduire les types
        self.types = [TYPE_TRANSLATION[t['type']['name']] for t in pokemon_data['types']]

        

        
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

#================================================================
    def calculate_damage(self, target):
        base_damage = 20  # Dégâts de base du projectile
        
         # Calcul du multiplicateur de type
        type_multiplier = 1
        for attacker_type in self.types:
            for defender_type in target.types:
                if attacker_type in TYPE_CHART and defender_type in TYPE_CHART[attacker_type]:
                    type_multiplier *= TYPE_CHART[attacker_type][defender_type]
        
        damage = ((2 * 50 / 5 + 2) * base_damage * self.attack / target.defense / 50 + 2) * type_multiplier
        
        return max(1, int(damage))
#===================================================================


    def shoot(self):
        self.shots_fired += 1
        current_accuracy = self.get_current_accuracy()
        
        will_hit = random.random() < current_accuracy  # Utilisation cohérente de will_hit
        
        projectile = Projectile(
            x=self.x + (self.width if not self.is_player else 0),
            y=self.y + self.height // 2,
            speed=10 if self.is_player else -10,
            source_pokemon=self,
            will_hit=will_hit
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

    def get_current_accuracy(self):
        if self.shots_fired < self.accuracy_threshold:
            return self.base_accuracy
        return self.reduced_accuracy        

# attaque spéciale : b = 10 projectiles (à partir de l'API)
    def special_attack(self):
     if not self.special_attack_available:
        return

    # Créer 10 projectiles avec différents angles
     for i in range(10):
        angle = random.uniform(-0.3, 0.3)  # Légère dispersion
        speed_modifier = random.uniform(0.8, 1.2)  # Variation de vitesse
        
        projectile = Projectile(
            x=self.x + (self.width if not self.is_player else 0),
            y=self.y + self.height // 2,
            speed=(10 if self.is_player else -10) * speed_modifier,
            source_pokemon=self,
            will_hit=True,
            angle=angle
        )
        self.projectiles.append(projectile)
    
    # Utilisation unique de l'attaque spéciale
     self.special_attack_available = False


class Projectile:
    def __init__(self, x, y, speed, source_pokemon, will_hit , angle=0):
        self.x = x
        self.y = y
        self.initial_y = y
        self.speed = speed
        self.radius = 5
        self.source_pokemon = source_pokemon
        self.will_hit = will_hit  # Utilisation cohérente de will_hit
        self.distance_traveled = 0
        self.deviation = random.uniform(-30, 30) if not will_hit else 0
        self.angle = angle

    def update(self):
        self.x += self.speed * math.cos(self.angle)
        self.y += self.speed * math.sin(self.angle)
        self.distance_traveled += abs(self.speed)
    
        if not self.will_hit:
           curve = math.sin(self.distance_traveled * 0.05) * self.deviation
           self.y = self.initial_y + curve

        

    def check_collision(self, target_pokemon):
        if not self.will_hit:  # Utilisation de will_hit au lieu de hit
            return False
            
        pokemon_rect = pygame.Rect(target_pokemon.x, target_pokemon.y, 
                                 target_pokemon.width, target_pokemon.height)
        projectile_rect = pygame.Rect(self.x - self.radius, self.y - self.radius, 
                                    self.radius * 2, self.radius * 2)
        
        if pokemon_rect.colliderect(projectile_rect):
            damage = self.source_pokemon.calculate_damage(target_pokemon)
            target_pokemon.health -= damage
            return True
        return False

    def draw(self, screen):
        color = BLACK if self.will_hit else (150, 150, 150)  # Utilisation de will_hit au lieu de hit
        pygame.draw.circle(screen, color, (int(self.x), int(self.y)), self.radius)

    
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

        self.capture_minigame = None
        
        self.pokemon_sprites = {}

        self.ai_pokemon = None

        # Positionnement pour la selection des 3 pokémons puis du pokémon seul et mini jeu 
        self.minigame_active = False
        self.minigame_start_time = 0
        self.star = None
        self.player_character = None
        self.minigame_result = None



        self.end_game_result = None  # Pour stocker le résultat de la partie
        self.captured_pokemon = None  # Pour stocker le Pokémon capturé

        pygame.init()
        pygame.font.init()
        pygame.mixer.init()  # Initialisation du système audio

        # Chargement du fond
        try:
            self.background = pygame.image.load("wall2.png")  # Assurez-vous d'avoir cette image
            self.background = pygame.transform.scale(self.background, (WINDOW_WIDTH, WINDOW_HEIGHT))
        except:
            print("Erreur de chargement du fond, utilisation d'un fond uni")
            self.background = None

        # Chargement des sons
        try:
            self.battle_music = pygame.mixer.Sound("music.mp3")  # Musique de fond
            self.shoot_sound = pygame.mixer.Sound("shoot_sound.wav")    # Son de tir
            # Régler le volume de la musique (0.0 à 1.0)
            self.battle_music.set_volume(0.3)
            self.shoot_sound.set_volume(0.5)
            self.battle_music.play(-1)  # -1 pour une lecture en boucle
        except:
            print("Erreur de chargement des sons")
            self.battle_music = None
            self.shoot_sound = None
        
        
    # 2. Modification de la méthode start_minigame pour utiliser le Pokémon sélectionné
    def start_minigame(self):
     self.minigame_active = True
     self.minigame_start_time = pygame.time.get_ticks()
    # Utiliser le Pokémon actuellement sélectionné au lieu du premier de l'équipe
     pokemon_data = None
     for pokemon in self.player.pokemon_team:
         if pokemon['id'] == self.player_pokemon.id:
             pokemon_data = pokemon
             break
    
    # Fallback au premier Pokémon si le Pokémon actuel n'est pas trouvé
     if not pokemon_data and self.player.pokemon_team:
         pokemon_data = self.player.pokemon_team[0]
    
     self.capture_minigame = CaptureMinigame(
         pokemon_data, 
         WINDOW_WIDTH, 
         WINDOW_HEIGHT
     )
     self.minigame_result = None


    def update_minigame(self):
        if not self.minigame_active or not self.capture_minigame:
            return
            
        result = self.capture_minigame.update()
        if result is not None:
            self.minigame_active = False
            self.minigame_result = result
            if result and hasattr(self, 'player_pokemon') and self.player_pokemon:
                self.player_pokemon.special_attack_available = True
                

    def draw_minigame(self):
        if not self.minigame_active or not self.capture_minigame:
            return
            
        self.screen.fill(WHITE)
        instructions = SMALL_FONT.render(
            "Capturez le Pokémon avec la Pokéball pour obtenir l'attaque spéciale!", 
            True, BLACK
        )
        self.screen.blit(instructions, (WINDOW_WIDTH//2 - instructions.get_width()//2, 60))
        
        self.capture_minigame.draw(self.screen)





    def load_available_pokemon(self):
    # Chargement de 50 Pokémon différents pour la sélection
        pokemon_ids = list(range(1, 51))  # IDs des 50 premiers Pokémon
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
            for pokeball in self.pokeballs:
                if not pokeball.captured_pokemon and not pokeball.is_thrown:
                    distance = math.sqrt((mouse_pos[0] - pokeball.x)**2 + 
                                      (mouse_pos[1] - pokeball.y)**2)
                    if distance < pokeball.radius:
                        self.selected_pokeball = pokeball
                        self.dragging = True
                        
        elif event.type == pygame.MOUSEBUTTONUP and self.dragging:
            mouse_pos = pygame.mouse.get_pos()
            for i, pokemon in enumerate(self.available_pokemon[:6]):
                pokemon_rect = pygame.Rect(50 + i * 200, 150, 100, 100)
                if pokemon_rect.collidepoint(mouse_pos):
                    sprite = self.pokemon_sprites.get(pokemon['name'])
                    if sprite:
                        self.selected_pokeball.throw(
                            pokemon_rect.centerx,
                            pokemon_rect.centery,
                            sprite
                        )
                        self.selected_pokeball.captured_pokemon = pokemon
                    
            self.dragging = False
            self.selected_pokeball = None
            
            captured_count = sum(1 for ball in self.pokeballs if ball.captured_pokemon)
            if captured_count == 3:
                self.player.pokemon_team = [ball.captured_pokemon for ball in self.pokeballs]
                remaining_pokemon = [p for p in self.available_pokemon 
                                  if p not in self.player.pokemon_team]
                self.ai_pokemon_team = random.sample(remaining_pokemon, 3)
                self.state = "BATTLE"
                self.setup_battle()


    def setup_battle(self):
     if not hasattr(self, 'player_pokemon'):
        self.player_pokemon = None
    
    # Choisir un nouveau Pokémon adverse aléatoire
     if not self.ai_pokemon or self.state == "END_GAME":
        remaining_pokemon = [p for p in self.available_pokemon 
                           if p not in self.player.pokemon_team]
        if remaining_pokemon:
            new_opponent = random.choice(remaining_pokemon)
            self.ai_pokemon = Pokemon(600, 300, new_opponent['id'], new_opponent, False)

    def save_game_data(self):
        with open("pokemon.txt", "a") as f:
            f.write(f"Date: {datetime.now()}\n")
            f.write(f"Player: {self.player.name}\n")
            f.write(f"Deck: {self.player.deck_name}\n")
            f.write(f"Pokemon utilisés: {[p['name'] for p in self.player.pokemon_team]}\n")
            f.write(f"Score: {self.player.score}\n")
            if self.captured_pokemon:
                f.write(f"Nouveau Pokemon capturé: {self.captured_pokemon['name']}\n")
            f.write("-" * 50 + "\n")

    def handle_battle_input(self, event):
     if self.minigame_active and self.capture_minigame:
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()[0]  # État du bouton gauche de la souris
        self.capture_minigame.handle_mouse(mouse_pos, mouse_pressed)
        return
        
    # Si aucun Pokémon n'est sélectionné
     if self.player_pokemon is None:
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            # Vérifie la zone de clic pour chaque Pokémon de l'équipe
            for i, pokemon in enumerate(self.player.pokemon_team):
                x_pos = 200 + i * 300
                y_pos = 150
                # Zone de clic de 150x150 pixels
                if (x_pos - 75 <= mouse_x <= x_pos + 75 and 
                    y_pos <= mouse_y <= y_pos + 150):
                    # Crée le Pokémon sélectionné
                    self.player_pokemon = Pokemon(100, 300, pokemon['id'], pokemon, True)
                    
                    # Lance le mini-jeu de capture
                    self.start_minigame()
                    break
     else:
        # Gestion des tirs pendant le combat
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Clic gauche
                self.player_pokemon.shoot()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_b and hasattr(self.player_pokemon, 'special_attack_available'):
                if self.player_pokemon.special_attack_available:
                    self.player_pokemon.special_attack()


    def update_battle(self):
     if self.player_pokemon and self.ai_pokemon:
        # Mise à jour des projectiles
        self.player_pokemon.update_projectiles()
        self.ai_pokemon.update_projectiles()

        # Gestion des collisions
        for projectile in self.player_pokemon.projectiles[:]:
            if projectile.check_collision(self.ai_pokemon):
                self.player_pokemon.projectiles.remove(projectile)

        for projectile in self.ai_pokemon.projectiles[:]:
            if projectile.check_collision(self.player_pokemon):
                self.ai_pokemon.projectiles.remove(projectile)

        # IA plus intelligente basée sur les types
        if random.random() < 0.1:  # 2% de chance de tirer par frame
            type_advantage = 1
            for ai_type in self.ai_pokemon.types:
                for player_type in self.player_pokemon.types:
                    if TYPE_CHART.get(ai_type, {}).get(player_type, 1) > 1:
                        type_advantage *= 1.5  

            # IA tire si elle a un avantage de type
            if random.random() < 0.02 * type_advantage:
                self.ai_pokemon.shoot()


        # IA plus intelligente avec précision
        if random.random() < 0.1:
            current_accuracy = self.ai_pokemon.get_current_accuracy()
            type_advantage = 1
            for ai_type in self.ai_pokemon.types:
                for player_type in self.player_pokemon.types:
                    if TYPE_CHART.get(ai_type, {}).get(player_type, 1) > 1:
                        type_advantage *= 1.5

            if random.random() < 0.02 * type_advantage:
                self.ai_pokemon.shoot()        


        # Vérification de la fin du combat
        if self.player_pokemon.health <= 0 or self.ai_pokemon.health <= 0:
            if self.ai_pokemon.health <= 0:
                self.player.score += 1
                self.end_game_result = "WIN"
                self.captured_pokemon = self.ai_pokemon_team[0]
                if self.captured_pokemon not in self.player.pokemon_team:
                    self.player.pokemon_team.append(self.captured_pokemon)
            else:
                self.end_game_result = "LOSE"
            
            self.save_game_data()
            self.state = "END_GAME"  # Assurez-vous que cette ligne est exécutée
            return  # Ajoutez un return ici pour arrêter l'update

    def draw_welcome(self):
        if self.background:
            self.screen.blit(self.background, (0, 0))
        else:
            self.screen.fill(WHITE)
        name_text = FONT.render(f"Nom: {self.player.name}", True, BLACK)
        deck_text = FONT.render(f"Nom du deck: {self.player.deck_name}", True, BLACK)
        self.screen.blit(name_text, (200, 200))
        self.screen.blit(deck_text, (200, 300))

    def draw_selection(self):
        if self.background:
           self.screen.blit(self.background, (0, 0))
        else:
            self.screen.fill(WHITE)
        
        title = FONT.render("Choisissez 3 Pokémon", True, BLACK)
        self.screen.blit(title, (WINDOW_WIDTH//2 - title.get_width()//2, 50))
    
        # Afficher les Pokémon disponibles dans une grille
        rows, cols = 5, 10
        cell_width, cell_height = 120, 120
        selection_count = sum(1 for p in self.available_pokemon if p in self.player.pokemon_team)
    
        for i, pokemon in enumerate(self.available_pokemon[:50]):
            row = i // cols
            col = i % cols
            x_pos = 50 + col * cell_width
            y_pos = 100 + row * cell_height
        
            # Chargement et stockage du sprite
            if pokemon['name'] not in self.pokemon_sprites:
               response = requests.get(pokemon['sprites']['front_default'])
               temp_file = f"temp_pokemon_{i}.png"
               with open(temp_file, 'wb') as f:
                   f.write(response.content)
               sprite = pygame.image.load(temp_file)
               sprite = pygame.transform.scale(sprite, (80, 80))
               self.pokemon_sprites[pokemon['name']] = sprite
               os.remove(temp_file)
        
            # Dessiner un cadre si le Pokémon est sélectionné
            is_selected = pokemon in self.player.pokemon_team
            if is_selected:
                pygame.draw.rect(self.screen, GREEN, (x_pos-5, y_pos-5, 90, 90), 3)
        
            self.screen.blit(self.pokemon_sprites[pokemon['name']], (x_pos, y_pos))
        
            # Affichage du nom
            name_text = SMALL_FONT.render(pokemon['name'].title(), True, BLACK)
            name_x = x_pos + 40 - name_text.get_width()//2
            self.screen.blit(name_text, (name_x, y_pos + 85))
    
            # Instructions
            if selection_count < 3:
                 instructions = SMALL_FONT.render(f"Sélectionnez {3-selection_count} Pokémon de plus", True, BLACK)
            else:
                 instructions = SMALL_FONT.render("Appuyez sur ENTRÉE pour continuer", True, GREEN)
            self.screen.blit(instructions, (WINDOW_WIDTH//2 - instructions.get_width()//2, WINDOW_HEIGHT - 50))


    def draw_battle(self):
     if self.background:
        self.screen.blit(self.background, (0, 0))
     else:
        self.screen.fill(WHITE)
        
     if self.state == "END_GAME":
        self.draw_end_game()
        return
    
     if self.player_pokemon is None:
        # Affichage de la sélection
        text = FONT.render("Choisissez votre Pokémon", True, BLACK)
        self.screen.blit(text, (WINDOW_WIDTH//2 - text.get_width()//2, 50))
        
        # Affichage des Pokémon avec caractéristiques verticales
        for i, pokemon in enumerate(self.player.pokemon_team):
            x_pos = 200 + i * 300
            y_pos = 150
            
            # Charger et afficher le sprite plus grand
            if pokemon['name'] not in self.pokemon_sprites:
                response = requests.get(pokemon['sprites']['front_default'])
                temp_file = f"temp_battle_{i}.png"
                with open(temp_file, 'wb') as f:
                    f.write(response.content)
                sprite = pygame.image.load(temp_file)
                self.pokemon_sprites[pokemon['name']] = sprite
                os.remove(temp_file)
            
            sprite = pygame.transform.scale(self.pokemon_sprites[pokemon['name']], (150, 150))
            self.screen.blit(sprite, (x_pos - 75, y_pos))
            
            # Dessiner un cadre pour indiquer la zone cliquable
            pygame.draw.rect(self.screen, BLACK, (x_pos - 75, y_pos, 150, 150), 2)
            
            # Affichage vertical des stats
            y_stat = y_pos + 160
            
            # Nom
            name_text = FONT.render(pokemon['name'].title(), True, BLACK)
            name_x = x_pos - name_text.get_width()//2
            self.screen.blit(name_text, (name_x, y_stat))
            y_stat += 40
            
            # Types
            types = [TYPE_TRANSLATION.get(t['type']['name'], t['type']['name']) for t in pokemon['types']]
            types_text = SMALL_FONT.render("Type: " + "/".join(types), True, BLACK)
            self.screen.blit(types_text, (x_pos - 75, y_stat))
            y_stat += 30
            
            # Attaque
            atk_text = SMALL_FONT.render(f"Attaque: {pokemon['stats'][1]['base_stat']}", True, BLACK)
            self.screen.blit(atk_text, (x_pos - 75, y_stat))
            y_stat += 30
            
            # Défense
            def_text = SMALL_FONT.render(f"Défense: {pokemon['stats'][2]['base_stat']}", True, BLACK)
            self.screen.blit(def_text, (x_pos - 75, y_stat))
            y_stat += 30
            
            # Vitesse
            spd_text = SMALL_FONT.render(f"Vitesse: {pokemon['stats'][5]['base_stat']}", True, BLACK)
            self.screen.blit(spd_text, (x_pos - 75, y_stat))
     else:
        # Affichage du combat (non modifié)
        self.player_pokemon.draw(self.screen)
        self.ai_pokemon.draw(self.screen)
        
        # Affichage des informations de combat
        player_info = f"{self.player_pokemon.name} - {'/'.join(self.player_pokemon.types)}"
        ai_info = f"{self.ai_pokemon.name} - {'/'.join(self.ai_pokemon.types)}"
        
        player_text = SMALL_FONT.render(player_info, True, BLACK)
        ai_text = SMALL_FONT.render(ai_info, True, BLACK)
        
        self.screen.blit(player_text, (50, 50))
        self.screen.blit(ai_text, (WINDOW_WIDTH - 200, 50))

     if self.player_pokemon:
        accuracy_text = SMALL_FONT.render(
            f"Précision: {int(self.player_pokemon.get_current_accuracy() * 100)}%",
            True, BLACK
        )
        self.screen.blit(accuracy_text, (50, 100))
        
        # Afficher l'information sur la capacité spéciale si elle est disponible
        if hasattr(self.player_pokemon, 'special_attack_available') and self.player_pokemon.special_attack_available:
            special_text = SMALL_FONT.render("Appuyez sur B pour attaque spéciale!", True, GREEN)
            self.screen.blit(special_text, (50, 130))




    # 1. Modification de la méthode draw_end_game pour afficher jusqu'à 20 Pokémon
    def draw_end_game(self):
     if self.background:
        self.screen.blit(self.background, (0, 0))
     else:
        self.screen.fill(WHITE)
    
    # Titre
     if self.end_game_result == "WIN":
        title = FONT.render("Victoire!", True, GREEN)
        subtitle = FONT.render("Vous avez capturé un nouveau Pokémon!", True, BLACK)
     else:
        title = FONT.render("Défaite!", True, RED)
        subtitle = FONT.render("Continuez à vous entraîner!", True, BLACK)
        
     self.screen.blit(title, (WINDOW_WIDTH // 2 - title.get_width() // 2, 50))
     self.screen.blit(subtitle, (WINDOW_WIDTH // 2 - subtitle.get_width() // 2, 100))

    # Affichage de votre équipe (modifié pour afficher jusqu'à 20 Pokémon)
     team_title = FONT.render("Votre équipe:", True, BLACK)
     self.screen.blit(team_title, (50, 150))

    # Organisation en grille pour afficher plus de Pokémon
     pokemon_per_row = 6
     pokemon_size = 80
     horizontal_spacing = 100
     vertical_spacing = 130
    
     for i, pokemon in enumerate(self.player.pokemon_team):
        row = i // pokemon_per_row
        col = i % pokemon_per_row
        x_position = 50 + col * horizontal_spacing
        y_position = 200 + row * vertical_spacing
        
        # Charger et afficher le sprite
        response = requests.get(pokemon['sprites']['front_default'])
        temp_file = f"temp_end_game_{i}.png"
        with open(temp_file, 'wb') as f:
            f.write(response.content)
        sprite = pygame.image.load(temp_file)
        sprite = pygame.transform.scale(sprite, (pokemon_size, pokemon_size))
        self.screen.blit(sprite, (x_position, y_position))
        
        # Nom du Pokémon
        name = SMALL_FONT.render(pokemon['name'], True, BLACK)
        self.screen.blit(name, (x_position, y_position + pokemon_size + 5))
        
        os.remove(temp_file)

    # Affichage du Pokémon capturé si victoire
     if self.end_game_result == "WIN" and self.captured_pokemon:
        captured_title = FONT.render("Pokémon capturé:", True, BLACK)
        
        # Positionnement du Pokémon capturé en bas à droite
        capture_x = WINDOW_WIDTH - 200
        capture_y = WINDOW_HEIGHT - 180
        self.screen.blit(captured_title, (capture_x, capture_y - 50))
        
        response = requests.get(self.captured_pokemon['sprites']['front_default'])
        temp_file = "temp_captured.png"
        with open(temp_file, 'wb') as f:
            f.write(response.content)
        sprite = pygame.image.load(temp_file)
        sprite = pygame.transform.scale(sprite, (100, 100))
        self.screen.blit(sprite, (capture_x, capture_y))
        
        name = SMALL_FONT.render(self.captured_pokemon['name'], True, BLACK)
        self.screen.blit(name, (capture_x, capture_y + 110))
        
        os.remove(temp_file)

    # Options de fin de partie
     y_options = WINDOW_HEIGHT - 100
     replay_text = FONT.render("R - Rejouer avec un autre Pokémon", True, BLACK)
     quit_text = FONT.render("Q - Quitter le jeu", True, BLACK)
     self.screen.blit(replay_text, (WINDOW_WIDTH // 2 - replay_text.get_width() // 2, y_options))
     self.screen.blit(quit_text, (WINDOW_WIDTH // 2 - quit_text.get_width() // 2, y_options + 50))


    def handle_selection_input(self, event):
     if event.type == pygame.MOUSEBUTTONDOWN:
        mouse_pos = pygame.mouse.get_pos()
        rows, cols = 5, 10
        cell_width, cell_height = 120, 120
        
        for i, pokemon in enumerate(self.available_pokemon[:50]):
            row = i // cols
            col = i % cols
            x_pos = 50 + col * cell_width
            y_pos = 100 + row * cell_height
            pokemon_rect = pygame.Rect(x_pos, y_pos, 80, 80)
            
            if pokemon_rect.collidepoint(mouse_pos):
                if pokemon in self.player.pokemon_team:
                    self.player.pokemon_team.remove(pokemon)
                elif len(self.player.pokemon_team) < 3:
                    self.player.pokemon_team.append(pokemon)
    
     elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
        if len(self.player.pokemon_team) == 3:
            remaining_pokemon = [p for p in self.available_pokemon 
                              if p not in self.player.pokemon_team]
            self.ai_pokemon_team = random.sample(remaining_pokemon, 3)
            self.state = "BATTLE"
            self.setup_battle()

    def run(self):
     try:    
        if self.battle_music:
            self.battle_music.play(-1)

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif self.state == "END_GAME":
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_r:  # Rejouer
                            # Réinitialiser pour un nouveau combat
                            self.player_pokemon = None
                            self.ai_pokemon = None
                            self.state = "BATTLE"
                            self.setup_battle()
                            # Garder l'équipe actuelle avec les Pokémon gagnés
                        elif event.key == pygame.K_q:  # Quitter
                            self.running = False
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                        self.running = False
                elif self.state == "WELCOME":
                    self.handle_welcome_input(event)
                elif self.state == "SELECTION":
                    self.handle_selection_input(event)
                elif self.state == "BATTLE":
                    self.handle_battle_input(event)

            # Mise à jour de l'affichage selon l'état
            if self.state == "WELCOME":
                self.draw_welcome()
            elif self.state == "SELECTION":
                self.draw_selection()
            elif self.state == "BATTLE":
                if self.minigame_active:
                    self.update_minigame()
                    self.draw_minigame()
                else:
                    self.update_battle()
                    self.draw_battle()
            elif self.state == "END_GAME":
                self.draw_end_game()

            pygame.display.flip()
            self.clock.tick(FPS)

     except Exception as e:
        print(f"Une erreur s'est produite: {e}")
     finally:
         pygame.quit()
  

if __name__ == "__main__":
    game = Game()
    game.run() 

