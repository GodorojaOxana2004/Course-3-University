package com.example.bookapp;

import com.example.dynamiclib.KeyRegistry;
import com.example.dynamiclib.model.Book;
import java.util.Arrays;

public class App {
    public static void main(String[] args) {
        KeyRegistry registry = new KeyRegistry();
        BookExtensions ext = new BookExtensions(registry);
        BookRepository repo = new BookRepository();

        Book b1 = new Book(1, "1984", "George Orwell");
        Book b2 = new Book(2, "Brave New World", "Aldous Huxley");

        b1.getContext().put(ext.RATING, 9.2);
        b1.getContext().put(ext.GENRES, Arrays.asList("Dystopian", "Political Fiction"));

        b2.getContext().put(ext.RATING, 8.8);
        b2.getContext().put(ext.SALES, 1500000);

        repo.add(b1);
        repo.add(b2);

        for (Book b : repo.findAll()) {
            System.out.println(b);
            System.out.println("  Rating: " + b.getContext().get(ext.RATING).orElse(null));
            System.out.println("  Genres: " + b.getContext().get(ext.GENRES).orElse(null));
            System.out.println("  Sales: " + b.getContext().get(ext.SALES).orElse(null));
        }
    }
}
