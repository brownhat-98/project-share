from bookapp.models import Book

class Cart:
    def __init__(self, request):
        self.session = request.session

        if 'cart' not in request.session:
            self.cart = self.session['cart'] = {}
        else:
            self.cart = self.session.get('cart', {})

    def add(self, product, quantity=1):
        product_id = str(product.id) 

        if product_id in self.cart:
            self.cart[product_id]['quantity'] += quantity
        else:
            self.cart[product_id] = {
                'price': product.price,
                'quantity': quantity
            }

        self.session['cart'] = self.cart
        self.session.modified = True 

    def __len__(self):
        return len(self.cart) 
    
    def get_quantity(self, product_id=1):
        return self.cart.get(str(product_id), {}).get('quantity', 0)

    def get_products(self):
        product_ids = self.cart.keys()
        products = Book.objects.filter(id__in=product_ids)
    
        return products


    def update(self, product, quantity):
        product_id = str(product.id)
        if product_id in self.cart:
            self.cart[product_id]['quantity'] = quantity
            if self.cart[product_id]['quantity'] <= 0:
                del self.cart[product_id]
        self.session['cart'] = self.cart
        self.session.modified = True
        


    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
        self.session['cart'] = self.cart
        self.session.modified = True    



    def clear(self):
        self.cart = {}
        self.session['cart'] = self.cart
        self.session.modified = True
    