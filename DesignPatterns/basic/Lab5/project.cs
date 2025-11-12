using System;

struct Prices
{
    public int Drink;
    public int First;
    public int Second;
}

struct Order
{
    public int DrinkCount;
    public int FirstCount;
    public int SecondCount;
}

class Program
{
    static int CalculateTotal(Prices prices, Order order)
    {
        int total = order.DrinkCount * prices.Drink + order.FirstCount * prices.First + order.SecondCount * prices.Second;
        return total;
    }

    static void Main()
    {
        Prices prices;
        prices.Drink = 10;
        prices.First = 20;
        prices.Second = 30;

       
        {
            Order order;
            order.DrinkCount = 2;
            order.FirstCount = 1;
            order.SecondCount = 0;

            int total = CalculateTotal(prices, order);
            Console.WriteLine("Стоимость заказа клиента 1: " + total);
        }


        {
            Order order;
            order.DrinkCount = 1;
            order.FirstCount = 0;
            order.SecondCount = 2;

            int total = CalculateTotal(prices, order);
            Console.WriteLine("Стоимость заказа клиента 2: " + total);
        }

        Console.ReadLine();
    }
}
