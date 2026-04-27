import math

class AggressiveAgent:
    def __init__(self, bot_instance):
        self.bot = bot_instance
        self.attack_range = 3
        self.burst_threshold = 0.4

    def get_best_target(self, enemies, player_pos):
        if not enemies: return None
        
        best_enemy = None
        highest_score = -1

        for enemy in enemies:
            # Hitung Jarak
            dist = math.sqrt((enemy['x'] - player_pos['x'])**2 + (enemy['y'] - player_pos['y'])**2)
            
            # Skor: Prioritas darah rendah & jarak dekat
            score = ((1 - enemy['hp']) * 100) + ((1 / (dist + 1)) * 50)
            
            if score > highest_score:
                highest_score = score
                best_enemy = enemy
        
        return best_enemy

    def run_logic(self, game_state):
        player = game_state['player']
        enemies = game_state['enemies']
        
        target = self.get_best_target(enemies, player)
        
        if target:
            # Kejar Musuh
            self.bot.move_to(target['x'], target['y'])
            
            # Gunakan Skill jika sekarat
            if target['hp'] < self.burst_threshold:
                self.bot.use_skill('all')
                
            # Serang
            self.bot.attack(target['id'])
        else:
            # Jika tidak ada musuh, cari item
            self.bot.find_loot()
