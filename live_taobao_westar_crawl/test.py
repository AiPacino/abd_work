#coding:utf-8

def select(table_name, condition=None, *args):
    print table_name
    print condition
    print args

def main():
#    select("what fuck slkdfja lsdf", condition=8,[3,])
    func(1,2,c=3)


def func(a, b, c=0, *args, **kw):
    print 'a =', a, 'b =', b, 'c =', c, 'args =', args, 'kw =', kw


if __name__ == '__main__':
    main()