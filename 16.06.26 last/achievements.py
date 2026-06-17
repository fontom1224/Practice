import json
import os

class AchievementManager:
    def __init__(self, save_file='achievements.json'):
        self.save_file = save_file
        self.achievements = self._default_achievements()
        self.load()
        self._ensure_defaults()

    def _default_achievements(self):
        return {
            'first_score': {'id':'first_score', 'name':'\nНачало положено', 'description':'\nНаберите 100 очков', 'unlocked':False, 'progress':0, 'target':100},
            'score_500': {'id':'score_500', 'name':'\n500', 'description':'\nНаберите 500 очков', 'unlocked':False, 'progress':0, 'target':500},
            'score_1000': {'id':'score_1000', 'name':'\nIt takes.. one', 'description':'\nНаберите 1000 очков', 'unlocked':False, 'progress':0, 'target':1000},
            'score_2000': {'id':'score_2000', 'name':'\nIt takes two', 'description':'\nНаберите 2000 очков', 'unlocked':False, 'progress':0, 'target':2000},
            'boss_killer': {'id':'boss_killer', 'name':'\nЭто ж Красный', 'description':'\nПобедите первого босса', 'unlocked':False, 'progress':0, 'target':0},
            'god_slayer': {'id':'god_slayer', 'name':'\nБогоубийца', 'description':'\nПобедите Бога-Астероида', 'unlocked':False, 'progress':0, 'target':0},
            'final_boss': {'id':'final_boss', 'name':'\nДа здравствует король', 'description':'\nПобедите финального босса', 'unlocked':False, 'progress':0, 'target':0},
            'medkit_collector': {'id':'medkit_collector', 'name':'\nКазуал', 'description':'\nСоберите 5 аптечек', 'unlocked':False, 'progress':0, 'target':5},
            'powerup_collector': {'id':'powerup_collector', 'name':'\nСкорострел', 'description':'\nСоберите 5 ускорителей', 'unlocked':False, 'progress':0, 'target':5},
            'power_bullet_user': {'id':'power_bullet_user', 'name':'\nСуперсаян', 'description':'\nИспользуйте 10 усиленных патронов', 'unlocked':False, 'progress':0, 'target':10},
            'asteroid_hunter': {'id':'asteroid_hunter', 'name':'\nБум', 'description':'\nУничтожьте 50 астероидов', 'unlocked':False, 'progress':0, 'target':50},
            'asteroid_master': {'id':'asteroid_master', 'name':'\nБольшой бум', 'description':'\nУничтожьте 100 астероидов', 'unlocked':False, 'progress':0, 'target':100},
            'first_death': {'id':'first_death', 'name':'\nТрупак', 'description':'\nУмрите впервые', 'unlocked':False, 'progress':0, 'target':0},
        }

    def _ensure_defaults(self):
        defaults = self._default_achievements()
        for key, value in defaults.items():
            if key not in self.achievements:
                self.achievements[key] = value
            else:
                for field in ['id', 'name', 'description', 'unlocked', 'progress', 'target']:
                    if field not in self.achievements[key]:
                        self.achievements[key][field] = value[field]
        self.save()

    def load(self):
        if os.path.exists(self.save_file):
            try:
                with open(self.save_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                self.achievements.update(data)
            except:
                pass

    def save(self):
        try:
            with open(self.save_file, 'w', encoding='utf-8') as f:
                json.dump(self.achievements, f, indent=2, ensure_ascii=False)
        except:
            pass

    def unlock(self, ach_id):
        if ach_id in self.achievements and not self.achievements[ach_id]['unlocked']:
            self.achievements[ach_id]['unlocked'] = True
            self.save()
            return True
        return False

    def add_progress(self, ach_id, amount=1):
        if ach_id in self.achievements and not self.achievements[ach_id]['unlocked']:
            ach = self.achievements[ach_id]
            if ach['target'] > 0:
                ach['progress'] += amount
                if ach['progress'] >= ach['target']:
                    self.unlock(ach_id)
                    return True
                else:
                    self.save()
        return False

    def check_event(self, event_type, value=None):
        """Обработка игровых событий, возвращает ID разблокированного достижения или None."""
        if event_type == 'score':
            for ach_id in ['first_score', 'score_500', 'score_1000', 'score_2000']:
                if ach_id in self.achievements and not self.achievements[ach_id]['unlocked']:
                    if value >= self.achievements[ach_id]['target']:
                        if self.unlock(ach_id):
                            return ach_id
        elif event_type == 'boss_defeated':
            mapping = {'boss': 'boss_killer', 'god': 'god_slayer', 'third': 'final_boss'}
            ach_id = mapping.get(value)
            if ach_id and not self.achievements[ach_id]['unlocked']:
                if self.unlock(ach_id):
                    return ach_id
        elif event_type == 'medkit_collected':
            if self.add_progress('medkit_collector'):
                return 'medkit_collector'
        elif event_type == 'powerup_collected':
            if self.add_progress('powerup_collector'):
                return 'powerup_collector'
        elif event_type == 'power_bullet_used':
            if self.add_progress('power_bullet_user'):
                return 'power_bullet_user'
        elif event_type == 'asteroid_destroyed':
            # проверяем оба достижения, возвращаем то, которое разблокировалось
            if not self.achievements['asteroid_hunter']['unlocked']:
                if self.add_progress('asteroid_hunter'):
                    return 'asteroid_hunter'
            if not self.achievements['asteroid_master']['unlocked']:
                if self.add_progress('asteroid_master'):
                    return 'asteroid_master'
        elif event_type == 'player_died':
            if not self.achievements['first_death']['unlocked']:
                if self.unlock('first_death'):
                    return 'first_death'
        return None