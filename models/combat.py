import random
from models.shadow import Shadow
from models.effects import Effect, EffectManager, EffectType

class Combat:
    def __init__(self, player, enemy):
        self.player = player
        self.enemy = enemy
        self.player_shadows = []
        self.turn_count = 0
        self.battle_log = []
        
        # Initialize effect managers
        self.player_effects = EffectManager()
        self.enemy_effects = EffectManager()
    
    def add_shadow(self, shadow):
        if len(self.player_shadows) < 3:
            self.player_shadows.append(shadow)
            return True
        return False
    
    def remove_shadow(self, shadow):
        if shadow in self.player_shadows:
            self.player_shadows.remove(shadow)
            return True
        return False
    
    def calculate_damage(self, attacker, defender):
        # Base damage calculation
        base_damage = attacker.strength
        
        # Add random variation (±20%)
        variation = random.uniform(0.8, 1.2)
        damage = int(base_damage * variation)
        
        # Apply defense reduction
        damage = max(1, damage - (defender.defense // 2))
        
        # Check for effects that modify damage
        if self.player_effects.has_effect(EffectType.WEAK) and attacker == self.player:
            damage = int(damage * 0.8)
        elif self.enemy_effects.has_effect(EffectType.WEAK) and attacker == self.enemy:
            damage = int(damage * 0.8)
        
        # Check for strength boost
        if self.player_effects.has_effect(EffectType.STRENGTH_BOOST) and attacker == self.player:
            damage = int(damage * 1.2)
        elif self.enemy_effects.has_effect(EffectType.STRENGTH_BOOST) and attacker == self.enemy:
            damage = int(damage * 1.2)
        
        return damage
    
    def player_attack(self):
        # Check if player is stunned
        if self.player_effects.has_effect(EffectType.STUN):
            self.battle_log.append("You are stunned and cannot attack!")
            return 0
        
        # Check for blindness
        if self.player_effects.has_effect(EffectType.BLIND):
            if random.random() < 0.3:  # 30% chance to miss
                self.battle_log.append("Your attack misses due to blindness!")
                return 0
        
        # Check for confusion
        if self.player_effects.has_effect(EffectType.CONFUSE):
            if random.random() < 0.3:  # 30% chance to hit self
                damage = self.calculate_damage(self.player, self.player)
                actual_damage = self.player.take_damage(damage)
                self.battle_log.append(f"You are confused and hit yourself for {actual_damage} damage!")
                return actual_damage
        
        # Check for fear
        if self.player_effects.has_effect(EffectType.FEAR):
            if random.random() < 0.2:  # 20% chance to flee
                self.battle_log.append("You are too afraid to attack!")
                return 0
        
        damage = self.calculate_damage(self.player, self.enemy)
        actual_damage = self.enemy.take_damage(damage)
        self.battle_log.append(f"You deal {actual_damage} damage to the enemy!")
        return actual_damage
    
    def enemy_attack(self):
        # Check if enemy is stunned
        if self.enemy_effects.has_effect(EffectType.STUN):
            self.battle_log.append("Enemy is stunned and cannot attack!")
            return 0
        
        # Check for blindness
        if self.enemy_effects.has_effect(EffectType.BLIND):
            if random.random() < 0.3:  # 30% chance to miss
                self.battle_log.append("Enemy's attack misses due to blindness!")
                return 0
        
        # Check for confusion
        if self.enemy_effects.has_effect(EffectType.CONFUSE):
            if random.random() < 0.3:  # 30% chance to hit self
                damage = self.calculate_damage(self.enemy, self.enemy)
                actual_damage = self.enemy.take_damage(damage)
                self.battle_log.append(f"Enemy is confused and hits itself for {actual_damage} damage!")
                return actual_damage
        
        # Check for fear
        if self.enemy_effects.has_effect(EffectType.FEAR):
            if random.random() < 0.2:  # 20% chance to flee
                self.battle_log.append("Enemy is too afraid to attack!")
                return 0
        
        damage = self.calculate_damage(self.enemy, self.player)
        actual_damage = self.player.take_damage(damage)
        self.battle_log.append(f"Enemy deals {actual_damage} damage to you!")
        return actual_damage
    
    def shadow_attack(self, shadow):
        if shadow in self.player_shadows:
            damage = self.calculate_damage(shadow, self.enemy)
            actual_damage = self.enemy.take_damage(damage)
            self.battle_log.append(f"{shadow.name} deals {actual_damage} damage to the enemy!")
            return actual_damage
        return 0
    
    def use_skill(self, skill_name):
        # Check for silence
        if self.player_effects.has_effect(EffectType.SILENCE):
            self.battle_log.append("You are silenced and cannot use skills!")
            return False
        
        # Basic skill system
        skills = {
            'fireball': {'mana_cost': 20, 'damage_multiplier': 1.5},
            'heal': {'mana_cost': 15, 'heal_amount': 30},
            'shadow_boost': {'mana_cost': 25, 'boost_amount': 1.5}
        }
        
        if skill_name not in skills:
            self.battle_log.append("Invalid skill!")
            return False
        
        skill = skills[skill_name]
        
        if not self.player.use_mana(skill['mana_cost']):
            self.battle_log.append("Not enough mana!")
            return False
        
        if skill_name == 'fireball':
            damage = int(self.calculate_damage(self.player, self.enemy) * skill['damage_multiplier'])
            actual_damage = self.enemy.take_damage(damage)
            self.battle_log.append(f"You cast Fireball and deal {actual_damage} damage!")
            
            # Chance to apply burn effect
            if random.random() < 0.3:  # 30% chance
                burn_effect = Effect(EffectType.BURN, 3, 1)
                self.enemy_effects.add_effect(burn_effect)
                self.battle_log.append("Enemy is burning!")
            return True
        
        elif skill_name == 'heal':
            self.player.heal(skill['heal_amount'])
            self.battle_log.append(f"You heal yourself for {skill['heal_amount']} HP!")
            return True
        
        elif skill_name == 'shadow_boost':
            for shadow in self.player_shadows:
                shadow.strength = int(shadow.strength * skill['boost_amount'])
            self.battle_log.append("Your shadows are empowered!")
            return True
    
    def attempt_shadow_extraction(self):
        if self.enemy.health <= self.enemy.max_health * 0.2:  # Enemy below 20% health
            if random.random() < 0.3:  # 30% chance to extract shadow
                shadow = Shadow(self.enemy.name, self.enemy.level)
                if self.player.add_shadow(shadow):
                    self.battle_log.append(f"Successfully extracted {self.enemy.name}'s shadow!")
                    return True
                else:
                    self.battle_log.append("Failed to extract shadow - maximum shadows reached!")
            else:
                self.battle_log.append("Failed to extract shadow!")
        else:
            self.battle_log.append("Enemy is too strong to extract shadow!")
        return False
    
    def execute_turn(self, action_type, skill_name=None):
        self.turn_count += 1
        
        # Process effects at the start of turn
        player_effect_results = self.player_effects.process_effects(self.player)
        enemy_effect_results = self.enemy_effects.process_effects(self.enemy)
        
        for result in player_effect_results:
            self.battle_log.append(result)
        for result in enemy_effect_results:
            self.battle_log.append(result)
        
        # Player's turn
        if action_type == 'attack':
            damage = self.player_attack()
        
        elif action_type == 'skill':
            if skill_name == 'fireball':
                if self.player.use_mana(20):
                    # Calculate spell damage with magical power
                    base_damage = 30
                    spell_multiplier = self.player.get_spell_power_multiplier()
                    damage = int(base_damage * spell_multiplier)
                    self.enemy.health -= damage
                    self.battle_log.append(f"You cast Fireball for {damage} damage! (Spell Power: +{int((spell_multiplier - 1) * 100)}%)")
                    
                    # Chance to apply burn effect
                    if random.random() < 0.3:  # 30% chance
                        burn_effect = Effect(EffectType.BURN, 3, 1)
                        self.enemy_effects.add_effect(burn_effect)
                        self.battle_log.append("Enemy is burning!")
                else:
                    self.battle_log.append("Not enough mana!")
                    return 'continue'
            
            elif skill_name == 'heal':
                if self.player.use_mana(15):
                    # Calculate heal amount with magical power
                    base_heal = 20
                    spell_multiplier = self.player.get_spell_power_multiplier()
                    heal_amount = int(base_heal * spell_multiplier)
                    self.player.heal(heal_amount)
                    self.battle_log.append(f"You heal for {heal_amount} health! (Spell Power: +{int((spell_multiplier - 1) * 100)}%)")
                else:
                    self.battle_log.append("Not enough mana!")
                    return 'continue'
        
        # Enemy's turn
        if self.enemy.health > 0:
            damage = self.enemy_attack()
        
        # Check battle end conditions
        if self.enemy.health <= 0:
            return 'victory'
        elif self.player.health <= 0:
            return 'defeat'
        
        return 'continue'
    
    def get_battle_status(self):
        """Get the current battle status."""
        status = {
            'Player': f"{self.player.name} (HP: {self.player.health}/{self.player.max_health}, MP: {self.player.mana}/{self.player.max_mana})",
            'Enemy': f"{self.enemy.name} (HP: {self.enemy.health}/{self.enemy.max_health})",
            'Turn': self.turn_count,
            'battle_log': self.battle_log
        }
        
        # Add active effects
        player_effects = self.player_effects.get_active_effects()
        enemy_effects = self.enemy_effects.get_active_effects()
        
        if player_effects:
            status['Player Effects'] = ', '.join([f"{effect[0]} ({effect[1]} turns)" for effect in player_effects])
        if enemy_effects:
            status['Enemy Effects'] = ', '.join([f"{effect[0]} ({effect[1]} turns)" for effect in enemy_effects])
        
        return status 