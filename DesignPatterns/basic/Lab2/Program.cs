using System.Threading;
using System;
Console.WriteLine("Hello,Jerry");
for (int i = 0; i < 3; i++)
{
    A();
    Thread.Sleep(500); 
}

static void A()
{
    Console.WriteLine("A");
    B();
    C();
}

static void B()
{
    Console.WriteLine("B");
}

static void C()
{
    Console.WriteLine("C");
}

Console.ReadKey();