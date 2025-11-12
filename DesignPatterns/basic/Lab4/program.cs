using System;


static void A()
{
    int a = 5;
    int b = 6;
    a = b;
    b = 7;
    Console.WriteLine(a);
}
static void B()
{
    int a = 5;
    int b = a + 6;
    a = 7;
    Console.WriteLine(b);
}

static void C()
{
    string a = "a";
    string b = a;
    a = "b";
    Console.WriteLine(a);
    Console.WriteLine(b);
    // string a = 5;
    // int a = 5;
    // int a = 6;
}

A();
B();
C();