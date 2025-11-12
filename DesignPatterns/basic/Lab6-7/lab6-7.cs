using System;

static void SumFor(int[] arr1, int[] arr2, int[] result)
{
    for(int i = 0; i < arr1.Length; i++)
    {
        result[i] = arr1[i] + arr2[i];
    }
}

static void SumWhile(int[] arr1, int[] arr2, int[] result)
{
    int i = 0;
    while(i < arr1.Length)
    {
        result[i] = arr1[i] + arr2[i];
        i++;
    }
}

static int MoreThanFive(int[] arr1, int[] arr2)
{
    int count = 0;
    for (int i = 0; i < arr1.Length; i++)
    {
        if (arr1[i] >= 5)
        {
            count++;
        }
    }

    for (int i = 0; i < arr2.Length; i++)
    {
        if (arr2[i] >= 5)
        {
            count++;
        }
    }

    return count;
}

static int MaxValue(int[] arr1, int[] arr2)
{
    int max = arr1[0];
    for (int i = 1; i < arr1.Length; i++)
    {
        if (arr1[i] > max)
        {
            max = arr1[i];
        }
    }

    for (int i = 1; i < arr2.Length; i++)
    {
        if (arr2[i] > max)
        {
            max = arr2[i];
        }
    }

    return max;
}

int[] array1 = { 0, 2, 7, 4, 5 };
int[] array2 = { 10, 15, 20, 25, 30 };

int[] result = new int[array1.Length];

Console.WriteLine("Цикл for:");
SumFor(array1, array2, result);
Console.WriteLine(string.Join(", ", result));

Console.WriteLine("Цикл while:");
SumWhile(array1, array2, result);
Console.WriteLine(string.Join(", ", result));

Console.WriteLine("Кол-во чисел больше пяти:");
int count = MoreThanFive(array1, array2);
Console.WriteLine(count);

Console.WriteLine("Максимальный элемент в массиве:");
int max = MaxValue(array1, array2);
Console.WriteLine(max);