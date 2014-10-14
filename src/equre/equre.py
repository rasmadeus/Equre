# -*- coding: utf-8 -*-

__author__="rasmadeus"
__date__ ="$14.10.2014 20:00:10$"


class EqurePoint:
    
    def __init__(self, x, y, value):
        self._x = x
        self._y = y
        self._value = value        
    
    def x(self):
        return self._x    
    
    def y(self):
        return self._y    
    
    def value(self):
        return self._value        
        
    def interpolate(self, point, value):
        """
        >>> point1 = EqurePoint(0.0, 10.0, 10.0)
        >>> point1.interpolate(EqurePoint(10.0, 0.0, 0.0), 5.0)
        (5.0, 5.0)
        >>> point1.interpolate(EqurePoint(10.0, 0.0, 10.0), 10.0)
        (5.0, 5.0)
        """
        import math
        length = point._value - self._value
        k_of_value = 0.5 if (length == 0) else (value - self._value) / length
        x_of_value = self._x + k_of_value * (point._x - self._x)
        y_of_value = self._y + k_of_value * (point._y - self._y)
        return (x_of_value, y_of_value)
        
        
    @staticmethod
    def make_from(line_of_file):
        """
        >>> line = '45 34 12'
        >>> point = EqurePoint.make_from(line)
        >>> point.value()
        12.0
        >>> line = '23'
        >>> point = EqurePoint.make_from(line)
        >>> point.value()
        0.0
        >>> point.x()
        23.0
        """
        def get_value(values, i):
            try:
                return float(values[i])
            except:
                return 0.0
            
        values = line_of_file.split()
        if len(values) == 0:
            raise Exception('line of file is empty')
        return EqurePoint(get_value(values, 0), get_value(values, 1), get_value(values, 2))

    
    
class EqureCurve:
    
    def __init__(self):
        self.clear()
        
    def clear(self):
        self._points = []
        
    def values(self):
        return [point.value() for point in self._points]
        
    def count(self):
        return len(self._points)
        
    def point(self, i):
        return self._points[i]
            
    def append(self, x, y, value):
        """
        >>> curve = EqureCurve()
        >>> curve.append(1, 2, 0)
        >>> curve.append(2, 4, -1)
        >>> curve.append(4, 1, 4)
        >>> print(curve.values())
        [-1, 0, 4]
        """
        self._append(EqurePoint(x, y, value))
        self._sort()
        
    def _sort(self):
        self._points.sort(key=lambda point: point.value())
        
    def _append(self, equre_curve):
        self._points.append(equre_curve)        
        
    def fill_from(self, path_to_file):
        """
        >>> path_to_test_file = './/test_data//equre_points.txt'
        >>> curve = EqureCurve()
        >>> curve.fill_from(path_to_test_file)
        >>> curve.values()
        [-23.2, -23.0, 0.0, 0.0, 2.0, 34.0]
        """
        for line_of_file in open(path_to_file, 'r'):
            try:
                point = EqurePoint.make_from(line_of_file)
                self._append(point)
            except:
                pass
        self._sort()
        
    def make_equal_curve_for(self, value):
        """
        >>> equre_curve = EqureCurve()
        >>> equre_curve.append(0.0, 10.0, 10.0)
        >>> equre_curve.append(10.0, 0.0, 0.0)
        >>> equre_curve.make_equal_curve_for(5.0)
        [(5.0, 5.0)]
        >>> equre_curve.append(5.0, 1.0, 5.0)
        >>> equre_curve.append(15.0, 7.0, 6.0)
        >>> equre_curve.make_equal_curve_for(5.0)
        [(5.0, 1.0), (5.0, 1.0), (5.0, 1.0), (5.0, 1.0), (5.0, 5.0), (14.166666666666668, 5.833333333333334)]
        """
        curve = []
        for i in range(self.count()):
            if self.point(i).value() <= value:
                for j in range(i, self.count(), 1):
                    if self.point(j).value() >= value:
                        curve.append(self.point(i).interpolate(self.point(j), value))
        curve.sort(key=lambda xy: xy[1])
        return curve 
    
    def make_equals_curves_for(self, begin_value, step):
        """
        >>> equre_curve = EqureCurve()
        >>> equre_curve.append(0.0, 10.0, 10.0)
        >>> equre_curve.append(10.0, 0.0, 0.0)
        >>> equre_curve.make_equals_curves_for(0.0, 5.0)
        {0.0: [(10.0, 0.0), (10.0, 0.0)], 10.0: [(0.0, 10.0), (0.0, 10.0)], 5.0: [(5.0, 5.0)]}
        """
        curves = {}
        current_value = begin_value
        last_value = self.point(self.count() - 1).value()
        while current_value <= last_value:
            curve = self.make_equal_curve_for(current_value)
            if len(curve) != 0:
                curves[current_value] = curve
            current_value += step
        return curves
    
    def make_out_files(self, begin_value, step, out_files_dir):
        curves = self.make_equals_curves_for(begin_value, step)
        for value, curve in curves.iteritems():
            from os import path
            out_file = open(path.join(out_files_dir, '{value}.txt'.format(value=value)), 'w')
            out_file.write(u'X,km\tH,km\n')
            for xh in curve:
                out_file.write('{x}\t{h}\n'.format(x=xh[0], h=xh[1]))
                        
                

            