import pygame
from pathlib import Path

SOURCEFILEDIR = Path(__file__).resolve().parents[1]
SOUND_PATH = SOURCEFILEDIR.joinpath('data/sound/')

pygame.mixer.init()

HIT_BLOCK_SOUND = pygame.mixer.Sound(SOUND_PATH.joinpath('blockhit.wav'))
COIN_SOUND = pygame.mixer.Sound(SOUND_PATH.joinpath('coin.wav'))
DEATH_SOUND = pygame.mixer.Sound(SOUND_PATH.joinpath('death.wav'))
JUMP_SOUND = pygame.mixer.Sound(SOUND_PATH.joinpath('jump.wav'))
SHOT_SOUND = pygame.mixer.Sound(SOUND_PATH.joinpath('shot.wav'))
KILL_MOB_SOUND = pygame.mixer.Sound(SOUND_PATH.joinpath('kill_mob.wav'))
COIN_SOUND = pygame.mixer.Sound(SOUND_PATH.joinpath('coin.wav'))
BONUS_GROW_SOUND = pygame.mixer.Sound(SOUND_PATH.joinpath('mushroomappear.wav'))
PICK_UP_BONUS_SOUND = pygame.mixer.Sound(SOUND_PATH.joinpath('mushroomeat.wav'))
SHOOT_SOUND = pygame.mixer.Sound(SOUND_PATH.joinpath('rlaunch.wav'))
SWING_SOUND = pygame.mixer.Sound(SOUND_PATH.joinpath('tarzan.wav'))
GAME_OVER_SOUND = pygame.mixer.Sound(SOUND_PATH.joinpath('gameover.wav'))
SUCCESS_SOUND = pygame.mixer.Sound(SOUND_PATH.joinpath('level_compleet.wav'))
LIVE_UP_SOUND = pygame.mixer.Sound(SOUND_PATH.joinpath('live_up.wav'))
SHOOT_SOUND.set_volume(0.3)

SWING_SOUND.set_volume(0.2)
pygame.mixer.set_num_channels(12)
TARZAN_CHANNEL= pygame.mixer.Channel(8)
DEAD_CHANNEL = pygame.mixer.Channel(9)
GAME_OVER_CHANNEL = pygame.mixer.Channel(10)
FINISCH_LEVEL_CHANNEL = pygame.mixer.Channel(11)

pygame.mixer.music.set_volume(1)


def play_music():
    is_playing = pygame.mixer.music.get_busy()
    if not is_playing :
        pygame.mixer.music.load(SOUND_PATH.joinpath('overworld.wav'))
        pygame.mixer.music.play(-1)

def stop_music():
    is_playing = pygame.mixer.music.get_busy()
    if is_playing :
        pygame.mixer.music.stop()

def jump_sound():
    JUMP_SOUND.play()

def death_sound():
    is_playing = pygame.mixer.music.get_busy()
    if is_playing :
        stop_swing_sound()
        pygame.mixer.music.stop()
    DEAD_CHANNEL.play(DEATH_SOUND)

def is_bussy_dead_sound():
    return DEAD_CHANNEL.get_busy()

def ennemie_hit_sound():
    SHOT_SOUND.play()

def pick_up_coin_sound():
    COIN_SOUND.play()

def bonus_grow_sound():
    BONUS_GROW_SOUND.play()

def pick_up_bonus_sound():
    PICK_UP_BONUS_SOUND.play()

def shoot_sound():
    SHOOT_SOUND.play()

def kill_mob_sound():
    KILL_MOB_SOUND.play()

def hit_block_sound():
    HIT_BLOCK_SOUND.play()

def live_up_sound():
    LIVE_UP_SOUND.play()
    
def swing_sound():
    if not TARZAN_CHANNEL.get_busy():
        TARZAN_CHANNEL.play(SWING_SOUND)

def stop_swing_sound():
    TARZAN_CHANNEL.stop()

def game_over_sound():
    if not  is_bussy_game_over_sound():
        GAME_OVER_CHANNEL.play(GAME_OVER_SOUND)

def success_sound ():
    stop_music()
    FINISCH_LEVEL_CHANNEL.play(SUCCESS_SOUND)

def is_bussy_finisched_level_sound():
    return FINISCH_LEVEL_CHANNEL.get_busy()

def is_bussy_game_over_sound():
    return GAME_OVER_CHANNEL.get_busy()

def play_end_game_song():    
    is_playing = pygame.mixer.music.get_busy()
    if not is_playing :
        pygame.mixer.music.load(SOUND_PATH.joinpath('end_game.mp3'))
        pygame.mixer.music.play()
    