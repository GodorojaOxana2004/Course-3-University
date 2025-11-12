using System;
using System.Text;

struct Book
{
    public string title;
    public bool isTaken;
}

class Program
{
    static Book[] books = new Book[5];

    static void Main()
    {
        Encoding.RegisterProvider(CodePagesEncodingProvider.Instance);
        Console.OutputEncoding = Encoding.UTF8;
        Console.InputEncoding = Encoding.GetEncoding(1251);

        books[0].title = "Война и мир";
        books[0].isTaken = false;

        books[1].title = "Преступление и наказание";
        books[1].isTaken = false;

        books[2].title = "Мастер и Маргарита";
        books[2].isTaken = false;

        books[3].title = "Анна Каренина";
        books[3].isTaken = false;

        books[4].title = "Идиот";
        books[4].isTaken = false;

        while (true)
        {
            Console.WriteLine("\n1.Взять книгу");
            Console.WriteLine("2.Вернуть книгу");
            Console.WriteLine("3.Показать все книги");
            Console.WriteLine("0.Выход");
            Console.Write("Выберите действие:");
            
            string choice = Console.ReadLine();

            if (choice == "1")
            {
                Console.Write("Введите название книги: ");
                string name = Console.ReadLine();
                BorrowBook(name);
            }
            else if (choice == "2")
            {
                Console.Write("Введите название книги: ");
                string name = Console.ReadLine();
                ReturnBook(name);
            }
            else if (choice == "3")
            {
                ViewAllBooks();
            }
            else if (choice == "0")
            {
                break;
            }
        }
    }

    static void BorrowBook(string bookTitle)
    {
        bookTitle = bookTitle.Trim();
        for (int i = 0; i < books.Length; i++)
        {
            if (books[i].title.Equals(bookTitle, StringComparison.OrdinalIgnoreCase))
            {
                if (books[i].isTaken)
                {
                    Console.WriteLine("Книга уже взята");
                }
                else
                {
                    books[i].isTaken = true;
                    Console.WriteLine("Книга выдана");
                }
                return;
            }
        }
        Console.WriteLine("Книга не найдена");
    }

    static void ReturnBook(string bookTitle)
    {
        bookTitle = bookTitle.Trim();
        for (int i = 0; i < books.Length; i++)
        {
            if (books[i].title.Equals(bookTitle, StringComparison.OrdinalIgnoreCase))
            {
                if (!books[i].isTaken)
                {
                    Console.WriteLine("Ошибка: книга не была взята");
                }
                else
                {
                    books[i].isTaken = false;
                    Console.WriteLine("Книга возвращена");
                }
                return;
            }
        }
        Console.WriteLine("Ошибка: такой книги нет в библиотеке");
    }

    static void ViewAllBooks()
    {
        Console.WriteLine("\nСписок книг:");
        for (int i = 0; i < books.Length; i++)
        {
            string status = books[i].isTaken ? "взята" : "доступна";
            Console.WriteLine($"{books[i].title} - {status}");
        }
    }
}