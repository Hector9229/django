class EstrategiaDescuento:
    def calcular(self, precio):
        raise NotImplementedError
 
 
class DescuentoElectronica(EstrategiaDescuento):
    def calcular(self, precio):
        return precio * 0.90   # 10% de descuento
 
 
class DescuentoRopa(EstrategiaDescuento):
    def calcular(self, precio):
        return precio * 0.80   # 20% de descuento
 
 
class SinDescuento(EstrategiaDescuento):
    def calcular(self, precio):
        return precio          # sin descuento
 
 
def obtener_estrategia(categoria_nombre):
    estrategias = {
        'Electronica': DescuentoElectronica(),
        'Ropa': DescuentoRopa(),
    }
    return estrategias.get(categoria_nombre, SinDescuento())
