class Elf:


    def __init__(self,name, mus_instrument, favourite_song):
        self.mus_instrument = mus_instrument
        self.favourite_song = favourite_song
        self.name = name
    def play_song(self):
        print(f'elf {self.name} playing {self.favourite_song}'
              f' on {self.mus_instrument}')

class Elf_ranger(Elf):
    def __init__(self, bow: dict, name , mus_instrument, favourite_song, opponent:list = []):
        super().__init__(name,mus_instrument,favourite_song)
        self.damage = bow["damage"]
        self.weapon = bow["name"]
        self.hp = 100
        self.opponent = opponent

    def fight(self):
        for i in self.opponent:
            i.hp -= self.damage
            print(f'ranger has dealt {self.damage} damage to {i.name}')
        if self.hp <= 0:
            print('ranger died')

class Elf_swordsman(Elf):
    def __init__(self, sword: dict, name , mus_instrument, favourite_song, opponent:list = []):
        super().__init__(name,mus_instrument,favourite_song)
        self.damage = sword["damage"]
        self.weapon = sword["name"]
        self.hp = 100
        self.opponent = opponent

    def fight(self):
        for i in self.opponent:
            i.hp -= self.damage
            print(f'swordsman has dealt {self.damage} damage to {i.name}')
        if self.hp <= 0:
            print('swordsman died')


class Elf_magician(Elf):
    def __init__(self, staff: dict, name , mus_instrument, favourite_song, opponent: list = []):
        super().__init__(name,mus_instrument,favourite_song)
        self.damage = staff["damage"]
        self.weapon = staff["name"]
        self.hp = 100
        self.opponent = opponent

    def fight(self):
        for i in self.opponent:
            i.hp -= self.damage
            print(f'magician has dealt {self.damage} damage to {i.name}')
        if self.hp <= 0:
            print('magician died')

bobichek_babka = Elf_swordsman({"name":"exkalibur","damage":99},'bobichek_babka',
                              'gitara','yagoda malinka'
                              )
bobichek_ded = Elf_ranger({"name":"M49","damage":99},'bobichek_ded',
                              'gitara','yagoda malinka'
                              )
bobichek_praded = Elf_magician({"name":"volshebnaya palochka","damage":99},'bobichek_praded',
                              'gitara','yagoda malinka'
                              )
def fight_elfs(bobichek_babka,bobichek_ded,bobichek_praded):
    bobichek_babka.opponent = [bobichek_ded,bobichek_praded]
    bobichek_ded.opponent = [bobichek_babka,bobichek_praded]
    bobichek_praded.opponent = [bobichek_ded,bobichek_babka]
    bobichek_babka.play_song()
    bobichek_ded.play_song()
    bobichek_praded.play_song()
    bobichek_babka.fight()
    bobichek_ded.fight()
    bobichek_praded.fight()


fight_elfs(bobichek_babka,bobichek_ded,bobichek_praded)