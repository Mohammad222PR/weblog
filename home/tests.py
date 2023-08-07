# test.py

import datetime
from django.test import TestCase
from .models import optype, ProductLines, Branche, Productid, Storagepk

class ProductLinesTest(TestCase):
    def setUp(self):
        # ایجاد شعبه برای تست
        self.branch = Branche.objects.create(name='شعبه تست')
        
        # ایجاد نوع عملیات برای تست
        self.op_type = optype.objects.create(s='فروش', r='برگشت از فروش', b='خرید', p='برگشت از خرید',
                                             m='موجودی ابتدای دوره', f='اضافات', d='کسورات', t='انتقالات انبار')
        
        # ایجاد کالای مرتبط برای تست
        self.product_id = Productid.objects.create(name='کالای تست', code='KT01')
        
        # ایجاد انبار مرتبط برای تست
        self.storage_pk = Storagepk.objects.create(number='انبار تست')
        
        # ایجاد عملیات برای تست
        self.product_line = ProductLines.objects.create(
            branch=self.branch,
            op_type=self.op_type,
            op_date=datetime.datetime.now(),
            op_num=1,
            product_id=self.product_id,
            units=10,  # به تعداد واحد‌ها بر اساس نیاز تست تغییر دهید
            retails=100,  # به مبلغ خرده‌فروش‌ها بر اساس نیاز تست تغییر دهید
            total_num=100,
            storage_pk=self.storage_pk,
            op_price=1000,
            dis_percent=10,
            dis_price=100,
            tax_amount=50,
            tax_percent=5,
            tru_price=900,
            total_amount=850,
        )
    
    def test_product_line_creation(self):
        # تست بررسی ایجاد عملیات به درستی
        product_line = ProductLines.objects.get(op_num=1)
        self.assertEqual(product_line.branch, self.branch)
        self.assertEqual(product_line.op_type, self.op_type)
        self.assertEqual(product_line.product_id, self.product_id)
        self.assertEqual(product_line.storage_pk, self.storage_pk)
        # و سایر فیلدها...
