package com.example.dynamiclib.model;

import com.example.dynamiclib.DynamicContext;

public class Book {
    private final int id;
    private final String title;
    private final String author;
    private final DynamicContext context = new DynamicContext();

    public Book(int id, String title, String author) {
        this.id = id;
        this.title = title;
        this.author = author;
    }

    public int getId() { return id; }
    public String getTitle() { return title; }
    public String getAuthor() { return author; }
    public DynamicContext getContext() { return context; }

    @Override
    public String toString() {
        return "Book{id=" + id + ", title='" + title + "', author='" + author + "'}";
    }
}
