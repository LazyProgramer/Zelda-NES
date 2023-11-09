class Obeserver:
    def __init__(self):
        self.player_hitbox = None
        self.sword_hitbox = None
        self.enemies_hitbox = []
    
    def update_player(self, player_hitbox, sword_hitbox):
        self.player_hitbox = player_hitbox
        self.sword_hitbox = sword_hitbox

    def update_enemy(self, enemy_hitbox):
        self.enemies_hitbox.append(enemy_hitbox)

    def notify(self):
        for enemy in self.enemies_hitbox:
            # print(f'Player:{self.player_hitbox}\nSword:{self.sword_hitbox}\nEnemy:{enemy}')
            if self.overlap(self.player_hitbox, enemy):
                return "Player"
            if self.overlap(self.sword_hitbox, enemy):
                return "Enemy"
        
        self.enemies_hitbox = []
        

    def overlap(self, hitbox1, hitbox2):
        d1x = hitbox1[0] - hitbox2[2]
        d1y = hitbox1[1] - hitbox2[3]

        d2x = hitbox2[0] - hitbox1[2]
        d2y = hitbox2[1] - hitbox1[3]

        if d1x > 0 or d1y > 0 or d2x > 0 or d2y > 0:
            return False
            
        return True
