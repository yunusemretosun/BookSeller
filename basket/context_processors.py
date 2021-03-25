from .basket import Basket

#gelen requeste basket iceriginde bir basket datasi gonderir.
#context_processorler settingste belirtilmelidir.
#Şablon içinde ise çektiğim verileri normal şekilde view’dan döndürmüş gibi yazdırıyorum.
def basket(request):
    return {'basket': Basket(request)}