package com.example.bookapp;

import com.example.dynamiclib.model.Book;
import java.util.ArrayList;
import java.util.List;

public class BookRepository {
    private final List<Book> books = new ArrayList<>();

    public void add(Book book) { books.add(book); }
    public List<Book> findAll() { return books; }
}
