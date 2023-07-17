class DB:
    def __init__(self, path):
        self.path = path
        self.data = {}
        with open(path, 'r') as file:
            for line in file:
                line = line.strip()
                parts = line.split('%')
                self.data[parts[0]] = [*parts]
        

    def Test(self, item):
        return str(item) in self.data.keys()
    

    def Save(self):
        text = ''
        for key in self.data.keys():
            StringItems = '%'.join(self.data[str(key)])
            text += f'{key}%{StringItems}\n'
        with open(self.path, 'w') as file:
            file.write(text)


    def AddString(self, key, mass):
        self.data[str(key)] = mass
        self.Save()

    
    def AddItem(self, key, item):
        mass: list
        mass = self.data[str(key)]
        mass.append(item)
        self.AddString(key, mass)


    def Delete(self, key):
        self.data.pop(key)
        self.Save()

    
    def Get(self, key):
        self.Update()
        Item = self.data[str(key)]
        return Item


    def Update(self):
        self.data = {}
        with open(self.path, 'r') as file:
            for line in file:
                line = line.strip()
                parts = line.split('%')
                self.data[parts[0]] = [*parts]