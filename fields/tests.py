from datetime import datetime

from django.test import TestCase

from .models import Field, FieldValue, FieldOption, InvalidDataTypeException


class TestField(TestCase):

    def is_valid(self):
        f = Field(name='Test Valid Field', data_type='INTEGER')
        self.assertTrue(f.is_valid_data_type())

    def is_invalid(self):
        f = Field(name='Test Invalid Field', data_type='NOPE')
        self.assertFalse(f.is_valid_data_type())

    def signal_works(self):
        f = Field(name='Test Nope Field', data_type='NOPE')
        try:
            f.save()
        except InvalidDataTypeException:
            self.assertTrue(True)
        f.data_type = 'INTEGER'
        f.save()


class TestFieldValue(TestCase):

    def test_proxied_attributes(self):
        f = Field(name='Test Proxy Field', data_type='INTEGER')
        f.save()
        fv = FieldValue(field=f, int_value=5)
        self.assertEqual(fv.name, f.name)
        self.assertEqual(fv.data_type, f.data_type)

    def test_int_value(self):
        f = Field(name='Test Integer Field', data_type='INTEGER')
        f.save()
        fv = FieldValue(field=f, int_value=5)
        self.assertEqual(fv.value, 5)

    def test_str_value(self):
        f = Field(name='Test String Field', data_type='STRING')
        f.save()
        fv = FieldValue(field=f, str_value='testing')
        self.assertEqual(fv.value, 'testing')

    def test_flt_value(self):
        f = Field(name='Test Float Field', data_type='FLOAT')
        f.save()
        fv = FieldValue(field=f, flt_value=1.0)
        self.assertEqual(fv.value, 1.0)

    def test_date_value(self):
        nowoclock = datetime.now()
        f = Field(name='Test Date Field', data_type='DATE')
        f.save()
        fv = FieldValue(field=f, date_value=nowoclock)
        self.assertEqual(fv.value, nowoclock)

    def test_opt_value(self):
        opts = ['Mary', 'Gary', 'Larry']
        fopts = []
        for o in opts:
            fo = FieldOption(name=o)
            fo.save()
            fopts.append(fo)
        f = Field(name='Test Option Field', data_type='OPTION')
        f.save()
        f.options = fopts
        fv = FieldValue(field=f, opt_value='Mary')
        self.assertEqual([x for x in fv.options.all()], fopts)
        self.assertEqual(fv.value, 'Mary')
