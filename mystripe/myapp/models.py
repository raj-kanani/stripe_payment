from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.IntegerField(default=0)
    file = models.FileField(upload_to="product_files/", blank=False, null=False)
    url = models.URLField()

    def __str__(self):
        return self.name

    def get_display_price(self):
        return "{0:.2f}".format(self.price / 100)


class OrderDetail(models.Model):
    id = models.BigAutoField(primary_key=True)
    customer_email = models.EmailField(verbose_name='Customer Email')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    amount = models.IntegerField(verbose_name='Amount')
    stripe_payment = models.CharField(max_length=150)
    has_paid = models.BooleanField(default=False, verbose_name='Payment Status')
    create_on = models.DateTimeField(auto_now_add=True)
    update_on = models.DateTimeField(auto_now_add=True)
