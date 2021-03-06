import os

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))

DEBUG = False

SCREENSHOT_PATH = os.path.join(PROJECT_DIR, 'screenshots')
# Profile: any, core, compat
OPENGL = {
    "version": (3, 3),
    "profile": "core",
    "forward_compat": True,
}

WINDOW = {
    "class": "demosys.context.headless.HeadlessWindow",
    "size": (1280, 720),
    "vsync": True,
    "resizable": True,
    "fullscreen": False,
    "title": "demosys-py",
    "cursor": True,
}

HEADLESS_FRAMES = 1

# MUSIC = os.path.join(PROJECT_DIR, 'resources/music/tg2035.mp3')
TIMER = 'demosys.timers.Timer'
# TIMER = 'demosys.timers.RocketTimer'
# TIMER = 'demosys.timers.RocketMusicTimer'
# TIMER = 'demosys.timers.MusicTimer'

ROCKET = {
    'mode': 'project',
    'rps': 60,
    'project': os.path.join(PROJECT_DIR, 'resources', 'cube.xml'),
    'files': os.path.join(PROJECT_DIR, 'resources', 'tracks'),
}

# What effects to load
EFFECTS = (
)

SHADER_DIRS = (
    os.path.join(PROJECT_DIR, 'resources/shaders'),
)

SHADER_FINDERS = (
    'demosys.core.shaderfiles.finders.FileSystemFinder',
    'demosys.core.shaderfiles.finders.EffectDirectoriesFinder',
)

TEXTURE_DIRS = (
    os.path.join(PROJECT_DIR, 'resource/textures'),
)

# Finder classes
TEXTURE_FINDERS = (
    'demosys.core.texturefiles.finders.FileSystemFinder',
    'demosys.core.texturefiles.finders.EffectDirectoriesFinder'
)
