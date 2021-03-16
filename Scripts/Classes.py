from User.UserData import *
import random as rd
import pygame
"""=====  Game [1]  ====="""


class Game:

    # Fonction exÃ©cutÃ©e au dÃ©marrage de Game -tremisabdoul
    def __init__(self):
        # SaveSlot devient une sous-classe de Game -tremisabdoul
        self.Saves = SaveSlot()
        # UserData devient une sous-classe de Game -tremisabdoul
        self.UserData = UserData()
        self.DataY = self.UserData.UserGraphicInfo.current_h
        self.DataX = self.UserData.UserGraphicInfo.current_w

        # Contient toutes les touches prÃ©ssÃ©es -tremisabdoul
        self.pressed = {}

        # Variables GÃ©nÃ©rales -tremisabdoul
        self.InGame = False
        self.Option = False
        self.Running = True
        self.Pause = False
        self.Lobby = True
        self.Fullscreen = 0
        self.Tickchecker = 1
        self.ActualFrame = 0
        self.Frame = 0
        self.Position = 0
        self.PositionPlayer = 0
        self.PlateformNumber = 1

    def Rescale(self, value, XorY):
        if XorY == "X":
            return round((value / 1280) * self.DataX)
        elif XorY == "Y":
            return round((value / 720) * self.DataY)

    def init_suite(self):
        # Player devient une sous-classe de Game -tremisabdoul
        self.Player = Player()
        # Sol devient une sous-classe de Game -Steven
        self.Sol = Sol()
        # Mouse devient une sous-classe de Game -tremisabdoul
        self.Mouse = Mouse()
        # UI devient une sous-classe de Game -tremisabdoul
        self.UI = UI()
        # Monster devient une sous-classe de Game - steven
        self.Monster = Monster()
        self.Background = Background()
        self.Wall = Wall()

        # CrÃ©ation du groupe composÃ© de tous les monstres -Steven
        self.all_Monster = pygame.sprite.Group()
        self.all_Monster.add(self.Monster)

        # CrÃ©ation du groupe composÃ© de tous les joueurs -Steven
        self.all_Player = pygame.sprite.Group()
        self.all_Player.add(self.Player)

        self.Entities = pygame.sprite.Group()
        self.Entities.add(self.Monster)
        self.Entities.add(self.Player)

        # CrÃ©ation du groupe composÃ© de toutes les plateformes -Steven
        self.all_plateform = pygame.sprite.Group()
        self.all_plateform.add(self.Sol)


"""=====  Game.Player [2.0]  ====="""


class Player(pygame.sprite.Sprite, Game):

    # Fonction exÃ©cutÃ©e au dÃ©marrage de Player -tremisabdoul
    def __init__(self):
        super().__init__()

        self.pop = False

        # Force devient une sous-classe de Player et Game est chargÃ© en tant que super-classe -tremisabdoul
        self.Force = Force()
        self.Game = Game

        # Statistiques -tremisabdoul
        self.Pv = 50
        self.MaxPv = 100
        self.Damage = 10
        self.Speed = 2
        self.SpeedY = 0
        # Statistique Variable -steven
        self.CDR = 0
        self.AttackSpeed = 0
        self.CCHit = 0
        self.CCSpell = 0
        self.CCDamage = 0
        self.Penetration = 0
        self.ManaRegen = 0
        self.XP_Multiplicator = 0
        self.Damage_Multiplicator = 0

        self.Level = 0
        self.Gold = 0

        # Statistique gagnÃ©e par niveau / points -steven
        self.Gain_Stat_Level = 5
        self.Point_Pv = 0
        self.Point_Damage = 0

        self.Weapon1 = Weapon()
        self.Weapon2 = Weapon()

        # DÃ©finit l'Ã©lÃ©ment visuel en tant que variable et la hitbox de Player -tremisabdoul
        self.image = pygame.image.load("Assets/Visual/Mystique/resp1.png")
        self.image = pygame.transform.scale(self.image, (self.image.get_width() * 2, self.image.get_height() * 2))
        self.rect = self.image.get_rect()
        self.rect = self.image.get_rect(bottomleft=self.rect.bottomleft)

        # Position de Player -tremisabdoul
        self.rect.center = (430, 600)

        self.LastY = 0
        self.YVector = 0
        self.YVectorblit = 0
        self.Base_Gravity = 0

        self.Movement = 1  # Droite = 1 Gauche = -1

        # Valeurs max et min que Player peut atteindre (Bords de l'Ã©cran x) -tremisabdoul
        self.MinX = 20
        self.MaxX = 1200

        # Valeurs max et min que Player peut atteindre (Bords de l'Ã©cran y) -tremisabdoul
        self.MinY = -20
        self.MaxY = 740
        self.MovementKey = False

    #   def Check_Collisions(rectA, rectB):
    #       if rectB.right < rectA.left:
    #           # rectB est Ã  gauche
    #           return False
    #       if rectB.bottom < rectA.top:
    #           # rectB est au-dessus
    #           return False
    #       if rectB.left > rectA.right:
    #           # rectB est Ã  droite
    #           return False
    #       if rectB.top > rectA.bottom:
    #           # rectB est en-dessous
    #           return False

    # Fonction de collision -tremisabdoul

    @staticmethod
    def check_collisions(sprite, group):
        return pygame.sprite.spritecollide(sprite, group, False, pygame.sprite.collide_rect)

    # Fonction de mouvement (Droite) -tremisabdoul
    def Move_Right(self):
        self.Force.xm += self.Speed
        self.Movement = 1

    # Fonction de mouvement (Gauche) -tremisabdoul
    def Move_Left(self):
        self.Force.xm -= self.Speed
        self.Movement = 0

    # Fonction de gain de stat ( valeur placÃ©e arbitrairement lol ) - steven
    def Gain_Stats(self):
        self.MaxPv += self.Gain_Stat_Level + (4 * self.Point_Pv)
        self.Damage += self.Gain_Stat_Level + (2 * self.Point_Damage)

    # Fonction appliquÃ© que si l'utilisateur meurt
    def Death(self):
        self.all_Monster = pygame.sprite.Group()
        self.Player.Pv = self.Player.MaxPv


"""=====  Game.Player.Force [2.1]  ====="""


#  Contient les vecteurs physiques -tremisabdoul
class Force:

    # Fonction exÃ©cutÃ©e au demarÃ©e au lancement de Force - tremisabdoul
    def __init__(self):

        self.x = float(0)
        self.xm = float(0)
        self.StepX = float(0)
        self.lastx = float(0)
        self.lasty = float(0)

        self.Game = Game

    # Fonction permettant un mouvement fluide -tremisabdoul
    def AccelerationFunctionX(self):

        # Forces appliquÃ©s + ((Forces appliquÃ©s lors de la derniÃ¨re frame / 1.3) / 1.1) -tremisabdoul
        self.StepX = self.xm + self.x + ((self.lastx / 1.3) / 1.1)

        if round(self.StepX) == 0:
            self.StepX = 0
            self.lastx = 0
            self.x = 0
            self.xm = 0
            return 0

        else:
            self.lastx = self.StepX
            self.x = 0
            self.xm = 0
            return self.StepX

    # Faut se dire que la gravitÃ© a une force de 33 et que lorsque
    # Base_Gravity est a 0 c'est que la force appliquÃ©e par le sol est de -33
    def Gravity(self, Game0, Target):
        base = Target.rect.y
        if Target.Base_Gravity < 22:  # Si force de sol > 0
            Target.Base_Gravity += 0.44  # Diminution de la force "Sol" (Ratio 0.66)
            # print("Gravity: ", Target.Base_Gravity)
            Target.rect.y += Target.Base_Gravity
        else:
            Target.Base_Gravity = 22  # Force de sol = 0
            # print("Gravity: ", 22)
            Target.rect.y += 22

        # VÃ©rification des collisions entre Player et toutes les plateformes
        Collide = Game0.Player.check_collisions(Target, Game0.all_plateform)
        print("\n", base, Target.rect.y)
        for item in Collide:
            print("\n", Target.Base_Gravity)
            print("\nCollide ? ", bool(item),
                  "\nFall ? ", bool(Target.YVector),
                  "\nBottom Collide ? ", bool(Target.rect.bottom <= item.rect.top + Target.Base_Gravity + 2))

            if item and Target.YVector <= 1 and (Target.rect.bottom <= item.rect.top + Target.Base_Gravity + 2):
                Target.rect.y = base
                Replace = item.rect.top - (Target.rect.bottom - 1)  # Y reset (Premier pixel du rect de plateforme)
                Target.SpeedY = 0  # Cancel le saut
                Target.Base_Gravity = 0  # Reset la force du sol (-33)
                print("\nStand: ", Replace)
                Target.rect.y += Replace


"""=====  Game.Sol [3]  ====="""


class Sol(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        # DÃ©finit l'Ã©lÃ©ment visuel en tant que variable -steven
        self.image = pygame.image.load("Assets/Visual/plateforme_base.png")

        # Transforme l'image sol en la rÃ©solution indiquÃ©e -tremisabdoul
        self.image = pygame.transform.scale(self.image, (1280, 34))

        # DÃ©finit la hitbox de sol -steven
        self.rect = self.image.get_rect()

        # Position de la plateforme principale -steven
        self.rect.x = 0
        self.rect.y = 686


"""=====  Game.Plateform [4]  ====="""


class Plateform(pygame.sprite.Sprite, Game):

    def __init__(self):
        super().__init__()

        # DÃ©finit l'Ã©lÃ©ment visuel en tant que variable -tremisabdoul
        self.image = pygame.image.load("Assets/Visual/plateforme_base.png")

        # Transforme l'image sol en la rÃ©solution indiquÃ©e -tremisabdoul
        self.image = pygame.transform.scale(self.image, (320, 20))

        # DÃ©finit la hitbox de sol -tremisabdoul
        self.rect = self.image.get_rect()

        import random as random
        # Position de la plateforme -tremisabdoul
        self.rect.x = random.randint(-20, 1900)
        self.rect.y = random.randint(100, 600)
        del random


"""=====  Game.Mouse [5]  ====="""


class Mouse(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()

        # Rends la sourie windows invisible -tremisabdoul
        pygame.mouse.set_visible(False)

        # Definit l'image (emplacent la sourie) -tremisabdoul
        self.image = pygame.image.load("Assets/Visual/UI/Mouse.png")
        self.image = pygame.transform.scale(self.image, (22, 22))

        # Cree la hit-box de l'image -tremisabdoul
        self.rect = self.image.get_rect()
        self.rect = self.image.get_rect(center=self.rect.center)


"""=====  Game.UI [6]  ====="""


# Interface -tremisabdoul
class UI:

    def __init__(self):
        super().__init__()

        """ CatÃ©gorie Pause """
        # Font grisÃ© (Ca prends full perf) -tremisabdoul
        self.baselayer = pygame.image.load("Assets/Visual/UI/baselayer.png")
        self.baselayer = pygame.transform.scale(self.baselayer, (1280, 720))

        # Boutton "REPRENDRE" -tremisabdoul
        self.resumebutton = pygame.image.load("Assets/Visual/UI/bouton_REPRENDRE.png")
        self.resumebutton = pygame.transform.scale(self.resumebutton, (140, 30))
        self.resumebuttonrect = self.resumebutton.get_rect()
        self.resumebuttonrect.x = 640 - 70
        self.resumebuttonrect.y = 360 - 40

        # Boutton "SAUVEGARDER" -tremisabdoul
        self.savebutton = pygame.image.load("Assets/Visual/UI/bouton_SAUVEGARDER.png")
        self.savebutton = pygame.transform.scale(self.savebutton, (172, 30))
        self.savebuttonrect = self.savebutton.get_rect()
        self.savebuttonrect.x = 640 - 86
        self.savebuttonrect.y = 360

        # Boutton "PARAMÃˆTRE" -steven
        self.settingsbutton = pygame.image.load("Assets/Visual/UI/bouton_SETTINGS.png")
        self.settingsbutton = pygame.transform.scale(self.settingsbutton, (100, 30))
        self.settingsbuttonrect = self.settingsbutton.get_rect()
        self.settingsbuttonrect.x = 640 - 50
        self.settingsbuttonrect.y = 360 + 40

        # Boutton "QUITER" -tremisabdoul
        self.quitbutton = pygame.image.load("Assets/Visual/UI/bouton_QUITTER.png")
        self.quitbutton = pygame.transform.scale(self.quitbutton, (100, 30))
        self.quitbuttonrect = self.quitbutton.get_rect()
        self.quitbuttonrect.x = 640 - 50
        self.quitbuttonrect.y = 360 + 80

        """ CatÃ©gorie Menu d'accueil """

        # IntÃ©gration de l'image qui apparaitrera du menu d'accueil -steven
        self.lobbybackground = pygame.image.load("Assets/Visual/background.jpg")
        self.lobbybackground = pygame.transform.scale(self.lobbybackground, (1280, 720))

        # IntÃ©gration du boutton "JOUER" -steven
        self.lobby_playbutton = pygame.image.load("Assets/Visual/UI/bouton_JOUER.png")
        self.lobby_playbutton = pygame.transform.scale(self.lobby_playbutton, (82, 30))
        self.lobby_playbuttonrect = self.lobby_playbutton.get_rect()
        self.lobby_playbuttonrect.x = 1000
        self.lobby_playbuttonrect.y = 360 - 30

        # IntÃ©gration du boutton "CHARGER" -steven
        self.lobby_loadbutton = pygame.image.load("Assets/Visual/UI/bouton_REPRENDRE.png")
        self.lobby_loadbutton = pygame.transform.scale(self.lobby_loadbutton, (140, 30))
        self.lobby_loadbuttonrect = self.lobby_loadbutton.get_rect()
        self.lobby_loadbuttonrect.x = 1000 - 30
        self.lobby_loadbuttonrect.y = 360

        # IntÃ©gration du boutton "QUITTER" -Steven
        self.lobby_quitbutton = pygame.image.load("Assets/Visual/UI/bouton_QUITTER.png")
        self.lobby_quitbutton = pygame.transform.scale(self.lobby_quitbutton, (100, 30))
        self.lobby_quitbuttonrect = self.lobby_quitbutton.get_rect()
        self.lobby_quitbuttonrect.x = 1000 - 60
        self.lobby_quitbuttonrect.y = 360 + 30


"""=====  Monstre [7]  ====="""


class Monster(pygame.sprite.Sprite, Game):

    # Fonction Ã©xÃ©cutÃ© au dÃ©marrage de Monster -steven
    def __init__(self):
        super().__init__()

        # Statistiques -steven
        self.Pv = 100
        self.MaxPv = 100
        self.DamageDealt = 10
        self.Speed = 3

        self.image = pygame.image.load("Assets/Visual/Entities/Monster/Slime/Stand1.png")

        self.rect = self.image.get_rect()

        self.rect.x = rd.randint(150, 1050)
        self.rect.y = 50
        self.LastY = 675

        self.YVector = 0
        self.YVectorblit = 0
        self.Base_Gravity = 0

        self.rect = self.image.get_rect(midtop=self.rect.midtop)

        # Barre de pv des monstres -tremisabdoul
        self.image0 = pygame.image.load("Assets/Visual/UI/100pv.png")
        self.image0 = pygame.transform.scale(self.image0, (200, 30))

        self.pvfontrect = self.image0.get_rect()
        self.pvfontrect = self.image0.get_rect(midbottom=self.pvfontrect.midbottom)
        self.pvfontrect.midbottom = self.rect.midtop
        self.pvfontrect.y += 10

        self.Direction = 1

    # Dessin concernant la barre de vie du monstre -steven / tremisabdoul
    def Life(self, Screen, Game):
        if self.Pv > 0:
            self.pvfontrect = self.image0.get_rect(midbottom=self.pvfontrect.midbottom)
            self.pvfontrect.midbottom = self.rect.midtop
            self.pvfontrect.y -= 7
            self.image0 = pygame.transform.scale(self.image0, (int(self.Pv / self.MaxPv * 64), 8))
            self.Pv -= 0.2
            Screen.blit(self.image0, (self.pvfontrect.x - Game.Position, self.pvfontrect.y))

    # DÃ©placement du monstre vers la droite -steven
    def Move_Right(self, Game):
        if Game.Player.check_collisions(self, Game.all_plateform):
            self.rect.x += self.Speed
        else:
            self.rect.x -= int(self.Speed * 1)
            self.Direction = 1

    # DÃ©placement du monstre vers la gauche -steven
    def Move_Left(self, Game):
        if Game.Player.check_collisions(self, Game.all_plateform):
            self.rect.x -= self.Speed
        else:
            self.rect.x += int(self.Speed * 1.5)
            self.Direction = 0

class Weapon:

    def __init__(self):

        # Type d'arme Ex: Mitraillette = 3
        self.MetaType = rd.randrange(1, 5, 1)

        # Arme en question Ex: Mitraillette.Poison = 3.4
        self.MetaWeapon = rd.randrange(1, 10, 1)

        # RarertÃ© Ex: Mitraillette.Poison.Rare = 3.4.2
        self.MetaClass = rd.randrange(1, 4, 1)

        # Donne l'ensemble des propiÃ©tÃ©es de l'arme  Ex: 3.4.2
        self.MetaName = [self.MetaType, self.MetaWeapon, self.MetaClass]

        self.Damage = rd.randrange(2, 9, 1)
        self.Speed = rd.randrange(41, 80, 1)/10
        self.CD = self.MetaWeapon * 3

        self.DamageBuff = 0
        self.SpeedBuff = 0
        self.CDR = 0
        self.tester = self.MetaClass

        while self.tester > 0:
            self.RandomTest = rd.randrange(1, 3, 1)
            self.tester -= 1
            if self.RandomTest == 1:
                self.DamageBuff += rd.randrange(1, 5, 1)
            if self.RandomTest == 2:
                self.SpeedBuff -= rd.randrange(1, 20, 1) / 10
            if self.RandomTest == 3:
                self.CDR += rd.randrange(1, 25, 1)
        del self.tester
        print("\nWeapon:", self.MetaName, "\nRarete", self.MetaClass,
              "\n\tDamage: ", self.Damage, "+",  self.DamageBuff, "\n\tSpeed: ", self.Speed, "+", self.SpeedBuff,
              "\n\tCD: ", self.CD, "* ( 100 / ( 100 +", "CDR = ", self.CDR, "))")


class Wall:
    def __init__(self):
        self.image = pygame.image.load("Assets/Visual/plateforme_base.png")
        self.rect = self.image.get_rect()
        self.rect = self.image.get_rect(midtop=self.rect.midtop)


class Background:

    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Assets/Visual/UI/Background.png")
        # self.image = pygame.transform.scale(self.image, (3848, 686))
        self.rect = self.image.get_rect()
        self.rect = self.image.get_rect(midtop=self.rect.midtop)
        self.rect.midtop = (self.rect.width / 3, 0)


def FrameLimiter(Game, time, tick):
    # Permet d'avoir des frames regulieres -tremisabdoul
    Game.Tickchecker = time.time()
    Game.Tickchecker -= tick

    while Game.Tickchecker < 0.017:
        Game.Tickchecker = time.time()
        Game.Tickchecker -= tick
