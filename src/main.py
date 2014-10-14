# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

__author__="rasmadeus"
__date__ ="$14.10.2014 19:16:28$"

if __name__ == "__main__":
    from equre import equre
    equre_curve = equre.EqureCurve()
    equre_curve.fill_from('c:\\Dev\\test\\in.txt')
    equre_curve.make_out_files(0.0, 5.0, 'c:\\Dev\\test\\out')
    print('Equals curves was created!')
