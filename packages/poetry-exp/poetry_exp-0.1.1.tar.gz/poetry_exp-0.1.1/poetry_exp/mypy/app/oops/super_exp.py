"""
super: To call the base/Parent class implementation
       - super gives you an object which resolves methods using only
         the part of MRO which comes after the class
       - super return the proxy object which routes method calls means calls the correct method
         implementation of method if exists
          - Bound Proxy: Bound to specific class or instance
          - Unbound proxy: not bound to any class or instance

class bound proxy: super(base-class, derived-class)
  - base-class: class object, derived-class: subclass of first argument
  - Python finds MRO for derived class
  - Then finds base class in that MRO
  - and take everything after base-class in that MRO and then finds the first class
    in that sequences with a matching method name

Instance Bound Proxy: super(class, instance-of-class), instead of binding to a class binds to an instance
       class: class object, instance-of-subclass: instance of first argument(means instance of class object)
   - Python finds MRO for second argument
  - Then finds the location of first argument in the MRO
  - and take everything after that for resolving methods


Using super in instance method:
  super(class-of-method, self)

Using super in class method:
super(class-of-method, class)
"""


class Emp(object):
    count = 0

    def __init__(self, name, age, salary):
        self.name = name
        self.age = age
        self.salary = salary
        Emp.count +=1

    def __repr__(self):
        return "Emp Name: {0}, Age: {1}".format(self.name, self.age)

    def privileges(self):
        return ['Medical', 'Transport']

    def print_salary_receipt(self):
        print ("Emp Name: {0}, Salary: {1}".format(self.name, self.salary))

    def __del__(self):
        Emp.count -= 1


class Manger(Emp):
    def __init__(self, name, age, salary):
        super(Manger, self).__init__(name, age, salary)

        # OR
        # Emp.__init__(self, name, age, salary)

    def privileges(self):
        return  ['Medical', 'Transport', 'Bonus']


if __name__ == '__main__':

    m = Manger("Ajay", 45, 20000)
    print (m)
    m.print_salary_receipt()
    print (m.privileges())
    print ('No of Emp: ', m.count )# 1

    m2 = Manger("Aman", 40, 30000)
    print (m2)
    m2.print_salary_receipt()
    print (m2.privileges())

    print ('No of Emp: ', m.count )# 2

    del m2
    print ('No of Emp: ', m.count)  # 1

    e = Emp("Aakash", 20, 10000)
    print (e)
    e.print_salary_receipt()
    print (e.privileges())

    print ('No of Emp: ', m.count) # 2


"""
Output:
Emp Name: Ajay, Age: 45
Emp Name: Ajay, Salary: 20000
['Medical', 'Transport', 'Bonus']
No of Emp:  1
Emp Name: Aman, Age: 40
Emp Name: Aman, Salary: 30000
['Medical', 'Transport', 'Bonus']
No of Emp:  2
No of Emp:  1
Emp Name: Aakash, Age: 20
Emp Name: Aakash, Salary: 10000
['Medical', 'Transport']
No of Emp:  2
"""