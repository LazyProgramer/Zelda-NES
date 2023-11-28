class Obeserver:
    def __init__(self):
        self.player_hitbox = None
        self.sword_hitbox = None
        self.enemies_directions = []
        self.enemies_hitbox = []
        self.enemies_projectiles = []
    
    def update_player(self, player_hitbox, sword_hitbox):
        self.player_hitbox = player_hitbox
        self.sword_hitbox = sword_hitbox

    def update_enemy(self, enemy_direction, enemy_hitbox):
        self.enemies_directions.append(enemy_direction)
        self.enemies_hitbox.append(enemy_hitbox)

    def update_projectiles(self, projectile_hitbox):
        self.enemies_projectiles.append(projectile_hitbox)

    def notify(self, player, enemies):
        # print(f'Sword: {self.sword_hitbox} | Enemies: {self.enemies_hitbox}')
        for e in range(len(self.enemies_hitbox)):
            
            if self.overlap(self.player_hitbox, self.enemies_hitbox[e]):
                player.tookDamaged()
            if self.overlap(self.sword_hitbox, self.enemies_hitbox[e]):
                enemies[e].damaged()
            if self.in_sight(self.player_hitbox, self.enemies_hitbox[e], self.enemies_directions[e]):
                enemies[e].shoot()
        
        for projectile in self.enemies_projectiles:
            if self.overlap(self.player_hitbox, projectile.hitbox):
                player.tookDamaged()
                projectile.state = 1

        
        self.enemies_hitbox = []
        self.enemies_directions = []
        self.enemies_projectiles = []
        
    def overlap(self, hitbox1, hitbox2):
        d1x = hitbox1[0] - hitbox2[2]
        d1y = hitbox1[1] - hitbox2[3]

        d2x = hitbox2[0] - hitbox1[2]
        d2y = hitbox2[1] - hitbox1[3]

        if d1x > 0 or d1y > 0 or d2x > 0 or d2y > 0:
            return False
            
        return True

    def in_sight(self, hitbox1, hitbox2, direction):
        hx = int((hitbox1[0] + hitbox1[2])/2)
        hy = int((hitbox1[1] + hitbox1[3])/2)

        # RIGHT LEFT
        if hitbox2[0] <= hx <= hitbox2[2] and direction[0] == 0:
            # print(f"|hitbox2[0] <= hx <= hitbox2[2]|direction\n{ hitbox2[0]} >= {hx} <= {hitbox2[2]}|{direction}")
            return True
        # DOWN UP
        if hitbox2[1] <= hy <= hitbox2[3] and direction[1] == 0:
            # print(f"|hitbox2[1] <= hy <= hitbox2[3]|direction\n{ hitbox2[1]} <= {hy} <= {hitbox2[3]}|{direction}")
            return True

        return False