class TiposDeVehiculos:
    mapping = {
        'VehicleLevel1': 'VehicleLevel1',  # Columna del CSV → atributo del objeto
        'VehicleLevel2': 'VehicleLevel2',
        'VehicleLevel3': 'VehicleLevel3'
    }

    def __init__(self, VehicleLevel1, VehicleLevel2, VehicleLevel3):
        self.VehicleLevel1 = VehicleLevel1
        self.VehicleLevel2 = VehicleLevel2
        self.VehicleLevel3 = VehicleLevel3

    def __repr__(self):
        return f"Level 1: {self.VehicleLevel1}, Level 2: {self.VehicleLevel2}, Level 3: {self.VehicleLevel3}"

class ModelosDeVehiculos:
    mapping = {
        'marca':'marca',
        'categoria':'categoria',
        'tipo':'tipo',
        'modelo':'modelo',
        'inicio':'inicio',
        'fin':'fin'
    }

    def __init__(self, marca, categoria, tipo, modelo, inicio, fin):
        self.marca = marca
        self.categoria = categoria
        self.tipo = tipo
        self.modelo = modelo
        self.inicio = inicio
        self.fin = fin

    def __repr__(self):
        return f"Marca: {self.marca}, Categoria: {self.categoria}, Tipo: {self.tipo}, Modelo: {self.modelo}, Inicio: {self.inicio}, Fin: {self.fin}"


