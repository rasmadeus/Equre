# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

__author__="rasmadeus"
__date__ ="$14.10.2014 19:56:43$"

def start_doc_strings_testing():
    import doctest
    from equre import equre
    print(doctest.testmod(equre))


import unittest
def start_unittesting():
    suite = unittest.TestLoader().discover(start_dir='.', pattern='test_*.py')
    unittest.TextTestRunner(verbosity=2).run(suite)


if __name__ == "__main__":
    start_doc_strings_testing()
    start_unittesting()