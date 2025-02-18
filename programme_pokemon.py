import pygame
import requests
import json
import os
import random
from datetime import datetime
import math

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

class Pokeball:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 20
        self.is_thrown = False
        self.target_x = 0
        self.target_y = 0
        self.speed = 10
        self.captured_pokemon = None
        self.animation_complete = False
        self.original_x = x
        self.original_y = y
        self.capture_animation = 0  # Pour l'animation de capture
        self.pokemon_sprite = None  # Pour stocker le sprite du Pokémon
        self.capturing = False
        self.pokemon_scale = 1.0    # Pour l'effet de réduction
        
    def throw(self, target_x, target_y, pokemon_sprite):
        if not self.is_thrown and not self.captured_pokemon:
            self.is_thrown = True
            self.target_x = target_x
            self.target_y = target_y
            self.pokemon_sprite = pokemon_sprite
            
    def update(self):
        if self.is_thrown and not self.animation_complete:
            if not self.capturing:
                dx = self.target_x - self.x
                dy = self.target_y - self.y
                distance = math.sqrt(dx**2 + dy**2)
                
                if distance < self.speed:
                    self.capturing = True
                else:
                    self.x += (dx/distance) * self.speed
                    self.y += (dy/distance) * self.speed
            else:
                # Animation de capture
                self.capture_animation += 1
                if self.capture_animation >= 30:  # Durée de l'animation
                    self.animation_complete = True
                    self.x = self.original_x
                    self.y = self.original_y
                
    def draw(self, screen):
        # Dessin de la Pokéball
        pygame.draw.circle(screen, (203, 0, 0), (int(self.x), int(self.y)), self.radius)
        pygame.draw.circle(screen, (255, 255, 255), (int(self.x), int(self.y)), self.radius - 2)
        pygame.draw.rect(screen, (0, 0, 0), 
                        (self.x - self.radius, self.y - 2, self.radius * 2, 4))
        pygame.draw.circle(screen, (0, 0, 0), (int(self.x), int(self.y)), 6)
        pygame.draw.circle(screen, (255, 255, 255), (int(self.x), int(self.y)), 5)
        pygame.draw.ellipse(screen, (255, 255, 255, 128), 
                          (self.x - self.radius//3, self.y - self.radius//2, 
                           self.radius//2, self.radius//4))
        
        # Affichage du Pokémon capturé en bas
        if self.captured_pokemon and self.pokemon_sprite and not self.capturing:
            sprite_size = 60  # Taille réduite pour l'affichage en bas
            scaled_sprite = pygame.transform.scale(self.pokemon_sprite, (sprite_size, sprite_size))
            screen.blit(scaled_sprite, 
                       (self.original_x - sprite_size//2, 
                        self.original_y + 40))
        
        # Animation de capture
        if self.capturing and self.pokemon_sprite and not self.animation_complete:
            self.pokemon_scale = max(0.1, 1.0 - (self.capture_animation / 30))
            current_size = int(100 * self.pokemon_scale)
            if current_size > 0:
                scaled_sprite = pygame.transform.scale(self.pokemon_sprite, 
                                                    (current_size, current_size))
                screen.blit(scaled_sprite, 
                           (self.x - current_size//2, 
                            self.y - current_size//2))


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

        # Positionnement des Pokéballs au centre de l'écran
        center_x = WINDOW_WIDTH // 2
        self.pokeballs = [
            Pokeball(center_x - 100, WINDOW_HEIGHT // 2),
            Pokeball(center_x, WINDOW_HEIGHT // 2),
            Pokeball(center_x + 100, WINDOW_HEIGHT // 2)
        ]
        self.selected_pokeball = None
        self.dragging = False
        self.pokemon_sprites = {}  # Pour stocker les sprites

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
        
        
    def start_minigame(self):
        self.minigame_active = True
        self.minigame_start_time = pygame.time.get_ticks()
        self.star = Star(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.player_character = {'x': WINDOW_WIDTH//2, 'y': WINDOW_HEIGHT//2, 'radius': 20, 'color': GREEN}
        self.minigame_result = None


    def update_minigame(self):
        if not self.minigame_active:
            return
    
       # Vérifier si le temps est écoulé (5 secondes)
        current_time = pygame.time.get_ticks()
        if current_time - self.minigame_start_time > 5000:
           self.minigame_active = False
           self.minigame_result = False
           self.setup_battle()
           return
    
    # Mettre à jour l'étoile
        self.star.update()

        # Déplacer le personnage du joueur avec les touches
        keys = pygame.key.get_pressed()
        speed = 5
        if keys[pygame.K_LEFT]:
           self.player_character['x'] -= speed
        if keys[pygame.K_RIGHT]:
           self.player_character['x'] += speed
        if keys[pygame.K_UP]:
           self.player_character['y'] -= speed
        if keys[pygame.K_DOWN]:
           self.player_character['y'] += speed

        # Limiter la position du personnage à l'écran
        self.player_character['x'] = max(self.player_character['radius'], 
                                  min(self.player_character['x'], 
                                      WINDOW_WIDTH - self.player_character['radius']))
        self.player_character['y'] = max(self.player_character['radius'], 
                                     min(self.player_character['y'], 
                                          WINDOW_HEIGHT - self.player_character['radius']))
        
        # Vérifier si le joueur a touché l'étoile
        distance = math.sqrt((self.player_character['x'] - self.star.x)**2 + 
                       (self.player_character['y'] - self.star.y)**2)
        if distance < self.player_character['radius'] + self.star.radius:
            self.minigame_active = False
            self.minigame_result = True
            self.setup_battle()


    def draw_minigame(self):
        if not self.minigame_active:
           return
      
        self.screen.fill(WHITE)
    
        # Afficher le temps restant
        elapsed_time = (pygame.time.get_ticks() - self.minigame_start_time) / 1000
        remaining_time = max(0, 5 - elapsed_time)
        time_text = FONT.render(f"Temps: {remaining_time:.1f} s", True, BLACK)
        self.screen.blit(time_text, (20, 20))

        # Instructions
        instructions = SMALL_FONT.render("Attrapez l'étoile pour obtenir une attaque spéciale!", True, BLACK)
        self.screen.blit(instructions, (WINDOW_WIDTH//2 - instructions.get_width()//2, 60))
    
        # Dessiner l'étoile
        self.star.draw(self.screen)

        # Dessiner le personnage du joueur
        pygame.draw.circle(self.screen, self.player_character['color'], 
                       (int(self.player_character['x']), int(self.player_character['y'])), 
                        self.player_character['radius'])







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
     if self.minigame_active or hasattr(self, 'minigame_result'):
        # Si le mini-jeu vient de se terminer ou est en cours
        self.player_pokemon = None
        self.ai_pokemon = Pokemon(600, 300, self.ai_pokemon_team[0]['id'], self.ai_pokemon_team[0], False)
        
        # Si le mini-jeu a été gagné, activer l'attaque spéciale
        if hasattr(self, 'minigame_result') and self.minigame_result:
            self.special_attack_available = True
        else:
            self.special_attack_available = False
     else:
        # Le mini-jeu n'a pas encore été joué, on le lance
        self.start_minigame()



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
     if self.player_pokemon is None:
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            for i, pokemon in enumerate(self.player.pokemon_team):
                # Utiliser la zone de sprite plus grande (150x150)
                pokemon_rect = pygame.Rect(200 + i * 300 - 75, 150, 150, 150)
                if pokemon_rect.collidepoint(mouse_pos):
                    self.player_pokemon = Pokemon(100, 300, pokemon['id'], pokemon, True)
                    # Transmettre le résultat du mini-jeu au Pokémon
                    if hasattr(self, 'minigame_result') and self.minigame_result:
                        self.player_pokemon.special_attack_available = True
     else:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_x:
                self.player_pokemon.shoot()
                if self.shoot_sound:
                    self.shoot_sound.play()
            elif event.key == pygame.K_b and self.player_pokemon.special_attack_available:
                self.player_pokemon.special_attack()
                if self.shoot_sound:
                    # Jouer le son plusieurs fois pour l'attaque spéciale
                    for _ in range(3):
                        self.shoot_sound.play()

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

        # Affichage de votre équipe
        team_title = FONT.render("Votre équipe:", True, BLACK)
        self.screen.blit(team_title, (50, 150))

        for i, pokemon in enumerate(self.player.pokemon_team):
            # Charger et afficher le sprite
            response = requests.get(pokemon['sprites']['front_default'])
            temp_file = f"temp_end_game_{i}.png"
            with open(temp_file, 'wb') as f:
                f.write(response.content)
            sprite = pygame.image.load(temp_file)
            sprite = pygame.transform.scale(sprite, (100, 100))
            self.screen.blit(sprite, (50 + i * 150, 200))
            
            # Nom du Pokémon
            name = SMALL_FONT.render(pokemon['name'], True, BLACK)
            self.screen.blit(name, (50 + i * 150, 310))
            
            os.remove(temp_file)

        # Affichage du Pokémon capturé si victoire
        if self.end_game_result == "WIN" and self.captured_pokemon:
            captured_title = FONT.render("Pokémon capturé:", True, BLACK)
            self.screen.blit(captured_title, (50, 350))
            
            response = requests.get(self.captured_pokemon['sprites']['front_default'])
            temp_file = "temp_captured.png"
            with open(temp_file, 'wb') as f:
                f.write(response.content)
            sprite = pygame.image.load(temp_file)
            sprite = pygame.transform.scale(sprite, (100, 100))
            self.screen.blit(sprite, (50, 400))
            
            name = SMALL_FONT.render(self.captured_pokemon['name'], True, BLACK)
            self.screen.blit(name, (50, 510))
            
            os.remove(temp_file)

        # Message pour continuer
        continue_text = SMALL_FONT.render("Appuyez sur ESPACE pour quitter", True, BLACK)
        self.screen.blit(continue_text, (WINDOW_WIDTH // 2 - continue_text.get_width() // 2, 550))

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
               self.battle_music.play(-1)  # Démarre la musique en boucle

            while self.running:
              for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif self.state == "END_GAME":
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                        self.running = False
                elif self.state == "WELCOME":
                    self.handle_welcome_input(event)
                elif self.state == "SELECTION":
                    self.handle_selection_input(event)
                elif self.state == "BATTLE":
                    if not self.minigame_active:
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
        # Optionnel: vous pourriez ajouter du code pour sauvegarder l'état du jeu
        # ou effectuer un nettoyage avant de terminer
        finally:
        # Ce bloc s'exécute toujours, qu'il y ait une exception ou non
           pygame.quit()      
    
class Star:
    def __init__(self, screen_width, screen_height):
        self.x = random.randint(50, screen_width - 50)
        self.y = random.randint(50, screen_height - 50)
        self.radius = 15
        self.color = YELLOW
        self.speed = 3
        self.direction = random.uniform(0, 2 * math.pi)
        self.screen_width = screen_width
        self.screen_height = screen_height
        
    def update(self):
        # Déplacement aléatoire
        self.direction += random.uniform(-0.2, 0.2)
        self.x += math.cos(self.direction) * self.speed
        self.y += math.sin(self.direction) * self.speed
        
        # Rebondir sur les bords
        if self.x < self.radius:
            self.x = self.radius
            self.direction = math.pi - self.direction
        elif self.x > self.screen_width - self.radius:
            self.x = self.screen_width - self.radius
            self.direction = math.pi - self.direction
        
        if self.y < self.radius:
            self.y = self.radius
            self.direction = -self.direction
        elif self.y > self.screen_height - self.radius:
            self.y = self.screen_height - self.radius
            self.direction = -self.direction
        
    def draw(self, screen):
        # Dessine une étoile simple
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
        points = []
        for i in range(5):
            angle = 2 * math.pi * i / 5 - math.pi / 2
            x = self.x + self.radius * math.cos(angle)
            y = self.y + self.radius * math.sin(angle)
            points.append((x, y))
        pygame.draw.polygon(screen, self.color, points)



if __name__ == "__main__":
    game = Game()
    game.run()