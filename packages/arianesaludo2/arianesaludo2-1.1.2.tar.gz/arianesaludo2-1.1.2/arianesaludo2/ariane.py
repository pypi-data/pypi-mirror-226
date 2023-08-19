class Ariane():
    def __init__(self):
        self.saludo = "Hola Ariane mi primera  libreria"
        self.result = None
        
    def show(self,saludo):
        print(self.saludo)
        print("Hola",saludo)
        
    def sumar(self, a,b):
        self.result = a + b
        return a + b
        

class Test(Ariane):
    def resta(self,a,b):
        return a -b
