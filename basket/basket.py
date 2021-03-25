from decimal import Decimal
from store.models import Product

import datetime



class Basket():
    """
    A base Basket class, providing some default behaviors that
    can be inherited or overrided, as necessary.
    """

    def __init__(self, request):
        self.session = request.session
        basket = self.session.get('skey')
        if 'skey' not in request.session:
            basket = self.session['skey'] = {}
        self.basket = basket

    def add(self, product, qty):
        """
        Adding and updating the users basket session data
        burada price i str olarak alıyoruz ancak matematiksel islem yaparken decimal e ceviricez.
        """
        product_id = str(product.id)

        if product_id in self.basket:
            self.basket[product_id]['qty'] = qty
        else:
            self.basket[product_id] = {'price': str(product.price), 'qty': qty}
        
        self.save()
        
    def __iter__(self):
        """
        product_idleri kullanarak 
        session un içindeki dataları querylerle database e yolluyoruz
        and return products
        """
        product_ids = self.basket.keys()
        products = Product.products.filter(id__in=product_ids)
        basket = self.basket.copy()

        #yukarida productlari basketin icinde bulunan idlere-keylere gore filtrelemistik
        for product in products:
            basket[str(product.id)]['product'] = product
        
        """
        burada for donerken her yield satirina geldiginde yieldin sagindaki ifadeyi dondurur
        return den farkli olarak sonladirma yapmaz ve degiskenleri saklar bitene kadar. 
        """
        for item in basket.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['qty']
            yield item

      
    
    def __len__(self):

        """
        Basket datasini ve itemlerin qty sayisini getirir
        """
        return sum(item['qty'] for item in self.basket.values())

   
    def get_total_price(self):
        return sum(Decimal(item['price']) * item['qty'] for item in self.basket.values())

   
    def delete(self,product):
        """
        session datadan item silme
        """
        product_id = str(product)

        if product_id in self.basket:
            del self.basket[product_id]
            self.save()

    def update(self, product, qty):
        """
        Update values in session data
        """
        product_id = str(product)
        if product_id in self.basket:
            self.basket[product_id]['qty'] = qty
        self.save()

    
    def save(self):
        self.session.modified = True
        